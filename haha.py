import streamlit as st
from newspaper import Article
from gtts import gTTS
import os
from textblob import TextBlob
import requests
from requests.exceptions import RequestException
import nltk

# Download 'punkt' tokenizer if not already downloaded
nltk.download('punkt', quiet=True)

# Function to perform sentiment analysis
def perform_sentiment_analysis(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    subjectivity_score = blob.sentiment.subjectivity
    if sentiment_score > 0:
        sentiment = "Positive"
    elif sentiment_score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return sentiment, sentiment_score, subjectivity_score

# Function to extract and display article details
def extract_article_details(article_url):
    try:
        response = requests.get(article_url, timeout=10)  # Check if URL is accessible
        if response.status_code == 200:
            article = Article(article_url)
            article.download()
            article.parse()
            article.nlp()

            st.header("Article Details")
            
            # Display complete text
            st.subheader("Complete Text")
            st.write(article.text)

            # Display author name
            st.subheader("Author")
            st.write(article.authors[0] if article.authors else "Not available")

            # Display publication date
            st.subheader("Publication Date")
            st.write(article.publish_date)

            # Display keywords
            st.subheader("Keywords")
            st.write(", ".join(article.keywords))

            # Display article summary
            st.header("Article Summary")
            st.subheader(article.title)
            st.write(article.summary)

            # Perform sentiment analysis on the article summary
            sentiment, polarity, subjectivity = perform_sentiment_analysis(article.summary)
            st.subheader("Sentiment Analysis (Article Summary)")
            st.write(f"Sentiment: {sentiment}")
            st.write(f"Polarity Score: {polarity}")
            st.write(f"Subjectivity Score: {subjectivity}")

            # Text-to-speech conversion for the article summary
            st.header("Listen to Article Summary (Audio)")
            audio_file = f"article_summary_audio.mp3"
            tts = gTTS(text=article.summary, lang='en')  # Change 'en' for different languages
            tts.save(audio_file)
            st.audio(audio_file, format='audio/mp3')

            # Delete the audio file after playing
            os.remove(audio_file)
        else:
            st.error("Error: Unable to access the article. Please check the link.")
    except Exception as e:
        st.error(f"Error: Unable to analyze the article. Error details: {e}")

# Streamlit app
def main():
    st.title("Article Analyzer with Text-to-Speech")

    # Input for article link
    article_link = st.text_input("Enter the article link:")

    if st.button("Analyze Article"):
        if article_link:
            try:
                extract_article_details(article_link)
            except Exception as e:
                st.error("Error: Unable to analyze the article. Please check the link.")

if __name__ == "__main__":
    main()
