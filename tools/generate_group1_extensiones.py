import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
BASE_TEMPLATE = ROOT / "productos" / "extensiones" / "hp-055" / "index.html"
DATA_FILE = ROOT / "productos" / "extensiones" / "_shared" / "group1-data.json"


def build_thumbs(images):
    rows = []
    for i, img in enumerate(images):
        label = "vista principal" if i == 0 else f"detalle {i}"
        alt = "Vista principal" if i == 0 else f"Detalle {i}"
        active = " active" if i == 0 else ""
        rows.append(
            """
                        <button class=\"pdp-thumb{active}\"
                                onclick=\"pdpSetImage('./img/{img}', this)\"
                                aria-label=\"Ver {label}\" role=\"listitem\">
                            <img src=\"./img/{img}\" alt=\"{alt}\">
                        </button>""".format(active=active, img=img, label=label, alt=alt).strip("\n")
        )
    return "\n".join(rows)


def build_strip(images):
    rows = []
    for i, img in enumerate(images):
        label = "vista principal" if i == 0 else f"detalle {i}"
        alt = "Vista principal" if i == 0 else f"Detalle {i}"
        rows.append(
            """
                        <div class=\"pdp-strip-item\" onclick=\"pdpOpenLightboxAt({idx})\" role=\"button\" tabindex=\"0\" aria-label=\"Ampliar {label}\">
                            <img src=\"./img/{img}\" alt=\"{alt}\" loading=\"lazy\">
                            <div class=\"pdp-strip-overlay\" aria-hidden=\"true\"><svg width=\"22\" height=\"22\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\" viewBox=\"0 0 24 24\"><circle cx=\"11\" cy=\"11\" r=\"8\"/><line x1=\"21\" y1=\"21\" x2=\"16.65\" y2=\"16.65\"/><line x1=\"11\" y1=\"8\" x2=\"11\" y2=\"14\"/><line x1=\"8\" y1=\"11\" x2=\"14\" y2=\"11\"/></svg></div>
                        </div>""".format(idx=i, label=label, img=img, alt=alt).strip("\n")
        )
    return "\n".join(rows)


def build_pdp_images(images):
    return "\n".join([f"            './img/{img}'," for img in images])


def build_specs(model, length):
    return """<tbody>
                                            <tr><td>Modelo</td><td>{model}</td></tr>
                                            <tr><td colspan=\"2\">1 Toma Polarizada</td></tr>
                                            <tr><td colspan=\"2\">{length}</td></tr>
                                            <tr><td colspan=\"2\">110V</td></tr>
                                            <tr><td colspan=\"2\">Uso Interior</td></tr>
                                        </tbody>""".format(model=model, length=length)


def build_related(current_slug, products):
    others = [p for p in products if p["slug"] != current_slug][:3]
    cards = []
    for p in others:
        cards.append(
            """
                        <li class=\"pdp-related-card\">
                            <a href=\"../{slug}/\" class=\"pdp-related-img-wrap\">
                                <img src=\"../{slug}/img/PRODUCTO_PRINCIPAL.webp\" alt=\"{name}\" loading=\"lazy\">
                            </a>
                            <div class=\"pdp-related-info\">
                                <span class=\"pdp-related-mod\">{model}</span>
                                <h3 class=\"pdp-related-name\"><a href=\"../{slug}/\">{name}</a></h3>
                                <a href=\"../{slug}/\" class=\"pdp-related-cta\">Ver producto</a>
                            </div>
                        </li>""".format(slug=p["slug"], name=p["name"], model=p["model"]).strip("\n")
        )
    return """            <section class=\"pdp-related\">
                <div class=\"container\">
                    <p class=\"section-eyebrow\">TAMBIÉN TE PUEDE INTERESAR</p>
                    <h2 class=\"pdp-related-title\">Productos similares</h2>
                    <ul class=\"pdp-related-grid\">
{cards}
                    </ul>
                </div>
            </section>""".format(cards="\n".join(cards))


