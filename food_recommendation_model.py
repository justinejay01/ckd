import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib


class FoodRecommendationModel:
    def __init__(self, train_file_path, test_file_path):
        self.df = pd.concat([
            pd.read_csv(train_file_path),
            pd.read_csv(test_file_path)
        ])
        self.cv = CountVectorizer()
        self.count_matrix = self.cv.fit_transform(self.df['FOOD DATA'])
        self.cosine_sim = cosine_similarity(
            self.count_matrix, self.count_matrix)

    def get_recommendations(self, patient_potassium):
        # Classify the patient's potassium level as low, safe, or high
        if 3.5 <= patient_potassium <= 5.0:
            food_level = 'LOW'
        elif 5.1 <= patient_potassium <= 6.0:
            food_level = 'SAFE'
        elif 6.1 <= patient_potassium <= 10.0:
            food_level = 'HIGH'
        # Get the list of foods that have the same food level as the patient's food level
        foods = self.df[self.df['FOOD LEVEL'] == food_level]['FOOD '].unique()

        # Get the list of foods that have a food potassium level that is safe for the patient's potassium level
        food_potassium_levels = self.df[self.df['FOOD LEVEL'] == food_level][[
            'FOOD ', 'FOOD_POTASSIUM_LEVEL']]
        safe_foods = food_potassium_levels[(
            food_potassium_levels['FOOD_POTASSIUM_LEVEL'] <= patient_potassium)]['FOOD '].unique()

        # Get the list of foods that have not been recommended yet
        recommended_foods = []
        for food in foods:
            if food in safe_foods:
                if not self.df[(self.df['PATIENT ID'] == 'patient') & (self.df['FOOD '] == food)].empty:
                    continue
                else:
                    recommended_foods.extend(
                        self.get_food_recommendations(food, self.cosine_sim))
            if len(recommended_foods) >= 10:
                break

        # Return the list of recommended foods
        return recommended_foods

    def get_food_recommendations(self, food, cosine_sim):
        # Get the index of the food in the dataset
        food_index = self.df[self.df['FOOD '] == food].index[0]

        # Get the pairwise similarity scores of all foods with the given food
        sim_scores = list(enumerate(cosine_sim[food_index]))

        # Sort the foods based on their similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the indices of the top 10 most similar foods
        top_indices = [i[0] for i in sim_scores[1:11]]

        # Return the names of the top 10 most similar foods
        return list(self.df['FOOD '].iloc[top_indices])


# Create an instance of the FoodRecommendationModel
model = FoodRecommendationModel('TRAIN.csv', 'TEST.csv')

# Save the trained model using joblib.dump()
joblib.dump(model, 'food_recommendation_model.sav')
