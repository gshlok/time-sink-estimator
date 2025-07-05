# Time Sink Estimator

Time Sink Estimator is a web application that recommends video games based on your interests, price preferences, and estimated time investment. It uses a machine learning model trained on real Steam data to predict how much time you might spend on each game.

## Features

- Select your favorite game tags and genres
- Set your price range and minimum playtime
- Receive personalized game recommendations
- View estimated playtime (in minutes and hours) for each recommended game

## Dataset

The app uses a cleaned version of the [Steam Store Games Dataset](https://www.kaggle.com/datasets/nikdavis/steam-store-games), which includes:

- Game metadata (genres, tags, developer, etc.)
- User rating counts (positive/negative)
- Average and median playtime
- Price and age requirements

## Machine Learning Approach

A Random Forest Regressor is trained to predict average playtime using:

- Game features: price, age, achievements, ratings
- Tags and genres (one-hot encoded)

Predicted playtime is used to help rank games based on your preferences.

## Project Structure

```
time-sink-estimator/
├── data/                   # Steam dataset (CSV)
├── model/                  # Saved model and encoder (joblib)
├── src/                    # Model training and prediction logic
│   └── ml_model.py
├── streamlit_app.py        # Main Streamlit app
├── train_playtime_model.py # Script to train and save ML model
├── requirements.txt        # Python dependencies
└── README.md
```

## How to Run Locally

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/time-sink-estimator.git
   cd time-sink-estimator
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Train the model (if you want to retrain or update the model):

   ```bash
   python train_playtime_model.py
   ```

4. Run the app:

   ```bash
   streamlit run streamlit_app.py
   ```

## Requirements

- Python 3.9 or higher
- pandas
- scikit-learn
- joblib
- streamlit

All dependencies are listed in `requirements.txt`.

## Example Usage

Select tags such as "RPG", "Strategy", or "Simulation", set your budget and playtime preferences, and the app will return games like:

- Sid Meier's Civilization V
- XCOM 2
- Slay the Spire

Each suggestion includes:
- Matching tags
- Price
- Predicted playtime (based on the machine learning model)

## Future Improvements

- Integration with real Steam account data (when API access is available)
- Additional filters for release year, developer, or rating
- Deployment to Streamlit Cloud or Hugging Face Spaces
