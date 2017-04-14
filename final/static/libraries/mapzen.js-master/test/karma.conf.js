// Karma configuration
// Generated on Fri Apr 22 2016 16:55:54 GMT-0400 (EDT)

module.exports = function (config) {
  config.set({

    // base path that will be used to resolve all patterns (eg. files, exclude)
    basePath: '../',

    // list of files / patterns to load in the browser
    files: [
      // test dependancies
      'node_modules/sinon/pkg/sinon.js',
      'node_modules/expect.js/index.js',
      'node_modules/happen/happen.js',
      'src/js/*.js',
      'src/js/**/*.js',
      'test/spec/mapControl.js',
      'test/spec/hash.js'
    ],

    plugins: [
      'karma-mocha',
      'karma-browserify',
      'karma-coverage',
      'karma-coveralls',
      'karma-phantomjs-launcher',
      'karma-browserstack-launcher'
    ],

    // frameworks to use
    // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
    frameworks: ['browserify', 'mocha'],
    // list of files to exclude
    exclude: [],

    client: {
      mocha: {
        timeout: 60000 // 60 seconds
      }
    },
    // preprocess matching files before serving them to the browser
    // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
    preprocessors: {
      'src/**/*.js': ['browserify'],
      'test/spec/*.js': ['browserify']
    },

    browserify: {
      debug: true,
      transform: [ ['babelify', {
        presets: 'es2015'}], ['browserify-istanbul', {
          instrumenterConfig: {
            embedSource: true
          }
        }]
      ]
    },

    coverageReporter: {
      type: 'html', // lcov or lcovonly are required for generating lcov.info files
      dir: 'coverage/'
    },

    // test results reporter to use
    // possible values: 'dots', 'progress'
    // available reporters: https://npmjs.org/browse/keyword/karma-reporter
    reporters: ['progress', 'coverage'],

    // web server port
    port: 9876,

    // enable / disable colors in the output (reporters and logs)
    colors: true,

    // level of logging
    // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
    logLevel: config.LOG_DEBUG,

    // enable / disable watching file and executing tests whenever any file changes
    autoWatch: true,

    // Continuous Integration mode
    // if true, Karma captures browsers, runs the tests and exits
    singleRun: true,

    // Concurrency level
    // how many browser should be started simultaneous
    concurrency: Infinity,

    // browser stack
    // global config of your BrowserStack account
    browserStack: {
      username: process.env.BROWSERSTACK_USERNAME,
      accessKey: process.env.BROWSERSTACK_KEY
    },
    // Tweaks for Browserstack timeout
    browserDisconnectTimeout: 60000, // default 2000
    browserDisconnectTolerance: 1, // default 0
    browserNoActivityTimeout: 4 * 60 * 1000, // default 10000,
    captureTimeout: 4 * 60 * 1000, // default 60000
    // define browsers
    customLaunchers: {
      bs_ie_window: {
        base: 'BrowserStack',
        browser: 'IE',
        browser_version: '11',
        os: 'Windows',
        os_version: '10'
      },
      bs_iphone6S: {
        base: 'BrowserStack',
        device: 'iPhone 6S',
        os: 'ios',
        os_version: '9.0'
      }
    },

    browsers: ['PhantomJS', 'bs_ie_window']
  });
};
