
/*
 * Handler function when image source is set and image is loaded
 */
img.onload = function() {
	// draw the image on the canvas
	ctx.drawImage(img,0,0);
}


/**
 * Function to request server to create a new room
 */
function create_room(){
	dataDict = {
		'type': '1',
		'action': 'create_room',
	}
	// send data to server to create room
	socket.send(JSON.stringify(dataDict));
	
}


/**
 * Function to display the join room dialog.
 */
function display_joincred(){
	document.getElementById("controls").style.display = "none";
	document.getElementById("joinCreds").style.display = "flex";
}


/**
 * Function to request server to join a room with room id
 */
function join_room(){
	let roomId = document.getElementById("room_id").value;

	if(roomId.length == 0){ // Check if room id is empty
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


/**
 * Function to set erase flag true. 
 */
function eraseElement(){
	eraseFlag = true;
}

/**
 * Function to set erase flag false. 
 */
function drawElement(){
	eraseFlag = false;
}

/**	
 * Function to increase the brush size
 */
function increaseBrushSize(){
	if(brushSize < 20){ // Check if brush size has not exceeded maximum size
		brushSize += 2;
	}
}

/**	
 * Function to decrease the brush size
 */
function decreaseBrushSize(){
	if(brushSize > 2){ // Check if brush size has not exceeded minimum size
		brushSize -= 2;
	}
}


/**
 * Function to copy the room id to clipboard
 */
function copyToClipboard() {
  var copyText = document.getElementById("roomIdDis");
  navigator.clipboard.writeText(copyText.innerText);
  set_snackbar("Copied to clipboard");
}


window.onload = function() {
	// Set Background Color
    ctx.fillStyle="#fff";
    ctx.fillRect(0,0,canvas.width,canvas.height);

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


	/**
	 * Handler function when user touches the canvas and sends the data to server
	 * @param {*} evt - mouse event
	 */
	function startDraw(evt) {
			
		if(!eraseFlag){
			ctx.beginPath();
			ctx.moveTo(
				evt.offsetX - 0,
				evt.offsetY - 0
			);
			// send the drawing data to room.
			sendMsgAsync(evt.offsetX,evt.offsetY,brushSize,"draw_start");
		}
		started = true;

	}


	/**
	 *
	 *
	 * @param {*} evt
	 */
	function drawMove(evt) {

			if (started && !eraseFlag) {
				ctx.lineTo(
					evt.offsetX - 0,
					 evt.offsetY - 0
				);
				
				ctx.strokeStyle = "#000";
				ctx.lineWidth = brushSize;
				ctx.stroke();
				//console.log("Drawing",evt.pageX,evt.pageY);
				sendMsgAsync(evt.offsetX,evt.offsetY,brushSize,"draw");
			}
			else if(started && eraseFlag){
				ctx.clearRect(evt.offsetX - 0, evt.offsetY - 0, brushSize*2, brushSize*2);
				sendMsgAsync(evt.offsetX,evt.offsetY,brushSize,"erase");
			}

		}
	
	function endDraw(evt) {
		started = false;
		if(!eraseFlag){
			sendMsgAsync(evt.offsetX,evt.offsetY,brushSize,"draw_end");
		}
		//sendMsg(evt.offsetX,evt.offsetY,"draw_end");
	}
	// Touch Events
	canvas.addEventListener('mousedown', startDraw, false);
	canvas.addEventListener('mouseup', endDraw, false);
	canvas.addEventListener('mousemove', drawMove, false);
	
	// Disable Page Move
	document.body.addEventListener('touchmove',function(evt){
		evt.preventDefault();
	},false);
	
};