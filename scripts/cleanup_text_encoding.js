"use strict";
// Lightweight fixer: remove � (U+FFFD) and common mojibake (Ã¡ Ã© Ã­ Ã³ Ãº Ã± …)
document.addEventListener("DOMContentLoaded", () => {
  const replacements = [
    [/\uFFFD/g, ""], // remove replacement chars
    [/Ã¡/g, "á"], [/Ã©/g, "é"], [/Ã­/g, "í"], [/Ã³/g, "ó"], [/Ãº/g, "ú"],
    [/Ã±/g, "ñ"], [/Ã�/g, "Á"], [/Ã‰/g, "É"], [/Ã�/g, "Í"], [/Ã“/g, "Ó"], [/Ãš/g, "Ú"], [/Ã‘/g, "Ñ"],
    [/â/g, "’"], [/â/g, "–"], [/â/g, "—"], [/â¦/g, "…"]
  ];

  const normalize = (txt) => {
    if (!txt) return txt;
    let out = txt;
    for (const [re, rep] of replacements) out = out.replace(re, rep);
    return out;
  };

  // Update text nodes
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  nodes.forEach((n) => { n.nodeValue = normalize(n.nodeValue); });

  // Update common attributes
  const attrs = ["alt", "title", "placeholder", "aria-label", "value"];
  document.querySelectorAll("*").forEach((el) => {
    attrs.forEach((a) => {
      if (el.hasAttribute && el.hasAttribute(a)) {
        const v = el.getAttribute(a);
        const nv = normalize(v);
        if (nv !== v) el.setAttribute(a, nv);
      }
    });
  });
});
