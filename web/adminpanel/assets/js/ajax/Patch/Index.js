$(document).ready(function(){
  const url = $('body').data('url');
  var dataTable = $('#ajax-datatable').DataTable({
    "processing":true,
    "serverSide":true,
    "dom": 'tpl',
    "sPaginationType": "simple",
    "language": {
      "url":url+"/assets/js/tr.json"
    },
    "searching": false,
    "ajax":{
      url:$('#ajax-datatable').data('url'),
      data: function ( d ) {
        d.search = {
          value : $('[name="search"]').val()
        }
      },
      type:"POST"
    },
  });
  $('[name="search"]').on('keyup',function(){
    dataTable.ajax.reload();
  });
  $(".Yukle").on("submit", function(e){
    e.preventDefault();
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Patch/Yukle",
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
          dataTable.ajax.reload();
          $('[data-bs-dismiss="modal"]').click();
        }
      },
      complete: function(){
        $(".site_loading").hide();
      },
      dataType: "json"
    })
  });
  $(".Manifest").on("submit", function(e){
    e.preventDefault();
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Patch/ManifestOlustur",
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
          location.reload();
        }
      },
      complete: function(){
        $(".site_loading").hide();
      },
      dataType: "json"
    })
  });
  $(document).on("click",".patchSil",function(){
    var buton = $(this);
    Swal.fire({
      title: buton.data('header'),
      text: buton.data('message'),
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: buton.data('yes'),
      cancelButtonText: buton.data('no'),
    }).then(function(result){
      if (result.isConfirmed) {
        $.ajax({
          type: "post",
          url: url+"/Patch/Sil",
          data: {yol: buton.data('id')},
          beforeSend: function(){
            $(".site_loading").show();
          },
          success: function(response){
            if (response.error) {
              toastr["error"](response.error);
            }else {
              toastr["success"](response.success);
              dataTable.ajax.reload();
            }
          },
          complete: function(){
            $(".site_loading").hide();
          },
          dataType: "json"
        })
      }
    });
  });
});
