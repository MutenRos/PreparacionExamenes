const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");

async function generatePDF() {
  const browser = await puppeteer.launch({
    headless: true,
    executablePath:
      "/home/dario/.cache/puppeteer/chrome-headless-shell/linux-144.0.7559.96/chrome-headless-shell-linux64/chrome-headless-shell",
    args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-gpu"],
  });

  const page = await browser.newPage();

  const htmlPath = path.join(__dirname, "OPENCLAW_MANUAL.html");
  const htmlContent = fs.readFileSync(htmlPath, "utf8");

  await page.setContent(htmlContent, { waitUntil: "networkidle0" });

  await page.pdf({
    path: path.join(__dirname, "OPENCLAW_MANUAL.pdf"),
    format: "A4",
    printBackground: true,
    margin: { top: "20mm", bottom: "20mm", left: "15mm", right: "15mm" },
  });

  await browser.close();
  console.log("PDF generated: OPENCLAW_MANUAL.pdf");
}

generatePDF().catch(console.error);
