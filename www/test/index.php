<!DOCTYPE HTML>
<html>

<head>  
  <script type="text/javascript">
  window.onload = function () {
    var chart = new CanvasJS.Chart("chartContainer",
    {
      title:{
      text: "Coal Reserves of Countries",   
      },
      axisY:{
        title:"Coal (mn tonnes)",   
      },
      data: [
      {        
        type: "stackedColumn100",
        toolTipContent: "{label}<br/><span style='\"'color: {color};'\"'><strong>{name}</strong></span>: {y}mn tonnes",
        name: "Anthracite and Bituminous",
        showInLegend: "true",
        dataPoints: [
        {  y: 111338 , label: "6h"},
        {  y: 49088, label: "7h" },
        {  y: 62200, label: "8h" },

        
        ]
      },  {        
        type: "stackedColumn100",
        toolTipContent: "{label}<br/><span style='\"'color: {color};'\"'><strong>{name}</strong></span>: {y}mn tonnes",
        name: "SubBituminous and Lignite",
        showInLegend: "true",
        dataPoints: [
        {  y: 135305 , label: "6h"},
        {  y: 107922, label: "7h" },
        {  y: 52300, label: "9h" },
      
       
        
        ]
      },            
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
