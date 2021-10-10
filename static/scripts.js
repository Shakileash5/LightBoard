
img.onload = function() {
	ctx.drawImage(img,0,0);
}

function create_room(){
	dataDict = {
		'type': '1',
		'action': 'create_room',
	}
	// send data to server to create room
	socket.send(JSON.stringify(dataDict));
	
}

function display_joincred(){
	document.getElementById("controls").style.display = "none";
	document.getElementById("joinCreds").style.display = "flex";
}

function join_room(){
	let roomId = document.getElementById("room_id").value;
	if(roomId.length == 0){
		console.log("Room Id is empty");
		return;
	}
	dataDict = {
		'type': '2',
		'action': 'join_room',
		'roomId': roomId,
	}
	// send data to server to join room
	socket.send(JSON.stringify(dataDict));
}

window.onload = function() {
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
				evt.offsetX - 0,
				evt.offsetY - 0
			);
			sendMsg(evt.offsetX,evt.offsetY,"draw_start");
			started = true;

		}


	function drawMove(evt) {

			if (started) {
				ctx.lineTo(
					evt.offsetX - 0,
					 evt.offsetY - 0
				);
				
				ctx.strokeStyle = "#000";
				ctx.lineWidth = 5;
				ctx.stroke();
				console.log("Drawing",evt.pageX,evt.pageY);
				sendMsg(evt.offsetX,evt.offsetY,"draw");
			}

		}
	
	function endDraw(evt) {
			started = false;
			sendMsg(evt.offsetX,evt.offsetY,"draw_end");
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