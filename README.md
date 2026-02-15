# Mashup Assignment
This project creates audio mashups by downloading YouTube videos of a singer, extracting audio, and merging them into a single file.

## Part I — Command Line Interface (CLI)

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run
```bash
python 102303230.py <singer_name> <num_videos> <duration> <output_file>
```

### Example
```bash
python 102303230.py "Ed Sheeran" 5 20 mashup.mp3
```

### Input
* Singer name (in quotes if multiple words)
* Number of videos (1-50)
* Duration in seconds (5-600)
* Output filename (.mp3)

### Output
* Creates merged audio file with specified name
* Downloads N videos, extracts Y seconds from each, merges into one file

---

## Part II — Web Service (Streamlit)

A web interface is implemented using Streamlit for easy mashup creation.

### Live Web App
**[https://your-app-name.streamlit.app](https://your-app-name.streamlit.app)**  

### Features
* Enter singer/artist name
* Specify number of videos and duration
* Email validation and delivery
* Download mashup as ZIP file
* Real-time progress tracking

### Run Locally
```bash
streamlit run app.py
```

---

## Requirements

* Python 3.8+
* FFmpeg (must be installed separately)
* See `requirements.txt` for Python packages

### Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html)

---

## Project Structure

```
youtube-mashup/
├── 102303230.py          # CLI program
├── app.py                # Streamlit web app
├── mashup.py             # Core logic
├── requirements.txt      # Dependencies
└── README.md             # Documentation
```

---

## Author

**Harditya Vir Singh Ghuman**  
Roll Number: 102303230