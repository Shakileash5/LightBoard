var socket = new WebSocket('ws://localhost:8000');
var socketRoom;

// get canvas
var myCanvas = document.getElementById("myCanvas");
var ctx = myCanvas.getContext("2d");
var started = false;

// Fill Window Width and Height
myCanvas.width = window.innerWidth;
myCanvas.height = window.innerHeight;

var img = new Image();
