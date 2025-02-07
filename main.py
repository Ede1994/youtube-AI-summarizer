#import required packages
import streamlit as st
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Get API keys from environment variables
GEMINI_API_KEY = os.getenv("Api_Key")

#Initializing model
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

#Configure the API Key
genai.configure(api_key=GEMINI_API_KEY)

#Function to get Video Transcripts
def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript])
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"

#Main Function includes the page items
def main():
    # Set page config
    st.set_page_config(
        page_title="AI Video Summarizer",
        page_icon="🎥",
        layout="wide"
    )

    # Custom CSS
    st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .summary-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Title with icon
    st.markdown('<p class="big-font">🎥 AI Video Summarizer</p>', unsafe_allow_html=True)

    # Subtitle
    st.write("📝 Get a quick summary of any YouTube video!")

    # Input field with icon
    youtube_url = st.text_input("🔗 Enter your YouTube video URL here:")

    # Button with icon
    if st.button("🚀 Summarize"):
        if GEMINI_API_KEY is None:
            st.error("❌ API Key is not set. Please set the API key in the .env file.")
        else:
            with st.spinner("🔍 Analyzing video content..."):
                # Extract video ID from URL
                video_id = youtube_url.split("v=")[1] if "v=" in youtube_url else youtube_url.split("/")[-1]
                
                # Get video transcript
                transcript = get_video_transcript(video_id)
                
                # Prepare prompt for Gemini
                # Can customize the prompt as per needed
                prompt = f"""
                Task: Provide a detailed and accurate summary of the following YouTube video based on its transcript.

                Video Title: video_title
                Video Description: video_description

                Transcript:
                {transcript}

                Please summarize the video content must following these guidelines same format:
                1. Main Topic: Identify and explain the primary subject or theme of the video.
                2. Key Points: List and briefly explain the main ideas or arguments presented.
                3. Supporting Information: Mention any significant facts, statistics, or examples used to support the main points.
                4. Structure: Describe how the video is organized (e.g., chronological, problem-solution, comparison, etc.).
                5. Conclusion: Summarize the video's conclusion or main takeaway.
                6. Tone and Style: Comment on the presenter's tone (formal, casual, humorous, etc.) and presentation style.
                7. Target Audience: Identify who this video seems to be aimed at.
                8. Length: Provide a summary of approximately 250-300 words.

                Please ensure the summary is coherent, well-structured, and captures the essence of the video content.
                """
                
                # Generate summary
                response = model.generate_content(prompt)
                
                # Display summary in a styled box
                st.markdown('<div class="summary-box">', unsafe_allow_html=True)
                st.subheader("📊 Video Summary")
                st.write(response.text)
                st.markdown('</div>', unsafe_allow_html=True)

    # Add some space
    st.write("")
    st.write("")

    # Footer
    st.markdown("""
    <div class="footer">
        <p>Developed  by ❤️ Sandeep Gudisa</p>
        <a href="https://github.com/GudisaSandeep" target="_blank"><i class="fab fa-github social-icons"></i></a>
        <a href="https://www.linkedin.com/public-profile/settings?trk=d_flagship3_profile_self_view_public_profile" target="_blank"><i class="fab fa-linkedin social-icons"></i></a>
        <a href="https://www.youtube.com/@AIProgrammingTelugu/featured" target="_blank"><i class="fab fa-youtube social-icons"></i></a>
    </div>
    """, unsafe_allow_html=True)

    # Include Font Awesome for social icons
    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    #Main Execution
    main()