const https = require('https');
const fs = require('fs');
const zlib = require('zlib');
const path = require('path');

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

async function getSigner() {
  const tgz = 'C:/Users/GreenAir/.gemini/antigravity/scratch/climatizadores-qc-app/apk_sign.tgz';
  await download('https://registry.npmjs.org/apk_sign_ts/-/apk_sign_ts-1.0.1.tgz', tgz);
  console.log('Downloaded apk_sign_ts tgz size:', fs.statSync(tgz).size);
}

getSigner().catch(console.error);
