# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Azure OpenAI deployment related utils"""
from openai.api_resources.deployment import Deployment
import openai
from openai.util import convert_to_dict


def infer_deployment(aoai_connection, model_name):
    """Infer deployment name in an AOAI connection, given model name."""
    if "properties" not in aoai_connection:
        raise ValueError("Parameter 'aoai_connection' is not populated correctly. Deployment inferring cannot be performed.")
    if model_name is None or model_name == "":
        raise ValueError("Parameter 'model_name' has no value. Deployment inferring cannot be performed.")
    openai.api_type = aoai_connection["properties"]["metadata"]["ApiType"]
    openai.api_version = aoai_connection["properties"]["metadata"]["ApiVersion"]
    openai.api_base = aoai_connection["properties"]["target"]
    openai.api_key = aoai_connection["properties"]["credentials"]["key"]
    deployment_list = convert_to_dict(Deployment.list(api_key=openai.api_key, api_base=openai.api_base, api_type=openai.api_type))
    for deployment in deployment_list["data"]:
        if deployment["model"] == model_name:
            return deployment["id"]
    raise Exception(f"Deployment for model={model_name} not found in AOAI workspace. Please retry with correct model name or create a deployment.")
