* The project name - "MuseTwin"
* Version 0.3V
* Build Status: 0.3V - is Ready; 1.0V - in progress
--------------------------------------------------------------------------------------------------------------------------------
This project – is my recommendation system for find similar music. 
--------------------------------------------------------------------------------------------------------------------------------
### Prerequisites
- Python 3.10+
- pip
- Git
--------------------------------------
### Installation
bash
git clone https://github.com/BankaHooks/MuseTwin.git
cd MuseTwin
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
--------------------------------------
**To run locally:** "uvicorn main:app --reload" in terminal
--------------------------------------
API Endpoints
Endpoint	                            Method	Description
/search?track_name=...&artist=...	    GET	    Find track features (artist, audio features)
/recommend?track_name=...&artist=...	GET	    Get 5 similar songs based on audio features
/health	                              GET	    Health check
--------------------------------------
**How it works**
User inputs a song name (and optional artist).
The system finds the track in the Spotify dataset.
It extracts audio features: danceability, energy, tempo, etc.
Cosine similarity is used to find the 5 most similar tracks (within the same genre).
Returns list of recommended songs.
--------------------------------------
📦 Dependencies
FastAPI
Pandas
NumPy
Scikit-learn
Uvicorn
--------------------------------------
[Project use Kaggle Spotify DataSet]
---------------------------------------
  **Roadmap**
☑ Core recommendation engine (cosine similarity)
☑ FastAPI REST API
☑ Basic HTML UI
□ Add TF-IDF and think about future of project
--------------------------------------
***Made by***
Daniel Kruchkov.
Software Engineer, building products with AI inside.

License
MIT — free to use, modify, and share.
