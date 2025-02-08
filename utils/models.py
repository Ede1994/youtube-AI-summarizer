#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Date   :    08.02.2025
Author :    Eric Einspänner
Mail   :    eric.einspaenner@med.ovgu.de
'''


# ***************************************************************************
# * Import
# ***************************************************************************
from google import genai
from mistralai import Mistral


# ***************************************************************************
# * Functions
# ***************************************************************************
def gemini_chat(content, api_key, model="gemini-2.0-flash"):
    r"""
    Chat with the Gemini API.
    
    Args:
        api_key (str): The API key for the Gemini API.
        model (str): The model to use for the chat.
        content (str): The content to send to the API.
    
    Returns:
        str: The response from the API.
    """
    # Initialize the Gemini API
    client = genai.Client(api_key=api_key)
    
    # Chat with the API
    response = client.models.generate_content(model=model,
                                              contents=content)
    
    # Return the response
    return response.text


def mistral_chat(content, api_key, model="mistral-small-latest"):
    r"""
    Chat with the Mistral API.
    
    Args:
        api_key (str): The API key for the Mistral API.
        model (str): The model to use for the chat.
        messages (list): A list of messages to send to the API.
    
    Returns:
        str: The response from the API.
    """
    # Initialize the Mistral API
    mistral = Mistral(api_key=api_key)
    
    # Chat with the API
    response = mistral.chat.complete(model=model, messages=[
        {
            "content": content,
            "role": "user",
        },
    ], stream=False)

    # Return the response
    return response.choices[0].message.content