document.addEventListener('DOMContentLoaded', async function() {
    // 자료 데이터 불러오기
    try {
        const response = await fetch('/data/all_materials.json');
        const allMaterials = await response.json();
        
        // 연구보고서만 필터링
        const reports = allMaterials.filter(item => item.type === 'report');
        
        // 연구보고서 목록 표시
        displayReports(reports);
        
        // 연구원 선택 필터 이벤트 설정
        const instituteSelect = document.getElementById('institute-select');
        if (instituteSelect) {
            instituteSelect.addEventListener('change', function() {
                const selectedInstitute = this.value;
                filterReports(reports, selectedInstitute);
            });
        }
    } catch (error) {
        console.error('자료를 불러오는 중 오류가 발생했습니다:', error);
        document.querySelector('.report-list').innerHTML = '<p>자료를 불러오는 데 실패했습니다.</p>';
    }
});

// 연구보고서 목록 표시 함수
function displayReports(reports) {
    const reportList = document.querySelector('.report-list');
    if (!reportList) return;
    
    if (reports.length === 0) {
        reportList.innerHTML = '<p>표시할 연구보고서가 없습니다.</p>';
        return;
    }
    
    let html = '';
    reports.forEach(report => {
        html += `
            <li class="report-item" data-institute="${report.institute}">
                <h3>${report.title}</h3>
                <p><strong>연구원:</strong> ${report.institute}</p>
                <p><strong>발행년도:</strong> ${report.year}</p>
                <p><strong>태그:</strong> ${report.tags.join(', ')}</p>
                <a href="${report.url}" target="_blank">자료 보기</a>
            </li>
        `;
    });
    
    reportList.innerHTML = html;
}

// 연구원 필터링 함수
function filterReports(reports, institute) {
    if (institute === 'all') {
        displayReports(reports);
        return;
    }
    
    const filteredReports = reports.filter(report => 
        report.institute.toLowerCase().includes(institute.toLowerCase())
    );
    
    displayReports(filteredReports);
}
