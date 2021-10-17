var socket = new WebSocket('ws://localhost:8000');
var socketRoom ;

socket.onopen = function() {
		console.log('Connected to server');
		set_snackbar("Connected to server");
};

socket.onmessage = function(data) {
		console.log(data.data);
		data = JSON.parse(data.data);
		console.log('Message from server: ',data);
		if(data.status == "200") {
			if(data.type == "1") {
				console.log("Room Creds recieved",data);
				document.getElementById("roomIdDis").innerHTML = data.roomId;
				document.getElementById("floatRoomId").style.display = "block";
				create_new_connection(data.host,data.port);
			}
			else if(data.type == "2") {
				console.log("Room Joined",data);
			}
			else if(data.type == "-1"){
				console.log("Unable to create or join room currently...")
			}
		}
		
};

socket.onclose = function() {
	console.log('Disconnected from server');
	set_snackbar("Disconnected from server");
};

