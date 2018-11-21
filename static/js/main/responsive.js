"use strict";
const ASIDE = ".aside-responsive";
const CONTENT = ".content-responsive";
const BAR = "#toggle-bars";
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
    $(ASIDE).removeClass("aside-responsive-off").addClass("aside-responsive-on");
    $(CONTENT).removeClass("content-responsive-off").addClass("content-responsive-on");
}
function hideBar () {
    $(ASIDE).removeClass("aside-responsive-on").addClass("aside-responsive-off");
    $(CONTENT).removeClass("content-responsive-on").addClass("content-responsive-off");
}