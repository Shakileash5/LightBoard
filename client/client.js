var net = require('net');

const port = 1200;
const host = '127.0.0.1';

const client = new net.Socket();


client.connect(port,host,function(){
   console.log(`Connected to server on ${host}:${port}`);
   //Connection was established, now send a message to the server.
   client.write('Hello from TCP client');
});

client.on('data',function(data){
   console.log(`Server Says : ${data}`); 
});

client.on('close',function(){
   console.log('Connection Closed');
});
//Add Error Event Listener
client.on('error',function(error){
   console.error(`Connection Error ${error}`); 
});