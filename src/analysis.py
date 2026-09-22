import pandas as pd
import matplotlib.pyplot as plt


def rating_vs_ingredients_count(df):
    rate_ing= df['n_ingredients'].corr(df['avg_rating'])
    return round(rate_ing,4)

def complexity_vs_rating(df):
    df['complexity']=df['n_ingredients']+df['n_steps']
    return df.groupby('category').apply(lambda a: a['complexity'].corr(a['avg_rating']))

def count_hidden_gems(df):
    rated=df[df['rating_count']>=3]
    rated['rating_z']=rated.groupby('category')['avg_rating'].transform(lambda s : (s-s.mean())/s.std())
    q25=rated['rating_count'].quantile(0.5)
    gems=rated.loc[(rated['rating_z']>0.75)&(rated['rating_count'] < q25)]
    return len(gems)

def ingredients_vs_time(df):
    minutes=round(df['minutes'].corr(df['avg_rating']),4)
    ingredients=round(df['n_ingredients'].corr(df['avg_rating']), 4)
    return f"minutes: {minutes}, ingredients: {ingredients}"

def complexity_vs_rating_plot(df):
    df = df.copy()
    df['complexity'] = df['n_ingredients'] + df['n_steps']

    corr_by_category = (
        df.groupby('category')
          .apply(lambda g: g['complexity'].corr(g['avg_rating']))
          .sort_values()
    )

    plt.figure(figsize=(10, 6))
    colors = ['crimson' if v < 0 else 'seagreen' for v in corr_by_category.values]
    plt.barh(corr_by_category.index, corr_by_category.values, color=colors)

    plt.axvline(0, color='black', linewidth=0.8)
    plt.title('Complexity-rating correlation by category', fontsize=14, fontweight='bold')
    plt.xlabel('correlation (complexity vs. rating)', fontsize=11)
    plt.grid(True, axis='x', alpha=0.3)
    plt.tight_layout()

    from pathlib import Path
    Path('outputs').mkdir(exist_ok=True)
    plt.savefig('outputs/complexity_rating_by_category.png', dpi=150)
    plt.show()


def main(df):
    print("Do recipes with more ingredients/steps rate worse, better, or about the same?: ")
    print(f"got a correlation of {rating_vs_ingredients_count(df)}, (no real pattern)")
    print()
    print("Does the complexity-rating relationship differ across categories (desserts vs. quick dinners)?: ")
    print(complexity_vs_rating(df))
    print()
    print("Are there 'hidden gem' recipes — high rating, low review count?: ")
    print(f"there is {count_hidden_gems(df)} hidden gem recipes.")
    print()
    print("Is total time (the dataset's single `minutes` value) a better or worse predictor of rating than ingredient count?: ")
    print(f"got correlations as: {ingredients_vs_time(df)}")
    print()
    complexity_vs_rating_plot(df)
    print("Chart saved to outputs/complexity_rating_by_category.png")


if __name__ == '__main__':
    df=pd.read_csv('data/processed/recipes.csv')
    print("=" * 50)
    print("How to read a correlation number:")
    print("  close to  1  -> strongly: more of X means higher rating")
    print("  close to -1  -> strongly: more of X means lower rating")
    print("  close to  0  -> no real pattern either way")
    print("=" * 50)
    print()
    main(df)