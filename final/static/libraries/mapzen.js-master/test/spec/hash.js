
describe('Map Hash Test', function () {
  var el;
  var map;
  var fakeResult;

  before(function (done) {
    fakeResult = require('../fixtures/autocomplete.json');
    done();
  })

  beforeEach(function () {
    el = document.createElement('div');
    document.body.appendChild(el);
    L.Mapzen.apiKey = 'mapzen-cstHyBQ';
    map = L.Mapzen.map(el,{
      _useTangram: false
    });
  });

  afterEach(function () {
    map.remove();
    el.parentNode.removeChild(el);
  })

  describe('Hash Working', function () {
    it('checks that hash for coord is working', function () {
      map.setView([51.505, -0.09], 13);
      var hash = L.Mapzen.hash({
        map: map
      });
      var zoom = hash._roundZDown(map.getZoom());
      var center = map.getCenter();

      var getPrecision = function (z) {
        return Math.max(0, Math.ceil(Math.log(z) / Math.LN2));
      };

      var precision = hash._precision(zoom);

      var hashLat = center.lat.toFixed(precision);
      var hashLng = center.lng.toFixed(precision);
      var hashVal = window.location.hash;
      hash._reset(); // For next test

      expect(hashVal).to.equal('#lat=' + hashLat + '&lng=' + hashLng + '&z=' + zoom);
    });

    it('checks that hash for search result is working', function () {
      var geocoder = L.Mapzen.geocoder();
      geocoder.addTo(map);

      var hash = L.Mapzen.hash({
        geocoder: geocoder
      });

      geocoder.showResults(fakeResult.features, 'foo');

      happen.once(geocoder._input, {
        type: 'keydown',
        keyCode: 40
      })
      happen.once(geocoder._input, {
        type: 'keydown',
        keyCode: 13
      })
      var encodedHashVal = encodeURIComponent(fakeResult.features[0].properties.gid);
      var hashVal = window.location.hash;
      hash._reset(); // For next test
      expect(hashVal).to.equal('#place='+encodedHashVal);
    });
  })
});
