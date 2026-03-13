import os
import glob

directory = r'c:\Users\Laptop store lhr\Desktop\SEOWEBSITE\DesignX_Project'
html_files = glob.glob(os.path.join(directory, '*.html'))

nav_old = '<li><a href="services.html">Services</a></li>'
nav_new = '''<li class="dropdown" style="position: relative;">
                <a href="services.html" style="display: flex; align-items: center; gap: 5px;">Our Services <i class="fas fa-caret-down"></i></a>
                <ul class="dropdown-menu">
                    <li><a href="web-design-company-miami.html">Web Design Miami</a></li>
                </ul>
            </li>'''

style_old = '</style>'
style_new = '''
        .dropdown:hover .dropdown-menu { display: flex !important; animation: fadeInUp 0.3s ease; }
        .dropdown-menu { display: none; position: absolute; top: 100%; left: 0; background: rgba(13, 13, 26, 0.95); backdrop-filter: blur(20px); border: 1px solid rgba(108, 99, 255, 0.2); border-radius: 12px; padding: 15px; min-width: 220px; list-style: none; flex-direction: column; gap: 10px; z-index: 1001; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .dropdown-menu li { width: 100%; text-align: left !important; }
        .dropdown-menu a { color: var(--muted) !important; font-size: 0.9rem !important; transition: color 0.3s; display: block; padding: 5px 0; }
        .dropdown-menu a:hover { color: var(--primary) !important; }
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>'''

for f in html_files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        updated = False
        # Update navigation
        if nav_old in content:
            content = content.replace(nav_old, nav_new)
            updated = True
            
        # Add CSS if not already there
        if updated and '.dropdown-menu' not in content:
            content = content.replace(style_old, style_new)
                
        if updated:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f'Updated {f}')
    except Exception as e:
        print(f"Failed to process {f}: {e}")
