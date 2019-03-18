'use strict';

const TABLE_ROW_DEVICE = '.table-row-device';
const TABLE_ROW_USER = '.table-row-user';

const table = {
    user: {
        window: ".table-user-window",
        tab: ".table-user-tab",
        content: "#table_user_content",
        preloader: "#table_user_preloader",
        button: {
            refresh: "#table_user_button_refresh"
        }
    },
    device: {
        window: ".table-device-window",
        tab: ".table-device-tab",
        content: "#table_device_content",
        preloader: "#table_device_preloader",
        button: {
            refresh: "#table_device_button_refresh",
            debug: "#table_device_button_debug",
            monitor: "#table_device_button_monitor"
        }
    }
};

let tableRowsHomePage = {
    state: {
        device: false,
        user: false
    },
    active: {
        device: null,
        user: null
    }
};