const https = require('https');

https.get('https://registry.npmjs.org/apk_sign_ts/latest', (res) => {
  let data = '';
  res.on('data', c => data += c);
  res.on('end', () => {
    const json = JSON.parse(data);
    console.log('apk_sign_ts latest:', json.version);
    console.log('main:', json.main);
    console.log('dependencies:', json.dependencies);
    console.log('tarball:', json.dist.tarball);
  });
}).on('error', e => console.error(e));
