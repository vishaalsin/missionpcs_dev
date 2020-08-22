$(document).ready(function(){
    $(".login-register").click(function(){
      $("#login-register-popup").show(1000);
    });
  });

$(document).ready(function(){
  $(".close-btn").click(function(){
    $("#login-register-popup").hide(1000);
  });
});


$(document).ready(function(){
  $(".signup-btn").click(function(){
    $(".login-section").hide(500);
    $(".register-section").show(500);
  });
});

$(document).ready(function(){
  $(".signin-btn").click(function(){
    $(".register-section").hide(500);
    $(".login-section").show(500);
  });
});
// function offsetAnchor() {
//   if (location.hash.length !== 0) {
//     window.scrollTo(window.scrollX, window.scrollY - 57);
//   }
// }
// $(document).on('click', 'a[href^="#"]', function(event) {
//   window.setTimeout(function() {
//     offsetAnchor();
//   }, 0);
// });

// window.setTimeout(offsetAnchor, 0);