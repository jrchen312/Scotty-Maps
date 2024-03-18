
// can define this through other means
const HEADER_HEIGHT = 56;

// hardcoded test values. 
// rotation: degree (0 is upwards, 90 is right, 270 is left)
// position values: must be less than the height of the image. 
let userY = 632;
let userX = 776;
let movingUp = true;
let rotation = 0;

$(document).ready(function(){
    var floorImg = $( "#floorImg" );

    // get the user position using http request
    function getUserLocation() {
        $.ajax({
            url: 'http://3.90.105.209:8000/get_user_location',
            type: 'GET',  // Specify the HTTP method
            dataType: 'json',  // Expect a JSON response from the server
            success: function(data) {
                console.log("User Location:", data);

                // Display the recorded position... 
                const user_x = data.x_pos * $("#floorImg").width();
                const user_y = data.y_pos * $("#floorImg").height();
                console.log(data.x_pos, data.y_pos, user_x, user_y);

                changeImgPos(user_x, user_y, 0);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                // Handle errors
                console.error("Error retrieving location:", textStatus, errorThrown);
            }
        });
    }

    getUserLocation();
    setInterval(getUserLocation, 500);

    // change position to center over a hallway (i.e the user's initial pos)
    // changeImgPos(userX, userY, rotation);

    // emulate server response?
    // update user's position, update the paths we need to draw?
    $("#userPaths").click(function() {
        
        // move user position
        if (movingUp) {
            userY = userY - 10;
            if (userY <=232) {
                movingUp = false;
            }
        } else {
            rotation = 270;
            userX = userX - 10;
        }
        
        changeImgPos(userX, userY, rotation);
        // redraw the paths

    });

});


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

}


