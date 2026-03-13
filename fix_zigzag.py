import re

path = r'c:\\Users\\Laptop store lhr\\Desktop\\SEOWEBSITE\\DesignX_Project\\index.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the universal responsive block to specifically handle zig-zag cards better
# We want the number on the left and card on the right for ALL steps on mobile.

new_zigzag_css = """
        /* Zigzag Responsive Fix */
        .process-timeline::before { display: none !important; }
        .zig-step { 
            display: flex !important; 
            flex-direction: row !important; 
            gap: 15px !important; 
            align-items: flex-start !important;
            margin-bottom: 30px !important;
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

# Find the end of the media query in the universal block and inject/replace
if '/* === UNIVERSAL RESPONSIVE BLOCK === */' in content:
    # Target the zig-step part specifically or replace the whole block
    # Let's just update the block
    content = re.sub(r'\.zig-step \{ grid-template-columns: 60px 1fr !important; gap: 10px !important; \}', new_zigzag_css.strip(), content)
    content = re.sub(r'\.zig-empty \{ display: none !important; \}', '', content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated zigzag responsiveness in index.html")
