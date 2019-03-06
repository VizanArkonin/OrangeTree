'use strict';

$(document).ready(function () {

    /**
     * Open device debug panel on new tab
     */
    $(table.device.button.debug).click(function () {
        let URL = '/monitor/' + $(tableRowsHomePage.active.device).children('[data-device-type-id]').text();

        window.open(URL, '_blank')
    });
});