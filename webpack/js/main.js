//jQuery = require('jquery');
Tether = require('tether');
require('bootstrap');
require('jquery-validation');

$(function() {
  $("form").validate({
    errorClass: "has-warning",
    validClass: "has-success",
    highlight: function(element, errorClass, validClass) {
      var group = $(element).parent(".form-group");
      if (group.length == 0) {
        // just use the element itself
        group = $(element);
      }
      group.addClass(errorClass).removeClass(validClass);
    },
    unhighlight: function(element, errorClass, validClass) {
      var group = $(element).parent(".form-group");
      if (group.length == 0) {
        // just use the element itself
        group = $(element);
      }
      group.addClass(validClass).removeClass(errorClass);
    },
  })
});
