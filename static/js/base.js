$(".submenu").parent().prepend('<i class="entypo-down-open-big sf"></i>');

$("#vert-nav .topmenu a").click( function() {
  var $t = $(this);
  var $menu = $t.next(".submenu");
  $menu.slideToggle('slow');
  $menu.parent().toggleClass('openmenu');
});

$("input,textarea").focus( function() {
  $(this).prev("label").addClass('focused');
}); 
 $("input,textarea").blur( function() {
  $(this).prev("label").removeClass('focused');
});

