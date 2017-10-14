


//----------------------------
// Namespacing
//----------------------------

/**
 * Add new namespaces.
 * For Hominy.models.model1 use:
 *   extend(Hominy, 'models.model1');
 * @param ns {string} - existing namespace string
 * @param nsString {string} - namespace to add
 */
function extend(ns, nsString) {
    'use strict';
    var parts, parent, pl, i;

    parts = nsString.split('.');
    parent = ns;
    pl = parts.length;

    for (i = 0; i < pl; i++) {
        // create a property if it doesnt exist
        if (typeof parent[parts[i]] === 'undefined') {
            parent[parts[i]] = {};
        }
        parent = parent[parts[i]];
    }
    return parent;
}

// ------------------------------------------------------------
// Backbone Models
// ------------------------------------------------------------

var Hominy = Hominy || {};
extend(Hominy, 'models');

Hominy.models.Person = Backbone.Model.extend({
    idAttribute: 'uuid',
    urlRoot: '/api/people',
    defaults: function() {
        return {
            // uuid: undefined,
            // name: '',
            // email: '',
        };
    }
});

Hominy.models.People = Backbone.Collection.extend({
    model: Hominy.models.Person,
    url: '/api/people'
});

Hominy.models.people = new Hominy.models.People();


$(document).ready(function() {
    'use strict';

});
