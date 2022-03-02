(function (func) {
    $.ajax({
        url: "/lanzhou_chart/",
        type: "post",
        dataType: "json",
        success: function (data) {
            func(data);
        }
    });
})(function (data) {
    var myChart = echarts.init(document.getElementById('chartmain_bar'), 'infographic');
    option = {
      title: {
            text: 'Stacked bar chart of furnish types of every region'
        },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          // Use axis to trigger tooltip
          type: 'shadow' // 'shadow' as default; can also be 'line' or 'shadow'
        }
      },
      legend: {
        x: 'right',
        y: 'top',
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'value',
        name: "Number",
        nameTextStyle:{
          padding:[0,0,-50,-40]
        }
      },
      yAxis: {
        type: 'category',
        data: ['城关', '安宁', '七里河', '西固', '榆中', '永登'],
        name: "District"
      },
      series: [
        {
          name: '毛坯',
          type: 'bar',
          stack: 'total',
          // label: {
          //   show: true
          // },
          emphasis: {
            focus: 'series'
          },
          data: data[0]
        },
        {
          name: '简装修',
          type: 'bar',
          stack: 'total',
          // label: {
          //   show: true
          // },
          emphasis: {
            focus: 'series'
          },
          data: data[1]
        },
        {
          name: '精装修',
          type: 'bar',
          stack: 'total',
          // label: {
          //   show: true
          // },
          emphasis: {
            focus: 'series'
          },
          data: data[2]
        },
        {
          name: '中装修',
          type: 'bar',
          stack: 'total',
          // label: {
          //   show: true
          // },
          emphasis: {
            focus: 'series'
          },
          data: data[3]
        },
        {
          name: '豪华装修',
          type: 'bar',
          stack: 'total',
          emphasis: {
            focus: 'series'
          },
          data: data[4]
        }
      ]
    };

    // Display the chart using the configuration items and data just specified
    myChart.setOption(option);
    // window.addEventListener("resize", function () {
    // myChart.resize();
});