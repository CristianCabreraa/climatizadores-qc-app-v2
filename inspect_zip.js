const fs = require('fs');

// Simple zip central directory parser
function inspectZip(zipPath) {
  const buf = fs.readFileSync(zipPath);
  // Find End of Central Directory Record (signature 0x06054b50)
  let eocdOffset = -1;
  for (let i = buf.length - 22; i >= 0; i--) {
    if (buf.readUInt32LE(i) === 0x06054b50) {
      eocdOffset = i;
      break;
    }
  }

  if (eocdOffset === -1) {
    console.log('Not a valid zip');
    return;
  }

  const cdOffset = buf.readUInt32LE(eocdOffset + 16);
  const totalEntries = buf.readUInt16LE(eocdOffset + 10);
  console.log('Total entries:', totalEntries, 'CD Offset:', cdOffset);

  let pos = cdOffset;
  const entries = [];
  for (let i = 0; i < totalEntries; i++) {
    const sig = buf.readUInt32LE(pos);
    if (sig !== 0x02014b50) break;
    const nameLen = buf.readUInt16LE(pos + 28);
    const extraLen = buf.readUInt16LE(pos + 30);
    const commentLen = buf.readUInt16LE(pos + 32);
    const name = buf.toString('utf8', pos + 46, pos + 46 + nameLen);
    entries.push(name);
    pos += 46 + nameLen + extraLen + commentLen;
  }

  console.log('Sample entries:');
  entries.filter(e => e.startsWith('assets/') || e.endsWith('.xml') || e.endsWith('.dex')).forEach(e => console.log(' - ' + e));
}

inspectZip('C:/Users/GreenAir/.gemini/antigravity/scratch/climatizadores-qc-app/temp_base.apk');
