'use strict';

$(document).ready(function () {
    //Refresh table devises
    $(table.device.button.refresh).click(function () {
        renderDevicesTable();
    });

    //Refresh table users
    $(table.user.button.refresh).click(function () {
       renderUsersTable();
    });
});
