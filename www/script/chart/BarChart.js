/**
 * BarChart, Displays data as bar chart. Te data provided can be any array
 * with couple (label, value) for each entry.
 * @author Matrat Erwan
 */
function BarChart(id, title) {

    this.id = id;

    this.data = [];

    this.chart = new CanvasJS.Chart(this.id, {

        title: {
            text: title,
            fontFamily: 'ChampWoff',
            fontSize: 30

        },
        axisX: {
            interval: 1,
            gridThickness: 0,
            labelFontSize: 10,
            labelFontWeight: "normal",
            labelFontFamily: "Lucida Sans Unicode",
            labelFontColor: 'black'

        },

        data: [{
                type: "column",
                name: "protocol",
                dataPoints: this.data
            }
        ]
    });


    this.chart.render();
}



BarChart.prototype.updateChart = function(array) {
    this.data.length = 0;

    for (var i = 0; i < array.length; i++) {
        this.data.push({
            y: array[i][1],
            label: array[i][0]
        });
    }
    this.chart.render();
};

