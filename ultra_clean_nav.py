import os
import re

def clean_and_fix_ultranav(content):
    # 1. Clean up CSS
    # Remove any previous Universal Responsive Blocks or Navigation styles
    # We'll look for anything between the head and the first section or similar
    # But safer to target specific tags we introduced or common nav patterns
    
    # Remove old universal blocks
    content = re.sub(r'/\* === UNIVERSAL RESPONSIVE BLOCK === \*/.*?/\* === END UNIVERSAL BLOCK === \*/', '', content, flags=re.DOTALL)
    content = re.sub(r'/\* Universal Navigation.*?\*/.*?(\}\s*|\n\s*)</style>', '</style>', content, flags=re.DOTALL)
    
    # Define the ONE TRUE CSS
    one_true_css = """
/* === ONE TRUE NAVIGATION & RESPONSIVE CSS === */
nav {
    position: fixed; top: 0; left: 0; right: 0; z-index: 2000;
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
.menu-toggle { display: none; color: #fff; font-size: 1.5rem; cursor: pointer; z-index: 2001; }

.dropdown { position: relative; }
.dropdown-menu {
    display: none; position: absolute; top: 100%; left: 0;
    background: rgba(13, 13, 26, 0.95); backdrop-filter: blur(10px);
    border: 1px solid rgba(108, 99, 255, 0.2); border-radius: 12px;
    padding: 15px; min-width: 220px; list-style: none; flex-direction: column; gap: 10px; z-index: 2002;
}
.dropdown:hover .dropdown-menu { display: flex; }
.dropdown-menu a { color: #94A3B8 !important; }
.dropdown-menu a:hover { color: #6C63FF !important; }

@media (max-width: 900px) {
    .menu-toggle { display: block; }
    .nav-links {
        position: fixed; top: 70px; left: -100%; width: 100%; height: calc(100vh - 70px);
        background: rgba(13, 13, 26, 0.98); backdrop-filter: blur(20px);
        flex-direction: column; justify-content: flex-start; align-items: center;
        padding: 40px 20px; transition: left 0.4s ease; gap: 20px; z-index: 1999; overflow-y: auto;
        display: none;
    }
    .nav-links.active { left: 0; display: flex; }
    .nav-links li { width: 100%; text-align: center; }
    .nav-links a { font-size: 1.2rem; padding: 15px; display: block; }
    .nav-actions .nav-cta { display: none; }
    
    .dropdown-menu {
        position: static !important; width: 100% !important; background: transparent !important;
        border: none !important; box-shadow: none !important; padding-left: 0 !important;
        display: none; opacity: 1 !important; visibility: visible !important; transform: none !important;
    }
    .dropdown.active .dropdown-menu { display: flex; }
    .dropdown a i { transition: transform 0.3s; }
    .dropdown.active a i { transform: rotate(180deg); }

    /* Zigzag Section Mobile Fix */
    .process-timeline::before { display: none !important; }
    .zig-step { 
        display: flex !important; flex-direction: row !important; gap: 15px !important; 
        align-items: flex-start !important; margin-bottom: 30px !important; text-align: left !important;
    }
    .zig-num-wrap { 
        width: 50px !important; min-width: 50px !important; order: 1 !important; 
        padding-top: 5px !important; display: flex !important; justify-content: center !important;
    }
    .zig-card { width: 100% !important; order: 2 !important; padding: 20px !important; }
    .zig-empty { display: none !important; }
    .zig-num { width: 40px !important; height: 40px !important; font-size: 0.85rem !important; }
    
    /* Other global responsive tweaks */
    .hero { padding-top: 100px !important; text-align: center; }
    .hero-content { max-width: 100% !important; }
    .hero-visual { display: none !important; }
    .problems-grid, .about-section, .contact-container, .footer-top { grid-template-columns: 1fr !important; }
}
/* === END ONE TRUE CSS === */
    """
    
    # Inject CSS
    existing_style = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    if existing_style:
        content = content.replace('</style>', one_true_css + '\n</style>', 1)
    else:
        content = content.replace('</head>', '<style>\n' + one_true_css + '\n</style>\n</head>', 1)

    # 2. Correct Nav HTML
    correct_nav_html = """
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
    content = re.sub(r'<nav>.*?</nav>', correct_nav_html, content, flags=re.DOTALL)

    # 3. Clean and Inject ONE TRUE JS
    # Remove all previous mobile menu scripts
    content = re.sub(r'<script>\s*// Universal Mobile Menu Logic.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script>\s*// === UNIVERSAL NAVIGATION SCRIPT ===.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script>\s*// === UNIVERSAL NAVIGATION SCRIPT ===.*?\}\)\(\);.*?</script>', '', content, flags=re.DOTALL)
    # Target common patterns of our previous scripts
    content = re.sub(r'const mobileMenu = document.getElementById\(\'mobile-menu\'\);.*?\.addEventListener\(\'click\',.*?\}\);', '', content, flags=re.DOTALL)

    one_true_js = """
<script>
    /* === ONE TRUE NAVIGATION JS === */
    (function() {
        const mobileMenu = document.getElementById('mobile-menu');
        const navLinks = document.querySelector('.nav-links');
        
        if (mobileMenu && navLinks) {
            mobileMenu.addEventListener('click', (e) => {
                e.stopPropagation();
                navLinks.classList.toggle('active');
                const icon = mobileMenu.querySelector('i');
                if (icon) {
                    icon.classList.toggle('fa-bars');
                    icon.classList.toggle('fa-times');
                }
            });
            
            navLinks.querySelectorAll('.dropdown > a').forEach(link => {
                link.addEventListener('click', (e) => {
                    if (window.innerWidth <= 900) {
                        e.preventDefault();
                        e.stopPropagation();
                        link.parentElement.classList.toggle('active');
                    }
                });
            });

            // Close menu when clicking outside
            document.addEventListener('click', (e) => {
                if (navLinks.classList.contains('active') && !navLinks.contains(e.target) && !mobileMenu.contains(e.target)) {
                    navLinks.classList.remove('active');
                    const icon = mobileMenu.querySelector('i');
                    if (icon) {
                        icon.classList.add('fa-bars');
                        icon.classList.remove('fa-times');
                    }
                }
            });

            // Close menu when clicking a non-dropdown link
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
    content = content.replace('</body>', one_true_js + '\n</body>')
    
    return content

pages = [f for f in os.listdir(r'c:\\Users\\Laptop store lhr\\Desktop\\SEOWEBSITE\\DesignX_Project') if f.endswith('.html')]
base_path = r'c:\\Users\\Laptop store lhr\\Desktop\\SEOWEBSITE\\DesignX_Project'

for page in pages:
    path = os.path.join(base_path, page)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = clean_and_fix_ultranav(content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Ultra Cleaned & Fixed {page}")
