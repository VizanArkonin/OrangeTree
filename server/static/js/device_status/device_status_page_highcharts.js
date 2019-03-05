'use strict';

$(document).ready(function () {
    let URL = '/deviceStatus/getMetrics/' + window.location.pathname.split("/").pop();
    // let URL = '/deviceStatus/getMetrics/DEV_LITE?timespan=24';
    let cpuTemp = [];
    let cpuTempTime = [];
    let cpuLoad = [];
    let cpuLoadTime = [];
    let ramUsed = [];
    let ramUsedTime = [];
    let ramUsedPercent = [];
    let ramUsedPercentTime = [];

    function showDeviceStatus (AjaxData) {
        for (let index = 0; index < AjaxData.readings.cpuTemp.length ; index++) {
            cpuTemp.push(AjaxData.readings.cpuTemp[index].value);
            cpuTempTime.push(AjaxData.readings.cpuTemp[index].timestamp);
        }
        for (let index = 0; index < AjaxData.readings.cpuLoad.length ; index++) {
            cpuLoad.push(AjaxData.readings.cpuLoad[index].value);
            cpuLoadTime.push(AjaxData.readings.cpuLoad[index].timestamp);
        }
        for (let index = 0; index < AjaxData.readings.ramKbUsed.length ; index++) {
            ramUsed.push(AjaxData.readings.ramKbUsed[index].value);
            ramUsedTime.push(AjaxData.readings.ramKbUsed[index].timestamp);
        }
        for (let index = 0; index < AjaxData.readings.ramPercentUsed.length ; index++) {
            ramUsedPercent.push(AjaxData.readings.ramPercentUsed[index].value);
            ramUsedPercentTime.push(AjaxData.readings.ramPercentUsed[index].timestamp);
        }
    }

    sendJSONRequest(URL, null, RequestMethod.GET, beforeSendEmpty,
                    showDeviceStatus, debug_callback, process_failures);

    Highcharts.setOptions({
        chart: {
            backgroundColor: 'rgba(54, 52, 48, 1)',
            borderRadius: 5
        },
        yAxis: {
            labels: {
                style: {
                    color: 'rgba(238, 82, 83, 1)'
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
                    color: 'rgba(238, 82, 83, 1)'
                }
            },
            title: {
                style: {
                    color: '#fff'
                }
            }
        },
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
                },
                max: 100
            },
            legend: {
              enabled: false
            },
            colors: ['#FFC31F'],
            series: [{
                name: 'CPU Temp °C ' + window.location.pathname.split("/").pop(),
                data: cpuTemp,
                tooltip: {
                    valueDecimals: 1
                }
            }],
        });
    }, 1000);

    setTimeout(function () {
        let chartCpuTemp = Highcharts.chart('cpu_load', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'CPU Load'
            },
            xAxis: {
                title: {
                    text: 'Time'
                },
                categories: cpuLoadTime,
                tickInterval: 24 * 3600 * 1000
            },
            yAxis: {
                title: {
                    text: 'CPU Load %'
                },
                max: 100
            },
            legend: {
              enabled: false
            },
            colors: ['#2bcbba'],
            series: [{
                name: 'CPU Load ' + window.location.pathname.split("/").pop(),
                data: cpuLoad,
                tooltip: {
                    valueDecimals: 1
                }
            }],
        });
    }, 1000);

    setTimeout(function () {
        let chartCpuTemp = Highcharts.chart('ram_used_kb', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'RAM Used kB'
            },
            xAxis: {
                title: {
                    text: 'Time'
                },
                categories: ramUsedTime,
                tickInterval: 24 * 3600 * 1000
            },
            yAxis: {
                title: {
                    text: 'Used kB'
                },
                max: 512000
            },
            legend: {
              enabled: false
            },
            colors: ['#ecf0f1'],
            series: [{
                name: 'RAM Used kB ' + window.location.pathname.split("/").pop(),
                data: ramUsed,
                tooltip: {
                    valueDecimals: 1
                }
            }],
        });
    }, 1000);

    setTimeout(function () {
        let chartCpuTemp = Highcharts.chart('ram_used_percent', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'RAM Used percent'
            },
            xAxis: {
                title: {
                    text: 'Time'
                },
                categories: ramUsedPercentTime,
                tickInterval: 24 * 3600 * 1000
            },
            yAxis: {
                title: {
                    text: 'Used %'
                },
                max: 100
            },
            legend: {
              enabled: false
            },
            colors: ['#ff3838'],
            series: [{
                name: 'RAM Used (%) - ' + window.location.pathname.split("/").pop(),
                data: ramUsedPercent,
                tooltip: {
                    valueDecimals: 1
                }
            }],
        });
    }, 1000);
 });