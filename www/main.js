/**
    * Setup all visualization elements when the page is loaded.
    */
function init() {

    var size_x = window.innerHeight/2 + window.innerHeight/6 ; // Tamaño del mapa 
    var size_y = window.innerHeight/2 + window.innerHeight/6;
    var ros = new ROSLIB.Ros({ // Conexión con ROS
        url: 'ws://localhost:9090'
    });
    ros.on('connection', function () {
        document.getElementById("status").innerHTML = "Conectado"; // Cambia el estado de la conexión
    });

    ros.on('error', function (error) {
        document.getElementById("status").innerHTML = "Error"; 
    });

    ros.on('close', function () {
        document.getElementById("status").innerHTML = "Terminada";
    });

    var patrolpublisherx = new ROSLIB.Topic({ // Publica las coordenadas x de los puntos en el topic /patrol/coords/x
        ros: ros,
        name: '/patrol/coords/x',
        messageType: 'std_msgs/Float32MultiArray'
    });
    var patrolpublishery = new ROSLIB.Topic({ // Publica las coordenadas y de los puntos en el topic /patrol/coords/y
        ros: ros,
        name: '/patrol/coords/y',
        messageType: 'std_msgs/Float32MultiArray'
    });

    var image_topic = new ROSLIB.Topic({ // Suscripción a la imagen de la cámara
        ros: ros, name: '/camera/rgb/image_raw/compressed',
        messageType: 'sensor_msgs/CompressedImage'
    });
    var person_topic = new ROSLIB.Topic({ // Suscripción a la imagen de la cámara con la detección de personas
        ros: ros, name: '/person_tracking/deepsort_image/compressed',
        messageType: 'sensor_msgs/CompressedImage'
    });

    var person_number = new ROSLIB.Topic({ // Suscripción al número de personas detectadas
        ros: ros, name: '/person_tracking/person_detections',
        messageType: 'std_msgs/Int32'
    });
    image_topic.subscribe(function (message) { // Callback de la imagen de la cámara
        document.getElementById('my_image').src = "data:image/jpg;base64," + message.data; 

    });
    person_topic.subscribe(function (message) { // Callback de la imagen de la cámara con la detección de personas
        document.getElementById('person_image').src = "data:image/jpg;base64," + message.data;
    });

    person_number.subscribe(function (message) { // Callback del número de personas detectadas
        document.getElementById("person-detec").innerHTML = message.data;
    });

    var viewer = new ROS2D.Viewer({ // Creación del mapa en el navegador web
        divID: 'map',
        width: size_x, // Tamaño del mapa x
        height: size_y // Tamaño del mapa y
    });

    //  Configura el cliente de mapa de ocupación para obtener el mapa del servidor de mapa de ROS.
    var gridClient = new ROS2D.OccupancyGridClient({
        ros: ros,
        rootObject: viewer.scene,
        continuous: true
    });
    // Escucha el evento de cambio de mapa y escala el mapa para que se ajuste a la ventana.
    gridClient.on('change', function () {
        viewer.scaleToDimensions(gridClient.currentGrid.width, gridClient.currentGrid.height); // Escala el mapa
        viewer.shift(gridClient.currentGrid.pose.position.x, gridClient.currentGrid.pose.position.y);
        console.log(gridClient.currentGrid.width + " " + gridClient.currentGrid.height); // Debug 
        console.log(gridClient.currentGrid.pose.position.x + " " + gridClient.currentGrid.pose.position.y);

    });
    document.getElementById('map').addEventListener('click', function (event) { // Evento de click en el mapa
        onMapClick(event); // Llama a la función onMapClick
    });
    // Función que transforma las coordenadas de la pantalla en coordenadas del mapa
    function screentoMap(x0, y0) {

        min_x = (gridClient.currentGrid.pose.position.x + gridClient.currentGrid.width) * -1; //Valor mínimo de x en el mapa
        max_x = gridClient.currentGrid.pose.position.x + gridClient.currentGrid.width; //Valor máximo de x en el mapa
        min_y = gridClient.currentGrid.pose.position.y + gridClient.currentGrid.height; //Valor mínimo de y en el mapa
        max_y = (gridClient.currentGrid.pose.position.y + gridClient.currentGrid.height) * -1; //Valor máximo de y en el mapa
        var mapCoords = { // Coordenadas del mapa
            x: (x0 - 0) * (max_x - min_x) / (size_x) + min_x, // Transformación de las coordenadas de la pantalla a las del mapa en x
            y: (y0 - 0) * (max_y - min_y) / (size_y) + min_y, // Transformación de las coordenadas de la pantalla a las del mapa en y
        };
        return mapCoords;
    }
    var line = new createjs.Shape(); // Creación de la línea

    var coordsxy = { 
        x: 0,
        y: 0
    };
    // Array de coordenadas 
    var coords = [];

    function onMapClick(event) {
        //  Obtener las coordenadas del evento de clic.
        var x = event.offsetX;
        var y = event.offsetY;

        if (x <= size_x && y <= size_y) { // Si las coordenadas están dentro del mapa

            // Transforma las coordenadas de la pantalla en coordenadas del mapa.
            var mapCoords = screentoMap(x, y);

            // Añade las coordenadas al array.
            coords.push(mapCoords);

            console.log('The map was clicked at (' + mapCoords.x + ', ' + mapCoords.y + ') in the map frame!'); // Debug

            if (coords.length > 1) {
                console.log(coords.length);
                // Se dibuja la línea en el mapa entre los dos últimos puntos del array.
                line.graphics.setStrokeStyle(0.2); // Grosor de la línea
                line.graphics.beginStroke("red");
                line.graphics.moveTo(coords[coords.length - 2].x, coords[coords.length - 2].y * -1); // Se multiplica por -1 para que la línea se dibuje correctamente
                line.graphics.lineTo(coords[coords.length - 1].x, coords[coords.length - 1].y * -1); 
                line.graphics.endStroke(); 
                gridClient.rootObject.addChild(line); 
            }

        }

    }

    var clearbutton = document.getElementById("clear");  // Botón para borrar la patrulla

    clearbutton.addEventListener("click", function () {
        // Elimina la línea del mapa.
        gridClient.rootObject.removeChild(line);
        line = new createjs.Shape();
        // Se vacía el array.
        coords = [];
    });

    var savebutton = document.getElementById("savep");  // Botón para guardar la patrulla

    savebutton.addEventListener("click", function () {
        if (coords.length < 2) {
            alert("Por favor, dibuje una patrulla");
            return;
        }
        // Creación del json con el array de coordenadas.
        var json = JSON.stringify(coords);
        // Creación del blob.
        var blob = new Blob([json], { type: "application/json" });
        // Prompt para introducir el nombre de la patrulla.
        var filename = prompt("Por favor, introduzca el nombre de la patrulla", "patrulla");

        //  Creación del enlace para descargar el archivo.
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');

        a.download = filename + ".json";
        a.href = url;
        a.textContent = "Download file!"; 
        document.body.appendChild(a); 
        a.click();
        document.body.removeChild(a); 
    });

    var loadbutton = document.getElementById("loadp");  //  Botón para cargar una patrulla

    loadbutton.addEventListener("click", function () {

        // Abre el explorador de archivos.
        var input = document.createElement('input');
        input.type = 'file';
        input.onchange = e => {
            // Obtiene el archivo seleccionado.
            var file = e.target.files[0];
            // Lee el archivo.
            var reader = new FileReader();
            reader.readAsText(file, "UTF-8");
            reader.onload = readerEvent => {
                // Parsea el json.
                var json = JSON.parse(readerEvent.target.result);
                // Vacía el array.
                coords = [];
                // Elimina la línea del mapa si existen
                gridClient.rootObject.removeChild(line);
                line = new createjs.Shape();
                // Añade las coordenadas al array.
                for (var i = 0; i < json.length; i++) {
                    coords.push(json[i]);
                }
                // Dibuja la línea en el mapa.
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

    var runbutton = document.getElementById("run");  // Botón para ejecutar la patrulla

    runbutton.addEventListener("click", function () {
        if (coords.length < 2) {
            alert("Patrulla invalida"); // Si no hay suficientes coordenadas
            return;
        }

        // console.log(coords); // Debug
        var coordsmsgx = [];
        var coordsmsgy = [];
        for (var i = 0; i < coords.length; i++) {
            coordsmsgx.push(coords[i].x); // Se añaden las coordenadas al array
            coordsmsgy.push(coords[i].y);
        }
        var msgcoordx = new ROSLIB.Message({ // Se crea el mensaje
            data: coordsmsgx
        });
        var msgcoordy = new ROSLIB.Message({
            data: coordsmsgy
        });

        // console.log(coordsmsgx);

        patrolpublisherx.publish(msgcoordx); // Se publica el mensaje
        patrolpublishery.publish(msgcoordy); 

    });
}