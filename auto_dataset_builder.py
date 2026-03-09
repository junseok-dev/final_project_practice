import os
import subprocess
import yt_dlp
import whisper
from pydub import AudioSegment
import json
import re

# --- [1. 프로젝트 설정: 특정 유튜버 타겟팅] ---
# 검색이 잘 되면서도 말투가 잘 살아있는 키워드로 구성했습니다.
KEYWORDS = [
    "유트루 수다 브이로그",          # 친근한 대화체 (유트루)
    "유트루 겟레디윗미 나레이션",     # 연속된 문장 (유트루)
    "헤이즐 뷰티 하울 설명",         # 전문적인 상품 홍보 (헤이즐)
    "헤이즐 브이로그 수다",          # 트렌디한 말투 (헤이즐)
    "플랜디 일상 나레이션",          # 차분하고 정갈한 톤 (플랜디)
    "플랜디 브이로그 목소리"         # 감성적인 구어체 (플랜디)
]

MAX_VIDEOS_PER_KEYWORD = 3  # 키워드당 3개씩 검색 (총 18개 시도)
OUTPUT_BASE = "influencer_special_dataset"
RAW_DIR = f"{OUTPUT_BASE}/01_raw"
VOCAL_DIR = f"{OUTPUT_BASE}/02_vocals"
SLICED_DIR = f"{OUTPUT_BASE}/wavs"

for d in [RAW_DIR, VOCAL_DIR, SLICED_DIR]:
    os.makedirs(d, exist_ok=True)

# --- [2. 3분 이내 한국어 소스 수집] ---
def fetch_target_youtubers():
    print("\n--- [Step 1] 지정 유튜버 데이터 검색 및 수집 시작 ---")
    
    def duration_filter(info, *, incomplete):
        duration = info.get('duration')
        if duration and duration > 180: # 3분(180초) 이내 영상만 허용
            return f"건너뜀: {duration}초 (3분 초과)"
        return None

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'wav', 'preferredquality': '192'}],
        'outtmpl': f'{RAW_DIR}/%(id)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
        'match_filter': duration_filter,
    }

    downloaded_files = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for kw in KEYWORDS:
            print(f"🔎 검색 중: {kw}...")
            # 한국어 소스를 확실히 하기 위해 '한국어' 키워드 추가
            search_query = f"ytsearch{MAX_VIDEOS_PER_KEYWORD}:{kw} 한국어"
            try:
                info = ydl.extract_info(search_query, download=True)
                if 'entries' in info:
                    for entry in info['entries']:
                        if entry:
                            file_path = os.path.join(RAW_DIR, f"{entry['id']}.wav")
                            if os.path.exists(file_path):
                                downloaded_files.append(file_path)
                                print(f"   ✅ 수집 완료: {entry['title'][:20]}...")
            except Exception as e:
                print(f"   ⚠️ 오류: {e}")

    print(f"📊 총 {len(downloaded_files)}개의 원본 파일이 준비되었습니다.")
    return downloaded_files

# --- [3. 보컬 분리 (Demucs)] ---
def separate_vocals(file_paths):
    print("\n--- [Step 2] 보컬 분리 작업 시작 ---")
    v_paths = []
    for path in file_paths:
        v_id = os.path.splitext(os.path.basename(path))[0]
        v_out = os.path.join(VOCAL_DIR, "htdemucs", v_id, "vocals.wav")
        if not os.path.exists(v_out):
            try:
                subprocess.run(["demucs", "--two-stems", "vocals", "-o", VOCAL_DIR, path], check=True)
            except: continue
        if os.path.exists(v_out): v_paths.append(v_out)
    return v_paths

# --- [4. 문장 정제 및 JSON 저장] ---
def slice_and_label_json(v_paths):
    print("\n--- [Step 3] 한국어 문장 추출 및 JSON 저장 시작 ---")
    model = whisper.load_model("base")
    json_data = {}
    count = 1

    for v_path in v_paths:
        # 한국어 고정 분석
        result = model.transcribe(v_path, language="ko", verbose=False)
        audio = AudioSegment.from_wav(v_path)
        
        for segment in result['segments']:
            text = segment['text'].strip()
            no_speech = segment.get('no_speech_prob', 0)
            has_korean = re.search('[가-힣]', text)
            
            # 필터: 효과음 제외(no_speech < 0.4) + 한글 포함 + 2.5초~10초 사이 문장
            if no_speech < 0.4 and has_korean and 2500 <= (int(segment['end']*1000) - int(segment['start']*1000)) <= 10000:
                file_name = f"influencer_data_{count:04d}.wav"
                target = os.path.join(SLICED_DIR, file_name)
                
                start, end = int(segment['start']*1000), int(segment['end']*1000)
                audio[start:end].set_frame_rate(22050).set_channels(1).export(target, format="wav")

                # 대사에 따옴표("") 포함 JSON 형식
                json_data[file_name] = f'"{text}"'
                print(f"   📄 [{count}] {file_name} 추출: \"{text}\"")
                count += 1

    # 최종 JSON 파일 저장
    json_path = os.path.join(OUTPUT_BASE, "metadata.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
    
    print(f"\n✨ 완료! 총 {count-1}개의 데이터가 JSON과 함께 생성되었습니다.")

if __name__ == "__main__":
    try:
        files = fetch_target_youtubers()
        if files:
            vocals = separate_vocals(files)
            slice_and_label_json(vocals)
        else:
            print("🚨 조건에 맞는 영상을 찾지 못했습니다. 키워드를 더 단순화해 보세요.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")