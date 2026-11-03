'use strict';
// Rodar: node --test scripts/tracking.test.cjs
const test = require('node:test');
const assert = require('node:assert');
const vm = require('node:vm');
const { inject, SNIPPET, MARK, GTM_ID } = require('./tracking.cjs');

const PAGE = '<!DOCTYPE html><html><head><meta charset="utf-8"/><title>x $& $1</title></head><body><a href="https://wa.me/1?text=a">W</a></body></html>';

test('acrescenta só o bloco antes de </head>; o resto fica byte a byte igual', () => {
  const out = inject(PAGE, 't');
  assert.strictEqual(out.replace(SNIPPET, ''), PAGE);
  assert.strictEqual(out.split(MARK).length - 1, 2);
  assert.ok(out.includes(GTM_ID));
  assert.ok(out.indexOf(SNIPPET) < out.indexOf('</head>'));
});

test('falha alto se já injetado ou sem exatamente um </head>', () => {
  assert.throws(() => inject(inject(PAGE, 't'), 't'), /já injetado/);
  assert.throws(() => inject('<html><body></body></html>', 't'), /achei 0/);
  assert.throws(() => inject('</head></head>', 't'), /achei 2/);
});

// Executa o listener real com um DOM mínimo e conta os eventos.
function run() {
  const handlers = {};
  const ctx = { window: {}, document: { addEventListener: (t, fn, cap) => { assert.strictEqual(cap, true); handlers[t] = fn; } } };
  ctx.window = ctx;
  const listener = SNIPPET.match(/<script>(window\.dataLayer[\s\S]*?)<\/script>/)[1];
  vm.runInNewContext(listener, ctx);
  const link = (href, id = '', where = {}) => ({ href, id, closest: (sel) => where[sel] || null });
  const fire = (type, button, a) => { handlers[type]({ type, button, target: { closest: (s) => (s === 'a[href]' ? a : null) } }); };
  return { dl: () => JSON.parse(JSON.stringify(ctx.dataLayer)), fire, link };
}

test('cada clique no WhatsApp gera exatamente um whatsapp_click', () => {
  const { dl, fire, link } = run();
  const wa = link('https://wa.me/5515996638821?text=Ol%C3%A1', '', { 'section[id]': { id: 'contato' } });
  fire('click', 0, wa);          // clique normal, toque, Enter, Ctrl+clique
  fire('auxclick', 1, wa);       // botão do meio (nova aba)
  fire('auxclick', 2, wa);       // clique direito: não conta
  fire('click', 0, link('tel:+5515996638821'));             // telefone: não conta
  fire('click', 0, link('https://www.instagram.com/x/'));    // outro link: não conta
  fire('click', 0, link('https://api.whatsapp.com/send?phone=1', 'diagnosticWhatsApp'));
  const ev = dl().filter((x) => x.event === 'whatsapp_click');
  assert.deepStrictEqual(ev, [
    { event: 'whatsapp_click', cta_local: 'contato' },
    { event: 'whatsapp_click', cta_local: 'contato' },
    { event: 'whatsapp_click', cta_local: 'diagnosticWhatsApp' },
  ]);
});

test('local do botão: cabeçalho e rodapé; nunca envia a URL nem o texto', () => {
  const { dl, fire, link } = run();
  fire('click', 0, link('https://wa.me/1', '', { header: {} }));
  fire('click', 0, link('https://wa.me/1', '', { footer: {} }));
  fire('click', 0, link('https://wa.me/1'));
  assert.deepStrictEqual(dl().map((x) => x.cta_local), ['cabecalho', 'rodape', 'pagina']);
  assert.ok(dl().every((x) => Object.keys(x).join() === 'event,cta_local'));
});
