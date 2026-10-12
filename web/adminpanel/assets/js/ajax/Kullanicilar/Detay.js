$(document).ready(function(){
  const url = $('body').data('url');
  $('.status_update').on('change',function(e){
    var id = $(this).data('id');
    $.ajax({
      type: "post",
      url: url+"/Kullanicilar/Durum",
      data: {id},
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
        }else {
          toastr["success"](response.success);
        }
      },
      dataType: "json"
    });
    e.preventDefault();
  });
  $('.oturumuSonlandir').on('click',function(e) {
    Swal.fire({
      title: $(this).data('header'),
      html:$(this).data('message'),
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: $(this).data('yes'),
      cancelButtonText: $(this).data('no'),
      closeOnConfirm: !1,
      closeOnCancel: !1
    })
    .then((result) => {
      if (result.value) {
        var userId = $(this).data('id');
        $.ajax({
          type: "post",
          url: url+"/Kullanicilar/OturumuSonlandir",
          data: {userId},
          success: function(response){
            if (response.error) {
              toastr["error"](response.error);
            }else {
              toastr["success"](response.success);
            }
          },
          dataType: "json"
        });
      }
    });
    e.preventDefault();
  });
});
