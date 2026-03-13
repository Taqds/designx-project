import os
import re

def fix_content(content):
    new_zigzag_css = """
        /* Zigzag Responsive Fix */
        .process-timeline::before { display: none !important; }
        .zig-step { 
            display: flex !important; 
            flex-direction: row !important; 
            gap: 15px !important; 
            align-items: flex-start !important;
            margin-bottom: 30px !important;
            text-align: left !important;
        }
        .zig-num-wrap { 
            width: 50px !important; 
            min-width: 50px !important; 
            order: 1 !important; 
            padding-top: 5px !important;
            display: flex !important;
            justify-content: center !important;
        }
        .zig-card { 
            width: 100% !important; 
            order: 2 !important; 
            padding: 20px !important;
        }
        .zig-empty { display: none !important; }
        .zig-num {
            width: 40px !important;
            height: 40px !important;
            font-size: 0.85rem !important;
        }
    """

    if '/* === UNIVERSAL RESPONSIVE BLOCK === */' in content:
        # Check if the zig-step fix is already clean
        if '/* Zigzag Responsive Fix */' not in content:
            # Replace the old grid-based one or inject it
            content = re.sub(r'\.zig-step \{ grid-template-columns: 60px 1fr !important; gap: 10px !important; \}', new_zigzag_css.strip(), content)
            # Support the other variant if it exists
            content = re.sub(r'\.zig-step \{ grid-template-columns: 1fr !important; gap: 30px !important; \}', new_zigzag_css.strip(), content)
        else:
            # Update it
            content = re.sub(r'/\* Zigzag Responsive Fix \*/.*?\.zig-num \{.*?\}', new_zigzag_css.strip(), content, flags=re.DOTALL)

    return content

pages = [f for f in os.listdir(r'c:\\Users\\Laptop store lhr\\Desktop\\SEOWEBSITE\\DesignX_Project') if f.endswith('.html')]
base_path = r'c:\\Users\\Laptop store lhr\\Desktop\\SEOWEBSITE\\DesignX_Project'

for page in pages:
    path = os.path.join(base_path, page)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = fix_content(content)
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed zigzag in {page}")

