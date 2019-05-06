var connected=false;
var socket = null;
function request_data(){
	if(connected){
	    socket.emit('request_data');
	}
}

window.setInterval(request_data, 100);


// setup data series
var x_data = {
    label: 'X',
    data: [0],
    borderColor: window.chartColors.red,
    backgroundColor: 'rgba(0,0,0,0)',
    fill: false,
}

var y_data = {
    label: 'Y',
    data: [0],
    borderColor: window.chartColors.blue,
    backgroundColor: 'rgba(0,0,0,0)',
    fill: false,
}

var z_data = {
    label: 'Z',
    data: [0],
    borderColor: window.chartColors.green,
    backgroundColor: 'rgba(0,0,0,0)',
    fill: false,
}


// Listen for async-reply message from main process
var datapoints = 0;
function streamData(raw_data) {

    // increment datapoints count
    datapoints++;
    
    // parse the input stream
    var accel_data = raw_data//.trim().split('\t');
    window.myLine.data.datasets[0].data.push(accel_data['x']);
    window.myLine.data.datasets[1].data.push(accel_data['y']);
    window.myLine.data.datasets[2].data.push((accel_data['z'] - 1.0));
    window.myLine.data.labels.push(datapoints++);
    
    // shift the queue to keep a maximum length of 200, so we don't overload the graph
    var maxLength = 100;
    var maxTime = 10000;
    if (window.myLine.data.datasets[0].data.length > maxLength)
        window.myLine.data.datasets[0].data.shift();
    if (window.myLine.data.datasets[1].data.length > maxLength)
        window.myLine.data.datasets[1].data.shift();
    if (window.myLine.data.datasets[2].data.length > maxLength)
        window.myLine.data.datasets[2].data.shift();
    if (window.myLine.data.labels.length > maxLength)
        window.myLine.data.labels.shift();
    if (datapoints > maxTime)
        datapoints = 0;
    
    // update the chart
    window.myLine.update();
    console.log(window.myLine.data);
    
    // set statistics values
	/*
    for (i = 0; i < 3; i++)
    {
        var dimension = 'x';
        dimension = String.fromCharCode(dimension.charCodeAt(0) + i);
        var sigma_str = "&sigma;<sub>" + dimension.toString() + "</sub> ";
        var sigma_val = math.round(math.std(window.myLine.data.datasets[i].data), 6).toString();
        document.getElementById("uc-stats-value-" + dimension).innerHTML = sigma_str + sigma_val;
    }*/

};

// set micro state
function setConnected(arg=false) {
    
    // set of messaging for micro controller state
    var failure = "Failed to connect to IMU";
    var success = "Connected!";
    var connected = 'img/connected.svg';
    var disconnected = 'img/disconnected.svg';
    
    // if connected, set the image and text to reflect
    if(arg){
        document.getElementById('uc-status-txt').innerHTML = success;
        document.getElementById('uc-status-img').src = connected;
        }
    else{
        document.getElementById('uc-status-txt').innerHTML = failure;
        document.getElementById('uc-status-img').src = disconnected;
    }
};

function establishSocketIO() {

    // establish socket connection to our own server
    socket = io.connect('http://' + document.domain + ':' + location.port);

    // set up callback for initial connection
    socket.on('connect', function() {
        socket.emit('initial_connect', {data: 'I\'m connected!'});
    });

    // set up callback for data stream
    socket.on('new_data', handleData);

    connected=true;

    // set conn status
    //setConnected(true);
}

function handleData(message){

    if (window.myLine){
    	streamData(message);
    }

}

function drawChart() {

        var randomScalingFactor = function() {
            return Math.round(Math.random() * 100);
        };

        var datapoints = [0, 20, 20, 60, 60, 120, NaN, 180, 120, 125, 105, 110, 170];
		var config = {
            type: 'line',
            data: {
                labels: [0],
                datasets: [x_data, y_data, z_data]
            },
            options: {
                showlines: false,
                elements: {
                  line: {
                      tension: 0,
                  }
                },  
                animation: {
                    duration: 0, // general animation time
                },
                hover: {
                    animationDuration: 0, // duration of animations when hovering an item
                },
                responsiveAnimationDuration: 0, // animation duration after a resize
                responsive: true,
                title:{
                    display:true,
                    text:'Accelerometer Raw Data (XYZ)'
                },
                tooltips: {
                    mode: 'index'
                },
                scales: {
                    xAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true
                        }
                    }],
                    yAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Value'
                        },
                        ticks: {
                            suggestedMin: -.05,
                            suggestedMax: .05,
                        }
                    }]
                }
            }
        };

        window.onload = function() {
            var ctx = document.getElementById("canvas").getContext("2d");
            window.myLine = new Chart(ctx, config);
        };



}
