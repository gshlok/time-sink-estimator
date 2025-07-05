import streamlit as st
import pandas as pd
from src.estimator import recommend_games

# Load and cache data
@st.cache_data
def load_data():
    df = pd.read_csv("data/steam.csv")
    df = df[df['name'].notnull()]
    df = df[df['average_playtime'] > 0]
    df = df[df['average_playtime'] <= 30000]
    df = df.drop_duplicates(subset='name')
    df = df.reset_index(drop=True)
    return df

df = load_data()

# Title
st.title("⏳ Time Sink Estimator")
st.markdown("**Find out how much time you're likely to sink into a game.**")

# Genre/tags selection
all_tags = sorted(list({tag.strip() for tags in df['steamspy_tags'].dropna() for tag in tags.split(';')}))


preferred_tags = st.multiselect("🎯 Choose your preferred tags/genres:", all_tags, default=["RPG", "Strategy"])

# Budget slider
max_price = st.slider("💸 Max Price (USD):", 0.0, 60.0, 20.0, step=1.0)

# Minimum playtime
min_playtime = st.slider("⏱️ Minimum average playtime (minutes):", 0, 1000, 60)

# Submit button
if st.button("🧠 Recommend Games"):
    user_profile = {
        "preferred_tags": preferred_tags,
        "max_price": max_price,
        "min_playtime": min_playtime
    }

    recommendations = recommend_games(df, user_profile, top_n=10)

    if len(recommendations) > 0:
        st.subheader("🎮 Top Recommendations:")
        st.dataframe(recommendations)
    else:
        st.warning("No matching games found with your preferences.")
