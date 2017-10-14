
// ------------------------------------------------------------
// Backbone Models
// ------------------------------------------------------------



$(document).ready(function() {
    'use strict';
    var models, people;

    console.log('document ready');

    models = Hominy.models;
    people = models.people;
    people.fetch({
        success: function() {
            var personList;
            console.log('People fetched!');
            personList = d3.select('#person-list').selectAll('li')
                .data(people.models);
            personList.enter()
                .append('li')
                .attr('class', 'lib-item')
                .text(function(d, i) {
                    return d.get('name');
                });
            personList.exit().remove();
        }
    });
});
