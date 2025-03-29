import os
import re
import psutil

def get_episode_number(filename):
    """Extracts episode number from filename using regex."""
    match = re.search(r"e(?:p|pisode)?[\s\.]*(\d+)", filename, re.IGNORECASE)
    if match:
        return match.group(1).lstrip("0")  # Remove leading zeros
    return None

def get_season_number(filename):
    """Extracts season number from filename using regex."""
    match = re.search(r"s(?:eason)?[\s\.]*(\d+)", filename, re.IGNORECASE)
    if match:
        return match.group(1).lstrip("0")
    return None

def get_file_quality(width, height):
    """Determine video quality based on width and height."""
    if width >= 3840 or height >= 2160:
        return "4K"
    elif width >= 1920 or height >= 1080:
        return "1080p"
    elif width >= 1280 or height >= 720:
        return "720p"
    elif width >= 854 or height >= 480:
        return "480p"
    else:
        return "SD"

def get_audio_type(audio_count):
    """Determine audio type based on the number of audio streams."""
    if audio_count == 1:
        return "Sub"
    elif audio_count == 2:
        return "Dual"
    elif audio_count >= 3:
        return "Multi"
    else:
        return "Unknown"

def format_file_size(size_in_bytes):
    """Converts bytes to human-readable format."""
    units = ["B", "KB", "MB", "GB", "TB"]
    size = size_in_bytes
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    return f"{size:.2f} {units[unit_index]}"

def get_system_stats():
    """Gets CPU, memory, and disk usage stats."""
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent  # Root partition

    return {
        "cpu": cpu_usage,
        "memory": memory_usage,
        "disk": disk_usage
  }
