// var ws;
var ws;

jQuery(document).ready(function(){
	console.log('start connection...');
  	var timerID = 0;
 	function keepAlive() {
	    // 14000 was the default
	    var timeout = 140000;
	    if (ws.readyState == ws.OPEN) {
	      console.log('keep alive: ' + timerID++);
	      ws.send('');
	    } else {
	      console.log('websocket IS CLOSED!! ');
	    }
	    timerId = setTimeout(keepAlive, timeout);
  	}
  	function cancelKeepAlive() {
   	 	if (timerId) {
     		clearTimeout(timerId);
    	}
  	}

	socketinit();
	keepAlive();
	jQuery('#msg').focus();

	jQuery('#msg').keydown(function (e) {
	    if (e.keyCode == 13 && jQuery('#msg').val()) {
	      console.log('ws: ', ws);
	      if (ws.readyState == 1) {
	        ws.send(jQuery('#msg').val());
	        jQuery('#msg').val('');
	      } else {
	        console.log('Connection with server is lost');
	    	socketinit();
	      }
	    }
  	});

	
});

function socketinit() {
  console.log('init websocket....');

  let o = window.location.origin;
  let uri = o.replace("http", "ws");
  console.log('location.origin NEW: ', uri)

  ws = new WebSocket(uri + '/k8s/log');
  ws.onopen = function () {
    console.log('websocket opened');
  };

  ws.onmessage = function (msg) {
  	console.log("recive msg",msg.data);
    jQuery("#reply").append("<span class=\"msg\">"+msg.data+"</span>");
  };
  ws.onclose = function (evt) {
    console.log('websocket onclose');
  }
}