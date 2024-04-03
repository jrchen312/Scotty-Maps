
// can define this through other means
const HEADER_HEIGHT = 56;

// global variable for the timeout id
let timeout_id = null;
const TIME_OUT_TIME = 4000; // trigger timeout after x milliseconds

// hardcoded test values. 
// rotation: degree (0 is upwards, 90 is right, 270 is left)
// position values: must be less than the height of the image. 
let user_x = 0;
let user_y = 0;

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

            new_user_x = data.x_pos * floorScaling.x_scaling + floorScaling.x_offset;
            new_user_y = data.y_pos * floorScaling.y_scaling + floorScaling.y_offset;

            const rotation = calculateAngleWithYAxis(user_x, user_y, new_user_x, new_user_y);

            // const rotation = data.rotation;
            user_x = new_user_x;
            user_y = new_user_y;

            // Time related things
            clearTimeout(timeout_id);
            timeout_id = setTimeout(websocketTimeout, TIME_OUT_TIME);

            const delay = Date.now()/1000 - data.time;

            total_delay += delay;
            const avg = total_delay / (++num_received);
            console.log(`Time elapsed(${delay}), total(${avg}), x_pos(${data.x_pos}), y_pos(${data.y_pos}), rot(${rotation})`);

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

});


function calculateAngleWithYAxis(x_pos, y_pos, new_x_pos, new_y_pos) {
    // Calculate the slope
    const slope = (new_y_pos - y_pos) / (new_x_pos - x_pos);
  
    // Calculate angle with respect to x-axis (in radians)
    let angleWithXAxis = Math.atan(slope); 
  
    // Convert to degrees
    angleWithXAxis = angleWithXAxis * (180 / Math.PI);
  
    // Adjust for inverted y-axis
    const angleWithYAxis = 180 - angleWithXAxis;
  
    return angleWithYAxis;
}

// Access the form on map.html and change the default behavior of submit
// to submit with AJAX. 
$(document).on('submit','#form',function(e){
    e.preventDefault();

    // Initial form validation
    const roomName = $("#roomInput").val().trim();

    if (roomName === "" || isNaN(user_x) || isNaN(user_y) || user_x === 0 || user_y === 0) {
        // Display an error message to the user (modify as needed)
        alert("Please fill in all fields with valid values. Coordinates cannot be 0.");
        return;  // Stop form submission 
    }

    submitFormAJAX(e);
});


function submitFormAJAX(e) {
    $.ajax({
        type: 'POST',
        url: e.currentTarget.action,
        data: {
            room_name: $("#roomInput").val(),
            user_x: user_x,
            user_y: user_y,

            // https://electrictoolbox.com/jquery-form-elements-by-name/
            csrfmiddlewaretoken:$('#form input[name=csrfmiddlewaretoken]').val()
        },
        success: updateMapNavigation,
        error: updateError
    });
}


/**
 * Main function to display the map navigation... 
 */
function updateMapNavigation(result) {
    console.log(result);

    // draw the navigation lines
    // TODO

    // update the div with the directions
    // TODO
}

/**
 * Parse xhr error and display it
 */
function updateError(xhr) {
    if (xhr.status == 0) {
        displayError("Cannot connect to server")
        return
    }

    if (!xhr.getResponseHeader('content-type') == 'application/json') {
        displayError("Received status=" + xhr.status)
        return
    }

    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }

    displayError(response)
}


/**
 * Basic visual message to display an issue with the form submission
 */
function displayError(message) {
    $("#error").html(`
        <div class="alert alert-danger" role="alert">
            An error occurred: ${message}
        </div>
    `);
}


/*
 * This function is run when the tag device is timed out
 * i.e. the tag device has stopped sending location data in past few seconds
 */
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

    // // draw the paths onto the div
    // for (let i=0; i < 1; i++) {
    //     positions.forEach(line => {
    //         drawNavigationLine(line.startX, line.startY, line.endX, line.endY);
    //     });

    // }

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


