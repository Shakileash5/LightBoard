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

var colors = ["#2ECC71","#9B59B6","#3498DB","E03E1B"]
var colorIdx = 0

const characters ='ABCDEFGHIJKLMNOPQRSTUVWXYZ';

var totalClients = 0;
var eraseFlag = false;
var brushSize = 4;
