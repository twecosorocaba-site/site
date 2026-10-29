#!/usr/bin/env bash
set -euo pipefail
mkdir -p public
unzip -oq TWCO_Premium_V17_Projeto_Vercel.zip -d public
gunzip -c patch-site.cjs.gz > patch-site.cjs
TWCO_PUBLIC_DIR=public node patch-site.cjs
python3 scripts/clean_hero.py public/assets/hero-referencia-exata.png public/assets/hero-clean-v19.png
python3 scripts/merge_hero.py public/assets/hero-referencia-exata.png public/assets/roof-original-pixels.png public/assets/hero-clean-v19.png public/assets/hero-seamless-v22.png
TWCO_PUBLIC_DIR=public node scripts/polish.cjs
cat scripts/roof-seam-fix.css >> public/assets/experience-polish.css
python3 scripts/instagram_feed.py
cp scripts/instagram-carousel.css public/assets/instagram-carousel.css
cp scripts/instagram-carousel.js public/assets/instagram-carousel.js
cp scripts/seo-pages.css public/assets/seo-pages.css
python3 scripts/seo_build.py
rm -rf public/api
