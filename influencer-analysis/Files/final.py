

import pandas as pd



# Required Columns:
# speech_sentiment  (-1 to +1)
# product_sentiment (-1 to +1)

df = pd.read_csv("INFLUENCER_DATA.csv")


df["sentiment_difference"] = abs(
    df["speech_sentiment"] - df["product_sentiment"]
)



df["authenticity_score"] = (1 - (df["sentiment_difference"] / 2)) * 100

# Safety clamp (prevents negative values)
df["authenticity_score"] = df["authenticity_score"].clip(0, 100)


def classify_authenticity(score):

    if score >= 80:
        return "Highly Authentic"
    
    elif score >= 50:
        return "Moderately Authentic"
    
    else:
        return "Low Authenticity"

df["authenticity_label"] = df["authenticity_score"].apply(classify_authenticity)


df.to_csv("INFLUENCER_AUTHENTICITY_ANALYSIS.csv", index=False)

print("Influencer Authenticity Analysis Completed Successfully!")
print(df[["speech_sentiment",
          "product_sentiment",
          "sentiment_difference",
          "authenticity_score",
          "authenticity_label"]].head())
