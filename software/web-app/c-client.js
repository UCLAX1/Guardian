var net = require('net');
 
var HOST = 'localhost';
var PORT = 5000;
 
var client = new net.Socket();

var iBuf = ""; //from computer to web-app, image
var cBuf = ""; //from computer to web-app, coordinates
var oBuf = ""; //from web-app to computer
const EventEmitter = require('events');
class BufEmitter extends EventEmitter {}

module.exports = new BufEmitter();

module.exports.on('submit', function(data) { //called each time controls are submitted
    oBuf = data;
    client.write(oBuf);
});
 
client.connect(PORT, HOST, function() {
    console.log('Client connected to: ' + HOST + ':' + PORT);
});
 
client.on('data', function(data) {    
    var rec = data.toString(); //current string recieved
    var index = rec.indexOf("Coords - ");
    if (index === -1 ) { //not a coordinate string, so it should be an image string
        index = rec.indexOf("breakbreakbreak");
        if ( index === -1) {
            iBuf = iBuf + rec;
        } else {
            iBuf = iBuf + rec.substring(0,index);
            module.exports.emit('image', iBuf); //send img to ws-server
            iBuf = ""; //reset buffer
        }
    } else {
        cBuf = rec.substring(index+"Coords - ".length,rec.length); //gets x,y,x,y
        module.exports.emit('coord', cBuf); 
        cBuf = "";
    }
    if (data.toString().endsWith('exit')) {
        client.destroy();
    }
});
 
// Add a 'close' event handler for the client socket
client.on('close', function() {
    console.log('Client closed');
});
 
client.on('error', function(err) {
    console.error(err);
});