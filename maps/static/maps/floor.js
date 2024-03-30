
// can define this through other means
const HEADER_HEIGHT = 56;

// global variable for the timeout id
let timeout_id = null;
const TIME_OUT_TIME = 4000; // trigger timeout after x milliseconds

// hardcoded test values. 
// rotation: degree (0 is upwards, 90 is right, 270 is left)
// position values: must be less than the height of the image. 
// let userY = 632;
// let userX = 776;
let userX = 330;
let userY = 709;
let movingUp = true;
let rotation = 0;


// garner more statistics:
let num_received = 0;
let total_delay = 0;

$(document).ready(function(){

    const floorId = JSON.parse(document.getElementById('floor-id').textContent);
    const tagId = JSON.parse(document.getElementById('tag-id').textContent);
    const ws_string =`ws://${window.location.host}/ws/get_location/${floorId}/${tagId}/`;

    const floorScaling = JSON.parse(document.getElementById('floor-scaling').textContent);

    // get the user position using websocket
    const webSocket = new WebSocket(ws_string);

    webSocket.onmessage = function(e) {
        const data = JSON.parse(JSON.parse(e.data).message);

        if (data.type == "update") {
            // hide the banner
            $("#loadingScreen").hide();

            const user_x = data.x_pos * floorScaling.x_scaling + floorScaling.x_offset;
            const user_y = data.y_pos * floorScaling.y_scaling + floorScaling.y_offset;

            const rotation = data.rotation;

            // Time related things
            clearTimeout(timeout_id);
            timeout_id = setTimeout(websocketTimeout, TIME_OUT_TIME);

            const delay = Date.now()/1000 - data.time;

            total_delay += delay;
            const avg = total_delay / (++num_received);
            console.log(`Time elapsed(${delay}), total(${avg})`);

            changeImgPos(user_x, user_y, rotation);
        } else {
            // maybe the tag disconnected 
            $("#loadingScreen").show();
        }
        
    };

    webSocket.onclose = function(e) {
        // show loading banner
        clearTimeout(timeout_id);

        $("#loadingScreen").show();

        console.error("socket closed early, unexpectedly.")
    }

    // // change position to center over a hallway (i.e the user's initial pos)
    // changeImgPos(userX, userY, rotation);
    // console.log(userX, userY);

    // emulate server response?
    // update user's position, update the paths we need to draw?
    $("#userPaths").click(function() {
        changeImgPos(userX, userY, rotation);
    });

});

function websocketTimeout() {
    console.log("running timeout function");
    $("#loadingScreen").show();
}


function drawNavigationLine(startX, startY, endX, endY) {
    // const canvas = document.getElementById('userPaths');
    // const context = canvas.getContext('2d');
  
    // context.beginPath();
    // context.moveTo(startX, startY);
    // context.lineTo(endX, endY);
    // context.lineWidth = 4;        // Adjust line thickness
    // context.strokeStyle = 'blue'; // Set line color
    // context.stroke();
  }
  

// test data. 
const positions = [
    { startX: 776, startY: 632, endX: 776, endY: 233 },
    { startX: 776, startY: 233, endX: 308, endY: 233 },
    { startX: 308, startY: 233, endX: 308, endY: 313 },
];

  

/**
 * Change the image position to center over a width and height pixel location
 * Takes into consideration the current height and width of the screen
 */
function changeImgPos(width, height, rotation) {

    const window_height = $(window).height() - HEADER_HEIGHT;
    const window_width = $(window).width();

    const new_top = -height + (window_height / 2);
    const new_left = -width + (window_width / 2);
    $("#floorImg").css({top: new_top, left: new_left});

    // set the userPaths div size to be equal to the image.
    $("#userPaths").attr("width", $("#floorImg").width());
    $("#userPaths").attr("height", $("#floorImg").height());

    // draw the paths onto the div
    for (let i=0; i < 1; i++) {
        positions.forEach(line => {
            drawNavigationLine(line.startX, line.startY, line.endX, line.endY);
        });

    }

    // move the position of the div to the same offset as the image
    $("#userPaths").css({top: new_top, left: new_left});

    // set position of arrow to be centered on the screen
    // console.log($("#userPos").height()/2);
    $("#userPos").css({
        visibility: "visible",
        top: window_height/2 - 15,
        left: window_width/2 - 10,
        rotate: `${rotation}deg`
    });

    // console.log(rotation);
}


