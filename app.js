const input = require('./controllers/gpio_controller');
// var web = require("./web_server/index");
const Gpio = require("./controllers/Gpio");

console.log('started');

let gpio29 = new Gpio({pin:29, mode:"out"});
let gpio28 = new Gpio({pin:28, mode:"out"});
let gpio27 = new Gpio({pin:27, mode:"out"});

function blink () {
    setInterval(function() {gpio29.toggle();}, 150);
    setInterval(function() {gpio28.toggle();}, 75);
    setInterval(function() {gpio27.toggle();}, 20);
}

blink();