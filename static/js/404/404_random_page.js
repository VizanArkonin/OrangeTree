/*
* A page for implementing the functions of randomly displaying pictures on page 404
* */
"use strict";
const PNG = ".png";
const IMG_404_DIRECTORY = "/img/404/";
const IMG_ID_404 = "#img-not-found";
let randomImage = ["Fry", "Bender", "Nibbler", "Roberto", "Zoidberg"];

$(document).ready(function() {
    $(IMG_ID_404).attr("src", IMG_404_DIRECTORY + randomImage [Math.floor(Math.random() * 5)] + PNG);
});

