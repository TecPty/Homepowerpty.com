// Remove stray replacement characters (�) that slipped due to encoding
document.addEventListener('DOMContentLoaded', () => {
  const decodeEntities = (str) => {
    const t = document.createElement('textarea');
    t.innerHTML = str;
    return t.value;
  };

  const replacements = [
    [/Ã¡/g, 'á'], [/Ã©/g, 'é'], [/Ã­/g, 'í'], [/Ã³/g, 'ó'], [/Ãº/ g, 'ú'], [/Ã±/g, 'ñ'],
    [/Ã/g, 'Á'], [/Ã‰/g, 'É'], [/ÃÍ/g, 'Í'], [/Ã“/g, 'Ó'], [/Ãš/g, 'Ú'], [/Ã‘/g, 'Ñ'],
    [/Ã‚Â°/g, '°'], [/Â°/g, '°'],
    [/ÃƒÂ¡/g, 'á'], [/ÃƒÂ©/g, 'é'], [/ÃƒÂ­/g, 'í'], [/ÃƒÂ³/g, 'ó'], [/ÃƒÂº/ g, 'ú'], [/ÃƒÂ±/g, 'ñ'],
    [/ElectrodomÃ©sticos/g, 'Electrodomésticos'],
    [/TecnologÃ­a/g, 'Tecnología'],
    [/PanamÃ¡/g, 'Panamá'],
    [/FunciÃ³n/g, 'Función'],
    [/garantÃ­a/g, 'garantía'],
    [/aÃ±o/g, 'año'],
    [/MÃ¡s/g, 'Más'],
    [/rÃ¡pido/g, 'rápido'],
    [/TelÃ©fono/g, 'Teléfono'],
    [/LogÃ­stica/g, 'Logística'],
    [/AdministraciÃ³n/g, 'Administración'],
    [/PosiciÃ³n/g, 'Posición'],
    [/AplicaciÃ³n/g, 'Aplicación'],
    [/PresiÃ³n/g, 'Presión'],
    [/CampeÃ³n/g, 'Campeón'],
    [/TitÃ¡n/g, 'Titán'],
    [/AlmacÃ©n/g, 'Almacén'],
    [/QuemaÃ±ores/g, 'Quemadores'],
    [/giraÃ±orio/g, 'giratorio'],
    [/ApagaÃ±o/g, 'Apagado'],
    [/vaÃ±or/g, 'vapor'],
    [/DepÃ³sito/g, 'Depósito'],
    [/piezoelÃ©ctrico/g, 'piezoeléctrico'],
    [/VÃ¡lvulas/g, 'Válvulas'],
    [/vÃ¡lvula/g, 'válvula'],
    [/SÃ­guenos/g, 'Síguenos']
  ];

  const normalize = (txt) => {
    if (!txt) return txt;
    let out = decodeEntities(txt).replace(/\uFFFD/g, '');
    for (const [re, rep] of replacements) out = out.replace(re, rep);
    return out;
  };

  // Fix text nodes
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  nodes.forEach(n => { n.nodeValue = normalize(n.nodeValue); });

  // Fix common attributes
  const attrTargets = ['alt', 'title', 'placeholder', 'aria-label', 'value'];
  document.querySelectorAll('*').forEach(el => {
    attrTargets.forEach(attr => {
      if (el.hasAttribute && el.hasAttribute(attr)) {
        const v = el.getAttribute(attr);
        const nv = normalize(v);
        if (nv !== v) el.setAttribute(attr, nv);
      }
    });
  });
});
