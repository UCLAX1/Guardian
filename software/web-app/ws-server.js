const io = require('socket.io')();

var curImg = "NOTHING YET";
var curCoord = "-1,-1,-1,-1";


const bufEmitter = require('./c-client'); 
bufEmitter.on('image', function(img) { //called each time a new image is recieved by client
    curImg = img;
});

bufEmitter.on('coord', function(coord) { //called each time a new image is recieved by client
    curCoord = coord;
});

io.on('connection', function (socket) {
    setInterval(() => {socket.emit('image', curImg);socket.emit('coord', curCoord);}, 40);

    socket.on('submit', function(data) {
        bufEmitter.emit('submit', data); //send data to socket
        console.log("Data: " + data);
    });
});



const port = 1337
io.listen(port)
console.log('Listening on port ' + port + '...')
