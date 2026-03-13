import os
import re

def fix_header(content):
    # 1. Ensure font-awesome is present
    if 'font-awesome' not in content:
        content = content.replace('</head>', '    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">\n</head>')

    # 2. Update/Inject Navigation Styling
    nav_style = """
        /* Modern Navigation Styling */
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
            background: rgba(13, 13, 26, 0.88);
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
            font-size: .9rem;
            font-weight: 500;
            transition: color .3s;
        }
        .nav-links a:hover { color: #6C63FF; }
        .nav-actions { display: flex; align-items: center; gap: 15px; }
        .nav-cta {
            background: linear-gradient(135deg, #6C63FF 0%, #FF6584 100%);
            color: #fff;
            padding: 8px 20px;
            border-radius: 50px;
            font-weight: 600;
            text-decoration: none;
            font-size: .85rem;
            transition: transform .2s;
        }
        .nav-cta:hover { transform: translateY(-2px); }
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
                display: flex; /* Override display: none if present */
            }
            .nav-links.active { left: 0; }
            .nav-links li { width: 100%; text-align: center; }
            .nav-links a { font-size: 1.1rem; padding: 10px; display: block; }
            .nav-cta { display: none; }
            
            .dropdown-menu {
                position: static !important;
                width: 100% !important;
                background: transparent !important;
                border: none !important;
                box-shadow: none !important;
                padding-left: 20px !important;
                display: none;
                opacity: 1 !important;
                transform: none !important;
            }
            .dropdown.active .dropdown-menu { display: flex; }
            .dropdown a i { transition: transform 0.3s; }
            .dropdown.active a i { transform: rotate(180deg); }
        }
        
        /* Dropdown Desktop Support */
        .dropdown { position: relative; }
        .dropdown:hover .dropdown-menu { display: flex; }
        .dropdown-menu {
            display: none;
            position: absolute;
            top: 100%;
            left: 0;
            background: rgba(13, 13, 26, 0.95);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(108, 99, 255, 0.2);
            border-radius: 12px;
            padding: 15px;
            min-width: 220px;
            list-style: none;
            flex-direction: column;
            gap: 10px;
            z-index: 1001;
        }
        .dropdown-menu a { color: #94A3B8 !important; }
        .dropdown-menu a:hover { color: #6C63FF !important; }
    """

    # Replace existing nav-related styles
    # We'll just append it to the end of the first <style> block or prepend it
    content = content.replace('</style>', nav_style + '\n    </style>', 1)

    # 3. Fix Hero Heading clamp minimum
    content = re.sub(r'font-size:\s*clamp\(2\.2rem', 'font-size: clamp(1.8rem', content)

    # 4. Inject Mobile Toggle into <nav>
    if 'id="mobile-menu"' not in content:
        nav_pattern = r'(<nav>.*?)(\s*</nav>)'
        def nav_sub(m):
            nav_inner = m.group(1)
            # Find the end of links or actions
            if '<div class="nav-actions">' in nav_inner:
                nav_inner = nav_inner.replace('</div>', '    <div class="menu-toggle" id="mobile-menu"><i class="fas fa-bars"></i></div>\n        </div>', 1)
            else:
                nav_inner += '    <div class="nav-actions"><a href="#contact" class="nav-cta">Get Started</a><div class="menu-toggle" id="mobile-menu"><i class="fas fa-bars"></i></div></div>'
            return nav_inner + m.group(2)
        
        # This is a bit risky, let's just manually fix the nav if it doesn't match
        # But for this task, I'll assume they have a <nav>...</nav> block.

    # 5. Inject JS
    js_code = """
    <script>
        // Universal Mobile Menu Logic
        const mobileMenu = document.getElementById('mobile-menu');
        const navLinks = document.querySelector('.nav-links');
        
        if (mobileMenu && navLinks) {
            mobileMenu.addEventListener('click', () => {
                navLinks.classList.toggle('active');
                const icon = mobileMenu.querySelector('i');
                icon.classList.toggle('fa-bars');
                icon.classList.toggle('fa-times');
            });
            
            navLinks.querySelectorAll('a').forEach(link => {
                link.addEventListener('click', (e) => {
                    const dropdown = link.parentElement.classList.contains('dropdown');
                    if (dropdown && window.innerWidth <= 900) {
                        e.preventDefault();
                        link.parentElement.classList.toggle('active');
                    } else {
                        navLinks.classList.remove('active');
                        const icon = mobileMenu.querySelector('i');
                        icon.classList.add('fa-bars');
                        icon.classList.remove('fa-times');
                    }
                });
            });
        }
    </script>
    """
    if 'mobile-menu' not in content:
        # If the page doesn't have the elements, this won't do much, but it's safe.
        pass
    
    # Check if a similar script already exists and replace it or append
    if 'Universal Mobile Menu Logic' not in content:
        content = content.replace('</body>', js_code + '\n</body>')
    
    return content

# List of files to process
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
        
        # Specifically fix the nav structure if it's missing the actions/toggle
        if 'menu-toggle' not in content:
            # Injecting it before </nav>
            content = content.replace('</nav>', '    <div class="nav-actions"><a href="#contact" class="nav-cta">Get Started</a><div class="menu-toggle" id="mobile-menu"><i class="fas fa-bars"></i></div></div>\n    </nav>')

        new_content = fix_header(content)
        
        # Specifically fix the "Solutions" section in index.html or pages that have it
        if page == 'index.html':
            # Fix the .width bug more definitively
            new_content = new_content.replace('.width { width: 1200px !important; margin: 0 auto; }', '.width { width: 100% !important; max-width: 1200px; margin: 0 auto; }')
            # Reduce minmax for services tab panel
            new_content = new_content.replace('minmax(300px, 1fr)', 'minmax(280px, 1fr)')

        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {page}")

