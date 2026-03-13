import os
import glob

directory = r'c:\Users\Laptop store lhr\Desktop\SEOWEBSITE\DesignX_Project'
html_files = glob.glob(os.path.join(directory, '*.html'))

for f in html_files:
    if 'sitemap.html' in f: continue
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        if '<h5>Quick Links</h5>' in content and 'sitemap.html' not in content:
            parts = content.split('<h5>Quick Links</h5>')
            after_header = parts[1].split('</ul>', 1)
            ul_content = after_header[0]
            if '<li><a href="faq.html">FAQ</a></li>' in ul_content:
                 new_ul = ul_content.replace('<li><a href="faq.html">FAQ</a></li>', '<li><a href="faq.html">FAQ</a></li>\n                    <li><a href="sitemap.html">Sitemap</a></li>')
                 content = parts[0] + '<h5>Quick Links</h5>' + new_ul + '</ul>' + after_header[1]
                 with open(f, 'w', encoding='utf-8') as file:
                     file.write(content)
                 print(f'Updated footer in {f}')
    except Exception as e:
        print(f"Error in {f}: {e}")
