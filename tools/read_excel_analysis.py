import pandas as pd

df = pd.read_excel('EXCEL DE PRODUCTOS PARA MKT.xlsx', header=1)
df = df.dropna(axis=1, how='all')
df = df.dropna(subset=['Numero'])
df = df.rename(columns={
    'Codigo': 'CODIGO_BARRA',
    'Numero': 'SKU',
    'Descripcion': 'DESC',
    'Piezas x bulto': 'BULTO',
    'Unnamed: 5': 'NOTA'
})
df = df[['CODIGO_BARRA', 'SKU', 'DESC', 'BULTO', 'NOTA']].copy()
df['SKU'] = df['SKU'].astype(str).str.strip()
df['CODIGO_BARRA'] = df['CODIGO_BARRA'].astype(str).str.strip().str.replace('.0', '', regex=False)

print(f"Total: {len(df)} productos")
print()
for _, r in df.iterrows():
    desc_lines = str(r['DESC']).split('\n') if pd.notna(r['DESC']) else ['']
    desc_first = desc_lines[0].strip()[:65]
    nota = f" [{r['NOTA']}]" if pd.notna(r['NOTA']) and str(r['NOTA']).strip() not in ['nan', ''] else ''
    print(f"  SKU: {r['SKU']:15s} | BARCODE: {r['CODIGO_BARRA']:15s} | {desc_first}{nota}")
