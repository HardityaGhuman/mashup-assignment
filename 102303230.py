#!/usr/bin/env python3
"""
YouTube Mashup CLI Tool
Roll Number: 102303230

Usage:
    python 102303230.py <singer_name> <num_videos> <duration> <output_file>

Example:
    python 102303230.py "Ed Sheeran" 5 20 mashup.mp3
"""

import sys
import os
from mashup import create_mashup


def validate_arguments(args):
    """
    Validate command line arguments.
    
    Args:
        args: List of command line arguments
    
    Returns:
        Tuple of (singer_name, num_videos, duration, output_file)
    
    Raises:
        ValueError: If arguments are invalid
    """
    if len(args) != 5:  # script name + 4 arguments
        raise ValueError(
            "Invalid number of arguments.\n"
            "Usage: python 102303230.py <singer_name> <num_videos> <duration> <output_file>"
        )
    
    singer_name = args[1].strip()
    num_videos_str = args[2].strip()
    duration_str = args[3].strip()
    output_file = args[4].strip()
    
    # Validate singer name
    if not singer_name:
        raise ValueError("Singer name cannot be empty")
    
    # Validate num_videos
    try:
        num_videos = int(num_videos_str)
        if num_videos < 1:
            raise ValueError("Number of videos must be at least 1")
        if num_videos > 50:
            raise ValueError("Number of videos cannot exceed 50")
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError(f"Number of videos must be a valid integer, got: {num_videos_str}")
        raise
    
    # Validate duration
    try:
        duration = int(duration_str)
        if duration < 5:
            raise ValueError("Duration must be at least 5 seconds")
        if duration > 600:
            raise ValueError("Duration cannot exceed 600 seconds (10 minutes)")
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError(f"Duration must be a valid integer, got: {duration_str}")
        raise
    
    # Validate output file
    if not output_file.endswith('.mp3'):
        raise ValueError("Output file must have .mp3 extension")
    
    # Check if output directory exists
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        raise ValueError(f"Output directory does not exist: {output_dir}")
    
    return singer_name, num_videos, duration, output_file


def main():
    """Main function to run the mashup CLI tool."""
    try:
        # Validate arguments
        singer_name, num_videos, duration, output_file = validate_arguments(sys.argv)
        
        print("=" * 60)
        print("YouTube Mashup Creator - Roll No: 102303230")
        print("=" * 60)
        print(f"\nConfiguration:")
        print(f"  Singer: {singer_name}")
        print(f"  Videos: {num_videos}")
        print(f"  Duration: {duration} seconds per video")
        print(f"  Output: {output_file}")
        print("\nStarting mashup creation...\n")
        
        # Create the mashup
        result = create_mashup(singer_name, num_videos, duration, output_file)
        
        print("\n" + "=" * 60)
        print("✓ SUCCESS!")
        print(f"✓ Mashup saved to: {result}")
        print("=" * 60)
        
        return 0
    
    except ValueError as e:
        print(f"\n❌ Argument Error: {str(e)}\n", file=sys.stderr)
        print("Usage: python 102303230.py <singer_name> <num_videos> <duration> <output_file>")
        print("Example: python 102303230.py \"Ed Sheeran\" 5 20 mashup.mp3")
        return 1
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())