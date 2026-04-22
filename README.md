# Cyberbullying Detection System ���

## Overview
This project is a web-based application that detects cyberbullying in text using a multilingual transformer model. It classifies input as CYBERBULLYING or NON-CYBERBULLYING with a confidence score.

## Features
- Real-time cyberbullying detection
- Confidence score and probability
- Multilingual support (XLM-RoBERTa)
- Streamlit web interface

## Tech Stack
- Python
- Streamlit
- PyTorch
- Hugging Face Transformers
- NumPy, Emoji, Regex

## Model
This project uses XLM-RoBERTa for classification.

The trained model (~1GB) is NOT included due to GitHub size limits.

## Model Setup
The model is loaded automatically from Hugging Face during first run.

Requirements:
- Internet connection (first time only)
- Model will be cached locally

## Project Structure
CYBERBULLYING/
│── app.py
│── predict_function.py
│── requirements.txt

## How to Run
pip install -r requirements.txt  
streamlit run app.py  

## Notes
- Model not uploaded due to size
- Loaded dynamically when running

