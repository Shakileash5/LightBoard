var socket = new WebSocket('ws://localhost:8000'); // create a new connection
var socketRoom ; // hold room server connection

/*
 * Handler function when server connection is established
 */
socket.onopen = function() {
		console.log('Connected to server');
		set_snackbar("Connected to server");
};

/*
 * Handler function when server receives a message.
 * @param {Object} message - the message received from the server
 */
socket.onmessage = function(data) {
		//console.log(data.data);
		data = JSON.parse(data.data);
		//console.log('Message from server: ',data);

		if(data.status == "200") { // if the message is a success message

			if(data.type == "1") { // if room is created
				console.log("Room Creds recieved",data);
				// set room id at the top of the page
				document.getElementById("roomIdDis").innerHTML = data.roomId;
				document.getElementById("floatRoomId").style.display = "block";
				create_new_connection(data.host,data.port); // create a new connection to the room
			}
			else if(data.type == "2") { // if room is available to join
				console.log("Room Joined",data);
			}
			else if(data.type == "-1"){ // if room is full or not available
				console.log("Unable to create or join room currently...")
			}
		}
		
};

/*
 * Handler function when server connection is closed
 */
socket.onclose = function() {
	console.log('Disconnected from server');
	set_snackbar("Disconnected from server");
};

