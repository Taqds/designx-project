import os
import glob

directory = r'c:\Users\Laptop store lhr\Desktop\SEOWEBSITE\DesignX_Project'
html_files = glob.glob(os.path.join(directory, '*.html'))

# 1. Update Navigation Dropdown to include both Miami and Fort Lauderdale
nav_old_dropdown = '''<ul class="dropdown-menu">
                    <li><a href="web-design-company-miami.html">Web Design Miami</a></li>
                </ul>'''
nav_new_dropdown = '''<ul class="dropdown-menu">
                    <li><a href="web-design-company-miami.html">Web Design Miami</a></li>
                    <li><a href="website-development-services-fort-lauderdale.html">Web Design Fort Lauderdale</a></li>
                </ul>'''

# 2. Update Footer to include Sitemap
footer_old = '<li><a href="faq.html">FAQ</a></li>'
footer_new = '''<li><a href="faq.html">FAQ</a></li>
                    <li><a href="sitemap.html">Sitemap</a></li>'''

for f in html_files:
    if 'sitemap.html' in f:
        continue
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        updated = False
        
        # Update Nav Dropdown
        if nav_old_dropdown in content:
            content = content.replace(nav_old_dropdown, nav_new_dropdown)
            updated = True
            
        # Update Footer
        if footer_old in content and 'sitemap.html' not in content:
            content = content.replace(footer_old, footer_new)
            updated = True
                
        if updated:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f'Updated {f}')
    except Exception as e:
        print(f"Failed to process {f}: {e}")
