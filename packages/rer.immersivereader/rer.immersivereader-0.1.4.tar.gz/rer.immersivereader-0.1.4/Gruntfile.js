const webpack = require('webpack');

module.exports = function(grunt) {
  'use strict';
  require('load-grunt-tasks')(grunt);

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    uglify: {
      immersivereader: {
        options: {
          sourceMap: true,
          sourceMapIncludeSources: false,
        },
        files: {
          './js/dist/rer-immersive-reader-compiled.min.js': [
            './js/dist/bundle-compiled.js',
          ],
        },
      },
    },
    webpack: {
      options: {
        stats: !process.env.NODE_ENV || process.env.NODE_ENV === 'development',
      },
    },
    requirejs: {
      immersivereader: {
        options: {
          baseUrl: './',
          generateSourceMaps: true,
          preserveLicenseComments: false,
          paths: {
            jquery: 'empty:',
          },
          wrapShim: true,
          name: './js/src/index.js',
          exclude: ['jquery'],
          out: './js/dist/bundle-compiled.js',
          optimize: 'none',
        },
      },
    },
    watch: {
      scripts: {
        files: ['./js/src/index.js'],
        tasks: ['requirejs', 'uglify'],
      },
    },
  });

  // CWD to static folder
  grunt.file.setBase('./src/rer/immersivereader/browser/static');

  grunt.registerTask('compile', ['webpack', 'requirejs', 'uglify']);
  grunt.registerTask('default', ['watch']);
};
