'use strict';

$(document).ready(function () {
    /**
     * Open device monitor panel on new tab
     */
    $(table.device.button.monitor).click(function () {
        let URL = '/deviceStatus/' + $(tableRowsHomePage.active.device).children('[data-device-type-id]').text();

        window.open(URL, '_blank')
    });
});