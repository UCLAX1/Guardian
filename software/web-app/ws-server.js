const io = require('socket.io')();

var curImg = "NOTHING YET";

const bufEmitter = require('./c-client'); 
bufEmitter.on('event', function(img) { //called each time a new image is recieved by client
    curImg = img;
    console.log("Computer client says: " + curImg);
});

io.on('connection', function (socket) {
    setInterval(() => {socket.emit('event', curImg);}, 100);
        
});

const port = 1337
io.listen(port)
console.log('Listening on port ' + port + '...')
