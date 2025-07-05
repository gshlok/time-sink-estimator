# src/profile_builder.py

def build_fake_user_profile():
    """
    Simulate a user profile with preferred tags and constraints.
    """
    profile = {
        'preferred_tags': ['RPG', 'Strategy', 'Open World', 'Adventure'],
        'max_price': 20.0,        # dollars
        'min_playtime': 60        # minutes
    }
    return profile
