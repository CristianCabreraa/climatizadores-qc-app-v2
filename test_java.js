const { execFile } = require('child_process');

execFile('java', ['-version'], (error, stdout, stderr) => {
  if (error) {
    console.log('Error executing java:', error.message);
  }
  console.log('stdout:', stdout);
  console.log('stderr:', stderr);
});
