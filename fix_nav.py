import os
import glob

directory = r'c:\Users\Laptop store lhr\Desktop\SEOWEBSITE\DesignX_Project'
html_files = glob.glob(os.path.join(directory, '*.html'))

# Remove sitemap from Nav if it was added incorrectly
nav_with_sitemap = '<li><a href="sitemap.html">Sitemap</a></li>'

for f in html_files:
    if 'sitemap.html' in f:
        continue
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Check if sitemap is in Nav (inside <ul class="nav-links">)
        # We target the one in Nav specifically if possible, or just remove it if it's there twice.
        # Given the previous context, it likely ended up in the nav.
        
        if nav_with_sitemap in content:
            # We only want to remove it from the Nav area, but it's hard to be surgical with simple replace.
            # However, the footer link uses a different structure usually (different indentation or context).
            # Let's check where it is.
            
            # If it's near FAQ in Nav:
            nav_faq_sitemap = '<li><a href="faq.html">FAQ</a></li>\n                    <li><a href="sitemap.html">Sitemap</a></li>'
            if nav_faq_sitemap in content:
                content = content.replace(nav_faq_sitemap, '<li><a href="faq.html">FAQ</a></li>')
            
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print(f"Failed to process {f}: {e}")
