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
// the function is needed to reload the page after session time because you can redirect to some page you want but it will not go there automatically you have to reload the page . Therefore the below function is needed .

function idleTimer() {
    var t;
    var session_time = 2000000; // time in seconds.
    //window.onload = resetTimer;
    window.onmousemove = resetTimer; // catches mouse movements
    window.onmousedown = resetTimer; // catches mouse movements
    window.onclick = resetTimer;     // catches mouse clicks
    window.onscroll = resetTimer;    // catches scrolling
    window.onkeypress = resetTimer;  //catches keyboard actions

//    function logout() {
//        window.location.href = '/action/logout';  //Adapt to actual logout script
//    }

   function reload() {
//            console.log("here");
          window.location.reload(1);  //Reloads the current page
   }

   function resetTimer() {
//    console.log("here reset timer");
        clearTimeout(t);
//        t = setTimeout(logout, 1800000);  // time is in milliseconds (1000 is 1 second)
        t= setTimeout(reload, session_time);  // time is in milliseconds (1000 is 1 second)
    }
}
idleTimer();

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