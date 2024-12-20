import streamlit as st
import yt_dlp
import os


def download_youtube_as_mp3(youtube_url, quality, output_path="downloads"):
    try:
        # Create output path if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        ydl_opts = {
            'format': 'bestaudio/best',  # Download the best audio format available
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Save as title.mp3
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',  # Use FFmpeg to extract audio
                'preferredcodec': 'mp3',  # Convert to MP3 format
                'preferredquality': str(quality),  # Set audio quality
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            mp3_filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
        return mp3_filename
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


def download_youtube_video(youtube_url, resolution, output_path="downloads"):
    try:
        # Create output path if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # yt-dlp options for specific resolution
        ydl_opts = {
            'format': f'bestvideo[height<={resolution}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            # MP4 format with resolution cap
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Save as title.mp4
            'merge_output_format': 'mp4',  # Merge audio and video into MP4
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            mp4_filename = ydl.prepare_filename(info)
        return mp4_filename
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


# Streamlit app
st.title("Download Audio and Video from YouTube")

# Input field for YouTube link
youtube_url = st.text_input("Enter the YouTube URL:")

# Dropdown for audio quality
quality = st.radio(
    "Select MP3 Quality (kbps):",
    options=[128, 192, 256, 320],
    index=0,  # Default to 192 kbps
)

# Button to trigger the conversion
if st.button("Download Audio Mp3"):
    if youtube_url:
        with st.spinner("Downloading and converting..."):
            mp3_file = download_youtube_as_mp3(youtube_url, quality)
        if mp3_file:
            st.success("Conversion complete!")
            st.download_button(
                label="Download MP3",
                data=open(mp3_file, "rb"),
                file_name=os.path.basename(mp3_file),
                mime="audio/mpeg"
            )
    else:
        st.warning("Please enter a valid YouTube URL.")

# Dropdown for video resolution
resolution = st.radio(
    "Select Video Resolution:",
    options=["360", "720", "1080"],
    index=0,  # Default to 720p
)

# Button to trigger the download
if st.button("Download Video Mp4"):
    if youtube_url:
        with st.spinner("Downloading video..."):
            video_file = download_youtube_video(youtube_url, resolution)
        if video_file:
            st.success("Download complete!")
            st.download_button(
                label="Download MP4",
                data=open(video_file, "rb"),
                file_name=os.path.basename(video_file),
                mime="video/mp4"
            )
    else:
        st.warning("Please enter a valid YouTube URL.")

