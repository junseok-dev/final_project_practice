import requests
from bs4 import BeautifulSoup
import time

def crawl_to_txt(pages=5, filename="hari_news_data.txt"):
    """
    지정한 페이지 수만큼 뉴스를 수집하여 텍스트 파일로 저장합니다.
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    base_url = "https://news.hada.io/"
    
    # 'w' 모드는 덮어쓰기, 'a' 모드는 기존 내용 뒤에 추가하기입니다.
    # 여기서는 실행할 때마다 새로 파일을 만듭니다.
    with open(filename, "w", encoding="utf-8") as f:
        f.write("=== 하리 테크 뉴스 수집 데이터 ===\n\n")
        
        total_count = 0
        for page in range(1, pages + 1):
            print(f"🔎 {page}페이지 수집 중...")
            params = {'page': page}
            
            try:
                response = requests.get(base_url, headers=headers, params=params)
                soup = BeautifulSoup(response.text, 'html.parser')
                topics = soup.select('.topic_row')

                for topic in topics:
                    title = topic.select_one('.topictitle h1').get_text(strip=True)
                    summary = topic.select_one('.topicdesc').get_text(strip=True)
                    link = base_url + topic.select_one('.topictitle a')['href']

                    # 텍스트 파일에 쓸 형식 구성
                    f.write(f"📌 제목: {title}\n")
                    f.write(f"📝 요약: {summary}\n")
                    f.write(f"🔗 링크: {link}\n")
                    f.write("-" * 50 + "\n") # 뉴스 간 구분선
                    
                    total_count += 1
                
                # 서버 부하 방지를 위해 잠깐 휴식
                time.sleep(1)

            except Exception as e:
                print(f"에러 발생: {e}")

    print(f"✅ 저장 완료! '{filename}' 파일에 총 {total_count}개의 뉴스가 기록되었습니다.")

# 실행: 10페이지 수집 (약 150~200개 데이터)
if __name__ == "__main__":
    crawl_to_txt(pages=10)