(function (func) {
    $.ajax({
        url: "/lanzhou_chart2/",
        type: "post",
        dataType: "json",
        success: function (data) {
            func(data);
        }
    });
})(function (data) {
    var myChart = echarts.init(document.getElementById('chartmain_scatter2'), 'infographic');
    option = {
        title: {
            text: 'Scatter chart of 50 Lanzhou housing price'
        },
        tooltip: {
            trigger: 'axis'
        },
        xAxis: {
            name: "ID",
        },
        yAxis: {
            name: "Price(ten thousand yuan)",
        },
        series: [
            {
                name:'Price',
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