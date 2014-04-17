var FavoritesIndex = function() {
  this.map = undefined;
  this.markers = {};
  this.setMarkers = function(marker_locations) {
    for (key in marker_locations) {
      var marker = marker_locations[key];
      var m = new google.maps.Marker({
        position: new google.maps.LatLng(marker.latitude, marker.longitude),
        map: map
      });
      this.markers[marker.address] = m;
    };
  }
  this.initialize = function(latitude, longitude) {
    var self = this;
    self.markers = {};
    var mapOptions = {
      center: new google.maps.LatLng(latitude, longitude),
      zoom: 14
    };
    self.map = new google.maps.Map(document.getElementById("map-canvas"),
        mapOptions);
    google.maps.event.addListener(map, 'center_changed', function() {
    });
    //map location click
    $('#favorite-list').on('click', '.map-location', function(evt){

      evt.preventDefault();
      var $this = $(this);
      var lt = $this.data('latitude');
      var ln = $this.data('longitude');
      self.map.panTo(new google.maps.LatLng(lt, ln));
    });
    $('#favorite-list').on('click', '.remove', function(evt) {
      var $this = $(this);
      evt.preventDefault();
      self.markers[$this.data('address')].setMap(null);
      $.post('/locations/delete/' + $this.data('id')).done(function(data, status) {
        $this.closest('.btn-group').slideUp(function(){ $(this).remove();});
      }).fail(function(txt){ console.log(txt); });
    });

    var input = document.getElementById('address-search');
    self.map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
    google.maps.event.addListener(map, 'click', function(evt) {
      $('#address-search').fadeOut();
    });

    var autocomplete = new google.maps.places.Autocomplete(
        /** @type {HTMLInputElement} */(document.getElementById('address-search')),
        { types: ['geocode'] });
    // When the user selects an address from the dropdown,
    // populate the address fields in the form.
    google.maps.event.addListener(autocomplete, 'place_changed', function() {
      fillInAddress(autocomplete);
    });
    $('#location-search').click(function(evt){
      evt.preventDefault();
      $('#address-search').fadeIn(function() {
        $(this).focus();
      });
    });

  };
  var fillInAddress = function(autocomplete) {
    var place = autocomplete.getPlace();
    document.getElementById('loc-lat').value = place.geometry.location['k'];
    document.getElementById('loc-long').value = place.geometry.location['A'];
    document.getElementById('loc-address').value = place.formatted_address;

    $('#address-confirm-modal').modal('show');
  };
  this.go_to = function(data) {
    var ltln = new google.maps.LatLng(data.latitude, data.longitude);
    var mark = new google.maps.Marker({
      position: ltln,
      map: map
    });
    markers[data.address] = mark;
    map.panTo(ltln);
  };
  this.getLocation = function() {
    if (navigator.geolocation)
    {
      navigator.geolocation.getCurrentPosition(function(position){
        self.initialize(position.coords.latitude, position.coords.longitude);
        $.get('/api/locations').done(function(data) {
          var arr = JSON.parse(data);
          self.setMarkers(arr);
        });
      });
    }
    else{
      self.initialize(-34.397, 150.644);
      $.get('/api/locations').done(function(data) {
        var arr = JSON.parse(data);
        self.setMarkers(arr);
      });
    }
  };
  return this;
}
function LocationLink(data){
  var li = $('<li></li>').addClass('btn-group');
  var link = $('<a></a>').addClass('map-location btn btn-sm btn-default').attr('href', '#').attr('data-latitude', data.latitude).attr('data-longitude', data.longitude);
  var remove = $('<a></a>').addClass('btn remove').attr('href', '#').attr('data-address', data.address).attr('data-id', data.id);
  remove.html('<span class="glyphicon glyphicon-remove"></span>');
  link.html(data.name);
  li.append(link);
  li.append(remove);
  return li;
}

var fav = FavoritesIndex();
google.maps.event.addDomListener(window, 'load', fav.getLocation);
$(function() {
  $('#location-edit-form').submit(function(evt) {
    evt.preventDefault();
    var location_action = document.getElementById('loc-action');
    var location_id = document.getElementById('loc-id');
    var csrf = $('#csrf_token').val();
    var location_params = {
      latitude: document.getElementById('loc-lat').value,
      longitude: document.getElementById('loc-long').value,
      address: document.getElementById('loc-address').value,
      name: document.getElementById('loc-name').value
    }
    if (location_params.name.trim() !== '') {

      var action = !!location_action ? location_action.value : 'create';
      var id = !!location_id ? '/' + location_id.value : '';

      $.post('/locations/'+action+id, {
        csrf_token: csrf,
        name: location_params.name,
        latitude: location_params.latitude,
        longitude: location_params.longitude,
        address: location_params.address
      }).done( function(data, success) {
        $('#favorite-list').append(LocationLink(data));
        $('#address-confirm-modal').modal('hide');
        $('#address-search').fadeOut();
        fav.go_to(data);
      }).fail( function(txt){
        console.log('failed', txt);
      });

    } else {
      //error
    }
  });
});
