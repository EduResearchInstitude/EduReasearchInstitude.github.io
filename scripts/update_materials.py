import json
import os
import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime

# 기존 자료 데이터 불러오기
def load_existing_materials():
    try:
        with open('data/all_materials.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# 새 자료인지 확인
def is_new_material(materials, title, institute):
    for material in materials:
        # 제목과 기관이 같고, URL도 같으면 동일 자료로 간주 (URL까지 비교하는 것이 더 정확함)
        if material['title'] == title and material['institute'] == institute:
            return False
    return True

# 연구원 정보 불러오기
def load_institutes():
    try:
        with open('data/institutes.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# 자료 저장하기
def save_materials(materials):
    os.makedirs('data', exist_ok=True) # data 폴더가 없으면 생성
    with open('data/all_materials.json', 'w', encoding='utf-8') as f:
        json.dump(materials, f, ensure_ascii=False, indent=2)

# 각 교육연구원별 크롤링 함수 (웹사이트 구조에 따라 수정 필요)

# 서울교육연구정보원 크롤링 함수 (자료 유형, 연도, 태그 추출 로직 강화)
def crawl_seoul_institute(materials, institute_info):
    base_url = institute_info['url']
    print(f"  > {institute_info['name']} 크롤링 시작...")
    
    try:
        # 서울교육연구정보원의 '연구보고서' 자료실 페이지 (예시 URL)
        report_url = f"{base_url}/cop/bbs/selectBoardList.do?bbsId=BBSMSTR_000000000121"
        response = requests.get(report_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        
        items = soup.select('table.board_list tbody tr') # 게시글 목록
        
        for item in items:
            try:
                title_elem = item.select_one('td.title a')
                date_elem = item.select_one('td.regdate') # 등록일 태그 (예시)

                if not title_elem:
                    continue
                    
                title = title_elem.get_text(strip=True).strip()
                link = title_elem.get('href')
                
                if link and not link.startswith('http'):
                    link = base_url + link # 상대 경로 처리

                if title and link and is_new_material(materials, title, institute_info['name']):
                    material_id = f"id_{institute_info['id']}_{len(materials) + 1}"
                    
                    # -------------------------------------------------------------
                    # 💡 개선된 자료 정보 추출 로직 💡
                    # -------------------------------------------------------------
                    # 1. 자료 유형 (type): 제목에 '지도안', '교육과정' 등 특정 키워드를 포함하는지 확인하여 유추
                    detected_type = "report" # 기본값
                    if "지도안" in title or "수업자료" in title:
                        detected_type = "guide"
                    elif "교육과정" in title or "정책연구" in title:
                        detected_type = "report" # 이미 기본값이지만 명시적으로
                    
                    # 2. 발행 연도 (year): 등록일 태그에서 연도 추출 (예시)
                    detected_year = "미상"
                    if date_elem:
                        full_date_str = date_elem.get_text(strip=True) # 예: 2025-09-29
                        try:
                            detected_year = str(datetime.strptime(full_date_str, '%Y-%m-%d').year)
                        except ValueError:
                            # 다른 날짜 형식일 경우 추가 처리 필요
                            pass
                    else:
                        # 날짜 태그가 없으면 현재 연도를 임시로 사용
                        detected_year = str(datetime.now().year)

                    # 3. 태그 (tags): 제목에서 키워드를 찾아 태그로 활용
                    detected_tags = [institute_info['region'], institute_info['id']] # 지역, ID는 기본 태그
                    if "AI" in title: detected_tags.append("AI")
                    if "미래교육" in title: detected_tags.append("미래교육")
                    if "진로" in title: detected_tags.append("진로")
                    if "과학" in title: detected_tags.append("과학")
                    if "수학" in title: detected_tags.append("수학")
                    # 기타 키워드에 따라 태그 추가 로직 구현
                    # -------------------------------------------------------------

                    new_material = {
                        "id": material_id,
                        "title": title,
                        "institute": institute_info['name'],
                        "type": detected_type,       # 추출된 유형 사용
                        "year": detected_year,       # 추출된 연도 사용
                        "tags": list(set(detected_tags)), # 중복 태그 제거
                        "url": link
                    }
                    materials.append(new_material)
                    print(f"    - 새 자료 추가: {title} (유형: {detected_type}, 연도: {detected_year})")
            except Exception as e:
                print(f"    - 자료 추출 중 오류 발생: {e} in {institute_info['name']}")
                    
    except requests.exceptions.RequestException as e:
        print(f"  > 요청 오류: {institute_info['name']} - {e}")
    except Exception as e:
        print(f"  > 서울교육연구정보원 크롤링 중 알 수 없는 오류: {e}")
    
    return materials

# 부산교육연구소 크롤링 함수
def crawl_busan_institute(materials, institute_info):
    base_url = institute_info['url']
    print(f"  > {institute_info['name']} 크롤링 시작...")

    try:
        # 부산교육연구소 자료실 URL (예시)
        response = requests.get(f"{base_url}/bbs/board.php?bo_table=data", timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        items = soup.select('table.board_list tr') 
        
        for item in items[1:]:
            try:
                title_elem = item.select_one('td.subject a') 
                date_elem = item.select_one('td.datetime') # 등록일 태그 (예시)

                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True).strip()
                link = title_elem.get('href')
                
                if link and not link.startswith('http'):
                    link = base_url + link

                if title and link and is_new_material(materials, title, institute_info['name']):
                    material_id = f"id_{institute_info['id']}_{len(materials) + 1}"
                    
                    # -------------------------------------------------------------
                    # 💡 개선된 자료 정보 추출 로직 (부산도 동일하게 적용) 💡
                    # -------------------------------------------------------------
                    detected_type = "report"
                    if "지도안" in title or "수업자료" in title:
                        detected_type = "guide"
                    
                    detected_year = "미상"
                    if date_elem:
                        full_date_str = date_elem.get_text(strip=True) # 예: 2025-09-29
                        try:
                            detected_year = str(datetime.strptime(full_date_str, '%Y-%m-%d').year)
                        except ValueError:
                            pass
                    else:
                        detected_year = str(datetime.now().year)

                    detected_tags = [institute_info['region'], institute_info['id']]
                    if "AI" in title: detected_tags.append("AI")
                    if "미래교육" in title: detected_tags.append("미래교육")
                    if "창의성" in title: detected_tags.append("창의성")
                    if "수학" in title: detected_tags.append("수학")
                    # -------------------------------------------------------------

                    new_material = {
                        "id": material_id,
                        "title": title,
                        "institute": institute_info['name'],
                        "type": detected_type,
                        "year": detected_year,
                        "tags": list(set(detected_tags)),
                        "url": link
                    }
                    materials.append(new_material)
                    print(f"    - 새 자료 추가: {title} (유형: {detected_type}, 연도: {detected_year})")
            except Exception as e:
                print(f"    - 자료 추출 중 오류 발생: {e} in {institute_info['name']}")
                
    except requests.exceptions.RequestException as e:
        print(f"  > 요청 오류: {institute_info['name']} - {e}")
    except Exception as e:
        print(f"  > 부산교육연구소 크롤링 중 알 수 없는 오류: {e}")
    
    return materials

# 대구창의융합교육원 크롤링 함수
def crawl_daegu_institute(materials, institute_info):
    base_url = institute_info['url']
    print(f"  > {institute_info['name']} 크롤링 시작...")

    try:
        # 대구창의융합교육원 자료실 URL (예시)
        response = requests.get(f"{base_url}/board/list.do?boardId=BBS_0000008", timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        
        items = soup.select('table.board_list tbody tr') 
        
        for item in items:
            try:
                title_elem = item.select_one('td.title a') 
                date_elem = item.select_one('td.reg_dt') # 등록일 태그 (예시)

                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True).strip()
                link = title_elem.get('href')
                
                if link and not link.startswith('http'):
                    link = base_url + link

                if title and link and is_new_material(materials, title, institute_info['name']):
                    material_id = f"id_{institute_info['id']}_{len(materials) + 1}"
                    
                    # -------------------------------------------------------------
                    # 💡 개선된 자료 정보 추출 로직 (대구도 동일하게 적용) 💡
                    # -------------------------------------------------------------
                    detected_type = "report"
                    if "지도안" in title or "수업자료" in title or "융합프로젝트" in title:
                        detected_type = "guide"
                    
                    detected_year = "미상"
                    if date_elem:
                        full_date_str = date_elem.get_text(strip=True) # 예: 2025-09-29
                        try:
                            detected_year = str(datetime.strptime(full_date_str, '%Y-%m-%d').year)
                        except ValueError:
                            pass
                    else:
                        detected_year = str(datetime.now().year)

                    detected_tags = [institute_info['region'], institute_info['id']]
                    if "창의" in title: detected_tags.append("창의")
                    if "융합" in title: detected_tags.append("융합")
                    if "과학" in title: detected_tags.append("과학")
                    if "수학" in title: detected_tags.append("수학")
                    # -------------------------------------------------------------

                    new_material = {
                        "id": material_id,
                        "title": title,
                        "institute": institute_info['name'],
                        "type": detected_type,
                        "year": detected_year,
                        "tags": list(set(detected_tags)),
                        "url": link
                    }
                    materials.append(new_material)
                    print(f"    - 새 자료 추가: {title} (유형: {detected_type}, 연도: {detected_year})")
            except Exception as e:
                print(f"    - 자료 추출 중 오류 발생: {e} in {institute_info['name']}")
                
    except requests.exceptions.RequestException as e:
        print(f"  > 요청 오류: {institute_info['name']} - {e}")
    except Exception as e:
        print(f"  > 대구창의융합교육원 크롤링 중 알 수 없는 오류: {e}")
    
    return materials

# 인천교육과학정보원 크롤링 함수
def crawl_incheon_institute(materials, institute_info):
    base_url = institute_info['url']
    print(f"  > {institute_info['name']} 크롤링 시작...")

    try:
        # 인천교육과학정보원 자료실 URL (예시)
        response = requests.get(f"{base_url}/boardCnts/list.do?boardID=1624&m=0301&s=ice", timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        
        items = soup.select('table.board_type01 tbody tr') # 예시 셀렉터
        
        for item in items:
            try:
                title_elem = item.select_one('td.tit a') 
                date_elem = item.select_one('td.date') # 등록일 태그 (예시)

                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True).strip()
                link = title_elem.get('href')
                
                if link and not link.startswith('http'):
                    link = base_url + link

                if title and link and is_new_material(materials, title, institute_info['name']):
                    material_id = f"id_{institute_info['id']}_{len(materials) + 1}"
                    
                    # -------------------------------------------------------------
                    # 💡 개선된 자료 정보 추출 로직 (인천도 동일하게 적용) 💡
                    # -------------------------------------------------------------
                    detected_type = "report"
                    if "지도안" in title or "수업자료" in title or "탐구보고서" in title:
                        detected_type = "guide"
                    
                    detected_year = "미상"
                    if date_elem:
                        full_date_str = date_elem.get_text(strip=True) # 예: 2025.09.29 또는 2025-09-29
                        try:
                            detected_year = str(datetime.strptime(full_date_str.replace('.', '-'), '%Y-%m-%d').year)
                        except ValueError:
                            pass
                    else:
                        detected_year = str(datetime.now().year)

                    detected_tags = [institute_info['region'], institute_info['id']]
                    if "과학" in title: detected_tags.append("과학")
                    if "정보" in title: detected_tags.append("정보")
                    if "환경" in title: detected_tags.append("환경")
                    # -------------------------------------------------------------

                    new_material = {
                        "id": material_id,
                        "title": title,
                        "institute": institute_info['name'],
                        "type": detected_type,
                        "year": detected_year,
                        "tags": list(set(detected_tags)),
                        "url": link
                    }
                    materials.append(new_material)
                    print(f"    - 새 자료 추가: {title} (유형: {detected_type}, 연도: {detected_year})")
            except Exception as e:
                print(f"    - 자료 추출 중 오류 발생: {e} in {institute_info['name']}")
                
    except requests.exceptions.RequestException as e:
        print(f"  > 요청 오류: {institute_info['name']} - {e}")
    except Exception as e:
        print(f"  > 인천교육과학정보원 크롤링 중 알 수 없는 오류: {e}")
    
    return materials

# 광주창의융합교육원 크롤링 함수 (앞서 제공된 코드 유지)
def crawl_gwangju_institute(materials, institute_info):
    base_url = institute_info['url']
    print(f"  > {institute_info['name']} 크롤링 시작...")

    try:
        response = requests.get(f"{base_url}/cop/bbs/selectBoardList.do?bbsId=BBSMSTR_000000000101", timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        
        items = soup.select('table.board_list tbody tr') 
        
        for item in items:
            try:
                title_elem = item.select_one('td.subject a') 
                date_elem = item.select_one('td.reg_dt') # 등록일 태그 (예시)

                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True).strip()
                link = title_elem.get('href')
                
                if link and not link.startswith('http'):
                    link = base_url + link

                if title and link and is_new_material(materials, title, institute_info['name']):
                    material_id = f"id_{institute_info['id']}_{len(materials) + 1}"
                    
                    # -------------------------------------------------------------
                    # 💡 개선된 자료 정보 추출 로직 (광주도 동일하게 적용) 💡
                    # -------------------------------------------------------------
                    detected_type = "report"
                    if "지도안" in title or "수업자료" in title or "창의체험" in title:
                        detected_type = "guide"
                    
                    detected_year = "미상"
                    if date_elem:
                        full_date_str = date_elem.get_text(strip=True) 
                        try:
                            detected_year = str(datetime.strptime(full_date_str, '%Y-%m-%d').year)
                        except ValueError:
                            pass
                    else:
                        detected_year = str(datetime.now().year)

                    detected_tags = [institute_info['region'], institute_info['id']]
                    if "창의" in title: detected_tags.append("창의")
                    if "융합" in title: detected_tags.append("융합")
                    if "교육" in title: detected_tags.append("교육")
                    # -------------------------------------------------------------

                    new_material = {
                        "id": material_id,
                        "title": title,
                        "institute": institute_info['name'],
                        "type": detected_type,
                        "year": detected_year,
                        "tags": list(set(detected_tags)),
                        "url": link
                    }
                    materials.append(new_material)
                    print(f"    - 새 자료 추가: {title} (유형: {detected_type}, 연도: {detected_year})")
            except Exception as e:
                print(f"    - 자료 추출 중 오류 발생: {e} in {institute_info['name']}")
                
    except requests.exceptions.RequestException as e:
        print(f"  > 요청 오류: {institute_info['name']} - {e}")
    except Exception as e:
        print(f"  > 광주창의융합교육원 크롤링 중 알 수 없는 오류: {e}")
    
    return materials


# 메인 함수
def main():
    # 기존 자료 불러오기
    materials = load_existing_materials()
    print(f"기존 자료 수: {len(materials)}")
    
    # 연구원 정보 불러오기
    institutes = load_institutes()
    if not institutes:
        print("연구원 정보를 찾을 수 없습니다.")
        return
    
    # 각 연구원별로 크롤링 실행
    for institute in institutes:
        print(f"\n--------------------------------------------------")
        print(f"  > {institute['name']} 자료 수집 시도 중...")
        
        if "서울교육연구정보원" in institute['name']:
            materials = crawl_seoul_institute(materials, institute)
        elif "부산교육연구소" in institute['name']:
            materials = crawl_busan_institute(materials, institute)
        elif "대구창의융합교육원" in institute['name']:
            materials = crawl_daegu_institute(materials, institute)
        elif "인천교육과학정보원" in institute['name']:
            materials = crawl_incheon_institute(materials, institute)
        elif "광주창의융합교육원" in institute['name']: 
            materials = crawl_gwangju_institute(materials, institute)
        else:
            print(f"  > {institute['name']} 에 대한 크롤링 함수가 없습니다. 스킵합니다.")
            
        # 크롤링 사이에 잠시 대기 (서버 부하 방지 및 차단 방지)
        time.sleep(random.uniform(2, 5)) # 2초에서 5초 사이 랜덤 대기

    # 수집한 자료 저장
    save_materials(materials)
    print(f"\n--------------------------------------------------")
    print(f"자료 수집 완료. 총 {len(materials)}개의 자료가 있습니다.")

# 스크립트 실행
if __name__ == "__main__":
    main()
