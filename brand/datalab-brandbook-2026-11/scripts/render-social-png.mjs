#!/usr/bin/env node
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { Resvg } from "@resvg/resvg-js";

const bookRoot = join(dirname(fileURLToPath(import.meta.url)), "..");
const socialDir = join(bookRoot, "assets", "social");
const fontsDir = join(bookRoot, "assets", "fonts");

const fontFiles = [
  join(fontsDir, "TitilliumWeb-Bold.ttf"),
  join(fontsDir, "OpenSans-Regular.ttf"),
  join(fontsDir, "OpenSans-SemiBold.ttf"),
];

for (const f of fontFiles) {
  if (!existsSync(f)) {
    console.error(`Missing font: ${f}`);
    process.exit(1);
  }
}

function render(name, width) {
  const svgPath = join(socialDir, `${name}.svg`);
  const svg = readFileSync(svgPath, "utf8");
  const resvg = new Resvg(svg, {
    fitTo: { mode: "width", value: width },
    font: { loadSystemFonts: false, fontFiles, defaultFontFamily: "Open Sans" },
  });
  writeFileSync(join(socialDir, `${name}.png`), resvg.render().asPng());
  console.log(`ok ${name}.png`);
}

render("post-1080x1080", 1080);
render("post-1200x627", 1200);
render("story-1080x1920", 1080);
