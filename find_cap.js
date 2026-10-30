const https = require('https');

function fetchJson(url) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, {
      headers: { 'User-Agent': 'Antigravity-Agent' }
    }, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, body: JSON.parse(data) });
        } catch (e) {
          resolve({ status: res.statusCode, body: data });
        }
      });
    });
    req.on('error', reject);
  });
}

async function findCapacitor() {
  const searchRes = await fetchJson('https://api.github.com/search/repositories?q=capacitor+apk+release&sort=stars');
  if (searchRes.body && searchRes.body.items) {
    for (const item of searchRes.body.items.slice(0, 8)) {
      const rels = await fetchJson(`https://api.github.com/repos/${item.full_name}/releases`);
      if (Array.isArray(rels.body)) {
        for (const rel of rels.body) {
          for (const asset of (rel.assets || [])) {
            if (asset.name.endsWith('.apk')) {
              console.log(`${item.full_name} -> ${asset.name} (${asset.size} bytes)`);
              console.log(`URL: ${asset.browser_download_url}`);
            }
          }
        }
      }
    }
  }
}

findCapacitor();
