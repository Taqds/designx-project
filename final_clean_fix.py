import os
import re

def clean_and_fix(content):
    # 1. Ensure font-awesome is present
    if 'font-awesome' not in content:
        content = content.replace('</head>', '    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">\n</head>')

    # 2. Remove ANY previous universal navigation blocks or duplicate responsive blocks
    # We look for the start and end of our typical blocks
    content = re.sub(r'/\* Universal Navigation.*?\*/.*?(\}\s*|\n\s*)</style>', '</style>', content, flags=re.DOTALL)
    # Also remove the specific broken snippets if any
    content = re.sub(r'\.nav-links \{\s*position: absolute;.*?\}', '', content, flags=re.DOTALL)
    content = re.sub(r'\.nav-links\.active \{ left: 0; \}', '', content)
    content = re.sub(r'\.nav-links li \{ width: 100%; text-align: center; \}', '', content)
    content = re.sub(r'\.nav-links a \{ font-size: 1.2rem; padding: 10px; display: block; \}', '', content)
    content = re.sub(r'\.nav-cta \{ display: none; \}', '', content)

    # 3. New Clean Responsive Block
    clean_style = """
    /* === UNIVERSAL RESPONSIVE BLOCK === */
    nav {
        position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
        padding: 0 5%; display: flex; justify-content: space-between; align-items: center;
        background: rgba(13, 13, 26, 0.95); backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(108, 99, 255, 0.15); height: 70px;
    }
    .nav-logo {
        font-size: 1.5rem; font-weight: 900;
        background: linear-gradient(135deg, #6C63FF 0%, #FF6584 100%);
        -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
    }
    .nav-links { display: flex; gap: 25px; list-style: none; align-items: center; }
    .nav-links a { color: #94A3B8; text-decoration: none; font-size: .95rem; font-weight: 500; transition: color .3s; }
    .nav-links a:hover { color: #6C63FF; }
    .nav-actions { display: flex; align-items: center; gap: 15px; }
    .nav-cta {
        background: linear-gradient(135deg, #6C63FF 0%, #FF6584 100%);
        color: #fff; padding: 10px 24px; border-radius: 50px; font-weight: 600;
        text-decoration: none; font-size: .9rem; transition: transform .2s;
    }
    .nav-cta:hover { transform: translateY(-3px); }
    .menu-toggle { display: none; color: #fff; font-size: 1.5rem; cursor: pointer; }

    .dropdown { position: relative; }
    .dropdown:hover .dropdown-menu { display: flex; }
    .dropdown-menu {
        display: none; position: absolute; top: 100%; left: 0;
        background: rgba(13, 13, 26, 0.95); backdrop-filter: blur(10px);
        border: 1px solid rgba(108, 99, 255, 0.2); border-radius: 12px;
        padding: 15px; min-width: 220px; list-style: none; flex-direction: column; gap: 10px; z-index: 1001;
    }
    .dropdown-menu a { color: #94A3B8 !important; }
    .dropdown-menu a:hover { color: #6C63FF !important; }

    @media (max-width: 900px) {
        .menu-toggle { display: block; }
        .nav-links {
            position: absolute; top: 70px; left: -100%; width: 100%; height: calc(100vh - 70px);
            background: rgba(13, 13, 26, 0.98); backdrop-filter: blur(20px);
            flex-direction: column; justify-content: flex-start; align-items: center;
            padding: 40px 20px; transition: left 0.4s ease; gap: 20px; z-index: 999; overflow-y: auto;
            display: flex !important;
        }
        .nav-links.active { left: 0; }
        .nav-links li { width: 100%; text-align: center; }
        .nav-links a { font-size: 1.2rem; padding: 10px; display: block; }
        .nav-actions .nav-cta { display: none; }
        
        .dropdown-menu {
            position: static !important; width: 100% !important; background: transparent !important;
            border: none !important; box-shadow: none !important; padding-left: 20px !important;
            display: none; opacity: 1 !important; visibility: visible !important; transform: none !important;
        }
        .dropdown.active .dropdown-menu { display: flex; }
        .dropdown a i { transition: transform 0.3s; }
        .dropdown.active a i { transform: rotate(180deg); }

        .hero { padding-top: 120px !important; text-align: center; }
        .hero-content { max-width: 100% !important; margin: 0 auto; }
        .hero-visual { display: none !important; }
        .hero-stats { justify-content: center; gap: 20px !important; }
        .hero h1 { font-size: 2.2rem !important; }
        .hero-btns { justify-content: center; }
        
        .problems-grid { grid-template-columns: 1fr !important; }
        .about-section, .contact-container, .footer-top { grid-template-columns: 1fr !important; gap: 30px !important; }
        .insight-card { padding: 25px !important; }
        .zig-step { grid-template-columns: 60px 1fr !important; gap: 10px !important; }
        .zig-empty { display: none !important; }
    }
    /* === END UNIVERSAL BLOCK === */
    """
    content = content.replace('</style>', clean_style + '\n</style>')

    # 4. Correct Nav HTML
    correct_nav = """
    <nav>
        <div class="nav-logo">DesignX</div>
        <ul class="nav-links">
            <li><a href="index.html">Home</a></li>
            <li class="dropdown">
                <a href="services.html" style="display: flex; align-items: center; gap: 5px;">Our Services <i class="fas fa-caret-down"></i></a>
                <ul class="dropdown-menu">
                    <li><a href="web-design-company-miami.html">Web Design Miami</a></li>
                    <li><a href="website-development-services-fort-lauderdale.html">Web Design Fort Lauderdale</a></li>
                </ul>
            </li>
            <li><a href="process.html">Process</a></li>
            <li><a href="results.html">Results</a></li>
            <li><a href="blog.html">Blog</a></li>
            <li><a href="faq.html">FAQ</a></li>
        </ul>
        <div class="nav-actions">
            <a href="index.html#contact" class="nav-cta">Start Project ↗</a>
            <div class="menu-toggle" id="mobile-menu">
                <i class="fas fa-bars"></i>
            </div>
        </div>
    </nav>"""
    content = re.sub(r'<nav>.*?</nav>', correct_nav, content, flags=re.DOTALL)

    # 5. Clean up duplicate scripts
    content = re.sub(r'<script>\s*// Universal Navigation Script.*?</script>', '', content, flags=re.DOTALL)
    js_code = """
    <script>
        // === UNIVERSAL NAVIGATION SCRIPT ===
        (function() {
            const mobileMenu = document.getElementById('mobile-menu');
            const navLinks = document.querySelector('.nav-links');
            if (mobileMenu && navLinks) {
                mobileMenu.addEventListener('click', () => {
                    navLinks.classList.toggle('active');
                    const icon = mobileMenu.querySelector('i');
                    if (icon) { icon.classList.toggle('fa-bars'); icon.classList.toggle('fa-times'); }
                });
                navLinks.querySelectorAll('.dropdown > a').forEach(link => {
                    link.addEventListener('click', (e) => {
                        if (window.innerWidth <= 900) {
                            e.preventDefault();
                            link.parentElement.classList.toggle('active');
                        }
                    });
                });
                navLinks.querySelectorAll('a:not(.dropdown > a)').forEach(link => {
                    link.addEventListener('click', () => {
                        navLinks.classList.remove('active');
                        const icon = mobileMenu.querySelector('i');
                        if (icon) { icon.classList.add('fa-bars'); icon.classList.remove('fa-times'); }
                    });
                });
            }
        })();
    </script>
    """
    content = content.replace('</body>', js_code + '\n</body>')

    return content

pages = [f for f in os.listdir(r'c:\\Users\\Laptop store lhr\\Desktop\\SEOWEBSITE\\DesignX_Project') if f.endswith('.html')]
base_path = r'c:\\Users\\Laptop store lhr\\Desktop\\SEOWEBSITE\\DesignX_Project'

for page in pages:
    path = os.path.join(base_path, page)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = clean_and_fix(content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Cleaned & Fixed {page}")

