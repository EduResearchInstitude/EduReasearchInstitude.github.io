document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    const root = path.includes('/pages/') ? '../' : ''; // pages 폴더에 있으면 상대 경로 조정

    function loadHTML(elementId, filePath) {
        fetch(root + 'includes/' + filePath) // '_includes'를 'includes'로 변경
            .then(response => response.text())
            .then(data => {
                document.getElementById(elementId).innerHTML = data;
                // 네비게이션 링크 경로 수정 (필요한 경우)
                if (elementId === 'nav-placeholder') {
                    const navLinks = document.querySelectorAll('#nav-placeholder nav a');
                    navLinks.forEach(link => {
                        let originalHref = link.getAttribute('href');
                        if (originalHref && originalHref.startsWith('pages/')) {
                            link.setAttribute('href', root + originalHref);
                        } else if (originalHref && originalHref === 'index.html' && root) {
                            link.setAttribute('href', root + originalHref);
                        } else if (originalHref && originalHref === 'search.html' && root) {
                            link.setAttribute('href', root + originalHref);
                        }
                    });
                }
            })
            .catch(error => console.error('Error loading HTML:', error));
    }

    loadHTML('header-placeholder', 'header.html');
    loadHTML('nav-placeholder', 'nav.html');
    loadHTML('footer-placeholder', 'footer.html');
});
