//jQuery = require('jquery');
Tether = require('tether');
require('bootstrap');

$(function() {
  $("#nav-menu").on("show.bs.collapse", function() {
      $("#open-nav-menu").collapse('hide');
  })
  $("#open-nav-menu").on("show.bs.collapse", function() {
      $("#open-nav-menu").collapse('hide');
  })
});
