/* TW&CO — substitui APENAS os depoimentos exibidos; preserva todo o restante do site. */
'use strict';
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const publicDir=path.resolve(process.env.TWCO_PUBLIC_DIR||path.join(root,'public'));
const selected=JSON.parse(fs.readFileSync(path.join(__dirname,'reviews-selected.json'),'utf8'));
const assert=require('node:assert/strict');
assert.equal(selected.reviews.length,6,'Quantidade de depoimentos inesperada');
assert.equal(new Set(selected.reviews.map(x=>x.author)).size,6,'Nomes duplicados');
for(const review of selected.reviews){
  assert.equal(review.rating,5);
  assert.ok(review.author&&review.text&&review.text.length<=600);
}
function replaceOnce(text,find,replacement,name){
  const first=text.indexOf(find); assert.ok(first>=0,name+' não encontrado');
  assert.equal(text.indexOf(find,first+find.length),-1,name+' duplicado');
  return text.slice(0,first)+replacement+text.slice(first+find.length);
}
const snapshotPath=path.join(publicDir,'assets','avaliacoes-verificadas.json');
let snapshot=JSON.parse(fs.readFileSync(snapshotPath,'utf8'));
assert.equal(snapshot.placeName,selected.placeName);
fs.writeFileSync(snapshotPath,JSON.stringify(selected,null,2)+'\n');
const siteJsPath=path.join(publicDir,'assets','site.js');
let js=fs.readFileSync(siteJsPath,'utf8');
const snapshotRegex=/^const snapshot=\{[^\r\n]*\};$/m;
assert.equal((js.match(new RegExp(snapshotRegex.source,'gm'))||[]).length,1,'Snapshot antigo não localizado exatamente uma vez');
js=js.replace(snapshotRegex,'const snapshot='+JSON.stringify({status:selected.status,source:selected.source,retrievedAt:selected.retrievedAt,reviews:selected.reviews})+';');
js=replaceOnce(js,
 'Avaliações consultadas no Google Maps em 29/10/2026. Novos comentários dependem de integração autorizada.',
 'Avaliações selecionadas a partir das capturas do Google Maps. Novos comentários dependem de atualização.',
 'Nota das avaliações no JS');
fs.writeFileSync(siteJsPath,js);
const homepage=path.join(publicDir,'index.html');
let html=fs.readFileSync(homepage,'utf8');
html=replaceOnce(html,
 '4 avaliações verificadas no Google Maps em 29/10/2026',
 '6 avaliações selecionadas do Google Maps',
 'Resumo das avaliações');
html=replaceOnce(html,
 '4 avaliações de 5 estrelas · Google Maps',
 '6 avaliações de 5 estrelas · Google Maps',
 'Contador do carrossel');
html=replaceOnce(html,
 'Avaliações consultadas no Google Maps em 29/10/2026. Novos comentários dependem de integração autorizada.',
 'Avaliações selecionadas conforme capturas do Google Maps fornecidas pela TW&CO.',
 'Rodapé das avaliações');
fs.writeFileSync(homepage,html);
console.log('TW&CO REVIEWS UPDATED: 6 selected cards; only homepage review labels, site.js snapshot and reviews JSON.');

