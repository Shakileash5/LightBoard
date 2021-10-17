var myCanvas = document.getElementById("myCanvas");
var ctx = myCanvas.getContext("2d");
var started = false;
    // Fill Window Width and Height
myCanvas.width = window.innerWidth;
myCanvas.height = window.innerHeight;

	// Set Background Color
//ctx.fillStyle="#fff";
//ctx.fillRect(0,0,myCanvas.width,myCanvas.height);

function start_draw(evt, x=null, y=null, flag = 0){
    if(flag == 0){
        x = evt.offsetX;
        y = evt.offsetY;
        sendMsgAsync(evt.offsetX,evt.offsetY,brushSize,"draw_start");
    }
    console.log("Started");
    started = true;
}

function move_draw(evt, x=null, y=null, brushSize=null, flag = 0){
    if(flag == 0){
        x = evt.offsetX;
        y = evt.offsetY;
        sendMsgAsync(evt.offsetX,evt.offsetY,brushSize,"draw_move");
    }
    ctx.strokeStyle = "#000";
	ctx.lineWidth = brushSize;
	ctx.stroke();
    if(started && eraseFlag && flag == 0){
		ctx.clearRect(evt.offsetX - 0, evt.offsetY - 0, brushSize*2, brushSize*2);
		sendMsgAsync(evt.offsetX,evt.offsetY,brushSize,"erase");
	}
     
}

function end_draw(evt) {
		started = false;
		if(!eraseFlag){
			sendMsgAsync(evt.offsetX,evt.offsetY,brushSize,"draw_end");
		}
		//sendMsg(evt.offsetX,evt.offsetY,"draw_end");
}