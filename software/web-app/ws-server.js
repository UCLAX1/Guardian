const io = require('socket.io')();

var curImg = "NOTHING YET";

const bufEmitter = require('./c-client'); 
bufEmitter.on('event', function(img) { //called each time a new image is recieved by client
    curImg = img;
});

io.on('connection', function (socket) {
    setInterval(() => {socket.emit('image', curImg);}, 40);

    socket.on('submit', function(data) {
        bufEmitter.emit('submit', data); //send data to socket
        console.log("Data: " + data);
    });
});



const port = 1337
io.listen(port)
console.log('Listening on port ' + port + '...')
