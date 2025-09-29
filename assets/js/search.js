// 샘플 데이터 (나중에 실제 데이터로 대체할 수 있습니다)
const searchData = [
    {
        id: "report001",
        title: "2025 교육과정 개정 연구",
        institute: "서울교육연구정보원",
        type: "report",
        year: 2025,
        tags: ["교육과정", "개정", "연구"],
        url: "https://serii.sen.go.kr"
    },
    {
        id: "report002",
        title: "AI 활용 교육 방안 연구",
        institute: "부산교육연구소",
        type: "report",
        year: 2024,
        tags: ["AI", "인공지능", "교육"],
        url: "#"
    },
    {
        id: "guide001",
        title: "AI를 활용한 과학 탐구 수업",
        institute: "서울교육연구정보원",
        type: "guide",
        subject: "과학",
        grade: "middle",
        year: 2025,
        tags: ["AI", "과학", "탐구"],
        url: "#"
    },
    {
        id: "guide002",
        title: "데이터 시각화로 배우는 통계",
        institute: "부산교육연구소",
        type: "guide",
        subject: "수학",
        grade: "high",
        year: 2024,
        tags: ["통계", "데이터", "시각화"],
        url: "#"
    },
    {
        id: "guide003",
        title: "디지털 스토리텔링 국어 수업",
        institute: "대구창의융합교육원",
        type: "guide",
        subject: "국어",
        grade: "elementary",
        year: 2025,
        tags: ["국어", "스토리텔링", "디지털"],
        url: "#"
    }
];

// 검색 함수
function performSearch() {
    const searchInput = document.getElementById('search-input').value.toLowerCase();
    const resultsContainer = document.getElementById('search-results');
    
    // 검색어가 비어있으면 결과를 표시하지 않음
    if (searchInput.trim() === '') {
        resultsContainer.innerHTML = '<p>검색어를 입력하세요.</p>';
        return;
    }
    
    // 검색 실행
    const results = searchData.filter(item => {
        return item.title.toLowerCase().includes(searchInput) || 
               item.institute.toLowerCase().includes(searchInput) ||
               item.tags.some(tag => tag.toLowerCase().includes(searchInput));
    });
    
    // 결과 표시
    if (results.length === 0) {
        resultsContainer.innerHTML = '<p>검색 결과가 없습니다.</p>';
    } else {
        let html = `<p>${results.length}개의 결과를 찾았습니다.</p>`;
        html += '<div class="results-list">';
        
        results.forEach(item => {
            html += `
                <div class="result-item">
                    <h3>${item.title}</h3>
                    <p><strong>기관:</strong> ${item.institute}</p>
                    <p><strong>유형:</strong> ${item.type === 'report' ? '연구보고서' : '수업지도안'}</p>
                    <p><strong>발행년도:</strong> ${item.year}</p>
                    <a href="${item.url}" target="_blank">자료 보기</a>
                </div>
            `;
        });
        
        html += '</div>';
        resultsContainer.innerHTML = html;
    }
}

// 페이지 로드 시 검색 버튼에 이벤트 리스너 추가
document.addEventListener('DOMContentLoaded', function() {
    const searchButton = document.getElementById('search-button');
    if (searchButton) {
        searchButton.addEventListener('click', performSearch);
    }
    
    // 엔터 키 입력 시 검색 실행
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }
});
