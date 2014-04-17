var LocationView = Backbone.View.extend({
  tagName: 'li',
  className: 'btn-group',
  template: _.template($('#location-template').html()),
  initialize: function(options) {
    this.model.on('change', this.render, this);
  },
  render: function() {
    this.$el.html(this.template(this.model.toJSON()));
    return this;
  }
});
