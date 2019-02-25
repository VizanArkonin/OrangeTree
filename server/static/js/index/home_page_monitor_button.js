'use strict';

$(document).ready(function () {
    /**
     * Open device monitor panel on new tab
     */
    $(table.device.button.monitor).click(function () {
        let URL = '/deviceStatus/' + $(tableRowsHomePage.active.device).children('[data-device-type-id]').text();

        window.open('http://127.0.0.1:5000' + URL, '_blank')
    });
});