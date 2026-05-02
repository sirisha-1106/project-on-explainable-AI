from moviepy.editor import VideoFileClip, AudioFileClip

# load video
video = VideoFileClip("reels/Nature.mp4")

# load audio
audio = AudioFileClip("Nature_sound.mp3")

# add audio to video
final_video = video.set_audio(audio)

# save new video
final_video.write_videofile("reels/Nature_with_sound.mp4",codec="libx264",audio_codec="aac",fps=2)