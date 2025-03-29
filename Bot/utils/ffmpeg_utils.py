import ffmpeg
import os

def encode_video(input_file, output_file, crf, codec, audio_codec, quality, watermark=None, watermark_position=None, metadata=None):
    """
    Encodes the video using ffmpeg.

    Args:
        input_file: Path to the input video file.
        output_file: Path to the output video file.
        crf: Constant Rate Factor (CRF) value.
        codec: Video codec.
        audio_codec: Audio codec.
        quality: Video quality (e.g., 720p, 1080p).  This might influence scaling.
        watermark: Text to use as a watermark (optional).
        watermark_position: Position of the watermark (optional).
        metadata: Dictionary of metadata to add (optional).
    """
    try:
        # Basic ffmpeg input
        input_kwargs = {"y": None}  # Overwrite output file if it exists
        output_kwargs = {"c:v": codec, "c:a": audio_codec, "crf": crf}

        # Add watermark if provided
        if watermark:
            # Get the position value
            position_value = watermark_position

            if not position_value:
                raise ValueError("Watermark position is required when watermark is provided.")

            drawtext_filter = f"drawtext=text='{watermark}':{position_value}:fontsize=24:fontcolor=white@0.8"
            input_kwargs["vf"] = drawtext_filter

        # Add metadata if provided
        if metadata:
            for key, value in metadata.items():
                output_kwargs[f"metadata:{key}"] = value

        # Run ffmpeg
        ffmpeg.input(input_file, **input_kwargs).output(output_file, **output_kwargs).run()

        return True
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr}")
        return False

def get_video_info(input_file):
    """Gets video information using ffmpeg."""
    try:
        probe = ffmpeg.probe(input_file)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        audio_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'audio']

        if not video_stream:
            return None

        width = video_stream['width']
        height = video_stream['height']
        duration = float(video_stream.get('duration', 0))

        audio_count = len(audio_streams)

        return {
            "width": width,
            "height": height,
            "duration": duration,
            "audio_count": audio_count
        }
    except ffmpeg.Error as e:
        print(f"FFmpeg probe error: {e.stderr}")
        return None
