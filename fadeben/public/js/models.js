Backbone.emulateJSON = true;

var Prediction = Backbone.Model.extend({
    idAttribute: "game_id",
    urlRoot: "/api/pickem/predictions"
});

var NFLGame = Backbone.Model.extend({
    urlRoot: "/api/nfl/games"
});

var PredictionView = Backbone.View.extend({
    events: {
        'change .selector input[type=radio]': 'predictionChanged'
    },
    initialize: function(options) {
        var self = this;
        this.model.on('change', function(model) { self.updateView(model); });
    },

    updateView: function(model) {
        console.debug("model changed!");
    },

    predictionChanged: function(event) {
        console.debug(event);
        val = $(this.el).find("input[type=radio]:checked").val()
        this.model.save({prediction: val});
    }
});

$(".choose-team").each(function() {
    var elem = this;
    new PredictionView({ el: elem, model: new Prediction({game_id: $(elem).data('game-id')}) });
});
