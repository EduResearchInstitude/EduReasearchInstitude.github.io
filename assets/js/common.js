document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    const isInPagesFolder = path.includes('/pages/');
    
    function loadHTML(elementId, filePath) {
        // 현재 페이지 위치에 따라 경로 조정
        const basePath = isInPagesFolder ? '../includes/' : 'includes/';
        
        fetch(basePath + filePath)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            })
            .then(data => {
                document.getElementById(elementId).innerHTML = data;
                
                // 네비게이션 링크 경로 조정
                if (elementId === 'nav-placeholder') {
                    const navLinks = document.querySelectorAll('#nav-placeholder nav a');
                    
                    navLinks.forEach(link => {
                        // 현재 페이지가 pages 폴더 내에 있는 경우
                        if (isInPagesFolder) {
                            if (link.classList.contains('home-link') || 
                                link.classList.contains('search-link')) {
                                // 홈, 검색 링크는 한 단계 위로 올라가야 함
                                link.setAttribute('href', '../' + link.getAttribute('href'));
                            } else {
                                // 나머지 링크는 pages/ 접두어 제거
                                let href = link.getAttribute('href');
                                if (href.startsWith('pages/')) {
                                    link.setAttribute('href', href.substring(6));
                                }
                            }
                        }
                    });
                }
            })
            .catch(error => {
                console.error(`Error loading ${filePath}:`, error);
                document.getElementById(elementId).innerHTML = `<p>메뉴를 불러오는 중 오류가 발생했습니다.</p>`;
            });
    }

    loadHTML('header-placeholder', 'header.html');
    loadHTML('nav-placeholder', 'nav.html');
    loadHTML('footer-placeholder', 'footer.html');
});
