import streamlit as st
import pytube

# importing packages
from pytube import YouTube
import os
import whisper
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns
nltk.download('vader_lexicon')

@st.cache_resource
def load_model():
    return whisper.load_model("base")

# Create a function to analyze sentiment
def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    return scores

st.set_page_config(layout="wide", page_title="Youtube Transcription",page_icon="▶️")
st.title("Extract text from Youtube video")
st.caption("Currently only supports English (more to come soon)")
url = st.text_input(
    "Youtube or Webpage URL",
    "",
    placeholder="https://www.youtube.com/watch?v=gIr9TQnV25A",
)
if st.button("Extract"):
    # url input from user
    yt = YouTube(str(url))
    st.markdown(f"<h2> Video Title : {yt.title}</h2> ", unsafe_allow_html=True)
    placeholder = st.empty()

    with st.spinner(text="Extracting audio from the video"):
        # extract only audio"
        video = yt.streams.filter(only_audio=True).first()

        # download the file
        out_file = video.download()

        model = load_model()
        result = model.transcribe(f"{out_file}")

        placeholder.text_area("Result",result["text"])
        scores = analyze_sentiment(result['text'])
        st.write("Sentiment scores:", scores)

        # Create a bar chart of the sentiment scores
        fig, ax = plt.subplots()
        ax.bar(scores.keys(), scores.values())
        st.pyplot(fig)
        
        os.remove(out_file)
