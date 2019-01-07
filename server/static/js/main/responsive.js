"use strict";
const SIDEBAR = ".sidebar-responsive";
const CONTENT = ".content-responsive";
const DESKTOP_TOGGLE_BAR = "#desktop-toggle-bar";
const MOBILE_TOGGLE_BAR = "#mobile-toggle-bar";
let propertiesBar = false;
/**
* Auxiliary script for adaptive layout
**/
$(function() {
    if (typeof (localStorage.getItem("bar")) === undefined) {
        localStorage.setItem("bar", "true");
    }
    if (localStorage.getItem("bar") === "true") {
        // Do display stuff here
        showBar();
    } else {
        // Do hide stuff here
        hideBar();
    }
});

$(document).ready(function () {
    $(DESKTOP_TOGGLE_BAR).click(function () {
        if (localStorage.getItem("bar") === "true") {
            hideBar();
            localStorage.setItem("bar", "false");
        } else {
            showBar();
            localStorage.setItem("bar", "true");
        }
    });

    $(MOBILE_TOGGLE_BAR).click(function () {
        if (propertiesBar === false) {
            $(".mobile-menu-container").css("width","100%");
            setTimeout(function () {
                $(".mobile-menu-container span").css("visibility","visible");
            }, 200);
            propertiesBar = true;
        } else {
            $(".mobile-menu-container").css("width","0");
            setTimeout(function () {
                $(".mobile-menu-container span").css("visibility","hidden");
            }, 100);
            propertiesBar = false;
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