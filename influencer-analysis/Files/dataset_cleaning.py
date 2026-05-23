# -*- coding: utf-8 -*-
"""
CLEAN FINAL INFLUENCER + PRODUCT DATASET (CLEANING ONLY)
Author: agals
"""

import pandas as pd

# ================= LOAD DATA =================
df = pd.read_csv("INFLUENCER_DATA.csv", encoding="utf-8")

# ================= CLEAN COLUMN NAMES =================
df.columns = df.columns.str.strip()

# ================= CLEAN TEXT COLUMNS =================
text_cols = [
    "influencer_name",
    "product_name",
    "product_category"
]

for col in text_cols:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace("â€º", ">", regex=False)
            .str.replace("Â®", "®", regex=False)
            .str.replace("\n", " ", regex=False)
            .str.strip()
        )

# ================= FIX NUMERIC COLUMNS =================
numeric_cols = [
    "views",
    "likes",
    "comments",
    "engagement_rate_%",
    "speech_sentiment",
    "product_rating",
    "product_review_count",
    "product_sentiment"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# ================= FIX BOOLEAN COLUMNS =================
bool_cols = [
    "has_product_overlay",
    "is_sponsored"
]

for col in bool_cols:
    if col in df.columns:
        df[col] = df[col].astype(bool)

# ================= RESET INDEX =================
df.reset_index(drop=True, inplace=True)

# ================= SAVE CLEAN DATA =================
df.to_csv(
    "FINAL_INFLUENCER_DATA.csv",
    index=False,
    encoding="utf-8-sig"
)

print("✅ Dataset cleaned successfully")
