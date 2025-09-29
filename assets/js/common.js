document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    // root 경로 설정: /pages/ 경로에 있을 경우 ../ 가 필요함
    // GitHub Pages는 보통 리포지토리 이름으로 시작하므로, 정확한 root path를 계산해야 함
    // 여기서는 페이지 URL의 첫 경로가 리포지토리 이름과 일치한다고 가정하고,
    // 그 뒤에 /pages/ 가 붙어있는지 확인하여 상대경로를 결정합니다.
    let root = '';
    if (path.includes('/pages/')) {
        // 예를 들어 /eduresearchinstitude.github.io/pages/reports.html 인 경우 root는 ../
        root = '../';
    } else if (path.split('/').filter(p => p).length > 1 && path.includes('/eduresearchinstitude.github.io/')) {
        // 루트가 아니라면 (예: /eduresearchinstitude.github.io/search.html)
        root = './'; // 현재 폴더 (GitHub Pages 루트 기준)
    }


    function loadHTML(elementId, filePath) {
        fetch(root + 'includes/' + filePath) // 'includes' 폴더에서 파일 로드
            .then(response => {
                if (!response.ok) { // 응답이 성공적이지 않으면 오류 처리
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            })
            .then(data => {
                const targetElement = document.getElementById(elementId);
                if (targetElement) {
                    targetElement.innerHTML = data;

                    // 네비게이션 링크 경로 수정 (로딩된 HTML 내의 링크)
                    if (elementId === 'nav-placeholder') {
                        const navLinks = targetElement.querySelectorAll('nav a');
                        navLinks.forEach(link => {
                            let originalHref = link.getAttribute('href');
                            if (originalHref) {
                                // GitHub Pages의 특성을 고려한 경로 조정
                                // 기본적으로 사이트 루트에서 상대경로로 작동하므로,
                                // 필요한 경우에만 root 변수를 앞에 추가합니다.
                                // 이 로직은 복잡해질 수 있으므로, 초기에는 단순하게 구성하는 것이 좋습니다.
                                // 현재 상태에서는 includes/nav.html의 링크가 site root를 기준으로 잘 작동하도록 하는 것이 목표입니다.
                                // 예를 들어, index.html의 href는 그대로 'index.html', pages/reports.html은 'pages/reports.html'
                                // 여기서는 추가적인 root 조정 없이, common.js가 파일을 불러온 후
                                // nav.html 내부의 링크는 해당 페이지의 상대경로로 간주하도록 두겠습니다.
                                // 나중에 복잡한 라우팅이 필요하면 이 부분을 더 자세히 조정해야 합니다.

                                // 현재 페이지가 pages 폴더 안에 있는지 확인
                                const isCurrentPageInPages = window.location.pathname.includes('/pages/');

                                // 불러온 nav의 링크가 /로 시작하지 않고 pages/ 또는 파일명인 경우
                                if (!originalHref.startsWith('/') && originalHref.includes('.html')) {
                                    // 현재 페이지가 pages 안에 있는데, 링크가 최상위 경로 파일(index.html, search.html)을 가리킨다면
                                    if (isCurrentPageInPages && (originalHref === 'index.html' || originalHref === 'search.html')) {
                                        link.setAttribute('href', '../' + originalHref);
                                    }
                                    // 현재 페이지가 pages 안에 있는데, 링크가 pages/ 안의 다른 파일을 가리킨다면
                                    else if (isCurrentPageInPages && originalHref.startsWith('pages/')) {
                                        // pages/contact.html -> contact.html로 수정되어야 함
                                        link.setAttribute('href', originalHref.replace('pages/', ''));
                                    }
                                    // 현재 페이지가 최상위에 있는데, 링크가 pages/ 안의 파일을 가리킨다면 그대로 유지
                                    // 현재 페이지가 최상위에 있는데, 링크가 최상위 파일인 경우 그대로 유지
                                }
                            }
                        });
                    }
                } else {
                    console.error(`Error: Element with ID '${elementId}' not found.`);
                }
            })
            .catch(error => console.error(`Error loading ${filePath}:`, error));
    }

    loadHTML('header-placeholder', 'header.html');
    loadHTML('nav-placeholder', 'nav.html');
    loadHTML('footer-placeholder', 'footer.html');
});
