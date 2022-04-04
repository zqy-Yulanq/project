(function(func) {
	$.ajax({
		url: "/lanzhou_chart4/",
		type: "post",
		dataType: "json",
		success: function(data) {
			func(data);
		}
	});
})
(function(data) {
	$.get('../static/js/620100.json', function(mapData) {
		var myChart = echarts.init(document.getElementById('chartmain_map'));
		echarts.registerMap('lanzhou', mapData);
		console.log(data[0]);
		console.log(data);
		var option = {
			title: {
				text: 'Average housing price of each region in Lanzhou',
			},
			tooltip: {
				trigger: 'item',
				formatter: '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{b}<br/>{c}万元'
			},
			toolbox: {
				show: false,
				orient: 'vertical',
				left: 'right',
				top: 'center',
				feature: {
					dataView: {
						readOnly: false
					},
					restore: {},
					saveAsImage: {}
				}
			},
			visualMap: {
				min: 50,
				max: 200,
				text: ['High', 'Low'],
				realtime: false,
				calculable: true,
				inRange: {
					color: ['lightskyblue', 'yellow', 'orangered']
				}
			},
			series: [{
				name: 'Average housing price of each region in Lanzhou',
				type: 'map',
				map: 'lanzhou',
				zoom: 1.0,
				label: {
					show: true
				},
				data: data,
				// Custom name mapping
				nameMap: {
					'七里河区': '七里河',
					'城关区': '城关',
					'安宁区': '安宁',
					'榆中县': '榆中',
					'永登县': '永登',
					'西固区': '西固',
					'红古区': '红古',
					'皋兰县': '皋兰',
				}
			}]
		}
		myChart.setOption(option);
	})
});
