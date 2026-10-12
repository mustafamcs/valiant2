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
  $(".Ekle").on("submit", function(e){
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Cark/Ekle",
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
    .fail(function(response) {
      toastr["error"](response.responseJSON.message);
    });
    e.preventDefault();
  });
  $(document).on('click','[data-bs-target="#duzenle"]', function(event) {
    $('.Duzenle [name="locale_name"]').val($(this).data('locale_name'));
    $('.Duzenle [name="newCount"]').val($(this).data('count'));
    $('.Duzenle [name="vnum"]').val($(this).data('vnum'));
    $('.Duzenle [name="count"]').val($(this).data('count'));
  });
  $(".Duzenle").on("submit", function(e){
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Cark/Duzenle",
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
          $('#duzenle').modal('hide');
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
  $(document).on('click','.esyaSil',function(e) {
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
        var vnum  = $(this).data('vnum');
        var count = $(this).data('count');
        $.ajax({
          type: "post",
          url: url+"/Cark/Sil",
          data: {vnum,count},
          success: function(response){
            if (response.error) {
              toastr["error"](response.error);
            }else {
              toastr["success"](response.success);
              dataTable.ajax.reload();
            }
          },
          dataType: "json"
        });
      }
    });
    e.preventDefault();
  });
  $(".SunucuyaGonder").on("submit", function(e){
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Cark/SunucuyaGonder",
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
  $('.Esyalar').select2({
    ajax: {
      url: url+'/Esya/Esyalar',
      dataType: 'json',
      delay : 250,
      processResults: function (data) {
        return {
          results: data
        };
      },
      cache : true
    }
  });
});
