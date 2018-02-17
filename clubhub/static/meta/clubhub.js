//clubhub.js - The Club Hub JS Supplement
//Copyright (c) 2017 George Moe - See LICENSE for more details.

//Event tracking with Google Analytics. Change to your own tracking code.
gtag("config", "YOUR GOOGLE ANALYTICS TRACKING ID");

//The main code
$(document).ready(function () {
    // =================== INIT ===================

    //Hide filter labels.
    $("#clear-filters").hide();
    $("#filterlist").hide();

    // =================== EVENT LIST SETUP ===================

    // Setup menu
    $("#togglemenu").click(function () {
        var $menu = $("#mainmenu");
        var $toggle = $("#togglemenu");
        if ($.trim($toggle.text()) === "Show Menu") {
            $menu.css({height: "auto"});
            var height = $menu.height();
            $menu.css({height: 0});
            $menu.animate({height: height});
            $toggle.removeClass("button-primary");
            $toggle.text("Hide Menu");
        } else {
            $menu.animate({height: 0}, function () {
                $menu.removeAttr("style");
                $toggle.addClass("button-primary");
            });
            $toggle.text("Show Menu");
        }
        $toggle.blur();
    });

    // Color events!
    var colors = [
        "#ff5555",
        "#5599ff",
        "#00d455",
        "#ff2ad4"
    ];
    var currentdate = "";
    var colorcursor = -1;
    $("#events .event").each(function () {
        var eventdate = $(this).find(".headerbar .date").text();
        if (eventdate != currentdate) {
            colorcursor = (colorcursor + 1) % colors.length;
            currentdate = eventdate;
        }
        $(this).find(".headerbar").css({background: colors[colorcursor]});
        $(this).css({borderColor: colors[colorcursor]});
    });

    // Mark ongoing events
    $("#events .event").each(function () {
        if (new Date() / 1000 > $(this).attr("data-start")) {
            $(this).find(".headerbar .date").html(
                '<p align="right"><span style="background-color: yellow; color: black;"> ' +
                '&nbsp;HAPPENING NOW&nbsp;' +
                '</span></p>');
        }
    });

// =================== EVENT BOX ACTIONS ===================


//Setup ReadMore, a plugin to hide long discriptions with a "Read More" button.
    $(".event .event-desc").readmore({
        moreLink: '<a class="readmore" href="#"><button class="button u-full-width">Show Full Description</button></a>',
        lessLink: '<a class="readmore" href="#"><button class="button u-full-width">Hide Description</button></a>'
    });

// =================== EVENT SEARCH SYSTEM ===================

// Show a random search inspiration in the searchbar
    var search_messages = [
        "What do you want to do today?",
        "What interests you?",
        "What do you want to explore?",
        "What do you have in mind?",
        "Where do you want to go?",
        "What do you want to see?",
        "What fascinates you?",
        "What are your interests?",
        "What excites you?",
        "What are you looking forward to?",
        "What would you like to find?",
        "Who do you want to meet?"
    ];
    $("#searchbar").attr("placeholder", search_messages[Math.floor(Math.random() * search_messages.length)]);

    function isString(object) {
        return typeof object === "string" || object instanceof String;
    }

    var searchkeys = [
        "title:",
        "host:",
        "description:",
        "location:",
        "starts:",
        "ends:"
    ];
    // Process the contents of the searchbar on change
    $("#searchbar").on("change keyup paste", function () {

        // Setup query
        // 1) Replace and with spaces, since spaces are treated as AND operands
        // 2) Split the query by OR operands
        // 3) Split those subqueries by spaces
        // 4) Clean output
        var query = $(this).val()
            .toLowerCase()
            .match(/((".*?")|(?!or)\b\S+|\s|[\.,"]+)+/g);

        if (query) {
            query = query.map(function (x) {
                x = $.trim(x)
                    .match(/[^\s"]+|"([^"]*)"/g);
                if (x) {
                    x = x.filter(function (x) {
                        return x && x !== "and";
                    })

                    var newx = [];
                    var searchkey_selected = false;
                    x.forEach(function (x) {
                        if (searchkeys.indexOf(x) >= 0) {
                            newx.push([x, []]);
                            searchkey_selected = true;
                        } else if (x == "body:") {
                            searchkey_selected = false;
                        } else {
                            if (searchkey_selected) {
                                newx[newx.length - 1][1].push(x);
                            } else {
                                newx.push(x);
                            }
                        }
                    });
                    x = newx;

                    return x.map(function (x) {
                        if (isString(x))
                            return x.replace(/"+/g, "");
                        else
                            return [x[0], x[1].map(function (x) {
                                return x.replace(/"+/g, "");
                            })];
                    }).filter(function (x) {
                        return x;
                    });
                }
            }).filter(function (x) {
                return x;
            });
        } else {
            query = [];
        }

        // Filter elements
        if (query.length == 0) {
            $("#events .event").show();
            $("#noresults").hide();
            $("#searchinfo").hide();
        } else {
            $("#searchinfo").show();
            $("#events .event").each(function () {
                // Compute searchable fields
                var body = $(this).text().toLowerCase();
                var title = $(this).find(".event-title").text().toLowerCase();
                var host = $(this).find(".event-host").text().toLowerCase();
                var description = $(this).find(".event-desc").text().toLowerCase();
                var location = $(this).find(".event-loc").text().toLowerCase();
                var starts = $(this).find(".event-start-time").text().toLowerCase();
                var ends = $(this).find(".event-end-time").text().toLowerCase();

                var fieldmap = {
                    "title:": title,
                    "host:": host,
                    "description:": description,
                    "location:": location,
                    "starts:": starts,
                    "ends:": ends
                };

                // Perform OR search between subqueries
                var show = query.some(function (item) {
                    // Perform AND search between subquery components
                    return item.every(function (item) {
                        var searchspace;
                        var searchfield;
                        if (isString(item)) {
                            searchfield = body;
                            searchspace = [item];
                        } else {
                            searchspace = item[1];
                            if (!(item[0] in fieldmap)) {
                                return true;
                            }
                            searchfield = fieldmap[item[0]];
                        }

                        return searchspace.every(function (item) {
                            return searchfield.indexOf(item) >= 0;
                        });
                    });
                });

                // Show matching events, hide others
                if (show) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            });

            // Display search interpretation
            $("#searchecho").html(query.map(function (q) {
                return '<span style="color: magenta"><b>has: [</b></span> ' + q.map(function (s) {
                        if (isString(s))
                            return '<span style="color: green"><b>' + s + '</b></span>'
                        else
                            return '<span style="color: #5599ff"><b>' + s[0] + ' [</b></span> '
                                + s[1].map(function (s) {
                                    return '<span style="color: green"><b>' + s + '</b></span>';
                                }).join(" and ")
                                + ' <span style="color: #5599ff"><b>]</b></span>';
                    }).join(" and ") + ' <span style="color: magenta"><b>]</b></span>'
            }).join(" or "));

            // If no events are returned by the search, show a message.
            if ($("#events .event:visible").length == 0) {
                $("#noresults").show();
            } else {
                $("#noresults").hide();
            }
        }
    });

    $("#searchhelp-toggle").click(function () {
        if ($("#searchhelp-toggle").text() == "Search Help") {
            $("#searchhelp").show();
            $("#searchhelp-toggle").text("Hide Help");
        } else {
            $("#searchhelp").hide();
            $("#searchhelp-toggle").text("Search Help");
        }
    });

    // Process search through URL query parameters
    var params = new URL(window.location).searchParams;
    if (params.get("search") !== null) {
        $("#searchbar").val(params.get("search")).trigger("change");
    }


// =================== TIMEZONES ===================

// Script to handle instant timezone setting
    $("#timezone-spinner").change(function () {
        $("#timezone-form").submit();
    });

// =================== CSS Buttons ===================

//Configure our css buttons to open the link specified by the data-link attribute.
    $(".css-button-link").each(function (index) {
        if ($(this).attr("data-newtab")) {
            $(this).wrap('<a target="_blank" href="' + $(this).attr("data-link") + '"></a>');
        } else {
            $(this).wrap('<a href="' + $(this).attr("data-link") + '"></a>');
        }
    });

// =================== Sticky Headerbars ===================
    function updateStickyheaders() {
        // Remove headers from the sticky header if they are below the top.
        $("#stickyhead .headerbar").each(function () {
            if ($(this).attr("origpos") > $(window).scrollTop()) {
                $(this).remove();
            }
        });

        // Reset all sticky headers.
        $("#stickyhead .headerbar").hide();
        $("#stickyhead .headerbar").offset({top: 0});
        $("#stickyhead .headerbar:last").show();

        // Check event headerbars to see if they should be placed in the sticky header.
        $("#events .headerbar:visible").each(function (index) {
            // Check that the header is above the top of the window
            if ($(this).offset().top < $(window).scrollTop()) {
                $headerbar = $(this).clone();
                // Check that the header is not already in the sticky header
                if ($("#stickyhead .headerbar[index=" + index + "]").length == 0) {
                    // Copy the headir into the sticky header
                    // Also add some useful metadata.
                    $headerbar.attr("origpos", $(this).offset().top);
                    $headerbar.attr("index", index);
                    $headerbar.css({borderColor: $(this).parents(".event").css("borderColor")});
                    $("#stickyhead").append($headerbar);
                    $("#stickyhead").width($(this).width());
                }
            } else if ($("#stickyhead .headerbar:visible").length > 0 &&
                $(this).offset().top < $("#stickyhead .headerbar:visible").offset().top + $("#stickyhead .headerbar:visible").height() + 10) {
                // Event headers nudge the stickyheaders out of the way.
                $("#stickyhead .headerbar:visible").offset({top: $(this).offset().top - $("#stickyhead .headerbar:visible").height() - 10});
            }
        });
    }

// Clear headers from the sticky headerbar.
    function clearStickyheaders() {
        $("#stickyhead").html("");
    }

// Update headers on scroll, resize, and page load.
    $(window).on("scroll", updateStickyheaders);
    $(window).on("resize", function () {
        clearStickyheaders();
        updateStickyheaders();
    });
    updateStickyheaders();

// =================== Event Tracking ===================
// Track various events on Google Analytics.
    $(".gcalbutton").click(function () {
        var event = $.trim($(this).parents(".event").attr("data-name"));
        var host = $.trim($(this).parents(".event").attr("data-host"));
        gtag("event", "GCalButtonClick", {
            "event_category": "engagement",
            "event_label": host + "|" + event
        });
    });

    $(".externbutton").click(function () {
        var event = $.trim($(this).parents(".event").attr("data-name"));
        var host = $.trim($(this).parents(".event").attr("data-host"));
        gtag("event", "ExternalButtonClick", {
            "event_category": "engagement",
            "event_label": host + "|" + event
        });
    });

    $(".rsvpbutton").click(function () {
        var event = $.trim($(this).parents(".event").attr("data-name"));
        var host = $.trim($(this).parents(".event").attr("data-host"));
        gtag("event", "RSVPButtonClick", {
            "event_category": "engagement",
            "event_label": host + "|" + event
        });
    });

    $(".event-poster").click(function () {
        var event = $.trim($(this).parents(".event").attr("data-name"));
        var host = $.trim($(this).parents(".event").attr("data-host"));
        gtag("event", "PosterClick", {
            "event_category": "engagement",
            "event_label": host + "|" + event
        });
    });

// Track event views as they appear in the window.
    var seen = [];

    function checkViewedEvents() {
        $(".event").each(function (index) {
            if ($(this).offset().top > $(window).scrollTop() &&
                $(this).offset().top < $(window).scrollTop() + $(window).height()) {
                var event = $.trim($(this).attr("data-name"));
                var host = $.trim($(this).attr("data-host"));
                if (!seen.includes(event + host)) {
                    seen.push(event + host);
                    gtag("event", "EventView", {
                        "event_category": "engagement",
                        "event_label": host + "|" + event
                    });
                }
            }
        });
    }

    $(window).on("scroll", checkViewedEvents);
    checkViewedEvents();
})
;
