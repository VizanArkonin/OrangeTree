"use strict";
const SIDEBAR = ".sidebar-responsive";
const CONTENT = ".content-responsive";
const BAR = "#desktop-toggle-bars";
/**
* Auxiliary script for adaptive layout
**/
$(function() {
    if (localStorage.getItem("bar") === "true") {
        // Do display stuff here
        showBar();
    } else {
        // Do hide stuff here
        hideBar();
    }
});

$(document).ready(function () {
    $(BAR).click(function () {
        if (localStorage.getItem("bar") === "true") {
            hideBar();
            localStorage.setItem("bar", "false");
        } else {
            showBar();
            localStorage.setItem("bar", "true");
        }
    });
});

function showBar () {
    $(SIDEBAR).removeClass("sidebar-responsive-off").addClass("sidebar-responsive-on");
    $(CONTENT).removeClass("content-responsive-off").addClass("content-responsive-on");
}
function hideBar () {
    $(SIDEBAR).removeClass("sidebar-responsive-on").addClass("sidebar-responsive-off");
    $(CONTENT).removeClass("content-responsive-on").addClass("content-responsive-off");
}