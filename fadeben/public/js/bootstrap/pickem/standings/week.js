(function($, FadeBen) {
	$(document).ready(function() {
		var dt = new FadeBen.DisplayTable();
	});

    $("#make-predictions").click(function(e) {
        e.preventDefault();
        $("#overlay-container").css({visibility: "visible"});
    });
})(window.jQuery, window.FadeBen);
