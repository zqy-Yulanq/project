(function (func) {
    $.ajax({
        url: "/chart/",
        type: "post",
        dataType: "json",
        success: function (data) {
            func(data);
        }
    });
})(function (data) {
    var myChart = echarts.init(document.getElementById('chartmain_scatter'), 'infographic');
    option = {
        title: {
            text: 'Scatter chart of 50 Boston housing price'
        },
        tooltip: {
            trigger: 'axis'
        },
        xAxis: {
            name: "ID",
        },
        yAxis: {
            name: "MEDV($1000)",
        },
        series: [
            {
                name:'MEDV',
                symbolSize: 10,
                data: data,
                type: 'scatter'
            }
        ]
    };
    // Display the chart using the configuration items and data just specified
    myChart.setOption(option);
    // window.addEventListener("resize", function () {
    // myChart.resize();
});