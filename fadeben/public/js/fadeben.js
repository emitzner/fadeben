(function($, FadeBen) {

	FadeBen = FadeBen || {};

	FadeBen.DisplayTable = FadeBen.DisplayTable || {};

	FadeBen.DisplayTable = function() {

		this.init();

	};

	FadeBen.DisplayTable.prototype = {

		bindSubMenus: function() {
			var selector = $(".data-table .sub-menu-launcher, .sub-menu-launcher");            
			var submenus = selector.on('click', function(event) {
				event.preventDefault();
				var siblings = $(this).siblings();
				var parent = $(this).parent();

				if (parent.hasClass('active')) {
					parent.removeClass('active');
					$(siblings[0]).hide();
				} else {
					parent.addClass('active');
					$(siblings[0]).show();
				}
			});
		},

		init: function() {
			this.bindSubMenus();
		}

	};

})($, FadeBen);
