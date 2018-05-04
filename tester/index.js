var fs = require('fs')
var tizen = require('tizen');
var path = require('tools/path')

var resPath = tizen.getResPath();
var dataPath = tizen.getDataPath();
path.testRoot = resPath;
path.writeableDir = dataPath;
path.dynamicmoduleDir = resPath + 'dynamicmodule';

var testfile = fs.openSync(resPath + 'testfile', 'r')

var buffer = new Buffer(128);
fs.readSync(testfile, buffer, 0, buffer.length, 0);
var testfileName = buffer.toString();
fs.closeSync(testfile);
console.log('test file: ', testfileName);

// Start test
process.on('exit', function(code){
  console.log('IoT.js test result:', code);
});
require(testfileName);