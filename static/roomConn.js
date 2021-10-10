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

function drawPoints(x,y){
	ctx.lineTo(
		x - 0,
		y - 0
	);

	ctx.strokeStyle = '#000';
	ctx.lineWidth = 5;
	ctx.stroke();
	console.log("Drawing");
	//sendMsg(evt.offsetX,evt.offsetY,"draw");
}

async function create_new_connection(host,port){
	socket.close();
	socketRoom = await new WebSocket('ws://localhost:1201');
	socketRoom.addEventListener("open", onOpen);
	socketRoom.addEventListener("message", onmessage);
	socketRoom.addEventListener("close", onclose);
	document.getElementById("containerDiv").style.display = "none";
	document.getElementById("canvasDiv").style.display = "block";
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
			drawPoints(data.x,data.y);
		}
		else if(data.action == "draw_end"){
			ctx.closePath();
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
	
	
}

function onclose(){
	console.log("Disconnected from room");
}

function sendMsg(x,y,action){
	dataDict = {
		'type': '3',
		'action': action,
		'x': x,
		'y': y,
	}
	socketRoom.send(JSON.stringify(dataDict));
}

function getCanvasData(){
	var canvas = document.getElementById("myCanvas");
	var data = canvas.toDataURL();
	return data;

}

