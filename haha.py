import streamlit as st
from newspaper import Article
from googletrans import Translator
from textblob import TextBlob
from gtts import gTTS
import os
import nltk
import requests
from requests.exceptions import RequestException

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

# Function to translate text
def translate_text(text, target_language):
    translator = Translator()
    translated_text = translator.translate(text, src='auto', dest=target_language)
    return translated_text.text

# Function to extract and display article details
def extract_article_details(article_url, target_language):
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

    # Translate article summary
    if target_language != "Original" and target_language is not None:
        translated_summary = translate_text(article.summary, target_language)

        st.header(f"Translated Summary ({target_language})")
        st.write(translated_summary)

        # Text-to-speech conversion for the translated summary
        st.header("Listen to Translated Summary (Audio)")
        translated_audio_file = f"translated_summary_audio.mp3"
        tts = gTTS(text=translated_summary, lang=target_language)
        tts.save(translated_audio_file)
        st.audio(translated_audio_file, format='audio/mp3')

        # Delete the translated audio file after playing
        os.remove(translated_audio_file)

# Streamlit app
def main():
    st.title("Article Translator with Sentiment Analysis and Translation")

    # Input for article link and language selection
    article_link = st.text_input("Enter the article link:")
    target_language = st.selectbox("Select Target Language", ["en", "es", "fr", "de", "it", "ur"])  # Language codes

    if st.button("Translate"):
        if article_link:
            try:
                extract_article_details(article_link, target_language)
            except Exception as e:
                st.error("Error: Unable to translate the article. Please check the link.")

if __name__ == "__main__":
    main()
