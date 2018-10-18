$(function(){
// Variables

// Create button on/off and out/in
    $(".btn-gpio").click(function(){
        $(this).toggleClass("btn-on btn-off");
        let nameButton = $(this).text();
            switch (nameButton){
                case "OFF":
                    $(this).text("ON");
                    break;
                case "ON":
                    $(this).text("OFF");
                    break;
                case "OUT":
                    $(this).text("IN");
                    break;
                case "IN":
                    $(this).text("OUT");
                    break;
                default:
                    $(this).text("not used");
            }
    });

    // Create a Tooltip
    $('[data-toggle="tooltip"]').tooltip();

});

// Just a class change, without involving jQuery
function toggleIcon(x) {
    x.classList.toggle("fa-lock-open")
}
