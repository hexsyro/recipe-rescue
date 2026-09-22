import pandas as pd
import numpy as np
import math
import ast

CATEGORIES = ['desserts', 'main-dish', 'breakfast', 'appetizers',
              'side-dishes', 'lunch', 'snacks', 'beverages']

NUTRITION_COLS=["calories", "fat_pdv", "sugar_pdv", "sodium_pdv", "protein_pdv",
   "sat_fat_pdv", "carbs_pdv"]

MAX_MINUTES=1440

df=pd.read_csv('data/raw/Raw_recipes.csv')
df1=pd.read_csv('data/raw/Raw_interactions.csv', usecols=['user_id', 'recipe_id', 'date', 'rating'])


def  rating_columns(df,df1):
    clean_rating=df1.drop(df1[df1['rating'] == 0].index)
    stats=clean_rating.groupby('recipe_id')['rating'].agg(avg_rating='mean', rating_count='count')

    recipes=pd.merge(df, stats, left_on='id', right_on='recipe_id', how='left')

    print(f"out of 230K+ recipes, {recipes['rating_count'].isna().sum()} recipes didn't had any rating")
    recipes=recipes.dropna()
    return recipes

# The dataset already have valid ingredients count as 'n_ingredients'
""" def count_ingredients(df):
    my_ingredients_count=df['ingredients'].apply(ast.literal_eval).apply(len)
    mismatch=df[my_ingredients_count != df['n_ingredients']]

    print(my_ingredients_count)
    print(df['n_ingredients'])
    print(f"mismatched ingredients count; {mismatch}")"""

def minutes_column(recipes):  
    m = pd.to_numeric(recipes['minutes'], errors='coerce').round()
    recipes['minutes'] = m.where((m > 0) & (m <= MAX_MINUTES))
        
    print(f"out of 230K+ recipes, {recipes['minutes'].isna().sum()} recipes didn't had cleaned minutes")
    recipes=recipes.dropna()
    return recipes
        

def nutrition_columns(recipes):  
    recipes[NUTRITION_COLS] = pd.DataFrame(recipes['nutrition'].apply(ast.literal_eval).to_list(), columns=NUTRITION_COLS, index=recipes.index)
    return recipes

def category_column(recipes):
    def pick_category(tags):
        for category in CATEGORIES:
            if category in tags:
                return category       # first match wins
        return 'other'                # nothing matched

    def assign_category(recipes):
        tags = recipes['tags'].apply(ast.literal_eval)
        recipes['category'] = tags.apply(pick_category)
        return recipes
    assign_category(recipes)
    return recipes

def main():
    cleaned_rating=rating_columns(df,df1)
    cleaned_minutes=minutes_column(cleaned_rating)
    cleaned_nutrition=nutrition_columns(cleaned_minutes)
    cleaned_category=category_column(cleaned_nutrition)
    cleaned_category.to_csv('data/processed/recipes.csv', index=False)
    

if __name__ == '__main__':
   main()