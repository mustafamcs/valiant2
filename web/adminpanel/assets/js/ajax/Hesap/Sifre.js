$(document).ready(function(){
  const url = $("body").data("url");
  $(".SifreDegistir").on("submit", function(e){
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Hesap/SifreDegistir",
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
          window.location.href = url;
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
  $('.mevcutSifreyiGoster').on('click',function(e) {
    if ($('[name="mevcutSifre"]').attr('type')=="text") {
      $('[name="mevcutSifre"]').attr('type','password');
    }else {
      $('[name="mevcutSifre"]').attr('type','text');
    }
  });
  $('.yeniSifreyiGoster').on('click',function(e) {
    if ($('[name="yeniSifre"]').attr('type')=="text") {
      $('[name="yeniSifre"]').attr('type','password');
    }else {
      $('[name="yeniSifre"]').attr('type','text');
    }
  });
});
