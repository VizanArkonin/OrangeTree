'use strict';

$(document).ready(function () {

    /**
     * Open device debug panel on new tab
     */
    $(table.device.button.debug).click(function () {
        let URL = '/monitor/' + $(tableRowsHomePage.active.device).children('[data-device-type-id]').text();

        window.open('http://127.0.0.1:5000' + URL, '_blank')
    });
});