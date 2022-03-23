(function (func) {
    $.ajax({
        url: "/chart2/",
        type: "post",
        dataType: "json",
        success: function (data) {
            func(data);
        }
    });
})(function (data) {
    var myChart = echarts.init(document.getElementById('chartmain_line'), 'infographic');
    option = {
        title: {
            text: 'Line chart of real and predicted price on test dataset--SVR model'
        },
        tooltip: {
            trigger: 'axis'
        },
        color:['#8FBC8F','#F08080'],
        legend: {
            x: 'right',
            y: 'top',
            data: ['real price', 'predicted price']
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
          max: 110,
        name: 'ID'
      },
      yAxis: {
        name: 'Price($1000)'
      },
      series: [
        {
          name: 'real price',
          type: 'line',
          data: data[0],
          itemStyle : {
            normal : {
                lineStyle:{
                    color:'#8FBC8F'
                }
            }
        }
        },
        {
          name: 'predicted price',
          type: 'line',
          data: data[1],
          itemStyle : {
            normal : {
                lineStyle:{
                    color:'#F08080'
                }
            }
          }
        }
      ]
    };
    // Display the chart using the configuration items and data just specified
    myChart.setOption(option);
    // window.addEventListener("resize", function () {
    // myChart.resize();
});