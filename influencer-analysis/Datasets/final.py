import os
import pandas as pd

# =========================
# BASE DIRECTORY (IMPORTANT FOR STREAMLIT)
# =========================
BASE_DIR = os.path.dirname(__file__)

# =========================
# LOAD DATASET
# =========================
input_path = os.path.join(BASE_DIR, "INFLUENCER_DATA.csv")
df = pd.read_csv(input_path)

# =========================
# SENTIMENT DIFFERENCE
# =========================
df["sentiment_difference"] = abs(
    df["speech_sentiment"] - df["product_sentiment"]
)

# =========================
# AUTHENTICITY SCORE CALCULATION
# =========================
df["authenticity_score"] = (1 - (df["sentiment_difference"] / 2)) * 100

# Clamp between 0 and 100
df["authenticity_score"] = df["authenticity_score"].clip(0, 100)

# =========================
# CLASSIFICATION FUNCTION
# =========================
def classify_authenticity(score):
    if score >= 80:
        return "Highly Authentic"
    elif score >= 50:
        return "Moderately Authentic"
    else:
        return "Low Authenticity"

df["authenticity_label"] = df["authenticity_score"].apply(classify_authenticity)

# =========================
# SAVE OUTPUT FILE (STREAMLIT SAFE)
# =========================
output_path = os.path.join(BASE_DIR, "INFLUENCER_AUTHENTICITY_ANALYSIS.csv")
df.to_csv(output_path, index=False)

# =========================
# OUTPUT
# =========================
print("Influencer Authenticity Analysis Completed Successfully!")

print(df[[
    "speech_sentiment",
    "product_sentiment",
    "sentiment_difference",
    "authenticity_score",
    "authenticity_label"
]].head())
