#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Project:    YouTube AI Summarizer
Date   :    18.02.2025
Author :    Eric Einspänner
Mail   :    eric.einspaenner@med.ovgu.de
'''

__version__ = "0.3.1"


# ***************************************************************************
# * Import
# ***************************************************************************
import os
import streamlit as st
from dotenv import load_dotenv
from utils.models import gemini_chat, mistral_chat
from utils.utils import get_video_transcript, load_prompt


# ***************************************************************************
# * Config
# ***************************************************************************
# Load environment variables
load_dotenv()

### Get API keys from environment variables
# Google Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Mistral
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")


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


    # Initialize session state for selected_model
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = None
    
    # Initialize response
    response = ""

    # Mistral and Gemini buttons side by side in the center
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("〽️ Mistral", use_container_width=True):
            # selected_model = "mistral"
            st.session_state.selected_model = "mistral"
    with col2:
        if st.button("🤖 Gemini", use_container_width=True):
            st.session_state.selected_model = "gemini"
    with col3:
        if st.button("More is coming!", use_container_width=True):
            st.write("More is coming!")
            st.session_state.selected_model = None


    # Input field with icon
    youtube_url = st.text_input("🔗 Enter your YouTube video URL here:")

    # Load prompts
    summarize_prompt = load_prompt("config/summarize_prompt.txt")
    notes_prompt = load_prompt("config/notes_prompt.txt")

    # Button container
    st.markdown('<div class="button-container2">', unsafe_allow_html=True)
    col4, col5 = st.columns(2)

    # Summarize button
    with col4:
        if st.button("🚀 Summarize", use_container_width=True):
            if GEMINI_API_KEY is None:
                st.error("❌ Gemini API Key is not set. Please set the API key in the .env file.")
            elif MISTRAL_API_KEY is None and st.session_state.selected_model == "mistral":
                st.error("❌ Mistral API Key is not set. Please set the API key in the .env file.")
            else:
                with st.spinner("🔍 Analyzing video content (this can take a few minutes)..."):
                    # Extract video ID from URL
                    video_id = youtube_url.split("v=")[1] if "v=" in youtube_url else youtube_url.split("/")[-1]
                    
                    # Get video transcript
                    transcript = get_video_transcript(video_id)
                    
                    # Prepare prompt for Gemini
                    prompt = summarize_prompt.format(transcript=transcript)
                    
                    # Generate summary
                    if st.session_state.selected_model == "gemini":
                        response = gemini_chat(content=prompt, api_key=GEMINI_API_KEY)
                    elif st.session_state.selected_model == "mistral":
                        response = mistral_chat(content=prompt, api_key=MISTRAL_API_KEY)


    # Notes button
    with col5:
        if st.button("📝 Notes", use_container_width=True):
            if GEMINI_API_KEY is None:
                st.error("❌ Gemini API Key is not set. Please set the API key in the .env file.")
            elif MISTRAL_API_KEY is None and st.session_state.selected_model == "mistral":
                st.error("❌ Mistral API Key is not set. Please set the API key in the .env file.")
            else:
                with st.spinner("🔍 Analyzing video content (this can take a few minutes)..."):
                    # Extract video ID from URL
                    video_id = youtube_url.split("v=")[1] if "v=" in youtube_url else youtube_url.split("/")[-1]
                    
                    # Get video transcript
                    transcript = get_video_transcript(video_id)
                    
                    # Prepare prompt for Gemini
                    prompt = notes_prompt.format(transcript=transcript)
                    
                    # Generate notes
                    if st.session_state.selected_model == "gemini":
                        response = gemini_chat(content=prompt, api_key=GEMINI_API_KEY)
                    elif st.session_state.selected_model == "mistral":
                        response = mistral_chat(content=prompt, api_key=MISTRAL_API_KEY)
                    
    # Display response in a styled box
    st.markdown('<div class="response-box">', unsafe_allow_html=True)
    st.subheader("📊 Response")
    st.write(response)
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
        <p>Developed by Ede1994</p>
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