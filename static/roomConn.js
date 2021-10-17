
/**
 * Generates a random string of the given length.
 * @param {number} length The length of the string to generate.
 * @return {string} The generated string. 
 */
function generateString(length) {
    let result = ' ';
    const charactersLength = characters.length;
    for ( let i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }

    return result;
}


/**
 * Initializes the canvas and the drawing tool.	
 * @param {number} x The x coordinate of the mouse.
 * @param {number} y The y coordinate of the mouse.
 */
function startDraw(x,y){
	console.log("Started Drawing");
	ctx.beginPath();
	ctx.moveTo(
		x - 0,
		y - 0
	);
	//sendMsg(evt.offsetX,evt.offsetY,"draw_start");
	//started = true;
}

function drawPoints(x,y,brushSize){
	ctx.lineTo(
		x - 0,
		y - 0
	);

	ctx.strokeStyle = '#000';
	ctx.lineWidth = brushSize;
	ctx.stroke();
	console.log("Drawing");
	//sendMsg(evt.offsetX,evt.offsetY,"draw");
}

function erasePoints(x,y,brushSize){
	ctx.clearRect(x - 0, y - 0, brushSize*2, brushSize*2);
}


function addClients(numberOfClients,flag=false){
	var clients = document.getElementById("clients");
	if(flag == true){
		clients.style.display = "block";
		for(let i = 0; i<numberOfClients;i++){
			clients.innerHTML = clients.innerHTML+"<div class='clientAcc' style=border-color:#"+Math.floor(Math.random()*16777215).toString(16)+">"+ generateString(1)+"</div>";
		}
	}
	else{
		clients.innerHTML = clients.innerHTML+"<div class='clientAcc' style=border-color:#"+Math.floor(Math.random()*16777215).toString(16)+">"+ generateString(1)+"</div>";
	}
	totalClients += 1;
}

function removeClient(){
	let clients = document.getElementById("clients");
	let descendants = clients.getElementsByTagName("*");
	if(descendants.length > 0){
		clients.removeChild(descendants[descendants.length-1]);
	}
	
}


async function create_new_connection(host,port){
	socket.close();
	socketRoom = await new WebSocket('ws://'+host+':'+port.toString());
	socketRoom.addEventListener("open", onOpen);
	socketRoom.addEventListener("message", onmessage);
	socketRoom.addEventListener("close", onclose);
	document.getElementById("containerDiv").style.display = "none";
	document.getElementById("canvasDiv").style.display = "block";
	document.getElementById("toolbar").style.display = "block";
	//addClients();
}

function onOpen(){
	console.log("Connection Opened");
	socketRoom.send(JSON.stringify({"type":"5","message":"Requesting canvas data"}));
}

function onmessage(data){
	//console.log(data.data,ctx);
	data = JSON.parse(data.data);
	if(data.type == "3"){
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
	else if(data.type == "4"){
		if(totalClients == 0){
			addClients(data.noOfClients,true);
		}
		else{
			addClients(data.noOfClients);
		}
		
	}
	else if(data.type == "5"){
		dataDict = {
			"type" : "6",
			"canvas" : getCanvasData(),
			"forClient" : data.forClient
		}
		socketRoom.send(JSON.stringify(dataDict));
	}
	else if(data.type == "6"){
		img.src = data.canvas;
	}
	else if(data.type == "7"){
		console.log("No canvas data available",data);
	}
	else if(data.type == "8"){
		removeClient();
		//console.log("one client left the room",data);
	}
	
}

function onclose(){
	console.log("Disconnected from room");
}

function sendMsgAsync(x,y,brushSize,action){
	setTimeout(sendMsg(x,y,brushSize,action), 0);
}
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

function getCanvasData(){
	var canvas = document.getElementById("myCanvas");
	var data = canvas.toDataURL();
	return data;

}

