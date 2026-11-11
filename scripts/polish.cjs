/* Post-processamento pós-V19, sem alterar o ZIP com as imagens originais. */
'use strict';
const fs=require('fs');
const path=require('path');
const publicDir=path.resolve(process.env.TWCO_PUBLIC_DIR || 'public');
const scriptDir=__dirname;
const htmlPath=path.join(publicDir,'index.html');
const page=fs.readFileSync(htmlPath,'utf8');
const originalScriptPath=path.join(publicDir,'assets/experience.js');
let original=fs.readFileSync(originalScriptPath,'utf8');
// O script antigo tentava rolar até a resposta mesmo quando recolhida.
original=original.replace(/document\.getElementById\('diagnosticAnswer'\)\?\.scrollIntoView\(\{[^;]*\}\);/g,'');
fs.writeFileSync(originalScriptPath,original);
let html=page;
if(!html.includes('id="diagnosticForm"')||!html.includes('id="diagnosticAnswer"')
  || !html.includes('id="atendimento"') || !html.includes('id="servicos"'))
  throw new Error('Estrutura inesperada; abortando refinamento.');
html=html.replace(/(<p id="diagnosticReply">)[\s\S]*?(<\/p>)/,'$1$2');
html=html.replace('id="diagnosticAnswer" aria-live="polite"',
  'id="diagnosticAnswer" aria-live="polite" aria-hidden="true" inert');
html=html.replace('</head>',
  '<link rel="stylesheet" href="assets/experience-polish.css"/></head>');
html=html.replace('</body>',
  '<script defer src="assets/experience-polish.js"></script></body>');
fs.copyFileSync(path.join(scriptDir,'experience-polish.css'),
  path.join(publicDir,'assets/experience-polish.css'));
fs.copyFileSync(path.join(scriptDir,'experience-polish.js'),
  path.join(publicDir,'assets/experience-polish.js'));
fs.writeFileSync(htmlPath,html,'utf8');
// Ajuste isolado: 4,3 s -> 3,2 s entre avaliações do Google.
const reviewsScriptPath=path.join(publicDir,'assets/site.js');
const reviewJs=fs.readFileSync(reviewsScriptPath,'utf8');
const oldInterval='},4300)}';
if(reviewJs.split(oldInterval).length!==2) throw new Error('Intervalo do carrossel de avaliações inesperado');
fs.writeFileSync(reviewsScriptPath,reviewJs.replace(oldInterval,'},3200)}'));

console.log('TW&CO Premium V20 — experiência refinada, demais seções intactas.');
