# YouTube Mashup

This project creates audio mashups by downloading YouTube videos of a specified singer, extracting the audio, and merging them into a single file.

## Features

- **Command Line Interface (CLI):** Quick script execution.
- **Web Interface (Streamlit):** User-friendly web app with email delivery.
- **Processing:** Automates downloading, audio conversion, trimming, and merging.

---

## Installation & Setup

Follow these steps to set up the project locally.

### 1. Prerequisites

- **Python 3.10 or higher** (Tested on Python 3.13)
- **FFmpeg** (Required for audio processing with `pydub`)

### 2. Install FFmpeg

You must have FFmpeg installed and added to your system PATH.

- **macOS:**
  ```bash
  brew install ffmpeg
  ```
- **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt update && sudo apt install ffmpeg
  ```
- **Windows:**
  Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add the `bin` folder to your System Environment Variables.

### 3. Clone and Install Dependencies

```bash
# Clone the repository
git clone <repository_url>
cd mashup-assignment

# Create a virtual environment (Recommended)
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

---

## 💻 Usage

### Part I: Command Line Interface (CLI)

Run the script from the terminal to create a mashup immediately.

**Syntax:**
```bash
python 102303230.py <singer_name> <num_videos> <duration> <output_file>
```

**Arguments:**
1. `singer_name`: Name of the artist (use quotes if it contains spaces).
2. `num_videos`: Number of videos to download (1-50).
3. `duration`: Duration in seconds to cut from each video (5-600).
4. `output_file`: Name of the output file (must end in `.mp3`).

**Example:**
```bash
python 102303230.py "Ed Sheeran" 5 20 mashup.mp3
```

This will:
1. Search for 5 "Ed Sheeran" videos.
2. Download them temporarily.
3. Cut the first 20 seconds from each.
4. Merge them into `mashup.mp3`.

---

### Part II: Web Service (Streamlit)

Launch the web interface for an interactive experience.

**Run Locally:**
```bash
streamlit run app.py
```
This will open the app in your default web browser (usually at `http://localhost:8501`).

### Streamlit Cloud Deployment & Limitations

The application is designed to be deployable on Streamlit Cloud. However, please note the following regarding YouTube downloads in cloud environments:

> **Important Notice: YouTube 403 / Bot Protection**
> 
> This app was deployed to Streamlit Cloud and other hosting platforms, however it encountered `HTTP 403 Forbidden` errors or failures to download videos. 
> 
> **Why?** This is a known limitation of `yt-dlp` and YouTube's anti-bot protection systems. YouTube aggressively limits or blocks requests coming from shared data center IP addresses (which Streamlit Cloud uses) to prevent automated scraping.
> 
> **Recommendation:** This application works **reliably in local environments** (your personal machine) where residential IP addresses are not typically blocked. If the cloud version fails, please run the app locally using the instructions above.

---

## Project Structure

```
mashup-assignment/
├── 102303230.py          # CLI entry point (Format: RollNumber.py)
├── app.py                # Streamlit web application
├── mashup.py             # Core logic (download, cut, merge)
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

---

## Author

**Harditya Vir Singh Ghuman**  
Roll Number: **102303230**