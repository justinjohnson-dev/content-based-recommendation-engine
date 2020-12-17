import pandas as pd
from rake_nltk import Rake
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

## IF reading from big CSV
# df = pd.read_csv('IMDb_movies.csv')
# df = df.head(20000)

## IF using free endpoint to grab 250 movies for testing
def get_recommendation(): # movie_name
    df = pd.read_csv('https://query.data.world/s/uikepcpffyo2nhig52xxeevdialfl7')

    # Setting df columns to lowercase to work for both use cases
    df.columns = [x.lower() for x in df.columns]
    
    # grabbing only the columns we want to compare with
    df = df[['title','genre','director','actors']]
    # setting columns to strs to avoid any errors in
    # the get_important_features function
    df['title'] = df['title'].astype(str)
    df['genre'] = df['genre'].astype(str)
    df['director'] = df['director'].astype(str)
    df['actors'] = df['actors'].astype(str)

    # create the column to hold combined strings
    df['important_features'] = get_important_features(df)

    # convert text to a matrix of token counts for important_features
    cm = CountVectorizer().fit_transform(df['important_features'])
    # get the cosine similarity matrix from count matrix
    cs = cosine_similarity(cm)
    print(cs)

    # Build a 1-dimensional array with movie titles
    titles = df['title']
    indices = pd.Series(df.index, index=df['title'])
    recommendations('The Dark Knight', indices, cs, titles).head(10)


# combine values into a column that we will use for comparison
def get_important_features(data):
    important_features = []
    for i in range(0, data.shape[0]):
        important_features.append(data['title'][i]+' '+data['genre'][i]+' '+data['director'][i]+' '+data['actors'][i])
    return important_features

# Function that get movie recommendations based on the cosine similarity score of movie genres
def recommendations(title, indices, cs, titles):
    try:
        idx = indices[title]
        sim_scores = list(enumerate(cs[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        movie_indices = [i[0] for i in sim_scores]

        print('')
        print('Recommendation engine suggests: ')
        print('===============================')
        print(titles.iloc[movie_indices])

        return titles.iloc[movie_indices]
    except Exception as e:
        print('')
        print('Movie was not found in dataset')
        print('')

