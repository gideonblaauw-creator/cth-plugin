#!/usr/bin/env bash
# Build HTML from part3-google-forms-question-list.md, then print PDF via Chromium.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$DIR/../../.." && pwd)"
cd "$REPO_ROOT/tools/reveal"
python3 "$DIR/build-questionnaire-html.py"
node -e "
const puppeteer=require('puppeteer-core');
(async()=>{
  const browser=await puppeteer.launch({
    executablePath: process.env.CHROME_PATH || '/usr/bin/chromium',
    args: ['--no-sandbox']
  });
  const page=await browser.newPage();
  await page.goto('file://$DIR/part3-cuestionario.html', { waitUntil: 'networkidle0' });
  await page.pdf({
    path: '$DIR/part3-cuestionario-mentor.pdf',
    format: 'A4',
    printBackground: true,
    margin: { top: 0, bottom: 0, left: 0, right: 0 }
  });
  await browser.close();
})();
" 2>&1
echo "PDF: $DIR/part3-cuestionario-mentor.pdf"