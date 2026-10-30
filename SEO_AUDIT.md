# TW&CO Premium — SEO técnico implementado (29/10/2026)

## Escopo
- SEO técnico: robots, sitemap index, páginas e imagens, canonical, meta title/description, OG e Twitter, favicon SVG, manifesto, 404, cabeçalhos/cache.
- Schema.org JSON-LD: AutoRepair, WebSite, WebPage, Service, BreadcrumbList e Article em páginas pertinentes. Sem marcar avaliações próprias para rich snippets.
- Páginas estáticas em pt-BR: serviços, quatro especialidades confirmadas, oficina em Sorocaba, sobre, contato, guia e dois artigos.
- Acessibilidade: textos descritivos e links internos, sem páginas "porta de entrada" para bairros fictícios.
- Arquivos opcionais: llms.txt, llms-full.txt e /ai/*.md. Google Search não dá benefício direto para esses arquivos.
- Performance: preservação da hero aprovada; preloads com prioridade, arquivos estáticos no mesmo domínio, cache e imagens lazy nas seções secundárias. Não foi alegado Lighthouse >= 90 sem medição real.

## Endereço oficial (30/10/2026)
- Domínio principal: https://www.tweco.com.br/
- https://tweco.com.br/ redireciona permanentemente (308) para a versão www.
- Canonical, Open Graph, dados estruturados, links internos, robots.txt e sitemaps gerados para a URL www.
- As páginas continuam publicadas na Vercel, mas a URL do projeto Vercel não deve ser enviada para indexação.
- Search Console e verificação de propriedade ainda exigem autenticação do proprietário na conta Google.

## Verificações que exigem proprietários/contas externas
1. Verificar domínio no Google Search Console, cadastrar sitemap e acompanhar cobertura e Core Web Vitals.
2. Concluído: domínio próprio vinculado à Vercel, versão www preferencial e canonical/sitemaps alinhados.
3. Revisar Perfil da Empresa no Google: categorias, horários, serviços, endereço e site; manter NAP consistente.
4. Criar metas no Google Analytics/Tag Manager somente com autorização e com consentimento/privacidade adequados.
5. Acompanhar métricas reais de LCP, INP, CLS no PageSpeed e corrigir com base em dados de campo.
6. Confirmar informações técnicas e os conteúdos dos guias com profissional da oficina antes de expandir o blog.
7. Não publicar ratings/reviews autodeclarados em JSON-LD.

## Fonte normativa
Google Search Central (sitemaps, dados estruturados e documentação AI features);
web.dev (imagem LCP e otimização do carregamento).
