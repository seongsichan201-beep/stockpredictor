from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import datetime
import os

try:
    from webdriver_manager.chrome import ChromeDriverManager
    _USE_WEBDRIVER_MANAGER = True
except Exception:
    _USE_WEBDRIVER_MANAGER = False


def run_auto_crawler():
    print("=== Google 뉴스 자동 크롤링 시작 ===")

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-browser-side-navigation")

    if _USE_WEBDRIVER_MANAGER:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)

    # "페이지 로딩 시간 제한" 강제 적용
    driver.set_page_load_timeout(8)

    url = "https://news.google.com/home?hl=ko&gl=KR&ceid=KR%3Ako"
    driver.get(url)
    time.sleep(2)

    print("스크롤 중...")

    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(8):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    print("링크 수집 중...")

    selectors = ["a.DY5T1d", "a.JtKRv", "a.WwrzSb"]
    links = []

    for selector in selectors:
        elems = driver.find_elements(By.CSS_SELECTOR, selector)
        for e in elems:
            url = e.get_attribute("href")
            if url and url not in links:
                links.append(url)

    print(f"총 {len(links)}개 링크 감지")

    news_data = []

    # 기사 반복 스캔
    for idx, link in enumerate(links, start=1):
        print(f"\n▶ {idx}번째 기사 스캔 중…")

        try:
            driver.get(link)
        except Exception:
            print("⚠ 페이지 로딩 실패 → 건너뜀")
            continue

        time.sleep(1)

        # 제목 3초 타임아웃
        try:
            title_elem = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            title = title_elem.text.strip()
        except Exception:
            title = "제목 없음"
            print("⚠ 제목을 찾을 수 없음")

        # 본문 3초 타임아웃
        try:
            paragraphs = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "p"))
            )
            body = "\n".join([p.text.strip() for p in paragraphs if p.text.strip()])
        except Exception:
            body = ""
            print("⚠ 본문 없음")

        # 제목 + 본문 둘 다 없음 → PASS
        if title == "제목 없음" and body == "":
            print("⚠ 기사 내용 없음 → 다음으로")
            continue

        news_data.append({
            "url": link,
            "title": title,
            "body": body
        })

        print(f"✔ 스캔 성공: {title}")

    driver.quit()

    # 저장
    os.makedirs("news_daily", exist_ok=True)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"news_daily/news_{today}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(news_data, f, ensure_ascii=False, indent=4)

    print(f"\n📁 저장 완료 → {filename}")
    print("=== 크롤링 종료 ===")
    

if __name__ == "__main__":
    run_auto_crawler()
