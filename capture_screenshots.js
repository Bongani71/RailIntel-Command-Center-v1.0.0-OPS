const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    if (!fs.existsSync('docs')) {
        fs.mkdirSync('docs');
    }

    console.log("Launching headless browser...");
    // Adding args to bypass sandbox limits which sometimes crash Windows Puppeteer
    const browser = await puppeteer.launch({ 
        headless: "new",
        defaultViewport: { width: 1920, height: 1080 },
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    
    console.log("Navigating to RailIntel Command Center...");
    await page.goto('http://localhost:8501', { waitUntil: 'domcontentloaded', timeout: 60000 });
    
    // Wait for the Streamlit app to fully render metrics
    await page.waitForTimeout(8000); 

    // Take Dashboard Screenshot
    console.log("Capturing Dashboard...");
    await page.screenshot({ path: 'docs/dashboard.png' });

    console.log("Navigating to Live Tracking Map...");
    await page.evaluate(() => {
        const labels = Array.from(document.querySelectorAll('label'));
        const mapLabel = labels.find(el => el.textContent.includes('Live Tracking Map') || el.textContent.includes('Tracking'));
        if (mapLabel) mapLabel.click();
    });
    
    await page.waitForTimeout(6000); 
    console.log("Capturing Map...");
    await page.screenshot({ path: 'docs/map.png' });

    console.log("Navigating to Fleet Telemetry...");
    await page.evaluate(() => {
        const labels = Array.from(document.querySelectorAll('label'));
        const telemetryLabel = labels.find(el => el.textContent.includes('Fleet Telemetry') || el.textContent.includes('Telemetry'));
        if (telemetryLabel) telemetryLabel.click();
    });
    
    await page.waitForTimeout(5000); 
    console.log("Capturing Telemetry...");
    await page.screenshot({ path: 'docs/telemetry.png' });

    console.log("Navigating to Tactical Log...");
    await page.evaluate(() => {
        const labels = Array.from(document.querySelectorAll('label'));
        const tacticalLabel = labels.find(el => el.textContent.includes('Tactical Log') || el.textContent.includes('Tactical'));
        if (tacticalLabel) tacticalLabel.click();
    });
    
    await page.waitForTimeout(5000); 
    console.log("Capturing Tactical Log...");
    await page.screenshot({ path: 'docs/tactical_log.png' });

    await browser.close();
    console.log("Screenshots captured safely and saved successfully.");
})();
