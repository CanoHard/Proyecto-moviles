/**
    * Setup all visualization elements when the page is loaded.
    */
function init() {
    // Connect to ROS.
    var size_x = window.innerHeight/2 + window.innerHeight/6 ;
    var size_y = window.innerHeight/2 + window.innerHeight/6;
    var ros = new ROSLIB.Ros({
        url: 'ws://localhost:9090'
    });
    ros.on('connection', function () {
        document.getElementById("status").innerHTML = "Conectado";
    });

    ros.on('error', function (error) {
        document.getElementById("status").innerHTML = "Error";
    });

    ros.on('close', function () {
        document.getElementById("status").innerHTML = "Terminada";
    });

    var patrolpublisherx = new ROSLIB.Topic({
        ros: ros,
        name: '/patrol/coords/x',
        messageType: 'std_msgs/Float32MultiArray'
    });
    var patrolpublishery = new ROSLIB.Topic({
        ros: ros,
        name: '/patrol/coords/y',
        messageType: 'std_msgs/Float32MultiArray'
    });

    var image_topic = new ROSLIB.Topic({
        ros: ros, name: '/camera/rgb/image_raw/compressed',
        messageType: 'sensor_msgs/CompressedImage'
    });
    var person_topic = new ROSLIB.Topic({
        ros: ros, name: '/person_tracking/deepsort_image/compressed',
        messageType: 'sensor_msgs/CompressedImage'
    });
    image_topic.subscribe(function (message) {
        document.getElementById('my_image').src = "data:image/jpg;base64," + message.data;

    });
    person_topic.subscribe(function (message) {
        document.getElementById('person_image').src = "data:image/jpg;base64," + message.data;
    });
    // Create the main viewer.
    var viewer = new ROS2D.Viewer({
        divID: 'map',
        width: size_x,
        height: size_y
    });

    // Setup the map client.
    var gridClient = new ROS2D.OccupancyGridClient({
        ros: ros,
        rootObject: viewer.scene,
        continuous: true
    });
    // Scale the canvas to fit to the map
    gridClient.on('change', function () {
        viewer.scaleToDimensions(gridClient.currentGrid.width, gridClient.currentGrid.height);
        viewer.shift(gridClient.currentGrid.pose.position.x, gridClient.currentGrid.pose.position.y);
        console.log(gridClient.currentGrid.width + " " + gridClient.currentGrid.height);
        console.log(gridClient.currentGrid.pose.position.x + " " + gridClient.currentGrid.pose.position.y);

    });
    document.getElementById('map').addEventListener('click', function (event) {
        // Call the custom event.
        onMapClick(event);
    });
    // Implement a function that transforms the screen coordinates into the map coordinates.
    function screentoMap(x0, y0) {

        min_x = (gridClient.currentGrid.pose.position.x + gridClient.currentGrid.width) * -1;
        max_x = gridClient.currentGrid.pose.position.x + gridClient.currentGrid.width;
        min_y = gridClient.currentGrid.pose.position.y + gridClient.currentGrid.height;
        max_y = (gridClient.currentGrid.pose.position.y + gridClient.currentGrid.height) * -1;
        var mapCoords = {
            x: (x0 - 0) * (max_x - min_x) / (size_x) + min_x,
            y: (y0 - 0) * (max_y - min_y) / (size_y) + min_y,
        };
        return mapCoords;
    }
    var line = new createjs.Shape();

    var coordsxy = {
        x: 0,
        y: 0
    };
    // Create an array to store the coordinates of the clicks.
    var coords = [];

    function onMapClick(event) {
        // Get the coordinates of the click event.
        var x = event.offsetX;
        var y = event.offsetY;

        if (x <= size_x && y <= size_y) {

            // Transform the screen coordinates into the map coordinates.
            var mapCoords = screentoMap(x, y);

            // Add the coordinates to the array.
            coords.push(mapCoords);

            console.log('The map was clicked at (' + mapCoords.x + ', ' + mapCoords.y + ') in the map frame!');

            if (coords.length > 1) {
                console.log(coords.length);
                // Draw a line between the last two clicks.
                line.graphics.setStrokeStyle(0.2);
                line.graphics.beginStroke("red");
                line.graphics.moveTo(coords[coords.length - 2].x, coords[coords.length - 2].y * -1);
                line.graphics.lineTo(coords[coords.length - 1].x, coords[coords.length - 1].y * -1);
                line.graphics.endStroke();
                gridClient.rootObject.addChild(line);
            }

        }

    }

    var clearbutton = document.getElementById("clear");  // Get the button

    clearbutton.addEventListener("click", function () {
        // Rremove all the lines from the map.
        gridClient.rootObject.removeChild(line);
        line = new createjs.Shape();
        // Clear the array.
        coords = [];
    });

    var savebutton = document.getElementById("savep");  // Get the button

    savebutton.addEventListener("click", function () {
        if (coords.length < 2) {
            alert("Por favor, dibuje una patrulla");
            return;
        }
        // Create a json object with the coordinates.
        var json = JSON.stringify(coords);
        // Create a blob with the json object.
        var blob = new Blob([json], { type: "application/json" });
        // Create promp to enter the name of the file.
        var filename = prompt("Por favor, introduzca el nombre de la patrulla", "patrulla");

        // Create a link to download the blob.
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');

        a.download = filename + ".json";
        a.href = url;
        a.textContent = "Download file!";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    });

    var loadbutton = document.getElementById("loadp");  // Get the button

    loadbutton.addEventListener("click", function () {

        // Open file explorer to select the file.
        var input = document.createElement('input');
        input.type = 'file';
        input.onchange = e => {
            // Get the file.
            var file = e.target.files[0];
            // Create a reader to read the file.
            var reader = new FileReader();
            reader.readAsText(file, "UTF-8");
            reader.onload = readerEvent => {
                // Get the json object from the file.
                var json = JSON.parse(readerEvent.target.result);
                // Clear the array.
                coords = [];
                // Clear the lines from the map.
                gridClient.rootObject.removeChild(line);
                line = new createjs.Shape();
                // Add the coordinates to the array.
                for (var i = 0; i < json.length; i++) {
                    coords.push(json[i]);
                }
                // Draw the lines.
                for (var i = 0; i < coords.length - 1; i++) {
                    line.graphics.setStrokeStyle(0.2);
                    line.graphics.beginStroke("red");
                    line.graphics.moveTo(coords[i].x, coords[i].y * -1);
                    line.graphics.lineTo(coords[i + 1].x, coords[i + 1].y * -1);
                    line.graphics.endStroke();
                    gridClient.rootObject.addChild(line);
                }
            }
        }
        input.click();
    });

    var runbutton = document.getElementById("run");  // Get the button

    runbutton.addEventListener("click", function () {
        if (coords.length < 2) {
            alert("Patrulla invalida");
            return;
        }

        // console.log(coords);
        var coordsmsgx = [];
        var coordsmsgy = [];
        for (var i = 0; i < coords.length; i++) {
            coordsmsgx.push(coords[i].x);
            coordsmsgy.push(coords[i].y);
        }
        var msgcoordx = new ROSLIB.Message({
            data: coordsmsgx
        });
        var msgcoordy = new ROSLIB.Message({
            data: coordsmsgy
        });

        // console.log(coordsmsgx);

        patrolpublisherx.publish(msgcoordx);
        patrolpublishery.publish(msgcoordy);

    });
}