from src.ml_model import preprocess_data, train_model, predict_playtime
import pandas as pd
import joblib


# Load data
df = pd.read_csv("data/steam.csv")

# Train model
X, y, mlb = preprocess_data(df)
model = train_model(X, y, model_type='random_forest')

# Test prediction
sample_game = {
    'price': 19.99,
    'required_age': 0,
    'achievements': 120,
    'positive_ratings': 4000,
    'negative_ratings': 300,
    'steamspy_tags': "RPG;Open World;Singleplayer",
    'genres': "Adventure;Action"
}

predicted_time = predict_playtime(model, mlb, sample_game)
print(f"Estimated playtime: {predicted_time} minutes")

joblib.dump(model, 'model/playtime_predictor.pkl')
joblib.dump(mlb, 'model/tag_encoder.pkl')
