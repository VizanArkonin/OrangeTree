'use strict';
const DISPLAY_NONE = {"display":"none"};
const DISPLAY_FLEX = {"display":"flex"};
const DISPLAY_BLOCK = {"display":"block"};

const TABLE_ROW_DEVICE = '.table-row-device';
const TABLE_ROW_USER = '.table-row-user';

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