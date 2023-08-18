#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/8/18
@Author  : mashenquan
@File    : openai_text_to_embedding.py
@Desc    : OpenAI Text-to-Embedding OAS3 api, which provides text-to-embedding functionality.
            For more details, checkout: `https://platform.openai.com/docs/api-reference/embeddings/object`
"""
import os
from pathlib import Path
from typing import List

import requests
from pydantic import BaseModel
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))  # fix-bug: No module named 'metagpt'
from metagpt.utils.common import initialize_environment
from metagpt.logs import logger


class Embedding(BaseModel):
    """Represents an embedding vector returned by embedding endpoint."""
    object: str  # The object type, which is always "embedding".
    embedding: List[
        float]  # The embedding vector, which is a list of floats. The length of vector depends on the model as listed in the embedding guide.
    index: int  # The index of the embedding in the list of embeddings.


class Usage(BaseModel):
    prompt_tokens: int
    total_tokens: int


class ResultEmbedding(BaseModel):
    object: str
    data: List[Embedding]
    model: str
    usage: Usage


class OpenAIText2Embedding:
    def __init__(self, openai_api_key):
        """
        :param openai_api_key: OpenAI API key, For more details, checkout: `https://platform.openai.com/account/api-keys`
        """
        self.openai_api_key = openai_api_key if openai_api_key else os.environ.get('OPENAI_API_KEY')

    def text_2_embedding(self, text, model="text-embedding-ada-002"):
        """Text to embedding

        :param text: The text used for embedding.
        :param model: One of ['text-embedding-ada-002'], ID of the model to use. For more details, checkout: `https://api.openai.com/v1/models`.
        :return: A json object of :class:`ResultEmbedding` class if successful, otherwise `{}`.
        """

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai_api_key}"
        }
        data = {"input": text, "model": model}
        try:
            response = requests.post("https://api.openai.com/v1/embeddings", headers=headers, json=data)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx responses
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred:{e}")
        return {}


# Export
def oas3_openai_text_to_embedding(text, model="text-embedding-ada-002", openai_api_key=""):
    """Text to embedding

    :param text: The text used for embedding.
    :param model: One of ['text-embedding-ada-002'], ID of the model to use. For more details, checkout: `https://api.openai.com/v1/models`.
    :param openai_api_key: OpenAI API key, For more details, checkout: `https://platform.openai.com/account/api-keys`
    :return: A json object of :class:`ResultEmbedding` class if successful, otherwise `{}`.
    """
    if not text:
        return ""
    if not openai_api_key:
        openai_api_key = os.environ.get("OPENAI_API_KEY")
    return OpenAIText2Embedding(openai_api_key).text_2_embedding(text, model=model)


if __name__ == "__main__":
    initialize_environment()

    v = oas3_openai_text_to_embedding("Panda emoji")
    print(v)
