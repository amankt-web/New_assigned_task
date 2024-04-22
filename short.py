from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, clips_array
from moviepy.video.tools.cuts import FramesMatches
# from moviepy.video.fx import vfx
from moviepy.video.fx.all import crossfadeout

# Function to extract interesting clips from the input video
def extract_clips(input_video, clip_timestamps):
    clips = []
    for start, end in clip_timestamps:
        clip = VideoFileClip(input_video).subclip(start, end)
        clips.append(clip)
    return clips

# Function to add music to the video
def add_music(video, music_file):
    audio = VideoFileClip(music_file).audio
    return video.set_audio(audio)

# Function to add transitions between clips

def add_transitions(clips, transition_duration):
    transitions = [clip.crossfadeout(transition_duration) for clip in clips[:-1]]
    return concatenate_videoclips(transitions + [clips[-1]])


# Function to add text overlays to the video
def add_text_overlay(video, text, duration):
    txt_clip = TextClip(text, fontsize=50, color='white')
    txt_clip = txt_clip.set_duration(duration).set_position(('center', 'bottom'))
    return CompositeVideoClip([video, txt_clip])

# Function to generate the short video
def generate_short_video(input_video, clip_timestamps, music_file, text_overlays):
    # Extract interesting clips from input video
    clips = extract_clips(input_video, clip_timestamps)
    
    # Add transitions between clips
    transition_duration = 1  # Adjust as needed
    video_with_transitions = add_transitions(clips, transition_duration)
    
    # Add music to the video
    video_with_music = add_music(video_with_transitions, music_file)
    
    # Add text overlays to the video
    duration_per_clip = 5  # Adjust as needed
    for i, text_overlay in enumerate(text_overlays):
        start_time = i * duration_per_clip
        end_time = (i + 1) * duration_per_clip
        video_with_music = add_text_overlay(video_with_music.subclip(start_time, end_time), text_overlay, duration_per_clip)
    
    # Resize and format video for social media (9:16 aspect ratio)
    video_with_music = video_with_music.resize(height=720).crop(x1=0, y1=0, width=720)
    
    # Export the final short video
    video_with_music.write_videofile("short_video.mp4", codec="libx264", fps=30)

# Example usage
input_video = "NewRobo.mp4"
clip_timestamps = [(5, 10), (15, 20), (25, 30)]  # Example clip timestamps (in seconds)
music_file = "Infected.mp3"
text_overlays = ["Clip 1", "Clip 2", "Clip 3"]  # Text to overlay on each clip

generate_short_video(input_video, clip_timestamps, music_file, text_overlays)
