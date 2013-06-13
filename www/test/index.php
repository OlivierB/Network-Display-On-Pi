	
<div id='chartContainer'></div>



	<script src="/lib/canvasjs.js"></script>

<script type="text/javascript">

var chart = new CanvasJS.Chart("chartContainer",
    {
      title:{
        text: "Top Oil Reserves",    
      },
      axisY: {
        title: "Reserves(MMbbl)"
      },
      legend: {
        verticalAlign: "bottom",
        horizontalAlign: "center"
      },
      theme: "theme2",
      data: [

      {        
        type: "column",  
        showInLegend: true, 
        legendMarkerColor: "grey",
        legendText: "MMbbl = one million barrels",
        dataPoints: [      
        {y: 297571, label: "Venezuela"},
        {y: 267017,  label: "Saudi" },
        {y: 175200,  label: "Canada"},
        {y: 154580,  label: "Iran"},
        {y: 116000,  label: "Russia"},
        {y: 97800, label: "UAE"},
        {y: 20682,  label: "US"},        
        {y: 20350,  label: "China"},        
        ]
      },   
      ]
    });

    chart.render();</script>