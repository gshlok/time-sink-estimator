import streamlit as st
import pandas as pd
import joblib
from src.ml_model import predict_playtime

# === Load model and encoder ===
model = joblib.load("model/playtime_predictor.pkl")
mlb = joblib.load("model/tag_encoder.pkl")

# === Load and cache data ===
@st.cache_data
def load_data():
    df = pd.read_csv("data/steam.csv")
    df = df[df['name'].notnull()]
    df = df[df['average_playtime'] > 0]
    df = df[df['average_playtime'] <= 30000]
    df = df.drop_duplicates(subset='name')
    df = df.reset_index(drop=True)

    df['tags'] = df['steamspy_tags'].fillna('').apply(lambda x: [t.strip() for t in str(x).split(';')])
    df['genres'] = df['genres'].fillna('').apply(lambda x: [g.strip() for g in str(x).split(';')])
    df['all_tags'] = df['tags'] + df['genres']

    return df

df = load_data()
all_tags = sorted(set(tag for sublist in df['all_tags'] for tag in sublist))

# === Arcade Style CSS ===
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    html, body, [class*='css']  {
        background-color: #18120e !important;
        color: #ffe600 !important;
        font-family: 'Press Start 2P', monospace !important;
    }
    .stApp {
        background-color: #18120e !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ffe600 !important;
        font-family: 'Press Start 2P', monospace !important;
        text-shadow: 2px 2px 0 #ff8800, 4px 4px 0 #000;
    }
    .stButton>button {
        background-color: #ffe600 !important;
        color: #18120e !important;
        border: 2px solid #ff8800 !important;
        font-family: 'Press Start 2P', monospace !important;
        font-weight: bold;
        box-shadow: 2px 2px 0 #ff8800;
    }
    .stSlider > div[data-baseweb="slider"] {
        background: #ffe60022 !important;
    }
    .stMultiSelect, .stSelectbox, .stSlider {
        color: #18120e !important;
        font-family: 'Press Start 2P', monospace !important;
    }
    .stDataFrame thead tr th {
        background-color: #ffe600 !important;
        color: #18120e !important;
        font-family: 'Press Start 2P', monospace !important;
    }
    .stDataFrame tbody tr td {
        background-color: #18120e !important;
        color: #ffe600 !important;
        font-family: 'Press Start 2P', monospace !important;
    }
    .stDataFrame {
        border: 2px solid #ff8800 !important;
        border-radius: 8px;
        box-shadow: 4px 4px 0 #ff8800;
    }
    .stMarkdown, .stWarning {
        color: #ffe600 !important;
        font-family: 'Press Start 2P', monospace !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# === Title ===
st.markdown("""
# TIME SINK ESTIMATOR
<small style='color:#ffe600;'>Enter your interests to get game recommendations with estimated playtime</small>
---
""", unsafe_allow_html=True)

# === User Input ===
preferred_tags = st.multiselect("Choose your preferred tags/genres:", all_tags, default=["RPG", "Strategy"])
max_price = st.slider("Max Price (USD):", 0.0, 60.0, 20.0, step=1.0)
min_playtime = st.slider("Minimum average playtime (minutes):", 0, 1000, 60)

# === Recommend Button ===
if st.button("Recommend Games"):
    # Step 1: Compute tag match score
    def tag_overlap_score(tags):
        return sum(tag in tags for tag in preferred_tags)

    df['match_score'] = df['all_tags'].apply(tag_overlap_score)

    # Step 2: Filter
    filtered = df[
        (df['match_score'] > 0) &
        (df['price'] <= max_price) &
        (df['average_playtime'] >= min_playtime)
    ]

    # Step 3: Predict playtime
    filtered['predicted_playtime'] = filtered.apply(lambda row: predict_playtime(model, mlb, {
        "price": row['price'],
        "required_age": row['required_age'],
        "achievements": row['achievements'],
        "positive_ratings": row['positive_ratings'],
        "negative_ratings": row['negative_ratings'],
        "steamspy_tags": row['steamspy_tags'],
        "genres": row['genres']
    }), axis=1)

    # Step 4: Sort by match_score + predicted_playtime
    top_games = (
        filtered.sort_values(by=['match_score', 'predicted_playtime'], ascending=[False, False])
        .drop_duplicates(subset='name')
        .head(10)
    )

    # Step 5: Display results
    if not top_games.empty:
        st.markdown("""
        <h3 style='color:#ffe600;text-shadow:2px 2px 0 #ff8800,4px 4px 0 #000;font-family:Press Start 2P,monospace;'>Top Game Recommendations</h3>
        """, unsafe_allow_html=True)
        display_df = top_games[['name', 'steamspy_tags', 'price', 'match_score', 'predicted_playtime']].copy()
        display_df.rename(columns={
            'name': 'Game',
            'steamspy_tags': 'Tags',
            'price': 'Price (USD)',
            'match_score': 'Tag Match Score',
            'predicted_playtime': 'Estimated Playtime (min)'
        }, inplace=True)
        display_df['Estimated Playtime (hrs)'] = (display_df['Estimated Playtime (min)'] // 60).astype(int)
        st.dataframe(display_df, use_container_width=True)
    else:
        st.warning("No matching games found with your preferences.")
