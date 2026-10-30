const https = require('https');
const fs = require('fs');
const zlib = require('zlib');

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

async function inspect() {
  console.log('Downloading template APK...');
  const tmpApk = 'C:/Users/GreenAir/.gemini/antigravity/scratch/climatizadores-qc-app/temp_base.apk';
  await download('https://github.com/LIN4CRE/DBSTEAM/releases/download/v1.0.0/DBSTEAM-v1.0.0.apk', tmpApk);
  console.log('Downloaded size:', fs.statSync(tmpApk).size);
}

inspect().catch(console.error);
