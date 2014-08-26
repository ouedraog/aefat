//jQuery to collapse the navbar on scroll
$(window).scroll(function() {
    if ($("#onepage").offset().top > 50) {
        $("#onepage").addClass("top-nav-collapse");
    } else {
        $("#onepage").removeClass("top-nav-collapse");
    }
});

//jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});
