document.addEventListener('DOMContentLoaded', async function() {
    try {
        // 연구원 정보 데이터 불러오기
        const response = await fetch('data/institutes.json');
        const institutes = await response.json();

        const instituteListContainer = document.getElementById('institute-list-container');
        if (instituteListContainer) {
            let listHtml = '<ul class="institute-list-links">';
            institutes.forEach(institute => {
                listHtml += `<li><a href="${institute.url}" target="_blank">${institute.name}</a></li>`;
            });
            listHtml += '</ul>';
            instituteListContainer.innerHTML = listHtml;
        }

    } catch (error) {
        console.error('인덱스 페이지 자료를 불러오는 중 오류 발생:', error);
        const instituteListContainer = document.getElementById('institute-list-container');
        if (instituteListContainer) {
            instituteListContainer.innerHTML = '<p>기관 정보를 불러오는 데 실패했습니다.</p>';
        }
    }
});
