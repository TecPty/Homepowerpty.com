import re

path = r'c:\Users\HP 15\Homepowerpty.com\styles\luxury.css'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the accent variable definition
text = re.sub(r'--color-accent:\s*#[a-fA-F0-9]+;', '--color-accent: #D6B55E;', text)

# Replace hardcoded #CFB53B with var(--color-accent)
text = re.sub(r'#CFB53B', 'var(--color-accent)', text, flags=re.IGNORECASE)

# Replace legacy #C9A84C that might not be variables
text = re.sub(r'#C9A84C', 'var(--color-accent)', text, flags=re.IGNORECASE)
text = re.sub(r'#c9a84c', 'var(--color-accent)', text, flags=re.IGNORECASE)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print('Color replaced successfully.')
