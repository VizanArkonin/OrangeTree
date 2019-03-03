'use strict';

$(document).ready(function () {
    let URL = '/deviceStatus/getMetrics/' + window.location.pathname.split("/").pop();
    let cpuTemp = [];
    let cpuTempTime = [];

    function showDeviceStatus (AjaxData) {
        for (let index = 0; index < AjaxData.readings.cpuTemp.length ; index++) {
            cpuTemp.push(AjaxData.readings.cpuTemp[index].value);
            cpuTempTime.push(AjaxData.readings.cpuTemp[index].timestamp);
        }
        for (let index = 0; index < AjaxData.readings.cpuLoad.length ; index++) {

        }
        for (let index = 0; index < AjaxData.readings.totalRam.length ; index++) {

        }
        for (let index = 0; index < AjaxData.readings.ramKbUsed.length ; index++) {

        }
        for (let index = 0; index < AjaxData.readings.ramPercentUsed.length ; index++) {

        }
    }

    sendJSONRequest(URL, null, RequestMethod.GET, beforeSendEmpty,
                    showDeviceStatus, debug_callback, process_failures);

    Highcharts.setOptions({
        chart: {
            backgroundColor: {
                linearGradient: [0, 0, 500, 500],
                stops: [
                    [0, 'rgb(255, 255, 255)'],
                    [1, 'rgb(240, 240, 255)']
                    ]
            },
            borderWidth: 2,
            plotBackgroundColor: 'rgba(255, 255, 255, .9)',
            plotShadow: true,
            plotBorderWidth: 1
        }
    });

    setTimeout(function () {
          let chartCpuTemp = Highcharts.chart('cpu_temp', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'CPU Temp'
            },
            xAxis: {
                title: {
                    text: 'Time'
                },
                categories: cpuTempTime
            },
            yAxis: {
                title: {
                    text: 'Temp °C'
                }
            },
            series: [{
                name: 'CPU Temp DEV_LITE',
                data: cpuTemp,
                tooltip: {
                    valueDecimals: 1
                }
            }],
        });
    }, 200);
});