import pickle
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# ===============================
# PAGE CONFIGURATION
# ===============================
st.set_page_config(
    page_title="CineMatch - Movie Recommendations",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# CUSTOM CSS
# ===============================
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }

    :root {
        --primary: #e50914;
        --secondary: #221f1f;
        --accent: #ffd700;
        --dark-bg: #141414;
        --card-bg: #221f1f;
    }

    body {
        background-color: var(--dark-bg);
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .main {
        padding: 0;
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
    }

    .stApp {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
    }

    /* Header Styling */
    .header-container {
        background: linear-gradient(90deg, #e50914 0%, #831010 100%);
        padding: 40px 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(229, 9, 20, 0.3);
        animation: slideDown 0.6s ease-out;
    }

    .header-title {
        font-size: 3.5em;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: -1px;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    .header-subtitle {
        font-size: 1.1em;
        color: #f0f0f0;
        opacity: 0.9;
    }

    /* Movie Card Styling */
    .movie-card {
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
        border-radius: 12px;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        border: 1px solid rgba(255,255,255,0.1);
        cursor: pointer;
    }

    .movie-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 12px 30px rgba(229, 9, 20, 0.4);
        border-color: #e50914;
    }

    .movie-poster {
        width: 100%;
        aspect-ratio: 2/3;
        object-fit: cover;
        transition: all 0.3s ease;
    }

    .movie-card:hover .movie-poster {
        filter: brightness(1.1) contrast(1.1);
    }

    .movie-info {
        padding: 15px;
        background: linear-gradient(180deg, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.8) 100%);
    }

    .movie-title {
        font-size: 1em;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 8px;
        line-height: 1.3;
        min-height: 2.6em;
    }

    .movie-year {
        font-size: 0.85em;
        color: #b0b0b0;
        margin-bottom: 8px;
    }

    .movie-rating {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.9em;
        color: #ffd700;
        font-weight: 600;
    }

    /* Input Styling */
    .stSelectbox, .stTextInput {
        margin-bottom: 15px;
    }

    div[data-baseweb="select"] > div {
        background-color: #2a2a2a !important;
        border-color: #e50914 !important;
    }

    div[data-baseweb="select"] > div:hover {
        border-color: #ff6b6b !important;
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #e50914 0%, #b20710 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 1.1em !important;
        padding: 12px 40px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(229, 9, 20, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(229, 9, 20, 0.5) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* Recommendation Container */
    .recommendation-container {
        background: rgba(32, 32, 32, 0.5);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(229, 9, 20, 0.3);
        border-radius: 15px;
        padding: 30px;
        margin-top: 30px;
        animation: fadeIn 0.6s ease-out;
    }

    .recommendation-title {
        font-size: 1.8em;
        font-weight: 800;
        color: #e50914;
        margin-bottom: 5px;
        letter-spacing: 0.5px;
    }

    .recommendation-subtitle {
        font-size: 0.95em;
        color: #b0b0b0;
        margin-bottom: 25px;
    }

    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .error-box {
        background-color: rgba(229, 9, 20, 0.2);
        border: 1px solid #e50914;
        border-radius: 8px;
        padding: 15px;
        color: #ff6b6b;
        margin: 15px 0;
    }

    .success-box {
        background-color: rgba(76, 175, 80, 0.2);
        border: 1px solid #4caf50;
        border-radius: 8px;
        padding: 15px;
        color: #81c784;
        margin: 15px 0;
    }

    .info-box {
        background: linear-gradient(135deg, rgba(229, 9, 20, 0.1) 0%, rgba(131, 16, 16, 0.1) 100%);
        border-left: 4px solid #e50914;
        border-radius: 8px;
        padding: 15px 20px;
        margin: 20px 0;
        font-size: 0.95em;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)


# ===============================
# CACHE CONFIGURATION
# ===============================
@st.cache_resource
def load_models():
    """Load pickle files with caching"""
    try:
        movies = pickle.load(open('movies.pkl', 'rb'))
        similarity = pickle.load(open('similarity.pkl', 'rb'))
        return movies, similarity
    except FileNotFoundError:
        st.error("❌ Model files not found! Make sure 'movies.pkl' and 'similarity.pkl' are in the same directory.")
        return None, None


@st.cache_data
def fetch_poster(movie_id):
    """Fetch movie poster from TMDB API with caching"""
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        data = requests.get(url, timeout=5).json()
        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/300x450?text=No+Poster"
    except Exception as e:
        st.warning(f"⚠️ Could not fetch poster for movie ID {movie_id}")
        return "https://via.placeholder.com/300x450?text=No+Poster"


# ===============================
# RECOMMENDATION FUNCTION
# ===============================
def recommend(movie, movies, similarity, num_recommendations=5):
    """Get movie recommendations"""
    try:
        if movie not in movies['title'].values:
            return None, None

        index = movies[movies['title'] == movie].index[0]
        distances = sorted(
            list(enumerate(similarity[index])),
            reverse=True,
            key=lambda x: x[1]
        )

        recommended_movie_names = []
        recommended_movie_posters = []

        for i in distances[1:num_recommendations + 1]:
            movie_id = movies.iloc[i[0]].get('id')
            if movie_id:
                poster = fetch_poster(movie_id)
                recommended_movie_posters.append(poster)
                recommended_movie_names.append(movies.iloc[i[0]]['title'])

        return recommended_movie_names, recommended_movie_posters
    except Exception as e:
        st.error(f"Error in recommendation: {str(e)}")
        return None, None


# ===============================
# MAIN APPLICATION
# ===============================
def main():
    # Load models
    movies, similarity = load_models()

    if movies is None or similarity is None:
        st.stop()

    # Header
    st.markdown("""
    <div class="header-container">
        <div class="header-title">🎬 CineMatch</div>
        <div class="header-subtitle">Discover movies tailored to your taste with AI-powered recommendations</div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        st.divider()

        st.markdown("**About CineMatch**")
        st.info("""
        CineMatch uses advanced collaborative filtering to recommend movies based on your selection.

        🎯 **How it works:**
        - Select a movie you like
        - Get 5 personalized recommendations
        - Discover your next favorite film!
        """)

    # Main content
    st.markdown("### 🎥 Select a Movie")
    st.markdown("""
    <div class="info-box">
        Choose a movie you enjoy, and we'll find similar films you might love!
    </div>
    """, unsafe_allow_html=True)

    # Movie selection
    movie_list = sorted(movies['title'].values)
    selected_movie = st.selectbox(
        "Type or select a movie",
        movie_list,
        label_visibility="collapsed"
    )

    # Recommendation button
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        recommend_button = st.button(
            "🎯 Get Recommendations",
            use_container_width=True
        )

    # Generate recommendations
    if recommend_button:
        with st.spinner("🔄 Finding perfect movies for you..."):
            time.sleep(0.5)

            recommended_names, recommended_posters = recommend(
                selected_movie,
                movies,
                similarity,
                num_recommendations=5
            )

            if recommended_names and recommended_posters:
                # Display recommendations
                st.markdown("""
                <div class="recommendation-container">
                    <div class="recommendation-title">🌟 Recommended for You</div>
                    <div class="recommendation-subtitle">Based on your selection of <b>""" + selected_movie + """</b></div>
                </div>
                """, unsafe_allow_html=True)

                # Create columns for movie cards
                cols = st.columns(5)

                for idx, (col, name, poster) in enumerate(zip(cols, recommended_names, recommended_posters)):
                    with col:
                        st.markdown(f"""
                        <div class="movie-card">
                            <img src="{poster}" class="movie-poster" alt="{name}">
                            <div class="movie-info">
                                <div class="movie-title">{name}</div>
                                <div class="movie-rating">⭐ Recommended</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("""
                <div class="success-box">
                    ✅ Found 5 amazing recommendations! Enjoy discovering these movies.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="error-box">
                    ❌ Could not generate recommendations. Please try another movie.
                </div>
                """, unsafe_allow_html=True)

    # Stats section
    st.divider()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📚 Movies in Database", len(movies))
    with col2:
        st.metric("🎯 Recommendation Engine", "Collaborative Filtering")
    with col3:
        st.metric("⚡ API", "TMDB v3")


if __name__ == "__main__":
    main()