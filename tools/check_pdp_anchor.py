import os, glob, re

files = glob.glob('productos/**/index.html', recursive=True)
without = [f for f in files if 'pdp-trust-bar' not in open(f, encoding='utf-8').read()]

sample = without[0]
content = open(sample, encoding='utf-8').read()
sections = re.findall(r'<section class="([^"]+)"', content)
print(f"File: {sample}")
print(f"Last sections: {sections[-5:]}")

# Check if pdp-cta-band or footer are present
print(f"Has pdp-cta-band: {'pdp-cta-band' in content}")
print(f"Has pdp-gallery-strip: {'pdp-gallery-strip' in content}")
print(f"Has pdp-below: {'pdp-below' in content}")
