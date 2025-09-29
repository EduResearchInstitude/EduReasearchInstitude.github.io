import json
import os
import requests
from bs4 import BeautifulSoup
import time
import random

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
    # data 폴더가 없으면 생성
    os.makedirs('data', exist_ok=True)
    
    with open('data/all_materials.json', 'w', encoding='utf-8') as f:
        json.dump(materials, f, ensure_ascii=False, indent=2)

# 크롤링 함수 (서울교육연구정보원)
def crawl_seoul_institute(materials, institute_info):
    base_url = institute_info['url']
    
    try:
        # 서울교육연구정보원 자료실 페이지
        response = requests.get(f"{base_url}/cop/bbs/selectBoardList.do?bbsId=BBSMSTR_000000000121")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 게시글 목록 찾기
            items = soup.select('table.board_list tbody tr')
            
            for item in items:
                try:
                    # 제목과 링크 추출
                    title_elem = item.select_one('td.title a')
                    if not title_elem:
                        continue
                        
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get('href')
                    if not link.startswith('http'):
                        link = base_url + link
                    
                    # 새 자료인 경우에만 추가
                    if is_new_material(materials, title, institute_info['name']):
                        # 자료 ID 생성
                        material_id = f"report{len(materials) + 1:03d}"
                        
                        # 새 자료 정보 생성
                        new_material = {
                            "id": material_id,
                            "title": title,
                            "institute": institute_info['name'],
                            "type": "report",  # 기본값
                            "year": 2025,      # 기본값
                            "tags": ["교육", "연구"],  # 기본 태그
                            "url": link
                        }
                        
                        materials.append(new_material)
                        print(f"새 자료 추가: {title}")
                except Exception as e:
                    print(f"자료 추출 중 오류 발생: {e}")
                    
    except Exception as e:
        print(f"서울교육연구정보원 크롤링 중 오류: {e}")
    
    return materials

# 부산교육연구소 크롤링 함수
def crawl_busan_institute(materials, institute_info):
    base_url = institute_info['url']
    
    try:
        # 부산교육연구소 자료실 페이지 (URL은 실제 사이트에 맞게 수정 필요)
        response = requests.get(f"{base_url}/bbs/board.php?bo_table=data")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 게시글 목록 찾기 (실제 웹사이트 구조에 맞게 수정 필요)
            items = soup.select('table.board_list tr')
            
            for item in items[1:]:  # 첫 번째 행은 헤더이므로 건너뜀
                try:
                    # 제목과 링크 추출
                    title_elem = item.select_one('td.subject a')
                    if not title_elem:
                        continue
                        
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get('href')
                    if not link.startswith('http'):
                        link = base_url + link
                    
                    # 새 자료인 경우에만 추가
                    if is_new_material(materials, title, institute_info['name']):
                        material_id = f"report{len(materials) + 1:03d}"
                        
                        new_material = {
                            "id": material_id,
                            "title": title,
                            "institute": institute_info['name'],
                            "type": "report",
                            "year": 2025,
                            "tags": ["교육", "연구"],
                            "url": link
                        }
                        
                        materials.append(new_material)
                        print(f"새 자료 추가: {title}")
                except Exception as e:
                    print(f"자료 추출 중 오류 발생: {e}")
                    
    except Exception as e:
        print(f"부산교육연구소 크롤링 중 오류: {e}")
    
    return materials

# 대구창의융합교육원 크롤링 함수
def crawl_daegu_institute(materials, institute_info):
    base_url = institute_info['url']
    
    try:
        # 대구창의융합교육원 자료실 페이지 (URL은 실제 사이트에 맞게 수정 필요)
        response = requests.get(f"{base_url}/board/list.do?boardId=BBS_0000008")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 게시글 목록 찾기
            items = soup.select('table.board_list tbody tr')
            
            for item in items:
                try:
                    title_elem = item.select_one('td.title a')
                    if not title_elem:
                        continue
                        
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get('href')
                    if not link.startswith('http'):
                        link = base_url + link
                    
                    if is_new_material(materials, title, institute_info['name']):
                        material_id = f"report{len(materials) + 1:03d}"
                        
                        new_material = {
                            "id": material_id,
                            "title": title,
                            "institute": institute_info['name'],
                            "type": "report",
                            "year": 2025,
                            "tags": ["교육", "연구", "창의융합"],
                            "url": link
                        }
                        
                        materials.append(new_material)
                        print(f"새 자료 추가: {title}")
                except Exception as e:
                    print(f"자료 추출 중 오류 발생: {e}")
                    
    except Exception as e:
        print(f"대구창의융합교육원 크롤링 중 오류: {e}")
    
    return materials

# 인천교육과학정보원 크롤링 함수
def crawl_incheon_institute(materials, institute_info):
    base_url = institute_info['url']
    
    try:
        # 인천교육과학정보원 자료실 페이지
        response = requests.get(f"{base_url}/boardCnts/list.do?boardID=1624&m=0301&s=ice")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 게시글 목록 찾기
            items = soup.select('table.board_type01 tbody tr')
            
            for item in items:
                try:
                    title_elem = item.select_one('td.tit a')
                    if not title_elem:
                        continue
                        
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get('href')
                    if not link.startswith('http'):
                        link = base_url + link
                    
                    if is_new_material(materials, title, institute_info['name']):
                        material_id = f"report{len(materials) + 1:03d}"
                        
                        new_material = {
                            "id": material_id,
                            "title": title,
                            "institute": institute_info['name'],
                            "type": "report",
                            "year": 2025,
                            "tags": ["교육", "과학", "정보"],
                            "url": link
                        }
                        
                        materials.append(new_material)
                        print(f"새 자료 추가: {title}")
                except Exception as e:
                    print(f"자료 추출 중 오류 발생: {e}")
                    
    except Exception as e:
        print(f"인천교육과학정보원 크롤링 중 오류: {e}")
    
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
        print(f"{institute['name']} 자료 수집 중...")
        
        if "서울교육연구정보원" in institute['name']:
            materials = crawl_seoul_institute(materials, institute)
        elif "부산교육연구소" in institute['name']:
            materials = crawl_busan_institute(materials, institute)
        elif "대구창의융합교육원" in institute['name']:
            materials = crawl_daegu_institute(materials, institute)
        elif "인천교육과학정보원" in institute['name']:
            materials = crawl_incheon_institute(materials, institute)
        
        # 다른 연구원들도 비슷한 방식으로 추가 가능
        # 크롤링 사이에 잠시 대기 (서버 부하 방지)
        time.sleep(random.uniform(1, 3))
    
    # 수집한 자료 저장
    save_materials(materials)
    print(f"자료 수집 완료. 총 {len(materials)}개의 자료가 있습니다.")

# 스크립트 실행
if __name__ == "__main__":
    main()
