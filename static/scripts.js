

var socket = new WebSocket('ws://localhost:8000');

function create_new_connection(host,port){
	socket = new WebSocket('ws://'+host+':'+port);
}

function create_room(){
	socket.send('create_room');
	socket.close();
	create_new_connection('localhost',8000);
	//socket = new WebSocket('ws://localhost:8000');
	//socket.send('join_room');
}

socket.onopen = function() {
		console.log('Connected to server');
		socket.send('Hello Server');
};

socket.onmessage = function(msg) {
		console.log('Message from server: ' + msg.data);
		if(msg.data == 'start') {
			started = true;
		}
		if(msg.data == 'stop') {
			started = false;
		}
		if(msg.data == 'clear') {
			ctx.fillStyle="#fff";
			ctx.fillRect(0,0,myCanvas.width,myCanvas.height);
		}
};

socket.onclose = function() {
		console.log('Disconnected from server');
};


window.onload = function() {
	var myCanvas = document.getElementById("myCanvas");
	var ctx = myCanvas.getContext("2d");
    var started = false;
    // Fill Window Width and Height
    myCanvas.width = window.innerWidth;
	myCanvas.height = window.innerHeight;

	// Set Background Color
    ctx.fillStyle="#fff";
    ctx.fillRect(0,0,myCanvas.width,myCanvas.height);

	// Touch Events Handlers
	draw = {
		started: false,
		start: function(evt) {
			
			ctx.beginPath();
			ctx.moveTo(
				evt.touches[0].pageX,
				evt.touches[0].pageY
			);

			this.started = true;

		},
		move: function(evt) {

			if (this.started) {
				ctx.lineTo(
					evt.touches[0].pageX,
					evt.touches[0].pageY
				);
				
				ctx.strokeStyle = "#000";
				ctx.lineWidth = 5;
				ctx.stroke();
			}

		},
		end: function(evt) {
			this.started = false;
		}
	};

	function startDraw(evt) {
			
			ctx.beginPath();
			ctx.moveTo(
				evt.pageX,
				evt.pageY
			);

			started = true;

		}


	function drawMove(evt) {

			if (started) {
				ctx.lineTo(
					evt.pageX,
					evt.pageY
				);
				
				ctx.strokeStyle = "#000";
				ctx.lineWidth = 5;
				ctx.stroke();
			}

		}
	
	function endDraw(evt) {
			started = false;
		}
	// Touch Events
	myCanvas.addEventListener('mousedown', startDraw, false);
	myCanvas.addEventListener('mouseup', endDraw, false);
	myCanvas.addEventListener('mousemove', drawMove, false);
	
	// Disable Page Move
	document.body.addEventListener('touchmove',function(evt){
		evt.preventDefault();
	},false);
	
};