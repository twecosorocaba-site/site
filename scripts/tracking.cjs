/* Rastreamento TW&CO: injeta o GTM e o aviso de clique no WhatsApp em todo HTML de public/.
   Só acrescenta um bloco antes de </head>. Não altera nada visível nem o <body>. */
'use strict';
const fs = require('fs');
const path = require('path');

const GTM_ID = 'GTM-WPSCGHLJ';
const MARK = '<!-- twco-tracking -->';

// Cada clique (esquerdo, Ctrl/Cmd+clique, toque, Enter ou botão do meio) num link do WhatsApp
// gera exatamente um evento whatsapp_click. Clique direito não conta. A URL com o texto da
// mensagem nunca é enviada: o diagnóstico pode conter o que o cliente digitou.
const LISTENER = `window.dataLayer=window.dataLayer||[];(function(){var RE=/^(https?:\\/\\/(wa\\.me|api\\.whatsapp\\.com|web\\.whatsapp\\.com)\\/|whatsapp:)/i;function local(a){if(a.id)return a.id;if(a.closest('header'))return'cabecalho';if(a.closest('footer'))return'rodape';var s=a.closest('section[id]');return s?s.id:'pagina';}function h(e){if(e.type==='click'?e.button!==0:e.button!==1)return;var a=e.target&&e.target.closest?e.target.closest('a[href]'):null;if(!a||!RE.test(a.href))return;window.dataLayer.push({event:'whatsapp_click',cta_local:local(a)});}document.addEventListener('click',h,true);document.addEventListener('auxclick',h,true);})();`;

const GTM = `(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','${GTM_ID}');`;

const SNIPPET = `${MARK}<script>${LISTENER}</script><script>${GTM}</script>${MARK}`;

function inject(html, file) {
  if (html.includes(MARK)) throw new Error(`rastreamento já injetado em ${file}`);
  const n = html.split('</head>').length - 1;
  if (n !== 1) throw new Error(`esperado 1 </head> em ${file}, achei ${n}`);
  return html.replace('</head>', () => SNIPPET + '</head>');
}

function htmlFiles(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) return htmlFiles(p);
    return e.name.endsWith('.html') ? [p] : [];
  });
}

function main() {
  const dir = path.resolve(process.env.TWCO_PUBLIC_DIR || 'public');
  const files = htmlFiles(dir);
  if (files.length === 0) throw new Error(`nenhum HTML em ${dir}`);
  for (const f of files) fs.writeFileSync(f, inject(fs.readFileSync(f, 'utf8'), f), 'utf8');
  console.log(`TW&CO rastreamento: ${GTM_ID} em ${files.length} páginas.`);
}

module.exports = { inject, SNIPPET, MARK, GTM_ID };
if (require.main === module) main();
