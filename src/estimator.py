# src/estimator.py

def score_game(game, user_profile):
    """
    Scores a game based on how well it matches the user profile.
    """
    game_tags = [tag.strip() for tag in game['steamspy_tags'].split(';')]
    match_tags = set(game_tags) & set(user_profile['preferred_tags'])
    tag_score = len(match_tags)

    price_score = 1 if game['price'] <= user_profile['max_price'] else 0
    playtime_score = 1 if game['average_playtime'] >= user_profile['min_playtime'] else 0

    total_score = tag_score * 2 + price_score + playtime_score
    return total_score


def recommend_games(df, user_profile, top_n=10):
    """
    Returns top N recommended games from DataFrame based on profile.
    """
    df = df.copy()
    df['match_score'] = df.apply(lambda row: score_game(row, user_profile), axis=1)
    recommendations = df[df['match_score'] > 0]
    recommendations = recommendations.sort_values(by='match_score', ascending=False)
    return recommendations[['name', 'steamspy_tags', 'price', 'average_playtime', 'match_score']].head(top_n)
