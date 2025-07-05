from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd
import numpy as np

def preprocess_data(df):
    df['tags'] = df['steamspy_tags'].fillna('').apply(lambda x: [t.strip() for t in str(x).split(';')])
    df['genres'] = df['genres'].fillna('').apply(lambda x: [g.strip() for g in str(x).split(';')])
    df['all_tags'] = df['tags'] + df['genres']

    mlb = MultiLabelBinarizer()
    tag_features = mlb.fit_transform(df['all_tags'])

    numeric_features = df[['price', 'required_age', 'achievements', 'positive_ratings', 'negative_ratings']].fillna(0)
    X = np.hstack((numeric_features.values, tag_features))
    y = df['average_playtime'].values

    return X, y, mlb

def train_model(X, y, model_type='random_forest'):
    if model_type == 'random_forest':
        model = RandomForestRegressor(n_estimators=100, random_state=42)
    else:
        raise ValueError("Unsupported model type")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)

    return model

def predict_playtime(model, mlb, game):
    tags = game['steamspy_tags']
    genres = game['genres']

    if isinstance(tags, str):
        tag_list = [tag.strip() for tag in tags.split(';')]
    else:
        tag_list = tags

    if isinstance(genres, str):
        genre_list = [g.strip() for g in genres.split(';')]
    else:
        genre_list = genres

    all_tags = tag_list + genre_list

    tag_vector = mlb.transform([all_tags])
    numeric_vector = np.array([[game['price'], game['required_age'], game['achievements'], game['positive_ratings'], game['negative_ratings']]])
    input_vector = np.hstack((numeric_vector, tag_vector))

    predicted = model.predict(input_vector)[0]
    return round(predicted)
