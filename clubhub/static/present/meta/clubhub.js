// Club Hub LIVE - The Automatic Slideshow Generator
// Copyright (c) 2015-2017 George Moe - See LICENSE.md for more details.

(function () {
    Number.prototype.mod = function (n) {
        return ((this % n) + n) % n;
    };
})();

var counter = 0;
var loops = 3;

//The main code
$(document).ready(function () {

    var colors = ["rgb(255,85,85)", "rgb(85,153,255)", "rgb(15,207,77)"];

    // =================== UTILS ===================

    function scrollToAnchor(aid) {
        var aTag = $("a[name='" + aid + "']");
        if (aTag.length) $('html,body').animate({
            scrollTop: aTag.offset().top
        }, 'slow');
    }

    function triggerReload() {
        $.ajax({
            url: window.location.protocol + "//" + window.location.host + "/present/?rand=" + Math.floor((1 + Math.random()) * 0x10000),
            type: "HEAD",
            timeout: 1000,
            success: function (response) {
                console.log("Updating...");
                location.reload();
            },
            error: function (error) {
                console.log(error);
                console.log("Offline.")

                //If the SUD can't connect to the internet, it will simply continue to show
                //the slides it has. The progress bar will go red to indicate that it is in offline mode.
                $("#timer").css("backgroundColor", "rgb(255,200,200)");
                setTimeout(function () {
                    triggerReload();
                }, 10000);
            }
        });
    }

    // =================== EVENT LIST SETUP ===================

    var colors = [
        "#ff5555",
        "#5599ff",
        "#00d455",
        "#ff2ad4"
    ];

    // Color events!
    var currentdate = "";
    var colorcursor = -1;
    $("#slideshow .event").each(function () {
        var eventdate = $(this).find(".headerbar .date").text();
        if (eventdate != currentdate) {
            colorcursor = (colorcursor + 1) % colors.length;
            currentdate = eventdate;
        }
        $(this).find(".headerbar").css({background: colors[colorcursor]});
        $(this).css({borderColor: colors[colorcursor]});
    });

    //Listen to when the slides change and to track the slideshow progress.
    //Use these events to set a timer for the slide.
    //When the step count exceeds a certain limit (indcating the age of the slideshow), refresh.
    function advanceSlide() {

        if (counter + 1 === $(".step").length * loops) {
            triggerReload();
        }

        //Set default slide duration here. SHOULD NOT EXCEED 60 seconds, unless you edit the Anti-Freeze Protocol.
        var duration = $(".step").get(counter.mod($(".step").length)).getAttribute("data-transition-duration");
        duration = duration ? parseInt(duration) : 10000;

        //Uncomment these lines to enable display optimizations.
        $("#event-" + (counter.mod($(".step").length))).show();
        scrollToAnchor("step-" + (counter.mod($(".step").length)));
        setTimeout(function () {
            $("#event-" + ((counter - 1).mod($(".step").length))).hide();
            counter++;
        }, 1000);

        $("#timerstat").css("float", "right").animate({
            width: "0%"
        }, 200, "linear", function () {
            $(this).css("float", "left").css("backgroundColor", colors[counter % 3]).animate({
                width: "100%"
            }, duration, "linear", function () {
                advanceSlide();
            });
        });
    }

    setTimeout(function () {
        animateClip("#titlecard", 0, 80, 1100);
    }, 2000);

    //Start slideshow!
    setTimeout(function () {
        advanceSlide();
    }, 5000);

    function animateClip(card, start, delta, end) {
        $(card).css("-webkit-clip-path", "circle(" + start + "px at center)");
        $(card).css("clip-path", "circle(" + start + "px at center)");
        if (start < end) {
            setTimeout(function () {
                animateClip(card, start + delta, delta, end)
            }, 10);
        }
    }
});