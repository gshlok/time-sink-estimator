import pandas as pd
from src.profile_builder import build_fake_user_profile
from src.estimator import recommend_games

# Load dataset
df = pd.read_csv('data/steam.csv')

# Basic cleaning
df = df[df['name'].notnull()]
df = df[df['average_playtime'] > 0]
df = df[df['average_playtime'] <= 30000]
df = df.drop_duplicates(subset='name')
df = df.reset_index(drop=True)

# Simulate user profile
user_profile = build_fake_user_profile()

# Get recommendations
top_recs = recommend_games(df, user_profile, top_n=10)
print(top_recs)
