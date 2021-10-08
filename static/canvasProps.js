var myCanvas = document.getElementById("myCanvas");
var ctx = myCanvas.getContext("2d");
var started = false;
    // Fill Window Width and Height
myCanvas.width = window.innerWidth;
myCanvas.height = window.innerHeight;

	// Set Background Color
ctx.fillStyle="#fff";
ctx.fillRect(0,0,myCanvas.width,myCanvas.height);