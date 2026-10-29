#!/usr/bin/env bash
set -euo pipefail
mkdir -p public
unzip -oq TWCO_Premium_V17_Projeto_Vercel.zip -d public
gunzip -c patch-site.cjs.gz > patch-site.cjs
TWCO_PUBLIC_DIR=public node patch-site.cjs
python3 scripts/clean_hero.py public/assets/hero-referencia-exata.png public/assets/hero-clean-v19.png
rm -rf public/api
