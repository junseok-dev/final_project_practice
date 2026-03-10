from moviepy.editor import VideoFileClip, AudioFileClip

# 1. Leonardo API 등으로 만든 무음 영상 불러오기
video = VideoFileClip("virtual_character_motion.mp4")

# 2. ElevenLabs API 등으로 만든 음성 파일 불러오기
audio = AudioFileClip("character_voice.mp3")

# 3. 영상에 오디오 입히기 (길이가 맞지 않으면 조정 가능)
final_video = video.set_audio(audio)

# 4. 최종 결과물 저장
final_video.write_videofile("final_virtual_influencer.mp4", fps=24)