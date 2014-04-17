var LocationCollectionView = Backbone.View.extend({
  initialize: function(locations) {
    this.container = $('#favorite-list');
    this.collection = locations;
    this.collection.on('sync', this.render, this);
    this.collection.fetch();
  },
  render: function(){
    var self = this;
    this.collection.each(function(location) {
      var view = new LocationView({model: location});
      self.container.append(view.render().el);
    });
  }
});
