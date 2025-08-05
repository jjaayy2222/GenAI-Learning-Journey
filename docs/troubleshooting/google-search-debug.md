# googlee-search-debug.md
**작성일**: 2025-08-06
**상황**: `Error during Google search: search() got an unexpected keyword argument 'num_results'` 출력
**발생위치**: `/GenAI-Learning-Journey/선택_GenAI/05_LLM_data_services/02_데이터_기반_서비스/5/web.py`

### `google_search` 함수 디버깅 기록

#### 1. **에러 발생 상황**

* **에러 메시지**: 

    ```python
       TypeError: search() got an unexpected keyword argument 'num_results'
    ```

* **원인_1**:
- **구글 검색 패키지 변경**
  - 변경된 패키지: `googlesearch` → **`googlesearch-python`**

- **변경 이유**
  - 기존 `googlesearch 패키지`에서 인자 관련 오류 발생
  - 새로운 패키지인 `googlesearch-python 패키지`로 변경하여 `stop 인자` 사용

- **`from googlesearch import search` 관련 패키지** 설치시 **주의**
  - `pip install googlesearch-python` = O
    - `googlesearch-python` : 웹 검색용 search() 포함, googlesearch 패키지 적용

  - `pip install googlesearch` = X
    - `googlesearch` = google API client, 검색 기능 X 
        
  - **오류 발생 시** : (터미널) `pip freeze | grep google`
    - `google==3.x.x` → `X` → **`uninstall googlesearch`** → pip install googlesearch-python
    - `googlesearch-python==1.x.x` → `O`



* **원인_2**:
- `googlesearch-python` 패키지의 `search()` 함수는 **`num_results`** 대신 **`stop`** 인자 사용
- `num_results`는 더 이상 지원되지 않으므로 `stop`으로 교체 필요<br><br>

---

#### 2. **해결 방법**

* **에러 발생 원인**: `num_results` 인자는 `googlesearch-python`의 `search()`에서 더 이상 지원되지 않음
* **수정 사항**: `num_results` → `stop`

    ```python
        def google_search(query: str, num_results=10) -> list:
            "Google 검색 결과에서 상위 URL을 가져오는 함수"
            try:
                # 수정 전
                # urls = [url for url in search(query, num_results=num_results)]

                # 수정 후
                urls = [url for url in search(query, stop=num_results)]         # num_results -> stop 
                return urls[:num_results]
            except Exception as e:
                print(f"Error during Google search: {e}")
                return []
    ```

#### 3. **추가 고려사항**

* `googlesearch-python` 패키지에서 더 이상 `num_results`를 받지 않으므로, 이를 사용하는 다른 코드가 있다면 동일한 방법으로 수정
* `search()` 함수에서 **`stop`** 인자를 받아 몇 개의 검색 결과에서 멈출지를 지정하는 방식으로 변경되었기 때문
