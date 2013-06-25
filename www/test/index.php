<!DOCTYPE HTML>
<html>
<head>  
<script type="text/javascript">
window.onload = function () {
    var chart = new CanvasJS.Chart("chartContainer",
    {
      title:{
        text: "Simple Date-Time Chart",
    },
    axisX:{
        title: "timeline",
        gridThickness: 1,
    },
    axisY: {
        title: "Downloads",
    },
    data: [
    {        
        type: "area",
        dataPoints: [//array
        { x: new Date('2013-06-25 16:00:00'), y: 0},
        { x: new Date('2013-06-25 16:30:00'), y: 150},
        { x: new Date('2013-06-25 17:00:00'), y: 40},
         { x: new Date('2013-06-25 17:30:00'), y: 140}
        

        ],
    }
    ]
});
    console.log(new Date('2013-06-25 16:18:20'))
    console.log(new Date(2013, 06, 25))
    chart.render();
}
</script>
<script type="text/javascript" src="../lib/canvasjs.min.js"></script>
</head>
<body>
<div id="chartContainer" style="height: 300px; width: 100%;">
</div>
</body>
</html>