import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns

column_names = ['user_id','item_id','rating','timestamp']

df = pd.read_csv('u.data',sep='\t',names=column_names)

movie_titles = pd.read_csv('Movie_Id_Titles')

df = pd.merge(df,movie_titles,on='item_id')

print(df.head())

print(df.groupby('title')['rating'].count().sort_values(ascending=False).head())

ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
ratings['num of ratings'] = pd.DataFrame(df.groupby('title')['rating'].count())

moviematrix = df.pivot_table(index='user_id',columns='title',values='rating')

def similar_movies(movie):
	movie_ratings = moviematrix[movie]
	corr_movies = moviematrix.corrwith(movie_ratings)
	corr_movies = pd.DataFrame(corr_movies,columns=['Correlation'])
	corr_movies = corr_movies.join(ratings['num of ratings'])
	corr_movies = corr_movies[corr_movies['num of ratings'] > 100]
	return corr_movies.dropna().sort_values('Correlation',ascending=False).head()

recommended_movies = similar_movies('Star Wars (1977)')
print(recommended_movies)