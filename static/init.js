HOST = "localhost" // Host name of the server
PORT = 8000 // Port at which server is running

// create socket object for server Connection
var socket = new WebSocket('ws://localhost:8000');
var socketRoom;

// get canvas
var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");
var started = false;

// Fill Window Width and Height
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// image object to load the canvas data from server
var img = new Image();

// colors to indicate different clients
var colors = ["#2ECC71","#9B59B6","#3498DB","E03E1B"]
var colorIdx = 0

// to create random character from alphaber
const characters ='ABCDEFGHIJKLMNOPQRSTUVWXYZ';

var totalClients = 0; // to keep track of no of clients in the rooom
var eraseFlag = false; // set erase flag to start erasing
var brushSize = 4; // default brush size


/**
 * @description: function to set message and show the snackbar
 * @param {string} message - message to be shown in the snackbar
 */
function set_snackbar(message) {
    var x = document.getElementById("snackbar");
    x.innerHTML = message;
    x.className = "show";
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}