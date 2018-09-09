$(function(){
    $(".btn-gpio").click(function () {
        $(this).toggleClass("btn-on btn-off");
        if ($('.btn-gpio').hasClass('btn-off')) {
            this.innerHTML('OFF');
        } else {
            this.innerHTML('ON');
        }
    });
});

