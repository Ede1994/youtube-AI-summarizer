#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Project:    YouTube AI Summarizer
Date   :    07.02.2025
Author :    Eric Einspänner
Mail   :    eric.einspaenner@med.ovgu.de
'''

__version__ = "0.1.0"


# ***************************************************************************
# * Import
# ***************************************************************************
import os
from pathlib import Path
import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
from utils.utils import get_video_transcript, load_prompt


# ***************************************************************************
# * Config
# ***************************************************************************
# Load environment variables
load_dotenv()
# Get API keys from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initializing model
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

# Configure the API Key
genai.configure(api_key=GEMINI_API_KEY)


# ***************************************************************************
# * Functions
# ***************************************************************************
def main():
    # Set page config
    st.set_page_config(
        page_title="YouTube AI Summarizer",
        page_icon="🎥",
        layout="wide"
    )

    # Custom CSS
    st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
        text-align: center;
    }
    .summary-box, .notes-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        text-align: center;
    }
    .center-content {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    .footer {
        text-align: center;
    }
    .button-container {
        display: flex;
        justify-content: center;
        gap: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Center the main content
    st.markdown('<div class="center-content">', unsafe_allow_html=True)

    # Title with icon
    st.markdown('<p class="big-font">YouTube AI Summarizer</p>', unsafe_allow_html=True)

    # Input field with icon
    youtube_url = st.text_input("🔗 Enter your YouTube video URL here:")

    # Load prompts
    summarize_prompt = load_prompt("config/summarize_prompt.txt")
    notes_prompt = load_prompt("config/notes_prompt.txt")

    # Button container
    st.markdown('<div class="button-container">', unsafe_allow_html=True)

    # Summarize button
    if st.button("🚀 Summarize"):
        if GEMINI_API_KEY is None:
            st.error("❌ API Key is not set. Please set the API key in the .env file.")
        else:
            with st.spinner("🔍 Analyzing video content (this can take a few minutes)..."):
                # Extract video ID from URL
                video_id = youtube_url.split("v=")[1] if "v=" in youtube_url else youtube_url.split("/")[-1]
                
                # Get video transcript
                transcript = get_video_transcript(video_id)
                
                # Prepare prompt for Gemini
                prompt = summarize_prompt.format(transcript=transcript)
                
                # Generate summary
                response = model.generate_content(prompt)
                
                # Display summary in a styled box
                st.markdown('<div class="summary-box">', unsafe_allow_html=True)
                st.subheader("📊 Video Summary")
                st.write(response.text)
                st.markdown('</div>', unsafe_allow_html=True)

    # Notes button
    if st.button("📝 Notes"):
        if GEMINI_API_KEY is None:
            st.error("❌ API Key is not set. Please set the API key in the .env file.")
        else:
            with st.spinner("🔍 Analyzing video content (this can take a few minutes)..."):
                # Extract video ID from URL
                video_id = youtube_url.split("v=")[1] if "v=" in youtube_url else youtube_url.split("/")[-1]
                
                # Get video transcript
                transcript = get_video_transcript(video_id)
                
                # Prepare prompt for Gemini
                prompt = notes_prompt.format(transcript=transcript)
                
                # Generate notes
                response = model.generate_content(prompt)
                
                # Display notes in a styled box
                st.markdown('<div class="notes-box">', unsafe_allow_html=True)
                st.subheader("📊 Video Notes")
                st.write(response.text)
                st.markdown('</div>', unsafe_allow_html=True)

    # Close the button-container div
    st.markdown('</div>', unsafe_allow_html=True)

    # Close the center-content div
    st.markdown('</div>', unsafe_allow_html=True)

    # Add some space
    st.write("")
    st.write("")

    # Footer
    st.markdown("""
    <div class="footer">
        <p>Developed by Eric Einspänner</p>
        <a href="https://github.com/Ede1994" target="_blank"><i class="fab fa-github social-icons"></i></a>
    </div>
    """, unsafe_allow_html=True)

    # Include Font Awesome for social icons
    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">
    """, unsafe_allow_html=True)


# ***************************************************************************
# * Main
# ***************************************************************************
if __name__ == "__main__":
    main()