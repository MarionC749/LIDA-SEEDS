window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, layer) {
                layer.bindTooltip(
                    feature.properties.tooltip
                );
            }

            ,
        function1: function(feature) {
                return {
                    color: "black",
                    weight: 1,
                    fillColor: feature.properties.colour,
                    fillOpacity: 0.3
                };
            }

            ,
        function2: function(feature) {
            return {
                color: "black",
                weight: 1,
                fillColor: feature.properties.fillColor,
                fillOpacity: 0.3
            };
        }

    }
});