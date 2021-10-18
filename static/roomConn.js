
/**
 * Generates a random string of the given length.
 * @param {number} length - The length of the string to generate.
 * @return {string} - The generated string. 
 */
function generateString(length) {
    let result = ' ';
    const charactersLength = characters.length;
    for ( let i = 0; i < length; i++ ) {
		let randomNum = Math.floor(Math.random() * charactersLength); // random number of range 0 - length of alphabets
        result += characters.charAt(randomNum);
    }

    return result;
}


/**
 * Adds the clients to the list
 * @param {number} numberOfClients - The number of clients in the room.
 * @param {boolean} [flag=false] - If true, the all the clients are added to the list, else one client is added to the list.
 */
function addClients(numberOfClients,flag=false){
	var clients = document.getElementById("clients");

	if(flag == true){ // Add all the clients to the list 
		clients.style.display = "block";
		for(let i = 0; i<numberOfClients;i++){
			clients.innerHTML = clients.innerHTML+"<div class='clientAcc' style=border-color:#"+Math.floor(Math.random()*16777215).toString(16)+">"+ generateString(1)+"</div>";
		}
	}
	else{ // Add one client to the list
		clients.innerHTML = clients.innerHTML+"<div class='clientAcc' style=border-color:#"+Math.floor(Math.random()*16777215).toString(16)+">"+ generateString(1)+"</div>";
		set_snackbar("New client joined the room");
	}
	totalClients += 1;
	
}


/**
 * Remove the clients from the list.
 */
function removeClient(){
	let clients = document.getElementById("clients");
	let descendants = clients.getElementsByTagName("*");
	if(descendants.length > 0){
		clients.removeChild(descendants[descendants.length-1]);
	}
	set_snackbar("Client left the room");
}

/**
 * Initializes the canvas and the drawing tool.	
 * @param {number} x - The x coordinate of the mouse.
 * @param {number} y - The y coordinate of the mouse.
 */
function startDraw(x,y){
	//console.log("Started Drawing");
	ctx.beginPath();
	ctx.moveTo(
		x - 0,
		y - 0
	);
}


/**
 * Draw the points on the canvas.
 * @param {number} x - The x coordinate of the mouse.
 * @param {number} y - The y coordinate of the mouse.
 * @param {number} brushSize - The size of the brush.
 */
function drawPoints(x,y,brushSize){
	ctx.lineTo(
		x - 0,
		y - 0
	);

	ctx.strokeStyle = '#000';
	ctx.lineWidth = brushSize;
	ctx.stroke();
	//console.log("Drawing");
	//sendMsg(evt.offsetX,evt.offsetY,"draw");
}


/**
 * erase the points on the canvas.
 * @param {number} x - The x coordinate of the point.
 * @param {*} y - The y coordinate of the point.
 * @param {*} brushSize - The size of the brush.
 */
function erasePoints(x,y,brushSize){
	ctx.clearRect(x - 0, y - 0, brushSize*2, brushSize*2);
}

/**
 * Close the server connection and redirect the connection to the room server.
 * @param {string} host - The host of the room server.
 * @param {*} port - The port of the room server.
 */
async function create_new_connection(host,port){
	socket.close(); // close the server connection
	
	socketRoom = await new WebSocket('ws://'+host+':'+port.toString()); // create a new connection to the room server
	
	// Add event listeners to the room server
	socketRoom.addEventListener("open", onOpen);
	socketRoom.addEventListener("message", onmessage);
	socketRoom.addEventListener("close", onclose);
	
	// display the canvas
	document.getElementById("containerDiv").style.display = "none";
	document.getElementById("canvasDiv").style.display = "block";
	document.getElementById("toolbar").style.display = "block";
	set_snackbar("Redirecting to the room!.")
}


/**
 * Handeler function when the server connection is opened.
 */
function onOpen(){
	console.log("Connection Opened");
	socketRoom.send(JSON.stringify({"type":"5","message":"Requesting canvas data"}));
	set_snackbar("Connected to room");
}


/**
 * Handler function when the server connection receives a message.
 * @param {object} data - The data received from the server.
 */
function onmessage(data){
	
	data = JSON.parse(data.data); // parse the data

	if(data.type == "3"){ // if the data is canvas data
		if(data.action == "draw_start"){
			startDraw(data.x,data.y);
		}
		else if(data.action == "draw"){
			drawPoints(data.x,data.y,data.brushSize);
		}
		else if(data.action == "draw_end"){
			ctx.closePath();
		}
		else if(data.action == "erase"){
			erasePoints(data.x,data.y,data.brushSize);
		}
	}
	else if(data.type == "4"){ // if the data is client data
		if(totalClients == 0){ // add all the clients to the list
			addClients(data.noOfClients,true);
		}
		else{ // else add the client
			addClients(data.noOfClients);
		}
		
	}
	else if(data.type == "5"){ // if the data is a request for canvas data
		dataDict = {
			"type" : "6",
			"canvas" : getCanvasData(),
			"forClient" : data.forClient
		}
		socketRoom.send(JSON.stringify(dataDict));
	}
	else if(data.type == "6"){ // if the data is canvas data from the room server
		img.src = data.canvas;
	}
	else if(data.type == "7"){ // if the data is a reply to a request for canvas data
		console.log("No canvas data available",data);
	}
	else if(data.type == "8"){ // if the client is disconnected
		removeClient();
		//console.log("one client left the room",data);
	}
	
}


/**
 * Handler function when the server connection is closed.
 */
function onclose(){
	console.log("Disconnected from room");
	set_snackbar("Disconnected from room")
}


/**
 * send the message to the room server asynchronously.
 * @param {number} x - The x coordinate of the point.
 * @param {number} y - The y coordinate of the point.
 * @param {number} brushSize - The size of the brush.
 * @param {string} action - The action to be performed on the canvas either draw or erase.
 */
function sendMsgAsync(x,y,brushSize,action){
	setTimeout(sendMsg(x,y,brushSize,action), 0);
}

/**
 * send the message to the room server.
 * @param {number} x - The x coordinate of the point.
 * @param {number} y - The y coordinate of the point.
 * @param {number} brushSize - The size of the brush.
 * @param {string} action - The action to be performed on the canvas either draw or erase.
 */
function sendMsg(x,y,brushSize,action){
	dataDict = {
		'type': '3',
		'action': action,
		'x': x,
		'y': y,
		'brushSize':brushSize
	}
	socketRoom.send(JSON.stringify(dataDict));
}


/**
 * Get the canvas data and return it as a base64 encoded string.
 * @return {string} - The canvas data as a base64 encoded string. 
 */
function getCanvasData(){
	var canvas = document.getElementById("myCanvas");
	var data = canvas.toDataURL();
	return data;

}

