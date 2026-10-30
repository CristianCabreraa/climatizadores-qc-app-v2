const https = require('https');

function searchNpm(q) {
  return new Promise((resolve) => {
    https.get(`https://registry.npmjs.org/-/v1/search?text=${encodeURIComponent(q)}&size=5`, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json.objects.map(o => ({ name: o.package.name, desc: o.package.description, version: o.package.version })));
        } catch (e) {
          resolve([]);
        }
      });
    }).on('error', () => resolve([]));
  });
}

async function run() {
  const pkgs = await searchNpm('apksigner');
  console.log('NPM Search results for apksigner:');
  pkgs.forEach(p => console.log(`- ${p.name}@${p.version}: ${p.desc}`));

  const pkgs2 = await searchNpm('sign apk');
  console.log('NPM Search results for sign apk:');
  pkgs2.forEach(p => console.log(`- ${p.name}@${p.version}: ${p.desc}`));
}

run();
