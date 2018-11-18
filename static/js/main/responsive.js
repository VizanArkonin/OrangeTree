"use strict";
const ASIDE = ".aside-responsive";
const CONTENT = ".content-responsive";
const BAR = "#toggle-bars";
/**
* Auxiliary script for adaptive layout
**/
$(document).ready(function () {
    $(BAR).click(function () {
        $(ASIDE).toggleClass("aside-responsive-off");
        $(CONTENT).toggleClass("content-responsive-off");
    });
});