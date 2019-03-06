'use strict';
/**
 * Basic style setting for highcharts
 */
Highcharts.setOptions({
        chart: {
            backgroundColor: '#363430',
            borderRadius: 5
        },
        yAxis: {
            labels: {
                style: {
                    color: '#EE5253'
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
                    color: '#EE5253'
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

$(document).ready(function () {
    let deviceName = window.location.pathname.split("/").pop();
    let URL = null;
    /**
     * The function makes an AJAX request, and if the call is successful, the function for rendering graphs is called.
     */
    function getDataDeviceStatus () {
        URL = '/deviceStatus/getMetrics/' + deviceName;

         sendJSONRequest(URL, null, RequestMethod.GET, beforeSendEmpty,
                        renderDeviceStatusCharts, debug_callback, process_failures);
    }

    /**
     * Getting a JSON object. Rendering highcharts based on received data.
     * @param ajaxData - JSON object
     */
    function renderDeviceStatusCharts (ajaxData) {
        let cpuTemp = [];
        let cpuTempTime = [];
        let cpuLoad = [];
        let cpuLoadTime = [];
        let ramUsed = [];
        let ramUsedTime = [];
        let ramUsedPercent = [];
        let ramUsedPercentTime = [];

        for (let index = 0; index < ajaxData.readings.cpuTemp.length ; index++) {
            cpuTemp.push(ajaxData.readings.cpuTemp[index].value);
            cpuTempTime.push(ajaxData.readings.cpuTemp[index].timestamp);
        }
        for (let index = 0; index < ajaxData.readings.cpuLoad.length ; index++) {
            cpuLoad.push(ajaxData.readings.cpuLoad[index].value);
            cpuLoadTime.push(ajaxData.readings.cpuLoad[index].timestamp);
        }
        for (let index = 0; index < ajaxData.readings.ramKbUsed.length ; index++) {
            ramUsed.push(ajaxData.readings.ramKbUsed[index].value);
            ramUsedTime.push(ajaxData.readings.ramKbUsed[index].timestamp);
        }
        for (let index = 0; index < ajaxData.readings.ramPercentUsed.length ; index++) {
            ramUsedPercent.push(ajaxData.readings.ramPercentUsed[index].value);
            ramUsedPercentTime.push(ajaxData.readings.ramPercentUsed[index].timestamp);
        }

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
                name: 'CPU Temp °C ' + deviceName,
                data: cpuTemp,
                tooltip: {
                    valueDecimals: 1
                }
            }],
        });

        let chartCpuLoad = Highcharts.chart('cpu_load', {
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
                name: 'CPU Load ' + deviceName,
                data: cpuLoad,
                tooltip: {
                    valueDecimals: 1
                }
            }],
        });

        let chartRamUsed = Highcharts.chart('ram_used_kb', {
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
                name: 'RAM Used kB ' + deviceName,
                data: ramUsed,
                tooltip: {
                    valueDecimals: 1
                }
            }],
        });

        let chartRamUsedPercent = Highcharts.chart('ram_used_percent', {
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
                name: 'RAM Used (%) - ' + deviceName,
                data: ramUsedPercent,
                tooltip: {
                    valueDecimals: 1
                }
            }],
        });
    }


    /**
     * Selecting the time interval for displaying graph data.
     */
    $('.button-timespan').on('click', function () {
        URL = '/deviceStatus/getMetrics/' + deviceName + '?timespan=' + $(this).attr('data-timespan');


        $('.button-timespan').removeClass('button-selection');
        $(this).addClass('button-selection');

        sendJSONRequest(URL, null, RequestMethod.GET, beforeSendEmpty,
                        renderDeviceStatusCharts, debug_callback, process_failures);
    });

    /**
     *  Function reload charts. Depending on the selected time interval.
     */
    $('.button-device-status-refresh').click(function () {
        sendJSONRequest(URL, null, RequestMethod.GET, beforeSendEmpty,
                        renderDeviceStatusCharts, debug_callback, process_failures);
    });

    getDataDeviceStatus();

    /**
     * Function reload charts (auto). Depending on the selected time interval.
     */
    setInterval(function () {
        sendJSONRequest(URL, null, RequestMethod.GET, beforeSendEmpty,
                        renderDeviceStatusCharts, debug_callback, process_failures);
    }, 60000);

 });