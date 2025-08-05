from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from googlesearch import search                                             # pip install googlesearch-python (터미널)




def google_search(query: str, num_results=10) -> list:
    "Google 검색 결과에서 상위 URL을 가져오는 함수"
    try:
        urls = [url for url in search(query, stop=num_results)]
        return urls[:num_results]
    except Exception as e:
        print(f"Error during Google search: {e}")
        return []


# 페이지의 텍스트 추출
def extract_text(url: str) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        return text

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""


def post_process(text: str) -> str:
    "크롤링된 텍스트 후처리하는 함수"

    # 연속된 \n을 \n으로 변경
    text = "\n".join([line for line in text.split("\n") if line.strip()])

    # 2000자로 자르기
    return text[:2000]


# 메인 크롤링 함수
def search_web(query: str) -> List[str]:
    """인터넷에서 query를 검색하고 상위 4개 페에지의 텍스트를 모아서 반환하는 함수

    Args:
        query (str): 웹에 검색할 문자열. 관련 정보를 웹에서 찾기 위해 검색할 적절한 검색어로 설정해야 함.

    Returns:
        list: 상위 4개 페이지의 텍스트 리스트
    """
    urls = google_search(query)
    text_list = []

    count = 0

    for url in urls:
        page_text = extract_text(url)
        if page_text:
            page_text = post_process(page_text)
            page_text = f"{count + 1}. {url}:\n{page_text}\n"
            text_list.append(page_text)
            count += 1

        if count >= 4:
            break
    return text_list
