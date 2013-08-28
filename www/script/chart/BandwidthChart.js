/**
 * BandwidthChart, interface displaying local, out, in and global bandwidth in a chart.
 * @author Matrat Erwan
 **/

function BandwidthChart(id, initializes, dataLength, style_line) {

    this.id = id;

    this.dataLength = dataLength; // number of dataPoints visible at any point
    this.style_line = style_line || "spline"; //style of the line

    this.local_network = []; // dataPoints
    this.incoming = []; // dataPoints
    this.outcoming = []; // dataPoints
    this.global = []; // dataPoints

    if (initializes) {

        var currentDate = new Date();
        var currentMili = currentDate.getTime() - (this.dataLength * 1000);

        // initializes arrays to begin the display of new points at the right part of the chart
        var iter = this.dataLength;
        while (iter--) {
            currentDate.setTime(currentMili);
            this.updateChart(0, 0, 0, 0, currentDate);
            currentMili += 1000;
        }
    }



    this.chart = new CanvasJS.Chart(this.id, {
        title: {
            text: "Traffic",
            fontFamily: "ChampWoff",
            fontSize: 30
        },
        toolTip: {
            // enabled: true,
            shared: true,
            content: "<span style='\"'color: {color};'\"'><strong>{name}</strong></span> {y} kB/s"
        },
        data: [{
            type: "area",
            name: "Global",
            color: "rgba(100,128,210, 0.2)",
            showInLegend: false,
            dataPoints: this.global
        }, {
            type: this.style_line,
            name: "Local Network",
            dataPoints: this.local_network,
            showInLegend: true,
            markerSize: 0
        }, {
            type: this.style_line,
            name: "Incoming",
            showInLegend: true,
            dataPoints: this.incoming,
            markerSize: 0
        }, {
            type: this.style_line,
            name: "Outcoming",
            showInLegend: true,
            dataPoints: this.outcoming,
            markerSize: 0
        }],
        axisY: {
            title: "kB/s",
            titleFontFamily: "ChampWoff",
            titleFontWeight: "bold"
        }
    });

    this.chart.render();
}



BandwidthChart.prototype.updateChart = function(local_, inp_, outp_, global_, time_) {
    if (time_) {
        this.xVal = new Date(time_);
    } else {
        this.xVal = new Date();
    }


    var yVal1 = local_;
    this.local_network.push({
        x: this.xVal,
        y: yVal1
    });

    var yVal2 = inp_;
    this.incoming.push({
        x: this.xVal,
        y: yVal2
    });

    var yVal3 = outp_;
    this.outcoming.push({
        x: this.xVal,
        y: yVal3
    });

    var yVal4 = global_;
    this.global.push({
        x: this.xVal,
        y: yVal4
    });

    this.xVal++;
    if (this.outcoming.length > this.dataLength && this.dataLength > 0) {
        this.local_network.shift();
        this.incoming.shift();
        this.outcoming.shift();
        this.global.shift();

    }
};


BandwidthChart.prototype.clean = function() {
    this.local_network.length = 0;
    this.incoming.length = 0;
    this.outcoming.length = 0;
    this.global.length = 0;
};

BandwidthChart.prototype.refresh = function() {
    this.chart.render();
};