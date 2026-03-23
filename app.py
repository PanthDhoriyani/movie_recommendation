import streamlit as st
import pickle
import pandas as pd
import requests


st.set_page_config(page_title="Movie Recommender", layout="wide")

### header
col1, col2 = st.columns([1, 6])
with col1:
    st.write("#### ->Panth-D")
with col2:
    st.title("🎬 Movie Recommendation System")

st.write("Find movies similar to your favorite ones")


movies = pickle.load(open("df_new.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))


API_KEY = "1ea05e7ba484cbde0bd820a33ca91721"

##image
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')

    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    return None

###model
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)),
                         reverse=True,
                         key=lambda x: x[1])[1:6]

    names = []
    posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names, posters

###side-slider
st.sidebar.header("Options")
st.sidebar.write("Select a movie to get recommendations")

##select
selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values
)


if st.button("Recommend"):
    with st.spinner("Loading recommendations..."):
        names, posters = recommend(selected_movie)

        st.subheader("Top 5 Recommendations")

        cols = st.columns(5)

        for i in range(5):
            with cols[i]:
                if posters[i]:
                    st.image(posters[i])
                st.write(names[i])