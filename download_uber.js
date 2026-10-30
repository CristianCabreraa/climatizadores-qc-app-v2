const https = require('https');
const fs = require('fs');

function download(url, dest) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return download(res.headers.location, dest).then(resolve).catch(reject);
      }
      if (res.statusCode !== 200) {
        return reject(new Error('Status: ' + res.statusCode));
      }
      const stream = fs.createWriteStream(dest);
      res.pipe(stream);
      stream.on('finish', () => {
        stream.close();
        resolve();
      });
    }).on('error', reject);
  });
}

async function getUber() {
  const dest = 'C:/Users/GreenAir/.gemini/antigravity/scratch/climatizadores-qc-app/uber-apk-signer.jar';
  console.log('Downloading uber-apk-signer...');
  await download('https://github.com/patrickfav/uber-apk-signer/releases/download/v1.3.0/uber-apk-signer-1.3.0.jar', dest);
  console.log('Downloaded uber-apk-signer size:', fs.statSync(dest).size);
}

getUber().catch(console.error);
