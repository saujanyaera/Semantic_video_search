#  Semantic Video Search (Flask Backend)

This project is a **Flask-based backend API** that allows users to upload a video and search for relevant segments using a text query. It processes the video, extracts embeddings, and returns the most relevant time intervals.

---

## 🚀 Features
- User uploads a video
- Search video content using text query
- Returns matching start and end timestamps
- Clean Flask structure
- Temporary file handling with auto cleanup
- CORS enabled for frontend integration

---

## 🏗️ Project Structure
project/
│
├── app.py # Main Flask backend
├── pipeline.py # Core video processing logic
├── uploads/ # Temporary uploaded videos
├── templates/
│ └── index.html # Frontend page
└── requirements.txt # Dependencies

## ⚙️ How It Works

1. User uploads a video
2. User sends a text query
3. Backend saves video temporarily
4. `final_video_processed()` runs:
   - Extracts video frames
   - the frames are converted into clip and each clips are converted into vector embeddings.
   - Converts text into embeddings
   - Matches similarity
5. Returns best matching time segment