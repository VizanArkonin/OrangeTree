"use strict";
const SIDEBAR_RESPONSIVE_OPEN = ".sidebar-responsive";
const CONTENT_RESPONSIVE_OPEN = ".content-responsive";
const DESKTOP_TOGGLE_BAR = "#desktop-toggle-bar";
const MOBILE_TOGGLE_BAR = "#mobile-toggle-bar";
const MOBILE_MENU_CONTAINER = ".mobile-menu-container";
const TEXT_VISIBILITY_DESKTOP = ".text-visibility-desktop";
const TEXT_VISIBILITY_MOBILE = ".text-visibility-mobile";

let BarIsOpenedMobile = false;
let BarIsOpenedDesktop = false;

/**
* Auxiliary script for adaptive layout
**/
$(document).ready(function () {

    // Actions when pressing the button of the navigation menu (for the desktop version)
    $(DESKTOP_TOGGLE_BAR).click(function () {
        if (BarIsOpenedDesktop === false) {
            $(SIDEBAR_RESPONSIVE_OPEN).removeClass("sidebar-responsive-off").addClass("sidebar-responsive-on");
            $(CONTENT_RESPONSIVE_OPEN).removeClass("content-responsive-off").addClass("content-responsive-on");
            $(TEXT_VISIBILITY_DESKTOP).css("visibility","hidden");
            setTimeout(function () {
                $(TEXT_VISIBILITY_DESKTOP).css("visibility","visible");
            }, 200);
            BarIsOpenedDesktop = true;
        } else {
            $(TEXT_VISIBILITY_DESKTOP).css("visibility","hidden");
            $(SIDEBAR_RESPONSIVE_OPEN).removeClass("sidebar-responsive-on").addClass("sidebar-responsive-off");
            $(CONTENT_RESPONSIVE_OPEN).removeClass("content-responsive-on").addClass("content-responsive-off");
            BarIsOpenedDesktop = false;
        }
    });

    // Actions when pressing the button of the navigation menu (for the mobile version)
    $(MOBILE_TOGGLE_BAR).click(function () {
        if (BarIsOpenedMobile === false) {
            $(MOBILE_MENU_CONTAINER).css("width","100%");
            setTimeout(function () {
                $(TEXT_VISIBILITY_MOBILE).css("visibility","visible");
            }, 200);
            BarIsOpenedMobile = true;
        } else {
            $(MOBILE_MENU_CONTAINER).css("width","0");
            setTimeout(function () {
                $(TEXT_VISIBILITY_MOBILE).css("visibility","hidden");
            }, 50);
            BarIsOpenedMobile = false;
        }
    });
});