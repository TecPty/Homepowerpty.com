import re, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base = r"c:\Users\HP 15\Homepowerpty.com"

# Get real folder names that actually exist
real_folders = set(os.listdir(os.path.join(base, "productos")))

# Find all HTML files sitewide
html_files = []
for root, dirs, files in os.walk(base):
    if '.git' in root or '.gemini' in root:
        continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

total_fixes = 0
for html_path in html_files:
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # Find all referencias to productos/FOLDER/ and validate against real folders
    def fix_folder_ref(m):
        folder = m.group(1)
        rest = m.group(2)
        # Check if folder exists
        if folder in real_folders:
            return m.group(0)  # Already correct
        # Try to find the correct folder: strip duplicate suffix
        # e.g., sandwichera-clasica-SJ-22-SJ-22 -> sandwichera-clasica-SJ-22
        # Pattern: if folder ends with -XYZ-XYZ, try -XYZ
        corrected = re.sub(r'-([A-Z0-9\-]+)-\1$', r'-\1', folder)
        if corrected in real_folders:
            return f"productos/{corrected}/{rest}"
        # Also try the reverse: remove last suffix entirely
        parts = folder.rsplit('-', 1)
        if len(parts) == 2 and parts[0] in real_folders:
            return f"productos/{parts[0]}/{rest}"
        return m.group(0)  # Can't fix, leave as-is

    content = re.sub(r'productos/([^/"\']+)/([^"\']*)', fix_folder_ref, content)

    if content != original:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        # Count changes
        changes = sum(1 for a, b in zip(original.split('\n'), content.split('\n')) if a != b)
        total_fixes += changes
        print(f"Fixed: {os.path.relpath(html_path, base)} ({changes} lines changed)")

print(f"\nTotal fixes: {total_fixes}")
