var net = require('net');
var HOST = 'localhost';
var PORT = 5000;

var buf = "";

net.createServer(function(sock) {

  console.log('CONNECTED: ' + sock.remoteAddress + ':' + sock.remotePort);
  setInterval(() => {sock.write('Hello World!')}, 100);
  sock.on('data', function(data) {
    buf = data.toString(); //
    console.log("Client says: " + buf);
  });

  sock.on('close', function (data) {
    console.log('CLOSED: ' + sock.remoteAddress + ':' + sock.remotePort);
  });

}).listen(PORT, HOST);

console.log('Server listening on ' + HOST + ':' + PORT);