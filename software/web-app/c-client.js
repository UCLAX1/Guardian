var net = require('net');
 
var HOST = 'localhost';
var PORT = 5000;
 
var client = new net.Socket();

var buf = "";
const EventEmitter = require('events');
class BufEmitter extends EventEmitter {}

module.exports = new BufEmitter();
 
client.connect(PORT, HOST, function() {
    console.log('Client connected to: ' + HOST + ':' + PORT);
});
 
client.on('data', function(data) {    
    var rec = data.toString(); //current string recieved
    var index = rec.indexOf("breakbreakbreak");
    if ( index === -1) {
        buf = buf + rec;
        console.log('Client received: partial string');
    } else {
        buf = buf + rec.substring(0,index);
        module.exports.emit('event', buf); //send img to ws-server
        client.write(buf); //this will be the base64 of the image
        console.log(buf);
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