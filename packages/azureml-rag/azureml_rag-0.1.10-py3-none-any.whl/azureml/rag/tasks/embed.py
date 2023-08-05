# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
import os
import pandas as pd
import pathlib
import time
import traceback

from azureml.rag.documents import Document, SUPPORTED_EXTENSIONS, DocumentChunksIterator, DocumentSource, split_documents, StaticDocument
from azureml.rag.embeddings import EmbeddingsContainer
from azureml.rag.utils.azureml import get_secret_from_workspace
from azureml.rag.utils.logging import get_logger, enable_stdout_logging, track_activity, _logger_factory, enable_appinsights_logging
from typing import Optional, Iterator

logger = get_logger('embed')


def create_embeddings(chunks: Iterator[Document],
                      previous_embeddings: Optional[EmbeddingsContainer],
                      output: str,
                      embeddings_model: str,
                      batch_size: Optional[int]):

    extra_args = {}
    if batch_size is not None:
        extra_args["batch_size"] = batch_size

    embeddings = previous_embeddings if previous_embeddings is not None else EmbeddingsContainer.from_uri(embeddings_model, **extra_args)

    pre_embed = time.time()
    embeddings.embed(chunks)
    post_embed = time.time()
    logger.info(f"Embedding took {post_embed - pre_embed} seconds", extra={'print': True})

    embeddings.save(output)


def read_chunks_into_documents(files: Iterator[pathlib.Path], chunk_format: str = 'csv') -> Iterator[Document]:
    # Append to list of texts and corresponding metadata
    file_max_chunk_len = 0
    for chunk_file in files:
        file_name = chunk_file.name
        logger.info(f'processing chunks for: {file_name}', extra={'print': True})
        max_chunk_len = 0
        num_chunks = 0
        if chunk_format == 'csv':
            # Ensure Chunk data is read as string even if it looks like another datatype.
            dtype = {'Chunk': str, 'Metadata': str}
            chunks_df = pd.read_csv(chunk_file, dtype=dtype, keep_default_na=False)
            chunks_dict = chunks_df.to_dict()
            for chunk_idx, chunk in chunks_dict["Chunk"].items():
                metadata = chunks_dict["Metadata"][chunk_idx]
                metadata_dict = json.loads(metadata)
                max_chunk_len = max(max_chunk_len, len(chunk))
                num_chunks += 1
                yield StaticDocument(data=chunk, metadata=metadata_dict, document_id=metadata_dict['source']['filename'] + str(chunk_idx), mtime=metadata_dict['source'].get('mtime'))

        elif chunk_format == 'jsonl':
            with open(chunk_file, 'r') as f:
                for line in f:
                    doc = StaticDocument.loads(line.strip())
                    max_chunk_len = max(max_chunk_len, len(doc.data))
                    num_chunks += 1
                    yield doc

        logger.info(f'processed {num_chunks} chunks from {file_name}, max_chunk_len = {max_chunk_len}', extra={'print': True})
        file_max_chunk_len = max(file_max_chunk_len, max_chunk_len)
    logger.info(f'longest chunk seen was {file_max_chunk_len}', extra={'print': True})


