

# ================= IMPORTS =================
import re
import time
import torch
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from transformers import pipeline
from googleapiclient.discovery import build


# ================= CONFIG =================
API_KEY = "API_KEY"

DEVICE = 0 if torch.cuda.is_available() else -1

youtube = build("youtube", "v3", developerKey=API_KEY)

sentiment_model = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
    top_k=None,
    device=DEVICE
)


# ================= TEXT UTILITIES =================
def clean_text(text):

    text = str(text).lower()

    # remove links
    text = re.sub(r"http\S+", "", text)

    # keep tamil + english
    text = re.sub(r"[^\w\s₹\.]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize(score):

    return round(max(min(score, 1), -1), 4)


# ================= SENTIMENT FUNCTIONS =================
def paragraph_sentiment(text):

    if not text.strip():
        return 0.0

    text = clean_text(text)[:512]

    result = sentiment_model(text)[0]

    scores = {x["label"]: x["score"] for x in result}

    positive = scores.get("LABEL_2", 0)
    negative = scores.get("LABEL_0", 0)

    sentiment = positive - negative

    return normalize(sentiment)


def product_review_overall_sentiment(reviews):

    scores = []

    for review in reviews:

        review = review.strip()

        if len(review.split()) < 3:
            continue

        review = clean_text(review)[:512]

        result = sentiment_model(review)[0]

        score_dict = {x["label"]: x["score"] for x in result}

        positive = score_dict.get("LABEL_2", 0)
        negative = score_dict.get("LABEL_0", 0)

        sentiment = positive - negative

        scores.append(sentiment)

    if scores:

        avg_score = sum(scores) / len(scores)

        return normalize(avg_score), len(scores)

    else:

        return 0.0, 0


# ================= AMAZON SCRAPER =================
def get_amazon_product_details(url):

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    wait = WebDriverWait(driver, 10)

    driver.get(url)

    try:

        product_name = wait.until(
            EC.presence_of_element_located((By.ID, "productTitle"))
        ).text.strip()

    except:

        product_name = "Unknown Product"

    try:

        rating = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[@data-hook='rating-out-of-text']")
            )
        ).text.split(" ")[0]

        product_rating = float(rating)

    except:

        product_rating = 0.0

    try:

        category = wait.until(
            EC.presence_of_element_located((By.ID, "nav-subnav"))
        ).text.strip()

    except:

        category = "Unknown Category"

    driver.quit()

    return product_name, product_rating, category


# ================= SPONSORED LOGIC =================

SPONSORED_KEYWORDS = [
    "sponsored",
    "paid partnership",
    "affiliate",
    "amazon link",
    "buy using my link",
    "use my code",
    "earn commission",
    "#ad"
]

PRODUCT_DETAIL_KEYWORDS = [
    "price",
    "₹",
    "rs",
    "features",
    "benefits",
    "how to use",
    "available on",
    "amazon",
    "flipkart"
]


def contains_promo(text):

    text = clean_text(text)

    return any(k in text for k in SPONSORED_KEYWORDS)


def has_full_product_details(text):

    text = clean_text(text)

    count = sum(k in text for k in PRODUCT_DETAIL_KEYWORDS)

    return count >= 3


def final_sponsored_decision(description, speech_score):

    if contains_promo(description):

        return True

    if has_full_product_details(description):

        return True

    if speech_score >= 0.85:

        return True

    return False


# ================= VIDEO PRODUCT MAP =================


