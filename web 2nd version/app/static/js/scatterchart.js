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
    //获取dom容器

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
    // window.addEventListener("resize", function () {
    // myChart.resize();
});