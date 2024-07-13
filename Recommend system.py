import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split

# Sample data: user-item interaction matrix (e.g., movie ratings)
data = {
    'user_id': [1, 1, 1, 2, 2, 3, 3, 3, 4, 4],
    'item_id': [1, 2, 3, 2, 3, 1, 2, 4, 1, 4],
    'rating': [5, 3, 4, 4, 5, 3, 4, 2, 5, 4]
}

df = pd.DataFrame(data)

# Create user-item matrix
user_item_matrix = df.pivot_table(index='user_id', columns='item_id', values='rating').fillna(0)
print(user_item_matrix)

# Compute user similarity
user_similarity = cosine_similarity(user_item_matrix)
print(user_similarity)

# Predict ratings
def predict_ratings(user_item_matrix, user_similarity):
    mean_user_rating = user_item_matrix.mean(axis=1)
    ratings_diff = (user_item_matrix - mean_user_rating[:, np.newaxis])
    pred = mean_user_rating[:, np.newaxis] + user_similarity.dot(ratings_diff) / np.array([np.abs(user_similarity).sum(axis=1)]).T
    return pred

user_prediction = predict_ratings(user_item_matrix.values, user_similarity)
print(user_prediction)

# Recommend items
def recommend_items(user_id, user_item_matrix, user_prediction, num_recommendations):
    user_idx = user_id - 1  # Adjust user_id to zero-indexed
    sorted_user_predictions = user_prediction[user_idx].argsort()[::-1]
    user_data = user_item_matrix.iloc[user_idx].values
    recommended_items = [i+1 for i in sorted_user_predictions if user_data[i] == 0][:num_recommendations]
    return recommended_items

# Example: Recommend 3 items for user with ID 1
user_id = 1
num_recommendations = 3
recommended_items = recommend_items(user_id, user_item_matrix, user_prediction, num_recommendations)
print(f"Recommended items for user {user_id}: {recommended_items}")
