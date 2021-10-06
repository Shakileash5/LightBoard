window.onload = function() {
	var myCanvas = document.getElementById("myCanvas");
	var ctx = myCanvas.getContext("2d");
    
    // Fill Window Width and Height
    myCanvas.width = window.innerWidth;
	myCanvas.height = window.innerHeight;

	// Set Background Color
    ctx.fillStyle="#fff";
    ctx.fillRect(0,0,myCanvas.width,myCanvas.height);
	
	var started = false;
	const socket = io('http://localhost:1200');
	socket.on('connect', () => {
      console.log("socket connected");
    });

    


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
			console.log("end");
		}
	};

	function startDraw(evt) {
			
			ctx.beginPath();
			ctx.moveTo(
				evt.pageX,
				evt.pageY
			);

			started = true;

		}


	function drawMove(evt) {

			if (started) {
				ctx.lineTo(
					evt.pageX,
					evt.pageY
				);
				
				ctx.strokeStyle = "#000";
				ctx.lineWidth = 5;
				ctx.stroke();
			}

		}
	
	function endDraw(evt) {
			started = false;
			console.log("end");
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