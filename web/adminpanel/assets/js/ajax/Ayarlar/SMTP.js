$(document).ready(function(){
  const url = $("body").data("url");
  $(".SMTPGuncelle").on("submit", function(e){
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Ayarlar/SMTPGuncelle",
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
          toastr["success"](response.success);
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
    if ($('[name="smtpEpostaSifresi"]').attr('type')=="text") {
      $('[name="smtpEpostaSifresi"]').attr('type','password');
    }else {
      $('[name="smtpEpostaSifresi"]').attr('type','text');
    }
  });
  $('[name="hazirAyarlar"]').on('change',function(event) {
    var host      = $(this).find(':selected').data('host');
    var mail      = $(this).find(':selected').data('mail');
    var port      = $(this).find(':selected').data('port');
    var security  = $(this).find(':selected').data('security');
    $('[name="smtpEpostaAdresi"').val(mail);
    $('[name="smtpEpostaSifresi"').val('');
    $('[name="smtpHost"').val(host);
    $('[name="smtpPort"').val(port);
    $('[name="smtpGuvenlik"').val(security);
  });
});
