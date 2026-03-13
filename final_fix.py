import os
import re

def fix_final(content):
    # 1. Correct the broken Nav
    correct_links = """
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
        </ul>"""
    
    new_nav = f"""
    <nav>
        <div class="nav-logo">DesignX</div>
        {correct_links}
        <div class="nav-actions">
            <a href="index.html#contact" class="nav-cta">Start Project ↗</a>
            <div class="menu-toggle" id="mobile-menu">
                <i class="fas fa-bars"></i>
            </div>
        </div>
    </nav>"""
    
    content = re.sub(r'<nav>.*?</nav>', new_nav, content, flags=re.DOTALL)

    # 2. Fix Grid Responsiveness
    content = re.sub(r'grid-template-columns:\s*1fr\s*1fr;', 'grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));', content)

    # 3. Ensure the dropdown mobile logic is robust
    # Make sure we don't have multiple copies of the JS
    if 'Universal Navigation Script' in content:
        # It's already there from the previous run
        pass
    
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
        
        new_content = fix_final(content)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Finalized {page}")
