<!DOCTYPE HTML>
<html>

<head>  
  <script type="text/javascript">
  window.onload = function () {
    var chart = new CanvasJS.Chart("chartContainer",
    {
      title:{
        text: "Paquet Loss",    
      },
      axisY2: {
        title:"% Paquet loss",
        minimum: 0,
        maximum: 100,    
      },
      axisY: {
        title: "Global flow (MB/s)"
      },
      legend: {
        verticalAlign: "bottom",
      },
      data: [

         {      
      type: "splineArea",  
        showInLegend: true, 
        legendText: "Global flow (MB/s)",
        dataPoints: [      
        
        { x: 10, y:11150000 },
        { x: 20, y:10210000},
        { x: 30, y:9023000 },
        { x: 40, y:4231000 },
        { x: 50, y:4073000},
        { x: 60, y:3592000},
        { x: 70, y:3087000},
        { x: 80, y:2453000}


        ]
      },
      {          
        type: "spline",  
        axisYType: "secondary",
        showInLegend: true,
        legendText: "% Paquet loss",
        dataPoints: [      
        { x: 10, y: 10},
        { x: 20, y: 45},
        { x: 30, y: 78},
        { x: 40, y: 66},
        { x: 50, y: 20},
        { x: 60, y: 10},
        { x: 70, y: 52},
        { x: 80, y: 77}


        ]
        
      }

      ]
    });

chart.render();
  }
  </script>
 <script type="text/javascript" src="/lib/canvasjs.min.js"></script></head>
<body>
  <div id="chartContainer" style="height: 300px; width: 100%;">
  </div>
</body>
</html>
