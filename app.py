import streamlit as st
import pickle

# Page config
st.set_page_config(page_title="Cinephilia", layout="wide")

# Adding background and style
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F0E6E6;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load data
new_df = pickle.load(open('movies.pkl','rb'))
#similarity = pickle.load(open('similarity.pkl','rb'))

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

similarity = cosine_similarity(vectors)

# Title
st.markdown("""
<h1 class="cinephilia-title">CINEPHILIA</h1>
<p class="subtitle">Find movies similar to what you like!</p>
""", unsafe_allow_html=True)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Bebas+Neue&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background-color: #0E1117;
    color: white;
}

.cinephilia-title {
    text-align: center;
    color: #E50914;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 70px;
    letter-spacing: 2px;
    margin-bottom: 0;
}

.subtitle {
    text-align: center;
    font-family: 'Poppins', sans-serif;
    font-size: 20px;
    margin-top: 0;
}
</style>
""", unsafe_allow_html=True)


# To fetch posters from OMDB site
import requests

def fetch_poster(movie_name):
    try:
        url = f"http://www.omdbapi.com/?t={movie_name}&apikey=35f42b8c"
        data = requests.get(url, timeout=10).json()

        poster = data.get("Poster")

        if poster and poster != "N/A":
            return poster
        else:
            return "https://via.placeholder.com/300x450"

    except:
        return "https://via.placeholder.com/300x450"




# Recommendation function
def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    names = []
    posters = []
    
    for i in movies_list:
        movie_name = new_df.iloc[i[0]].title
        names.append(new_df.iloc[i[0]].title)
        posters.append(fetch_poster(movie_name))
        
    return names, posters





# Dropdown
selected_movie = st.selectbox(
    "Select a movie",
    new_df['title'].values
)





# Button
col1, col2, col3 = st.columns([2, 1, 2])

with col2:
    recommend_clicked = st.button("recommend", use_container_width=True)

if recommend_clicked:
    # Selected movie section
    selected_movie_poster = fetch_poster(selected_movie)

    center1, center2, center3 = st.columns([1.5, 2, 1.5])

    with center2:
        st.image(selected_movie_poster, width=525)
        st.markdown(
            f"<p style='text-align: center; font-size:18px; font-weight:600;'>{selected_movie}</p>",
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Recommendations section
    st.markdown("<h3 style='text-align: center;'>Based on what you like......</h3>", unsafe_allow_html=True)

    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.caption(names[i])





# Automatic suggestions of movies
st.markdown("---")
st.subheader("You may also like these!")

random_movies = new_df.sample(5)

cols = st.columns(5)

for i, (_, row) in enumerate(random_movies.iterrows()):
    with cols[i]:
        movie_name = row['title']
        poster = fetch_poster(movie_name)

        st.image(poster)
        st.caption(movie_name)
