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
    //获取dom容器

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
    // window.addEventListener("resize", function () {
    // myChart.resize();
});