video_product_map = [
{"video_url":"https://youtube.com/shorts/brMLaEj9cEE","audio_file":r"C:\Users\welcome-pc\influencer\speech1.txt","product_link":"https://amzn.in/d/5tC5yPH","review_file":r"C:\Users\welcome-pc\reviews\product1_reviews.txt","has_product_overlay":False},
{"video_url":"https://youtube.com/shorts/vjJ_nJ5b_RE","audio_file":r"C:\Users\welcome-pc\influencer\speech2.txt","product_link":"https://amzn.in/d/8CEAzNB","review_file":r"C:\Users\welcome-pc\reviews\product2_reviews.txt","has_product_overlay":True},
{"video_url":"https://youtube.com/shorts/rbvObFG8AOo","audio_file":r"C:\Users\welcome-pc\influencer\speech3.txt","product_link":"https://amzn.in/d/427Soas","review_file":r"C:\Users\welcome-pc\reviews\product3_reviews.txt","has_product_overlay":True},
{"video_url":"https://youtube.com/shorts/hYZK0Cp1x4g","audio_file":r"C:\Users\welcome-pc\influencer\speech4.txt","product_link":"https://amzn.in/d/2TKgouT","review_file":r"C:\Users\welcome-pc\reviews\product4_reviews.txt","has_product_overlay":True},
{"video_url":"https://youtube.com/shorts/fWws53YY1uY","audio_file":r"C:\Users\welcome-pc\influencer\speech5.txt","product_link":"https://amzn.in/d/ctIrQZv","review_file":r"C:\Users\welcome-pc\reviews\product5_reviews.txt","has_product_overlay":True},

{"video_url":"https://youtube.com/shorts/CsB0UrEKWYM","audio_file":r"C:\Users\welcome-pc\influencer\speech6.txt","product_link":"https://amzn.in/d/8Im00kA","review_file":r"C:\Users\welcome-pc\reviews\product6_reviews.txt","has_product_overlay":False},
{"video_url":"https://youtube.com/shorts/a6m0TahEPiY","audio_file":r"C:\Users\welcome-pc\influencer\speech7.txt","product_link":"https://amzn.in/d/0NPA7Ds","review_file":r"C:\Users\welcome-pc\reviews\product7_reviews.txt","has_product_overlay":False},
{"video_url":"https://youtube.com/shorts/cj4s8d3MaME","audio_file":r"C:\Users\welcome-pc\influencer\speech8.txt","product_link":"https://amzn.in/d/0wUp3Pd","review_file":r"C:\Users\welcome-pc\reviews\product8_reviews.txt","has_product_overlay":True},
{"video_url":"https://youtube.com/shorts/QqDLutjCLEI","audio_file":r"C:\Users\welcome-pc\influencer\speech9.txt","product_link":"https://amzn.in/d/4sUTIi9","review_file":r"C:\Users\welcome-pc\reviews\product9_reviews.txt","has_product_overlay":True},
{"video_url":"https://youtube.com/shorts/oQW2cIl1cIY","audio_file":r"C:\Users\welcome-pc\influencer\speech10.txt","product_link":"https://amzn.in/d/gbKbYmS","review_file":r"C:\Users\welcome-pc\reviews\product10_reviews.txt","has_product_overlay":False},

{"video_url":"https://youtube.com/shorts/nl5i1N44rZo","audio_file":r"C:\Users\welcome-pc\influencer\speech11.txt","product_link":"https://amzn.in/d/dquNRAL","review_file":r"C:\Users\welcome-pc\reviews\product11_reviews.txt","has_product_overlay":True},
{"video_url":"https://youtube.com/shorts/5jp05FnMo6c","audio_file":r"C:\Users\welcome-pc\influencer\speech12.txt","product_link":"https://amzn.in/d/fZlEsHA","review_file":r"C:\Users\welcome-pc\reviews\product12_reviews.txt","has_product_overlay":False},
{"video_url":"https://youtube.com/shorts/i4hTCEEVQRQ","audio_file":r"C:\Users\welcome-pc\influencer\speech13.txt","product_link":"https://amzn.in/d/5TYbeIc","review_file":r"C:\Users\welcome-pc\reviews\product13_reviews.txt","has_product_overlay":False},
{"video_url":"https://youtube.com/shorts/XPX6_xxamxA","audio_file":r"C:\Users\welcome-pc\influencer\speech14.txt","product_link":"https://amzn.in/d/bY2VvgN","review_file":r"C:\Users\welcome-pc\reviews\product14_reviews.txt","has_product_overlay":False},
{"video_url":"https://youtube.com/shorts/9fhH8d-WZiE","audio_file":r"C:\Users\welcome-pc\influencer\speech15.txt","product_link":"https://amzn.in/d/4lsj2Tn","review_file":r"C:\Users\welcome-pc\reviews\product15_reviews.txt","has_product_overlay":True},

{"video_url":"https://youtube.com/shorts/MevIat4gh6I","audio_file":r"C:\Users\welcome-pc\influencer\speech16.txt","product_link":"https://amzn.in/d/6K617KD","review_file":r"C:\Users\welcome-pc\reviews\product16_reviews.txt","has_product_overlay":True},
{"video_url":"https://youtube.com/shorts/ySS9gTzmXo4","audio_file":r"C:\Users\welcome-pc\influencer\speech17.txt","product_link":"https://amzn.in/d/5TvzOyU","review_file":r"C:\Users\welcome-pc\reviews\product17_reviews.txt","has_product_overlay":True},
{"video_url":"https://youtube.com/shorts/eqSvPb6t4ig","audio_file":r"C:\Users\welcome-pc\influencer\speech18.txt","product_link":"https://amzn.in/d/iKlVj4J","review_file":r"C:\Users\welcome-pc\reviews\product18_reviews.txt","has_product_overlay":True},
{"video_url":"https://youtube.com/shorts/qkY2tV0YmXk","audio_file":r"C:\Users\welcome-pc\influencer\speech19.txt","product_link":"https://amzn.in/d/0ICebfR","review_file":r"C:\Users\welcome-pc\reviews\product19_reviews.txt","has_product_overlay":True},
{"video_url":"https://youtube.com/shorts/NH7HN6flgZU","audio_file":r"C:\Users\welcome-pc\influencer\speech20.txt","product_link":"https://amzn.in/d/4YSb1WA","review_file":r"C:\Users\welcome-pc\reviews\product20_reviews.txt","has_product_overlay":True},

{"video_url":"https://youtube.com/shorts/Y-wleOchRF4","audio_file":r"C:\Users\welcome-pc\influencer\speech21.txt","product_link":"https://amzn.in/d/9i9TyIp","review_file":r"C:\Users\welcome-pc\reviews\product21_reviews.txt","has_product_overlay":False},
{"video_url":"https://youtube.com/shorts/klQSloSHCVU","audio_file":r"C:\Users\welcome-pc\influencer\speech22.txt","product_link":"https://amzn.in/d/0td3iTz","review_file":r"C:\Users\welcome-pc\reviews\product22_reviews.txt","has_product_overlay":True},
{"video_url":"https://youtube.com/shorts/8tCqAzTVkCg","audio_file":r"C:\Users\welcome-pc\influencer\speech23.txt","product_link":"https://amzn.in/d/8VGxbln","review_file":r"C:\Users\welcome-pc\reviews\product23_reviews.txt","has_product_overlay":False},
{"video_url":"https://youtube.com/shorts/v8EoWdgS0ME","audio_file":r"C:\Users\welcome-pc\influencer\speech24.txt","product_link":"https://amzn.in/d/6WNRAz9","review_file":r"C:\Users\welcome-pc\reviews\product24_reviews.txt","has_product_overlay":False},
{"video_url":"https://youtube.com/shorts/jQh4OpDCgJ4","audio_file":r"C:\Users\welcome-pc\influencer\speech25.txt","product_link":"https://amzn.in/d/ex8Sln4","review_file":r"C:\Users\welcome-pc\reviews\product25_reviews.txt","has_product_overlay":False},

{"video_url":"https://youtube.com/shorts/_tVc_95cSpQ","audio_file":r"C:\Users\welcome-pc\influencer\speech26.txt","product_link":"https://amzn.in/d/9yzeOi2","review_file":r"C:\Users\welcome-pc\reviews\product26_reviews.txt","has_product_overlay":False},
{"video_url":"https://youtube.com/shorts/GGaWGFObOsg","audio_file":r"C:\Users\welcome-pc\influencer\speech27.txt","product_link":"https://amzn.in/d/gompj3B","review_file":r"C:\Users\welcome-pc\reviews\product27_reviews.txt","has_product_overlay":False},
{"video_url":"https://youtube.com/shorts/WFOfEEv9LuE","audio_file":r"C:\Users\welcome-pc\influencer\speech28.txt","product_link":"https://amzn.in/d/gi3tjVV","review_file":r"C:\Users\welcome-pc\reviews\product28_reviews.txt","has_product_overlay":False},
{"video_url":"https://youtube.com/shorts/UxRK5TjniE8?si=B5LWcegYNaMBtZxA","audio_file":r"C:\Users\welcome-pc\influencer\speech29.txt","product_link":"https://amzn.in/d/duZlQdR","review_file":r"C:\Users\welcome-pc\reviews\product29_reviews.txt","has_product_overlay":False},
{"video_url":"https://youtube.com/shorts/uQyOrGaOgm8?si=Qdco2quPtJmR3iLS","audio_file":r"C:\Users\welcome-pc\influencer\speech30.txt","product_link":"https://amzn.in/d/3SGGlEq","review_file":r"C:\Users\welcome-pc\reviews\product30_reviews.txt","has_product_overlay":False},

{"video_url":"https://youtube.com/shorts/uEJoRyv72rM?si=43IjhsqM510mjFfJ","audio_file":r"C:\Users\welcome-pc\influencer\speech31.txt","product_link":"https://amzn.in/d/imcvJT1","review_file":r"C:\Users\welcome-pc\reviews\product31_reviews.txt","has_product_overlay":True},
{"video_url":"https://youtube.com/shorts/zf1uAeqly5Y?si=hiYZWZQkvZOVgZLC","audio_file":r"C:\Users\welcome-pc\influencer\speech32.txt","product_link":"https://amzn.in/d/iEiSpsS","review_file":r"C:\Users\welcome-pc\reviews\product32_reviews.txt","has_product_overlay":False},
{"video_url":"https://youtube.com/shorts/96CusrSnA50","audio_file":r"C:\Users\welcome-pc\influencer\speech33.txt","product_link":"https://amzn.in/d/75OTG48","review_file":r"C:\Users\welcome-pc\reviews\product33_reviews.txt","has_product_overlay":True},
{"video_url":"https://youtube.com/shorts/MvVznRSTIZo","audio_file":r"C:\Users\welcome-pc\influencer\speech34.txt","product_link":"https://amzn.in/d/7CdZLiB","review_file":r"C:\Users\welcome-pc\reviews\product34_reviews.txt","has_product_overlay":True},
{"video_url":"https://youtube.com/shorts/kg1otbKteyU","audio_file":r"C:\Users\welcome-pc\influencer\speech35.txt","product_link":"https://amzn.in/d/9y0lLnd","review_file":r"C:\Users\welcome-pc\reviews\product35_reviews.txt","has_product_overlay":True},

{"video_url":"https://youtube.com/shorts/TVIJoi09wcg","audio_file":r"C:\Users\welcome-pc\influencer\speech36.txt","product_link":"https://amzn.in/d/jlMmlpv","review_file":r"C:\Users\welcome-pc\reviews\product36_reviews.txt","has_product_overlay":True},
{"video_url":"https://youtube.com/shorts/lb4_Ruxbze8","audio_file":r"C:\Users\welcome-pc\influencer\speech37.txt","product_link":"https://amzn.in/d/eIK8SYO","review_file":r"C:\Users\welcome-pc\reviews\product37_reviews.txt","has_product_overlay":True},
{"video_url":"https://youtube.com/shorts/AFpd0-K2KEg","audio_file":r"C:\Users\welcome-pc\influencer\speech38.txt","product_link":"https://amzn.in/d/fvaIunF","review_file":r"C:\Users\welcome-pc\reviews\product38_reviews.txt","has_product_overlay":True},
{"video_url":"https://youtube.com/shorts/YC73rD2Ts64","audio_file":r"C:\Users\welcome-pc\influencer\speech39.txt","product_link":"https://amzn.in/d/4UTclBM","review_file":r"C:\Users\welcome-pc\reviews\product39_reviews.txt","has_product_overlay":True},
{"video_url":"https://youtube.com/shorts/1d-sMwgifb8","audio_file":r"C:\Users\welcome-pc\influencer\speech40.txt","product_link":"https://amzn.in/d/aRRb08T","review_file":r"C:\Users\welcome-pc\reviews\product40_reviews.txt","has_product_overlay":True},

{"video_url":"https://youtube.com/shorts/rm5kgrfuaLw","audio_file":r"C:\Users\welcome-pc\influencer\speech41.txt","product_link":"https://amzn.in/d/hbTfHw6","review_file":r"C:\Users\welcome-pc\reviews\product41_reviews.txt","has_product_overlay":True},
{"video_url":"https://youtube.com/shorts/1H7cRW4RQsQ","audio_file":r"C:\Users\welcome-pc\influencer\speech42.txt","product_link":"https://amzn.in/d/geaAesu","review_file":r"C:\Users\welcome-pc\reviews\product42_reviews.txt","has_product_overlay":False},
{"video_url":"https://youtube.com/shorts/1AOOx9Isr2Y","audio_file":r"C:\Users\welcome-pc\influencer\speech43.txt","product_link":"https://amzn.in/d/1ssYInu","review_file":r"C:\Users\welcome-pc\reviews\product43_reviews.txt","has_product_overlay":True},
{"video_url":"https://youtube.com/shorts/yRNZI7OXdQM","audio_file":r"C:\Users\welcome-pc\influencer\speech44.txt","product_link":"https://amzn.in/d/gLKi3Ka","review_file":r"C:\Users\welcome-pc\reviews\product44_reviews.txt","has_product_overlay":False},
{"video_url":"https://youtube.com/shorts/D-riz8tPtb8","audio_file":r"C:\Users\welcome-pc\influencer\speech45.txt","product_link":"https://amzn.in/d/22uN3Cq","review_file":r"C:\Users\welcome-pc\reviews\product45_reviews.txt","has_product_overlay":True},

{"video_url":"https://youtube.com/shorts/uTf9VRGqOeM","audio_file":r"C:\Users\welcome-pc\influencer\speech46.txt","product_link":"https://amzn.in/d/1sEsCGt","review_file":r"C:\Users\welcome-pc\reviews\product46_reviews.txt","has_product_overlay":True},
{"video_url":"https://youtube.com/shorts/fR9GBsfn4lQ?si=Vxx6v8EbsMB1AQjo","audio_file":r"C:\Users\welcome-pc\influencer\speech47.txt","product_link":"https://amzn.in/d/4NWaQVK","review_file":r"C:\Users\welcome-pc\reviews\product47_reviews.txt","has_product_overlay":False},
{"video_url":"https://youtube.com/shorts/3huBh1eqBF8?si=bAxldfrjGEbdtKOU","audio_file":r"C:\Users\welcome-pc\influencer\speech48.txt","product_link":"https://amzn.in/d/7cEuRRo","review_file":r"C:\Users\welcome-pc\reviews\product48_reviews.txt","has_product_overlay":True},
{"video_url":"https://youtube.com/shorts/wehefkkHtJk","audio_file":r"C:\Users\welcome-pc\influencer\speech49.txt","product_link":"https://amzn.in/d/1B2JwFa","review_file":r"C:\Users\welcome-pc\reviews\product49_reviews.txt","has_product_overlay":True},
{"video_url": "https://youtube.com/shorts/HpwFUgPMgkc?si=O68j03Oo6cOVDEbe","audio_file": r"C:\Users\welcome-pc\influencer\speech50.txt","product_link": "https://amzn.in/d/3cWH5sP","review_file": r"C:\Users\welcome-pc\reviews\product50_reviews.txt","has_product_overlay":True}
]