def replace_once(text, pattern, repl):
    new_text, count = re.subn(pattern, repl, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"Pattern not found or duplicated: {pattern[:40]}")
    return new_text


def render_page(base_html, product, products):
    name = product["name"]
    model = product["model"]
    length = product["length"]
    images = product["images"]

    desc = f"{name} — Consulta disponibilidad y precios mayoristas en Home Power PTY, Panamá."
    wa_text = quote(f"Hola, me interesa el producto {name} {model}")
    wa_href = f"https://wa.me/50769838322?text={wa_text}"

    html = base_html
    html = replace_once(html, r"<title>.*?</title>", f"<title>{name} — HomePower PTY</title>")
    html = replace_once(html, r'<meta name="description" content=".*?">', f'<meta name="description" content="{desc}">')
    html = replace_once(html, r"<span class=\"crumb-current\">.*?</span>", f"<span class=\"crumb-current\">{name}</span>")
    html = replace_once(html, r"<img id=\"pdpMainImg\"\s+src=\"\.\/img\/.*?\"\s+alt=\".*?\">", f"<img id=\"pdpMainImg\"\n                             src=\"./img/{images[0]}\"\n                             alt=\"{name} — HomePower PTY\">")
    html = replace_once(html, r"<h1 class=\"pdp-name\">.*?</h1>", f"<h1 class=\"pdp-name\">{name}</h1>")
    html = replace_once(html, r"<p class=\"pdp-model\">.*?</p>", f"<p class=\"pdp-model\">{model}</p>")
    html = replace_once(html, r"<p class=\"pdp-short-desc\">.*?</p>", f"<p class=\"pdp-short-desc\">{desc}</p>")

    html = replace_once(
        html,
        r"<div class=\"pdp-spec-pills\">.*?</div>\s*</div>\s*<div class=\"pdp-cta-group\">",
        """<div class=\"pdp-spec-pills\">
                        <div class=\"pdp-spec-pill\"><span>1 Toma Polarizada</span></div>
                        <div class=\"pdp-spec-pill\"><span>{length}</span></div>
                        <div class=\"pdp-spec-pill\"><span>110V</span></div>
                        <div class=\"pdp-spec-pill\"><span>Uso Interior</span></div>
                    </div>

                    <div class=\"pdp-cta-group\">""".format(length=length)
    )

    html = re.sub(r'https://wa\.me/50769838322\?text=[^"\']+', wa_href, html)

    html = replace_once(
        html,
        r"<div class=\"pdp-thumbs\" role=\"list\" aria-label=\"[^\"]*\">.*?</div>\s*</div>\s*\n\s*<!-- RIGHT: INFO PANEL -->",
        """<div class=\"pdp-thumbs\" role=\"list\" aria-label=\"Imágenes del producto\">\n{thumbs}\n                    </div>
                </div>

                <!-- RIGHT: INFO PANEL -->""".format(thumbs=build_thumbs(images))
    )

    html = replace_once(
        html,
        r"<div class=\"pdp-gallery-strip-grid\">.*?</div>\s*</div>\s*</section>",
        """<div class=\"pdp-gallery-strip-grid\">\n{items}\n                    </div>
                </div>
            </section>""".format(items=build_strip(images))
    )

    html = replace_once(
        html,
        r"<tbody>.*?</tbody>",
        build_specs(model, length)
    )

    html = replace_once(
        html,
        r"const pdpImages = \[.*?\];",
        "const pdpImages = [\n{rows}\n        ];".format(rows=build_pdp_images(images))
    )

    html = replace_once(
        html,
        r"<section class=\"pdp-related\">.*?</section>",
        build_related(product["slug"], products)
    )

    return html


def main():
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    products = data["products"]
    base_html = BASE_TEMPLATE.read_text(encoding="utf-8")

    for p in products:
        out = ROOT / "productos" / "extensiones" / p["slug"] / "index.html"
        html = render_page(base_html, p, products)
        out.write_text(html, encoding="utf-8")
        print(f"Updated: {out}")


if __name__ == "__main__":
    main()

