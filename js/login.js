$("#submit").click(function() {
  var username = $("#username").val();
  var pass = $("#pass").val();
  // alert(username+pass)
  $.get("/login", { username: $("#username").val(), pass: $("#pass").val() }, function(data) {
    if(data=="tech")
      window.location.replace("/technician.html");
    else if(data=="doctor")
      window.location.replace("/doctor.html");
    else
      window.location.replace("/admin.html");
  }).fail(function() {
    alert("failed");
  });
  // $.ajax({
  //   type: "POST",
  //   url: "/login",
  //   timeout: 2000,
  //   ContentType: "application/text",
  //   data: "city",
  //   success: function(data) {
  //     //show content
  //     alert("Success!");
  //   },
  //   error: function(jqXHR, textStatus, err) {
  //     //show error message
  //     alert("text status " + textStatus + ", err " + err);
  //   }
  // });
});
