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
            backgroundColor: '#191815',
            borderRadius: 5
        },
        yAxis: {
            labels: {
                style: {
                    color: '#fff'
                }
            },
            title: {
                style: {
                    color: '#fff'
                }
            }
        },
        xAxis: {
            labels: {
                style: {
                    color: '#fff'
                }
            },
            title: {
                style: {
                    color: '#fff'
                }
            }
        },
        colors: ['#DAAF37'],
        title: {
            style: {
                color: '#fff'
            }
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
                categories: cpuTempTime,
                tickInterval: 24 * 3600 * 1000
            },
            yAxis: {
                title: {
                    text: 'Temp °C'
                }
            },
            legend: {
              enabled: false
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