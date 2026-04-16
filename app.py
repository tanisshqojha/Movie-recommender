import streamlit as st
import pickle

# Page config
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# Adding background and style
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0E1117;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load data
new_df = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# Title
st.markdown("<h1 style='text-align: center; color: #E50914;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Find movies similar to your favorites</p>", unsafe_allow_html=True)

# Recommendation function
def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(new_df.iloc[i[0]].title)
        
    return recommended_movies

# Dropdown
selected_movie = st.selectbox(
    "🎥 Select a movie",
    new_df['title'].values
)

# Button
if st.button('Recommend!'):
    recommendations = recommend(selected_movie)
    
    st.subheader("Recommended Movies:")
    
    cols = st.columns(5)
    
    for i in range(5):
        with cols[i]:
            st.markdown(f"**{recommendations[i]}**")