import os, re

pdps = ['ht-15', 'ht-15a', 'ht-18', 'ht-22a', 'ck-02-22', 'ck-02-24', 'wj-9008', 'wj-9009', 'jr-a101', 'jr-ld8', 'mm-931', 'mm-933', 'jd389', 'sj-22', 'sj-40']

for slug in pdps:
    for cat in os.listdir('productos'):
        path = os.path.join('productos', cat, slug, 'index.html')
        if os.path.exists(path):
            with open(path, encoding='utf-8') as f:
                content = f.read()
            m_title = re.search(r'<title>(.*?)</title>', content)
            m_h1 = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
            title = m_title.group(1).strip() if m_title else 'NO TITLE'
            h1 = re.sub('<[^>]+>', '', m_h1.group(1)).strip() if m_h1 else 'NO H1'
            print(f'{slug}: title="{title}" | h1="{h1}"')