# ================= MAIN PIPELINE =================
final_data = []

for item in video_product_map:

    vid = item["video_url"].split("/shorts/")[1].split("?")[0]

    try:

        v = youtube.videos().list(
            part="snippet,statistics",
            id=vid
        ).execute()["items"][0]

    except:

        continue

    views = int(v["statistics"].get("viewCount", 1))
    likes = int(v["statistics"].get("likeCount", 0))
    comments_count = int(v["statistics"].get("commentCount", 0))

    engagement = round(((likes + comments_count) / views) * 100, 3)

    # Speech Sentiment
    try:

        speech_text = open(item["audio_file"], encoding="utf-8").read()

        speech_score = paragraph_sentiment(speech_text)

    except:

        speech_score = 0.0

    # Amazon Data
    product_name, product_rating, product_category = get_amazon_product_details(
        item["product_link"]
    )

    # Review Sentiment
    try:

        reviews = open(item["review_file"], encoding="utf-8").readlines()

    except:

        reviews = []

    product_score, review_count = product_review_overall_sentiment(reviews)

    description = v["snippet"].get("description", "")

    has_product_overlay = item.get("has_product_overlay", False)

    sponsored = final_sponsored_decision(
        description,
        speech_score
    )

    promotion = sponsored or has_product_overlay

    final_data.append({

        "influencer_name": v["snippet"]["channelTitle"],
        "views": views,
        "likes": likes,
        "comments": comments_count,
        "engagement_rate_%": engagement,
        "speech_sentiment": speech_score,
        "product_name": product_name,
        "product_category": product_category,
        "product_rating": product_rating,
        "product_review_count": review_count,
        "product_sentiment": product_score,
        "has_product_overlay": has_product_overlay,
        "is_sponsored": sponsored,
        "promotion": promotion

    })

    print(f"Influencer: {v['snippet']['channelTitle']}")
    print(f"Product: {product_name}")
    print(f"Speech Sentiment: {speech_score}")
    print(f"Product Sentiment: {product_score}")
    print(f"Has Product Overlay: {has_product_overlay}")
    print(f"Sponsored (Keyword + Speech): {sponsored}")
    print(f"Promotion (Sponsored OR Overlay): {promotion}")
    print("-" * 50)

    time.sleep(2)


# ================= SAVE DATASET =================
df = pd.DataFrame(final_data)

df.to_csv("INFLUENCER_DATA.csv", index=False)

print("Dataset saved successfully ")