# Function to extract audio from video
def extract_audio(filepath):
    st.write('Extracting audio from video file...')
    tic = time.time()
    dirname = os.path.dirname(filepath)
    file_name = os.path.basename(filepath)
    file_basename = file_name.split('.')[0]
    mp3_path = os.path.join(dirname, file_basename+".mp3")
    subprocess.run(['ffmpeg', '-i', filepath, '-f', 'mp3', '-ab', '192000', '-vn', mp3_path])
    toc = time.time()
    st.write(f'Time for extract_audio: {toc-tic}s')
    return mp3_path

# Function to extract subtitles
def extract_subtitle(filepath, model_size, srt_path):
    tic = time.time()
    st.write('Loading model...')
    model = whisper.load_model(model_size)
    
    st.write('Transcribing in progress...')
    result = model.transcribe(audio=filepath)
    st.write('Done')
    
    toc = time.time()
    st.write(f'Time for extract_subtitle: {toc-tic}s')

    from whisper.utils import WriteSRT
    with open(srt_path, "w", encoding="utf-8") as srt:
        writer = WriteSRT(os.path.dirname(filepath))
        writer.write_result(result, srt)

# Function to merge subtitles with video
def merge_subtitles(video_path, srt_path, output_path):
    st.write('Merging subtitles with video...')
    subprocess.run(['ffmpeg', '-i', video_path, '-vf', f'subtitles={srt_path}', output_path])
    st.write('Subtitles merged successfully.')

# Streamlit UI
st.title("Video Transcription and Subtitle Extraction")

uploaded_file = st.file_uploader("Choose a video file", type=["mp4"])
model_size = st.selectbox("Select Whisper model size", ["base", "small", "medium", "large-v1", "large-v2"])
submit_button = st.button("Process Video")

if uploaded_file is not None and submit_button:
    video_path = Path(uploaded_file.name)
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())

    mp3_path = extract_audio(video_path)
    srt_path = video_path.with_suffix('.srt')
    extract_subtitle(mp3_path, model_size, srt_path)

    # Manually create new file name for the output video
    output_path = video_path.stem + '_subtitled.mp4'
    output_path = Path(output_path)
    
    merge_subtitles(str(video_path), str(srt_path), str(output_path))
    
    st.success('Process complete!')
    st.video(output_path)
