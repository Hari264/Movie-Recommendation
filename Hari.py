import pandas as pd
import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    dataa = data.json()
    poster_path = dataa['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path



from bs4 import BeautifulSoup
from urllib.request import urlopen
import io

from scraper_api import ScraperAPIClient
client = ScraperAPIClient('a156500cd01cb7d1041dcae8e1836aa4')

st.title("Movie recommendation system")


def Bollywoodmovie_details_fetcher(imdb_link):
    ## Call to website using SDK
    url_data = client.get(imdb_link).text
    ## Fetch the site data
    s_data = BeautifulSoup(url_data, 'html.parser')
    ## Find the tag in which Image link is stored
    imdb_dp = s_data.find("meta", property="og:image")
    ## Get the URL of Image
    movie_poster_link = imdb_dp.attrs['content']

    ## TO get movie title
    movie_find = s_data.find("meta", property="og:title")
    movie_name = movie_find.attrs['content']
    movie_name = str(movie_name).replace('- IMDb', '')

    ## To find the movie descrpiton
    imdb_content = s_data.find("meta", property="og:description")
    movie_descr = imdb_content.attrs['content']
    movie_descr = str(movie_descr).split('.')
    movie_story = 'Story: ' + str(movie_descr[2]).strip() + '.'

    ## Fetch Director
    movie_director = movie_descr[0]

    ## Fetch Cast
    movie_cast = str(movie_descr[1]).replace('With', 'Cast: ').strip()

    return movie_name, movie_director, movie_cast, movie_story, movie_poster_link
def recommend_Bollywood(option):
    index = bmovie[bmovie['title'] == option].index[0]
    distances = sorted(list(enumerate(bsimilarity[index])), reverse=True, key=lambda x: x[1])
    print("Recomending......")
    recommend_movies = []
    posters = []
    cast = []
    director = []
    story = []

    for i in distances[1:6]:
        movie_id = bmovie.imdbId.iloc[i[0]]
        imdb_link = "https://www.imdb.com/title/"+movie_id+"/?ref_=fn_tt_tt_1"
        recommend_movies.append(bmovie.iloc[i[0]].title)
        movie_name, movie_director, movie_cast, movie_story, movie_poster_link = Bollywoodmovie_details_fetcher(imdb_link)
        # posters.append(Bollywoodmovie_details_fetcher(imdb_link))
        posters.append( movie_poster_link)
        story.append(movie_story)
        director.append(movie_director)
        cast.append(movie_cast)
    return recommend_movies,posters,cast,director,story

bmovie_list = pickle.load(open("Bollywood.pkl","rb"))
bmovie = pd.DataFrame(bmovie_list)
bsimilarity = pickle.load(open("Bollywood_similarity.pkl","rb"))



def recommend(option):
    index = movie[movie['title'] == option].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movie.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movie.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


movie_list = pickle.load(open("Movies (1).pkl","rb"))
movie = pd.DataFrame(movie_list)
similarity = pickle.load(open("similarity.pkl","rb"))

genre = st.radio(
    "Select The Industry",
    ('Hollywood', 'Bollywood'))

if genre == 'Bollywood':
    op = st.selectbox(
        "Search for your movie : ",
        bmovie["title"])

    if st.button("Recommend"):
        recommendations, poster,cast,director,story = recommend_Bollywood(op)
        cola, colb, colc, cold, cole = st.columns(5)
        with cola:
            st.write(director[0])
            st.image(poster[0])


            st.write(story[0])



        with colb:
            st.write(director[1])
            st.image(poster[1])
            st.write(story[1])

        with colc:
            st.write(director[2])
            st.image(poster[2])


            st.write(story[2])


        with cold:
            st.write(director[3])
            st.image(poster[3])


            st.write(story[3])


        with cole:
            st.write(director[4])
            st.image(poster[4])
            st.write(story[4])




if genre == "Hollywood":
    option = st.selectbox(
            "Search for your movie : ",
            movie["title"])
    if st.button("Recommend.") :

            recommendations, poster = recommend(option)
            cola, colb, colc, cold, cole = st.columns(5)
            with cola:
                st.write(recommendations[0])
                st.image(poster[0])
            with colb:
                st.write(recommendations[1])
                st.image(poster[1])
            with colc:
                st.write(recommendations[2])
                st.image(poster[2])
            with cold:
                st.write(recommendations[3])
                st.image(poster[3])
            with cole:
                st.write(recommendations[4])
                st.image(poster[4])



link ="https://hari264-hari-main-80xfbh.streamlit.app/"
agree = st.checkbox("Want to give feed back.")

if agree:
    Feedback = st.select_slider(
        'Please Rate Us.',
        options=['😒', '😏', '😐', '🙂', '😁'])

    # You can check .empty documentation
    placeholder = st.empty()

    with placeholder.container():

        btn = st.button("Submit")

    # If btn is pressed or True
    if btn:
        # This would empty everything inside the container
        st.title(Feedback)

