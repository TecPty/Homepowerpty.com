const fs = require('fs');
const path = require('path');

const relatedBlock = `
            <section class="pdp-related">
                <div class="container">
                    <p class="section-eyebrow">TAMBIÉN TE PUEDE INTERESAR</p>
                    <h2 class="pdp-related-title">Productos similares</h2>
                    <ul class="pdp-related-grid">
                        <li class="pdp-related-card">
                            <a href="../hp-021/" class="pdp-related-img-wrap">
                                <img src="../hp-021/img/PRODUCTO_PRINCIPAL.webp" alt="Batidora de Mano 7 Velocidades" loading="lazy">
                            </a>
                            <div class="pdp-related-info">
                                <span class="pdp-related-mod">HP-021</span>
                                <h3 class="pdp-related-name"><a href="../hp-021/">Batidora de Mano 7 Velocidades</a></h3>
                                <a href="../hp-021/" class="pdp-related-cta">Ver producto</a>
                            </div>
                        </li>
                    </ul>
                </div>
            </section>`;

const files = [
    'productos/batidoras/hp-024/index.html',
    'productos/batidoras/hp-044/index.html',
    'productos/batidoras/hp-045/index.html'
];

files.forEach(file => {
    const filePath = path.join(process.cwd(), file);
    if (!fs.existsSync(filePath)) {
        console.log(`File not found: ${file}`);
        return;
    }

    let content = fs.readFileSync(filePath, 'utf8');
    
    if (content.includes('hp-021')) {
        console.log(`HP-021 already present in ${file}`);
        return;
    }

    // Insertar antes del cierre de </main>
    if (content.includes('</main>')) {
        content = content.replace('</main>', relatedBlock + '\n        </main>');
        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`Updated ${file} by inserting section before </main>`);
    } else {
        console.log(`Could not find </main> tag in ${file}`);
    }
});
