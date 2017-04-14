// Tangram can't be bundled from source since it needs to be able to access a full copy of itself
// (either as a URL or full string of all source code) in order to load itself into web workers
// This script injects the Tangram with script tag, so that Tangram doesn't need to be included with outside tag
var L = require('leaflet');
var BasemapStyles = require('./basemapStyles');

var tangramLayerInstance;
var tangramVersion = '0.12';
var tangramPath = 'https://mapzen.com/tangram/' + tangramVersion + '/';

/**
 * The URL_PATTERN handles the old vector.mapzen.com origin (until it is fully
 * deprecated) as well as the new v1 tile.mapzen.com endpoint.
 */
var URL_PATTERN = /((https?:)?\/\/(vector|tile).mapzen.com([a-z]|[A-Z]|[0-9]|\/|\{|\}|\.|\||:)+(topojson|geojson|mvt|png|tif|gz))/;

var TangramLayer = L.Class.extend({
  includes: L.Mixin.Events,
  options: {
    fallbackTile: L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {}),
    tangramURL: tangramPath + 'tangram.min.js',
    scene: BasemapStyles.BubbleWrapMoreLabels
  },

  initialize: function (opts) {
    this.options = L.Util.setOptions(this, opts);

    if (opts && opts.debug) {
      this.options.tangramURL = tangramPath + 'tangram.debug.js';
    }
    this.hasWebGL = this._hasWebGL();

    this._setUpApiKey();

    // Start importing script
    // When there is no Tangram object available.
    if (typeof Tangram === 'undefined') {
      this._importScript(this.options.tangramURL);
    } else {
      // Not more than one Tangram instance is allowed.
      // console.log('Tangram is already on the page.');
    }
  },

  addTo: function (map) {
    if (typeof Tangram === 'undefined') {
      if (this.hasWebGL) {
        // If Tangram is not loaded yet, add layer when script is loaded
        this.oScript.onload = this.setUpTangramLayer.bind(this, map);
      } else {
        if (map.options.fallbackTile) {
          console.log('WebGL is not available, falling back to fallbackTile option.');
          map.options.fallbackTile.addTo(map);
        } else {
          // When WebGL is not avilable
          console.log('WebGL is not available, falling back to OSM default tile.');
          this.options.fallbackTile.addTo(map);
        }
      }
    } else {
      this.setUpTangramLayer(map);
    }
  },

  setUpTangramLayer: function (map) {
    this._layer = Tangram.leafletLayer(this.options).addTo(map);
    var self = this;

    self._layer.scene.subscribe({

      // Check for existing API key at load (before scene renders)
      load: function (scene) {
        var globalKey = self.options.apiKey;

        // If a key has been set (via L.Mapzen.apiKey or options.apiKey),
        // inject the key into any scene file calling Mapzen vector tiles.
        // This will overwrite any existing API keys set in the scene file.
        if (globalKey && self._isValidMapzenApiKey(globalKey)) {
          self._injectApiKey(scene.config, globalKey);
          return;
        }

        // If no key has been set, make sure key already exists in scene file
        if (self._isApiKeyMissing(scene) === true) {
          self._throwApiKeyWarning();
        } else {
          // Carry on. Scene already has or doesn't require an API key.
        }
      }
    });

    // Fire 'loaded' event when Tangram layer has been initialized
    self._layer.on('init', function () {
      self.fire('loaded', {
        layer: self._layer,
        version: Tangram.version
      });
    });
  },

  _setUpApiKey: function () {
    // If there is no api key in the option object, grab the global one.
    this.options.apiKey = this.options.apiKey || L.Mapzen.apiKey;
  },

  /**
   * A basic check to see if an api key string looks like a valid key.
   * Not _is_ a valid key, just _looks like_ one.
   */
  _isValidMapzenApiKey: function (string) {
    return (typeof string === 'string' && string.match(/^[-a-z]+-[0-9a-zA-Z_-]{5,7}$/));
  },

  /**
   * Adapted from Tangram Frame's API-key check
   *
   * Parses a Tangram scene object for sources that specify a Mapzen
   * vector tile service URL, and checks whether an API key is specified.
   *
   * @param {Object} scene - Tangram scene object
   */
  _isApiKeyMissing: function (scene) {
    var keyIsMissing = false;

    for (var i = 0, j = Object.keys(scene.config.sources); i < j.length; i++) {
      var source = scene.config.sources[j[i]];
      var valid = false;

      // Check if the source URL is a Mapzen-hosted vector tile service
      if (!source.url.match(URL_PATTERN)) continue;

      // Check if the API key is set on the params object
      if (source.url_params && source.url_params.api_key) {
        var apiKey = source.url_params.api_key;
        var globalApi = scene.config.global.sdk_mapzen_api_key;
        // Check if the global property is valid
        if (apiKey === 'global.sdk_mapzen_api_key' && this._isValidMapzenApiKey(globalApi)) {
          valid = true;
        } else if (this._isValidMapzenApiKey(apiKey)) {
          valid = true;
        }
      } else if (source.url.match(/(\?|&)api_key=[-a-z]+-[0-9a-zA-Z_-]{7}/)) {
        // Check if there is an api_key param in the query string
        valid = true;
      }

      if (!valid) {
        keyIsMissing = true;
        break;
      }
    }
    return keyIsMissing;
  },

  /**
   * Adapted from Tangram Play's automatic API-key insertion code
   *
   * Parses a Tangram scene config object for sources that specify a Mapzen
   * vector tile service URL, and injects an API key if the vector tile
   * service is hosted at vector.mapzen.com or tile.mapzen.com.
   *
   * This mutates the original `config` object by necessity. Tangram does not
   * expect it to be passed back in after it's modified.
   *
   * @param {Object} config - Tangram scene config object
   * @param {string} apiKey - the API key to inject
   */
  _injectApiKey: function (config, apiKey) {
    for (var i = 0, j = Object.keys(config.sources); i < j.length; i++) {
      var source = config.sources[j[i]];

      // Check if the source URL is a Mapzen-hosted vector tile service
      if (source.url.match(URL_PATTERN)) {
        // Add a default API key as a url_params setting.
        var params = L.extend({}, source.url_params, {
          api_key: apiKey
        });

        // Mutate the original on purpose.
        source.url_params = params;
      }
    }
  },

  _importScript: function (sSrc) {
    this.oScript = document.createElement('script');
    this.oScript.type = 'text/javascript';
    this.oScript.onerror = this._loadError;

    if (document.currentScript) document.currentScript.parentNode.insertBefore(this.oScript, document.currentScript);
    // If browser doesn't support currentscript position
    // insert script inside of head
    else document.getElementsByTagName('head')[0].appendChild(this.oScript);
    this.oScript.src = sSrc;
  },

  _loadError: function (oError) {
    console.log(oError);
    throw new URIError('The script ' + oError.target.src + ' is not accessible.');
  },

  _throwApiKeyWarning: function () {
    console.warn('A valid API key is required for access to Mapzen Vector Tiles.');
  },

  _hasWebGL: function () {
    try {
      var canvas = document.createElement('canvas');
      return !!(window.WebGLRenderingContext && (canvas.getContext('webgl') || canvas.getContext('experimental-webgl')));
    } catch (x) {
      return false;
    }
  }
});

module.exports = TangramLayer;

module.exports.tangramLayer = function (opts) {
  // Tangram can't have more than one map on a browser context.
  if (!tangramLayerInstance) {
    tangramLayerInstance = new TangramLayer(opts);
  } else {
    // console.log('Only one Tangram map on page can be drawn. Please look at https://github.com/tangrams/tangram/issues/350');
  }
  return tangramLayerInstance;
};
