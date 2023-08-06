function changeSlide(direction="forward") {
    var dict = {
        "back": "first",
        "forward": "last"
    }
    if (direction=="back") {
        var target = $('.slide.active').prev('.slide');
    } else {
        var target = $('.slide.active').next('.slide');
    }
    if (target.length == 0) {
        target = $('.slide:'+dict[direction]);
    }
    $('.slide.active').removeClass('active');
    target.addClass('active');
    $('html, body').scrollTop(target.offset().top - 40);
}

window.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") {
        changeSlide("back");
    } else if (e.key === "ArrowRight") {
        changeSlide();
    }
})

$(".next").click(function() {
    changeSlide();
});

$(".previous").click(function() {
    changeSlide("back");
});
