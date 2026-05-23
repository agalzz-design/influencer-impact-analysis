# Influencer Impact: Analyzing the Authenticity of Social Media Influencers on Product Promotion

## Project Overview
This project focuses on analyzing whether social media influencers genuinely recommend products or promote them mainly for sponsorship purposes. The system compares influencer opinions with actual customer reviews to measure authenticity using sentiment analysis and engagement metrics.

The project combines YouTube influencer analysis, Amazon product review analysis, Natural Language Processing (NLP), speech-to-text conversion, and machine learning to generate an Authenticity Score.

---

## Objectives
- Analyze influencer product promotions using real-time data
- Extract YouTube video metrics using YouTube API
- Scrape Amazon product reviews and ratings
- Convert influencer speech into text using OpenAI Whisper
- Perform sentiment analysis using RoBERTa NLP model
- Compare influencer sentiment with customer sentiment
- Generate an authenticity score and classification
- Visualize insights using an interactive Streamlit dashboard

---

## System Architecture

### 1. Influencer Data Collection
YouTube API is used for collecting:
- Views
- Likes
- Comments
- Video descriptions

### 2. Audio Processing
Influencer speech is converted into text using:
- OpenAI Whisper Large Model

### 3. Product Review Collection
Amazon reviews are collected using:
- Selenium WebDriver

### 4. Sentiment Analysis
Speech transcripts and customer reviews are analyzed using:
- CardiffNLP RoBERTa Sentiment Model

### 5. Authenticity Scoring
The system compares:
- Influencer sentiment
- Customer review sentiment
- Product ratings
- Engagement rate
- Sponsorship indicators

Final score classification:
- Highly Authentic
- Moderately Authentic
- Low Authenticity

---

## Technologies Used

### Programming Language
- Python

### Libraries and Frameworks
- Pandas
- NumPy
- Streamlit
- Plotly
- Selenium
- Transformers
- Whisper

### APIs and Models
- YouTube Data API
- OpenAI Whisper
- CardiffNLP RoBERTa Model

---

## Dashboard Features
- KPI Metrics Panel
- Authenticity Score Gauge
- Sentiment Comparison Charts
- Global Sentiment Scatter Plot
- Promotion History Table
- Interactive Data Visualization

---

## Dataset
The project evaluates:
- 50 influencer-product combinations
- Amazon product reviews
- YouTube influencer videos
- Speech transcripts
- Sentiment datasets

---

## Future Enhancements
- Multi-platform analysis:
  - Instagram
  - TikTok
  - Facebook

- Real-time automated pipelines
- Computer Vision for product overlay detection
- Deep learning for persuasive speech analysis

---

## Conclusion
This project demonstrates that high engagement alone does not indicate influencer credibility. By combining speech-to-text processing, NLP sentiment analysis, and customer review comparison, the system provides a data-driven framework to evaluate influencer authenticity.

---

## Developed By
Agalya S
