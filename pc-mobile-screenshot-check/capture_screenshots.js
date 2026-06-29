/**
 * FDL SORT - Automatic Multi-device Screenshot Capture Script
 * Fuses Puppeteer for B2B high-fidelity rendering.
 */

const puppeteer = require('puppeteer');
const path = require('class-path'); // fallback to standard path

const TARGETS = [
  {
    name: '1-homepage',
    url: 'https://www.fdlsorterai.com/'
  },
  {
    name: '2-ai-sorter',
    url: 'https://www.fdlsorterai.com/products/ai-optical-sorter/index.html'
  },
  {
    name: '3-about',
    url: 'https://www.fdlsorterai.com/about/index.html'
  }
];

const DEVICES = [
  {
    type: 'pc',
    width: 1440,
    height: 900,
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  },
  {
    type: 'mobile',
    width: 390,
    height: 844,
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    isMobile: true,
    hasTouch: true
  }
];

async function capture() {
  console.log('🚀 Starting FDL SORT Automated Screenshot Capture Engine...');
  const browser = await puppeteer.launch({ headless: "new" });

  try {
    for (const target of TARGETS) {
      for (const device of DEVICES) {
        const page = await browser.newPage();
        await page.setUserAgent(device.userAgent);
        await page.setViewport({
          width: device.width,
          height: device.height,
          isMobile: device.isMobile || false,
          hasTouch: device.hasTouch || false
        });

        console.log(`📸 Navigating to [${target.url}] on ${device.type.toUpperCase()}...`);
        // Wait until network is idle to ensure Base64 images and styles are fully decoded
        await page.goto(target.url, { waitUntil: 'networkidle2', timeout: 60000 });
        
        // Wait additional 1.5s for layout stabilizers
        await page.waitForTimeout ? await page.waitForTimeout(1500) : new Promise(r => setTimeout(r, 1500));

        const fileName = `${target.name}-${device.type}.png`;
        const outputPath = fileName; // save to current directory
        
        console.log(`💾 Saving high-contrast rendering to [${fileName}]...`);
        await page.screenshot({ path: outputPath, fullPage: true });
        await page.close();
      }
    }
    console.log('🎉 All 6 high-fidelity dual-device screenshots captured successfully!');
  } catch (err) {
    console.error('❌ Screenshot capture failed:', err);
  } finally {
    await browser.close();
  }
}

capture();
