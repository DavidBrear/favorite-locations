var LocationsCollection = Backbone.Collection.extend({
  model: Location,
  url: '/api/locations'
});
