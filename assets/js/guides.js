document.addEventListener('DOMContentLoaded', async function() {
    // 자료 데이터 불러오기
    try {
        const response = await fetch('../data/all_materials.json');
        const allMaterials = await response.json();
        
        // 수업지도안만 필터링
        const guides = allMaterials.filter(item => item.type === 'guide');
        
        // 수업지도안 목록 표시
        displayGuides(guides);
        
        // 필터링 이벤트 설정
        setupFilters(guides);
    } catch (error) {
        console.error('자료를 불러오는 중 오류가 발생했습니다:', error);
        document.querySelector('.guide-grid').innerHTML = '<p>자료를 불러오는 데 실패했습니다.</p>';
    }
});

// 수업지도안 표시 함수
function displayGuides(guides) {
    const guideGrid = document.querySelector('.guide-grid');
    if (!guideGrid) return;
    
    if (guides.length === 0) {
        guideGrid.innerHTML = '<p>표시할 수업지도안이 없습니다.</p>';
        return;
    }
    
    let html = '';
    guides.forEach(guide => {
        html += `
            <div class="guide-card" data-institute="${guide.institute}" data-subject="${guide.subject || ''}" data-grade="${guide.grade || ''}">
                <h3>${guide.title}</h3>
                <p><strong>연구원:</strong> ${guide.institute}</p>
                <p><strong>교과목:</strong> ${guide.subject || '기타'}</p>
                <p><strong>대상:</strong> ${getGradeText(guide.grade)}</p>
                <p><strong>발행년도:</strong> ${guide.year}</p>
                <a href="${guide.url}" target="_blank">자료 다운로드</a>
            </div>
        `;
    });
    
    guideGrid.innerHTML = html;
}

// 학년 텍스트 변환 함수
function getGradeText(grade) {
    if (!grade) return '모든 학년';
    
    switch(grade) {
        case 'elementary': return '초등학교';
        case 'middle': return '중학교';
        case 'high': return '고등학교';
        default: return grade;
    }
}

// 필터 설정 함수
function setupFilters(guides) {
    const instituteSelect = document.getElementById('institute-select');
    const subjectSelect = document.getElementById('subject-select');
    const gradeSelect = document.getElementById('grade-select');
    
    if (instituteSelect && subjectSelect && gradeSelect) {
        // 필터 변경 이벤트
        const filterChangeHandler = () => {
            const selectedInstitute = instituteSelect.value;
            const selectedSubject = subjectSelect.value;
            const selectedGrade = gradeSelect.value;
            
            filterGuides(guides, selectedInstitute, selectedSubject, selectedGrade);
        };
        
        // 이벤트 리스너 추가
        instituteSelect.addEventListener('change', filterChangeHandler);
        subjectSelect.addEventListener('change', filterChangeHandler);
        gradeSelect.addEventListener('change', filterChangeHandler);
    }
}

// 필터링 함수
function filterGuides(guides, institute, subject, grade) {
    let filteredGuides = [...guides];
    
    // 연구원 필터링
    if (institute !== 'all') {
        filteredGuides = filteredGuides.filter(guide => 
            guide.institute.toLowerCase().includes(institute.toLowerCase())
        );
    }
    
    // 교과목 필터링
    if (subject !== 'all') {
        filteredGuides = filteredGuides.filter(guide => 
            guide.subject && guide.subject.toLowerCase() === subject.toLowerCase()
        );
    }
    
    // 학년 필터링
    if (grade !== 'all') {
        filteredGuides = filteredGuides.filter(guide => 
            guide.grade && guide.grade.toLowerCase() === grade.toLowerCase()
        );
    }
    
    // 필터링된 결과 표시
    displayGuides(filteredGuides);
}
