import pandas as pd

# print("START")

movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

# print("FILES LOADED")

movies = movies.merge(credits, on='title')

# print("MERGED")

movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

movies.dropna(inplace=True)

# print("FINAL SHAPE:", movies.shape)
# print(movies.head())


# Convert data into usable form
import ast

# Converting genres, keywords, cast into lists.
def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return L
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)


# Extract top 3 cast members
def convert_cast(text):
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter != 3:
            L.append(i['name'])
            counter += 1
        else:
            break
    return L

movies['cast'] = movies['cast'].apply(convert_cast)



# Fetch the Director from crew
def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L

movies['crew'] = movies['crew'].apply(fetch_director)


# Clean text (important)
def collapse(L):
    return [i.replace(" ", "") for i in L]

movies['cast'] = movies['cast'].apply(collapse)
movies['crew'] = movies['crew'].apply(collapse)
movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)


# Create "tags" 
movies['overview'] = movies['overview'].apply(lambda x: x.split())
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']


# Final clean dataset
new_df = movies[['movie_id','title','tags']]
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))


# Conversion of text to vector
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()
# print(new_df.head())

# Calculate similarity 
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)





# Building recommendation function
def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    
    for i in movies_list:
        recommended_movies.append(new_df.iloc[i[0]].title)
        
    return recommended_movies

# Testing it recommend('American Pie')
# Running app
import pickle

pickle.dump(new_df, open('movies.pkl','wb'))
pickle.dump(similarity, open('similarity.pkl','wb'))
