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

st.subheader(
    "Upload a file with a column called text to produce the overall sentiment of the provided text"
)
st.caption("Author : Parth Bhardwaj")
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)
    analyzer = SentimentIntensityAnalyzer()
    if "text" not in df.columns:
        st.write("text column missing in the uploaded file")
    else:
        df["overall_score"] = ""
        df["positive"] = ""
        df["negative"] = ""
        df["neutral"] = ""
        # Add a placeholder
        latest_iteration = st.empty()
        bar = st.progress(0)
        div = (len(df) // 100) + 1
        for i in range(len(df)):
            output = analyzer.polarity_scores(df["text"][i])
            df["overall_score"][i] = output["compound"]
            df["positive"][i] = output["pos"]
            df["negative"][i] = output["neu"]
            df["neutral"][i] = output["neg"]
            latest_iteration.text(f"{i+1} Sentences Analyzed")
            bar.progress(i // div + 1)
            time.sleep(0.1)

        st.write(df)
        @st.cache
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(df)

        st.download_button(
            label="Download result as CSV",
            data=csv,
            file_name=str(time.time())+'result_df.csv',
            mime='text/csv',
        )
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
        # make a new col called sentiment
