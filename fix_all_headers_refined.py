import os
import re

def fix_content(content, filename):
    # 1. Ensure font-awesome is present
    if 'font-awesome' not in content:
        content = content.replace('</head>', '    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">\n</head>')

    # 2. Universal Navigation Styling (Cleaned up)
    nav_style = """
        /* Universal Navigation Styling */
        nav {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            padding: 0 5%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(13, 13, 26, 0.9);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(108, 99, 255, 0.15);
            height: 70px;
        }
        .nav-logo {
            font-size: 1.5rem;
            font-weight: 900;
            background: linear-gradient(135deg, #6C63FF 0%, #FF6584 100%);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .nav-links {
            display: flex;
            gap: 25px;
            list-style: none;
            align-items: center;
        }
        .nav-links a {
            color: #94A3B8;
            text-decoration: none;
            font-size: .95rem;
            font-weight: 500;
            transition: color .3s;
        }
        .nav-links a:hover { color: #6C63FF; }
        .nav-actions { display: flex; align-items: center; gap: 15px; }
        .nav-cta {
            background: linear-gradient(135deg, #6C63FF 0%, #FF6584 100%);
            color: #fff;
            padding: 10px 24px;
            border-radius: 50px;
            font-weight: 600;
            text-decoration: none;
            font-size: .9rem;
            transition: transform .2s;
        }
        .nav-cta:hover { transform: translateY(-3px); }
        .menu-toggle { display: none; color: #fff; font-size: 1.5rem; cursor: pointer; }

        @media (max-width: 900px) {
            .menu-toggle { display: block; }
            .nav-links {
                position: absolute;
                top: 70px;
                left: -100%;
                width: 100%;
                height: calc(100vh - 70px);
                background: rgba(13, 13, 26, 0.98);
                backdrop-filter: blur(20px);
                flex-direction: column;
                justify-content: flex-start;
                align-items: center;
                padding: 40px 20px;
                transition: left 0.4s ease;
                gap: 20px;
                z-index: 999;
                overflow-y: auto;
                display: flex !important;
            }
            .nav-links.active { left: 0; }
            .nav-links li { width: 100%; text-align: center; }
            .nav-links a { font-size: 1.2rem; padding: 10px; display: block; }
            .nav-cta { display: none; }
            .nav-actions .nav-cta { display: none; } /* Hide any CTAs inside nav-actions on mobile */
            
            .dropdown-menu {
                position: static !important;
                width: 100% !important;
                background: transparent !important;
                border: none !important;
                box-shadow: none !important;
                padding-left: 20px !important;
                display: none;
                opacity: 1 !important;
                visibility: visible !important;
                transform: none !important;
            }
            .dropdown.active .dropdown-menu { display: flex; }
            .dropdown a i { transition: transform 0.3s; }
            .dropdown.active a i { transform: rotate(180deg); }
        }
    """

    # Replace existing nav-related styles (or the previous universal ones)
    if '/* Universal Navigation Styling */' in content:
        # Replace the whole block if multiple exists or just update the one
        content = re.sub(r'/\* Universal Navigation Styling \*/.*?@keyframes fadeInUp { from { opacity: 0; transform: translateY\(10px\); } to { opacity: 1; transform: translateY\(0\); } }', nav_style, content, flags=re.DOTALL)
    else:
        content = content.replace('</style>', nav_style + '\n    </style>', 1)

    # 3. Fix Grid Responsiveness (Problems grid)
    # Target grid-template-columns: 1fr 1fr; or repeat(auto-fit, minmax(..., 1fr))
    content = re.sub(r'grid-template-columns:\s*1fr\s*1fr;', 'grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));', content)
    content = re.sub(r'grid-template-columns:\s*repeat\(auto-fit,\s*minmax\(300px,\s*1fr\)\);', 'grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));', content)

    # 4. Hero Heading Responsiveness
    content = re.sub(r'font-size:\s*clamp\(2\.2rem', 'font-size: clamp(1.8rem', content)

    # 5. Fix HTML Navigation (Avoid duplicates)
    # We want a clean: <nav> <logo> <links> <actions><cta><toggle></actions> </nav>
    links_match = re.search(r'(<ul class="nav-links">.*?</ul>)', content, re.DOTALL)
    if links_match:
        links_html = links_match.group(1)
        # Reconstruct Nav
        new_nav = f"""
    <nav>
        <div class="nav-logo">DesignX</div>
        {links_html}
        <div class="nav-actions">
            <a href="index.html#contact" class="nav-cta">Start Project ↗</a>
            <div class="menu-toggle" id="mobile-menu">
                <i class="fas fa-bars"></i>
            </div>
        </div>
    </nav>"""
        # Replace the old nav block
        content = re.sub(r'<nav>.*?</nav>', new_nav, content, flags=re.DOTALL)

    # 6. Universal JS (Fixing dropdown toggles)
    js_code = """
    <script>
        // Universal Navigation Script
        (function() {
            const mobileMenu = document.getElementById('mobile-menu');
            const navLinks = document.querySelector('.nav-links');
            
            if (mobileMenu && navLinks) {
                mobileMenu.addEventListener('click', () => {
                    navLinks.classList.toggle('active');
                    const icon = mobileMenu.querySelector('i');
                    icon.classList.toggle('fa-bars');
                    icon.classList.toggle('fa-times');
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
                        if (icon) {
                            icon.classList.add('fa-bars');
                            icon.classList.remove('fa-times');
                        }
                    });
                });
            }
        })();
    </script>
    """
    if 'Universal Navigation Script' not in content:
        content = content.replace('</body>', js_code + '\n</body>')
    else:
        # Update it
        content = re.sub(r'<script>\s*// Universal Navigation Script.*?</script>', js_code, content, flags=re.DOTALL)

    return content

pages = [
    'index.html',
    'web-design-company-miami.html',
    'services.html',
    'process.html',
    'results.html',
    'blog.html',
    'faq.html',
    'reviews.html'
]

base_path = r'c:\\Users\\Laptop store lhr\\Desktop\\SEOWEBSITE\\DesignX_Project'

for page in pages:
    path = os.path.join(base_path, page)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = fix_content(content, page)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Refined {page}")

