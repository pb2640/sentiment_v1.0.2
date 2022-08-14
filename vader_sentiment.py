"""
This app lets the user upload a df of size < = 200Mb,
with one of the columns as Text. It analyzes the sentiment
of the column and produces a dataframe ready to be downloaded
If there is a date column it also shows the sentiment trend over the 
time period
"""

# import libraries
import pandas as pd
import streamlit as st
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.title(
    "Upload a file with a column called text to produce the overall sentiment of the provided text"
)
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)
    analyzer = SentimentIntensityAnalyzer()
    if "text" not in df.columns:
        st.write("text column missing in the uploaded file")
    else:
        df["sentiment"] = ""
        # Add a placeholder
        latest_iteration = st.empty()
        bar = st.progress(0)
        div = (len(df) // 100) + 1
        for i in range(len(df)):
            df["sentiment"][i] = analyzer.polarity_scores(df["text"][i])
            latest_iteration.text(f"Iteration {i+1}")
            bar.progress(i // div + 1)
            time.sleep(0.1)

        st.write(df)

        # make a new col called sentiment