def main(args, logger, activity_logger):
    if args.chunks_source and args.documents_source:
        activity_logger.activity_info['error'] = 'chunks_source and documents_source were both specified'
        raise ValueError("Cannot specify both --chunks_source and --documents_source")
    elif args.chunks_source is None and args.documents_source is None:
        activity_logger.activity_info['error'] = 'Neither chunks_source nor documents_source were specified'
        raise ValueError("Must specify either --chunks_source or --documents_source")

    splitter_args = {
        "chunk_size": args.chunk_size,
    }
    if args.chunk_overlap:
        splitter_args['chunk_overlap'] = args.chunk_overlap

    # Mount previous embeddings if given
    previous_embeddings = None
    if args.previous_embeddings is not None:
        from azureml.dataprep.fuse.dprepfuse import MountOptions, rslex_uri_volume_mount
        mnt_options = MountOptions(
            default_permission=0o555, allow_other=False, read_only=True)
        try:
            with rslex_uri_volume_mount(args.previous_embeddings, f'{os.getcwd()}/previous_embeddings', options=mnt_options) as mount_context:
                previous_embeddings_dir_name = None
                # list all folders in previous_embeddings_container_path and find the latest one
                try:
                    previous_embeddings_dir_name = str(max([dir for dir in pathlib.Path(
                        mount_context.mount_point).glob('*') if dir.is_dir() and dir.name != os.environ['AZUREML_RUN_ID']], key=os.path.getmtime).name)
                except Exception as e:
                    logger.warning(
                        f'failed to get latest folder from {mount_context.mount_point} with {e}.', extra={'print': True})
                    pass

                if previous_embeddings_dir_name is not None:
                    logger.info(
                        f'loading from previous embeddings from {previous_embeddings_dir_name} in {mount_context.mount_point}', extra={'print': True})
                    try:
                        previous_embeddings = EmbeddingsContainer.load(
                            previous_embeddings_dir_name, mount_context.mount_point)
                    except Exception as e:
                        logger.warn(
                            f'Failed to load from previous embeddings with {e}.\nCreating new Embeddings.', extra={'print': True})
        except Exception as e:
            logger.warning(f'Failed to load previous embeddings from mount with {e}, proceeding to create new embeddings.', extra={'print': True})

    # Load chunks to embed
    if args.documents_source is not None:
        logger.info("Getting chunks from documents_source", extra={'print': True})

        def filter_and_log_extensions(sources: Iterator[DocumentSource], allowed_extensions=args.allowed_extensions) -> Iterator[DocumentSource]:
            """Filter out sources with extensions not in allowed_extensions."""
            total_files = 0
            skipped_files = 0
            skipped_extensions = {}
            kept_extension = {}
            for source in sources:
                total_files += 1
                if allowed_extensions is not None:
                    if source.path.suffix not in allowed_extensions:
                        skipped_files += 1
                        ext_skipped = skipped_extensions.get(source.path.suffix, 0)
                        skipped_extensions[source.path.suffix] = ext_skipped + 1
                        logger.debug(f'Filtering out extension "{source.path.suffix}" source: {source.filename}')
                        continue
                ext_kept = kept_extension.get(source.path.suffix, 0)
                kept_extension[source.path.suffix] = ext_kept + 1
                yield source
            logger.info(f"[DocumentChunksIterator::filter_extensions] Filtered {skipped_files} files out of {total_files}")

        chunked_documents = DocumentChunksIterator(
            files_source=args.input_data,
            glob=args.input_glob,
            base_url=args.documents_source_base_url,
            document_path_replacement_regex=args.document_path_replacement_regex,
            file_filter=filter_and_log_extensions,
            chunked_document_processors = [lambda docs: split_documents(docs, splitter_args=splitter_args)],
        )

        def flatten_iterator(iterable):
            for i in iterable:
                for j in i:
                    yield j

        chunks = flatten_iterator(chunked_documents)
    elif args.chunks_source is not None:
        logger.info("Reading chunks from the chunks_source", extra={'print': True})

        files = pathlib.Path(args.chunks_source).rglob("**/*")

        chunks = read_chunks_into_documents(files)
    else:
        raise ValueError("Must specify either --chunks_source or --documents_source")

    create_embeddings(chunks,
                      previous_embeddings,
                      args.output,
                      args.embeddings_model,
                      args.batch_size)


def main_wrapper(args, logger):
    with track_activity(logger, "embed") as activity_logger:
        try:
            main(args, logger, activity_logger)
        except Exception:
            activity_logger.error(f"embed failed with exception: {traceback.format_exc()}")  # activity_logger doesn't log traceback
            raise


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    # If chunking done inline
    parser.add_argument("--documents_source", required=False, type=str)
    parser.add_argument("--source_glob",
                        type=str, default="**/*")
    parser.add_argument("--allowed_extensions", type=str, default=",".join(SUPPORTED_EXTENSIONS))
    parser.add_argument("--documents_source_base_url", type=str, default="")
    parser.add_argument("--document_path_replacement_regex", type=str, required=False)
    parser.add_argument("--chunk_size", type=int, default=512)
    parser.add_argument("--chunk_overlap", type=int, default=None)
    # If chunking was done separately
    parser.add_argument("--chunks_source", required=False, type=str)
    # If adding to previously generated Embeddings
    parser.add_argument("--previous_embeddings", required=False, type=str, default=None)
    parser.add_argument("--output", type=str)
    # Embeddings settings
    parser.add_argument("--embeddings_model", type=str, default="text-embedding-ada-002")
    parser.add_argument("--batch_size", type=int, default=1)
    args = parser.parse_args()

    print('\n'.join(f'{k}={v}' for k, v in vars(args).items()))

    enable_stdout_logging()
    enable_appinsights_logging()

    os.environ["OPENAI_API_KEY"] = get_secret_from_workspace("OPENAI-API-KEY")

    try:
        main_wrapper(args, logger)
    finally:
        if _logger_factory.appinsights:
            _logger_factory.appinsights.flush()
            time.sleep(5)
