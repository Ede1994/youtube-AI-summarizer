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
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi


# ***************************************************************************
# * Functions
# ***************************************************************************
def get_video_transcript(video_id):
    r"""
    Get the transcript of a YouTube video.
    
    Args:
        video_id (str): The ID of the YouTube video.
    
    Returns:
        str: The transcript of the video.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # return " ".join([entry['text'] for entry in transcript])
        return "Hello World!"
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"


def load_prompt(file_path):
    r"""
    Load the prompt from a file.

    Args:
        file_path (str): The path to the file containing the prompt.
    
    Returns:
        str: The prompt text.
    """
    return Path(file_path).read_text()