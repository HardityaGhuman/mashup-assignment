import os
import yt_dlp
from pydub import AudioSegment
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def search_and_download_videos(singer_name, num_videos, output_dir="downloads"):
    """
    Search for singer's videos on YouTube and download them.
    
    Args:
        singer_name: Name of the singer to search
        num_videos: Number of videos to download
        output_dir: Directory to save downloads
    
    Returns:
        List of downloaded video file paths
    """
    os.makedirs(output_dir, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'extractor_retries': 5,
        'fragment_retries': 5,
        'skip_unavailable_fragments': True,
        'ignoreerrors': False,
        'nocheckcertificate': True,
    }
    
    search_query = f"{singer_name} official audio"
    downloaded_files = []
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.info(f"Searching for {singer_name} videos...")
            search_results = ydl.extract_info(f"ytsearch{num_videos}:{search_query}", download=True)
            
            if 'entries' in search_results:
                for entry in search_results['entries']:
                    if entry:
                        video_id = entry.get('id')
                        # Find the downloaded file
                        for ext in ['webm', 'm4a', 'mp3', 'opus']:
                            filepath = os.path.join(output_dir, f"{video_id}.{ext}")
                            if os.path.exists(filepath):
                                downloaded_files.append(filepath)
                                logger.info(f"Downloaded: {entry.get('title', 'Unknown')}")
                                break
        
        logger.info(f"Successfully downloaded {len(downloaded_files)} videos")
        return downloaded_files
    
    except Exception as e:
        logger.error(f"Error downloading videos: {str(e)}")
        raise


def convert_to_audio(video_path, audio_format="mp3"):
    """
    Convert video file to audio format.
    
    Args:
        video_path: Path to video file
        audio_format: Output audio format (default: mp3)
    
    Returns:
        Path to converted audio file
    """
    try:
        audio_path = video_path.rsplit('.', 1)[0] + f'.{audio_format}'
        
        # Load the audio from video
        audio = AudioSegment.from_file(video_path)
        
        # Export as mp3
        audio.export(audio_path, format=audio_format)
        
        logger.info(f"Converted to audio: {audio_path}")
        return audio_path
    
    except Exception as e:
        logger.error(f"Error converting {video_path}: {str(e)}")
        raise


def cut_audio(audio_path, duration_seconds):
    """
    Cut audio to specified duration from the beginning.
    
    Args:
        audio_path: Path to audio file
        duration_seconds: Duration to keep (in seconds)
    
    Returns:
        AudioSegment object
    """
    try:
        audio = AudioSegment.from_file(audio_path)
        
        # Cut to specified duration (duration is in milliseconds for pydub)
        cut_audio = audio[:duration_seconds * 1000]
        
        logger.info(f"Cut audio to {duration_seconds} seconds")
        return cut_audio
    
    except Exception as e:
        logger.error(f"Error cutting audio {audio_path}: {str(e)}")
        raise


def merge_audios(audio_segments, output_file):
    """
    Merge multiple audio segments into one file.
    
    Args:
        audio_segments: List of AudioSegment objects
        output_file: Output file path
    """
    try:
        # Start with empty audio
        merged = AudioSegment.empty()
        
        # Concatenate all audio segments
        for segment in audio_segments:
            merged += segment
        
        # Export merged audio
        merged.export(output_file, format="mp3")
        
        logger.info(f"Merged audio saved to: {output_file}")
        return output_file
    
    except Exception as e:
        logger.error(f"Error merging audios: {str(e)}")
        raise


def create_mashup(singer_name, num_videos, duration_seconds, output_file):
    """
    Complete mashup process: download, convert, cut, and merge.
    
    Args:
        singer_name: Name of the singer
        num_videos: Number of videos to download
        duration_seconds: Duration to cut from each video
        output_file: Final output file path
    
    Returns:
        Path to the final mashup file
    """
    download_dir = "temp_downloads"
    
    try:
        # Step 1: Download videos
        logger.info("Step 1: Downloading videos...")
        video_files = search_and_download_videos(singer_name, num_videos, download_dir)
        
        if not video_files:
            raise ValueError("No videos were downloaded")
        
        # Step 2: Convert to audio and cut
        logger.info("Step 2: Processing audio files...")
        audio_segments = []
        
        for video_file in video_files:
            try:
                # Convert to audio
                audio_file = convert_to_audio(video_file)
                
                # Cut to specified duration
                cut_segment = cut_audio(audio_file, duration_seconds)
                audio_segments.append(cut_segment)
                
            except Exception as e:
                logger.warning(f"Skipping file due to error: {str(e)}")
                continue
        
        if not audio_segments:
            raise ValueError("No audio segments were processed successfully")
        
        # Step 3: Merge all audio segments
        logger.info("Step 3: Merging audio files...")
        merge_audios(audio_segments, output_file)
        
        # Cleanup temporary files
        logger.info("Cleaning up temporary files...")
        cleanup_temp_files(download_dir)
        
        logger.info(f"✓ Mashup created successfully: {output_file}")
        return output_file
    
    except Exception as e:
        logger.error(f"Error creating mashup: {str(e)}")
        # Cleanup on error
        cleanup_temp_files(download_dir)
        raise


def cleanup_temp_files(directory):
    """Remove temporary download directory and files."""
    try:
        if os.path.exists(directory):
            import shutil
            shutil.rmtree(directory)
            logger.info("Temporary files cleaned up")
    except Exception as e:
        logger.warning(f"Could not clean up temp files: {str(e)}")