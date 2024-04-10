
// can define this through other means
const HEADER_HEIGHT = 56;

// global variable for the timeout id
let timeout_id = null;
const TIME_OUT_TIME = 4000; // trigger timeout after x milliseconds

// rotation: degree (0 is upwards, 90 is right, 270 is left)
// position values: must be less than the height of the image. 
let user_x = 0;
let user_y = 0;

// garner more statistics:
let num_received = 0;
let total_delay = 0;

// Paths
let canvas_paths = Array();

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

            // const rotation = calculateAngleWithYAxis(user_x, user_y, new_user_x, new_user_y);

            const rotation = data.rotation;
            user_x = new_user_x;
            user_y = new_user_y;

            // Time related things
            clearTimeout(timeout_id);
            timeout_id = setTimeout(websocketTimeout, TIME_OUT_TIME);

            const delay = Date.now()/1000 - data.time;

            total_delay += delay;
            const avg = total_delay / (++num_received);
            // console.log(`Time elapsed(${delay}), total(${avg}), x_pos(${data.x_pos}), y_pos(${data.y_pos}), rot(${rotation})`);

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

    $("#exit-navigation-button").on("click", function() {
        toggle_navigation(false);

        const canvas = document.getElementById('userPaths');
        const context = canvas.getContext('2d');
        context.clearRect(0, 0, canvas.width, canvas.height);

        canvas_paths = Array();
    });

});


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

    submitFormAJAX(user_x, user_y);
});


function submitFormAJAX(u_x, u_y) {
    const floorId = JSON.parse(document.getElementById('floor-id').textContent);

    $.ajax({
        type: 'POST',
        url: "/update_navigation_directions",
        data: {
            floor_id: floorId,
            room_name: $("#roomInput").val(),
            user_x: u_x,
            user_y: u_y,

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
    // console.log(result);

    // mvoe that canvas thing
    // set the userPaths div size to be equal to the image.
    $("#userPaths").attr("width", $("#floorImg").width());
    $("#userPaths").attr("height", $("#floorImg").height());

    // draw the navigation lines
    const directions = result.directions;
    drawNavigationLineWrapper(directions);

    console.log("😡😡😡😡");
    console.log(directions, result);
    canvas_paths = directions;

    // update the div with the directions
    // TODO
    toggle_navigation(true);
}

function toggle_navigation(show_navigation) {
    if (show_navigation) {
        $("#location-select").hide();
        $("#navigation-info").show();
        $("#navigation-view").show();
    } else {
        $("#location-select").show();
        $("#navigation-info").hide();
        $("#navigation-view").hide();
    }
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
    const canvas = document.getElementById('userPaths');
    const context = canvas.getContext('2d');
  
    context.beginPath();
    context.moveTo(startX, startY);
    context.lineTo(endX, endY);
    context.lineWidth = 4;        // Adjust line thickness
    context.strokeStyle = 'blue'; // Set line color
    context.stroke();
}

function drawNavigationLineWrapper(directions) {
    const canvas = document.getElementById('userPaths');
    const context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.width, canvas.height);

    for (let i=0; i < directions.length; i++) {
        directions.forEach(line => {
            drawNavigationLine(line[0], line[1], line[2], line[3]);
        });
    }
}


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

    // move the position of the div to the same offset as the image
    $("#userPaths").css({top: new_top, left: new_left});
    realign_paths(width, height);
    drawNavigationLineWrapper(canvas_paths);

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


// align path
function realign_paths(width, height) {
    // Only do things if we are able...
    // i.e. we are connectedd to the websocket, and paths have been selected. 
    const connected_to_ws = !($("#loadingScreen").is(":visible"));
    if ((canvas_paths.length > 0) && connected_to_ws) {

        // first, determine if the first path is vertical or horizontal
        let vertical = ((canvas_paths[0][0] - canvas_paths[0][2]) == 0);
        // align the path with the user's y position if vertical, vice versa. 
        if (vertical) {
            canvas_paths[0][1] = Math.round(height);
        } else {

            canvas_paths[0][0] = Math.round(width);
        }

        // ((canvas_paths[0][0] - width)^2 + (canvas_paths[0][1]-height)^2)^(1/2);
        const distance = Math.sqrt(
                    Math.pow(canvas_paths[0][0] - width, 2) + 
                    Math.pow(canvas_paths[0][1] - height, 2)
        );

        // Secondly, if we are still too far away, then call for new navigation
        // paths...
        if (distance > 50) {
            submitFormAJAX(width, height);
        }

        // Thirdly, if the line segment is too short, we should ask for nav
        // instructions using the end of the line segment as the user location
        // if (canvas_paths.length > 2) {
        //     submitFormAJAX(canvas_paths[0][2], canvas_paths[0][3]);
        // }
    }
}
 