# 🎮 Time Sink Estimator

Ever wondered how much of your life a new game might consume? This AI-powered tool estimates how many hours you're likely to spend on any given game based on your past gaming habits.

## 🔍 What It Does
- Input: Game name
- Background: Steam user history (simulated for now using public dataset)
- Output: Estimated playtime (in hours)

## 📦 Features
- Load and analyze Steam dataset
- Build user-like profiles based on genre and playtime preferences
- Recommend and estimate time for new games

## 🧰 Tech Stack
- Python
- Pandas
- Matplotlib / Seaborn (optional)
- Google Colab for exploration
- Streamlit (coming soon for UI)

## 📁 Folder Structure
```
time-sink-estimator/
├── data/
│   └── steam.csv                   # Kaggle dataset
├── notebooks/
│   └── exploration.ipynb          # Colab notebook for EDA
├── src/
│   ├── profile_builder.py         # Logic to create user profile from game history
│   ├── estimator.py               # Logic to estimate playtime for a given game
├── requirements.txt               # Libraries used
├── README.md                      # Project overview
└── .gitignore                     # Files to ignore in git
```

## 🚀 Setup
```bash
pip install pandas matplotlib seaborn
```

Use Google Colab or run locally.

## ✅ Progress
- [x] Phase 1: Dataset exploration in Colab
- [ ] Phase 2: User profile simulation
- [ ] Phase 3: Game similarity + playtime logic
- [ ] Phase 4: Streamlit UI
- [ ] Phase 5: Add ML model (optional)

## 📌 Data Source
- [Steam Store Games - Kaggle](https://www.kaggle.com/datasets/nikdavis/steam-store-games)