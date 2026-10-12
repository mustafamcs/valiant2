$(document).ready(function(){
  const url = $("body").data("url");
  $(".KullaniciEkle").on("submit", function(e){
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Kullanicilar/KullaniciEkle",
      contentType: false,
      processData: false,
      data: data,
      beforeSend: function(){
        $(".site_loading").show();
      },
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
        }else {
          window.location.href = response.url;
        }
      },
      complete: function(){
        $(".site_loading").hide();
      },
      dataType: "json"
    })
    .fail(function(response) {
      toastr["error"](response.responseJSON.message);
    });
    e.preventDefault();
  });
  $('.sifreyiGoster').on('click',function(e) {
    if ($('[name="userPassword"]').attr('type')=="text") {
      $('[name="userPassword"]').attr('type','password');
    }else {
      $('[name="userPassword"]').attr('type','text');
    }
  });
});
