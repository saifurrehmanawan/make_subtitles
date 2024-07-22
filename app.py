import streamlit as st
import subprocess

def generate_subtitles(video_path, lang):
    subprocess.run(["python3", "transcript.py", "-i", video_path, "-l", lang, "-o", "output.srt"])

def translate_subtitles(input_srt, src_lang, output_srt, tgt_lang, token):
    subprocess.run(["python3", "translate.py", "-i", input_srt, "-il", src_lang, "-o", output_srt, "-ol", tgt_lang, "-t", token])

def merge_subtitles(video_path, srt_path):
    subprocess.run(["./merge-srt-to-mp4.sh", video_path, srt_path])

st.title("Auto Subtitle Generator")

uploaded_file = st.file_uploader("Upload a video file", type=["mp4"])

if uploaded_file is not None:
    video_path = f"./{uploaded_file.name}"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())

    st.video(video_path)

    lang = st.selectbox("Select language for transcription", ["English", "Japanese", "Spanish", "Chinese"])
    src_lang = lang.lower()

    if st.button("Generate Subtitles"):
        generate_subtitles(video_path, src_lang)
        st.success("Subtitles generated!")

    if st.button("Translate Subtitles"):
        tgt_lang = st.selectbox("Select target language for translation", ["Chinese", "Japanese", "Spanish"])
        output_srt = "translated.srt"
        api_token = st.text_input("Enter ChatGPT API Token")
        if api_token:
            translate_subtitles("output.srt", src_lang, output_srt, tgt_lang, api_token)
            st.success("Subtitles translated!")

    if st.button("Merge Subtitles with Video"):
        merge_subtitles(video_path, "translated.srt")
        st.video(f"{video_path}_with_subtitles.mp4")
        st.success("Subtitles merged with video!")
