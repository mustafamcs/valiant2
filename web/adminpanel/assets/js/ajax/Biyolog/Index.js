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
      url: url+"/Biyolog/Ekle",
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
    var id = $(this).data('id');
    $.ajax({
      type: "get",
      url: url+"/Biyolog/Detay/"+id,
      beforeSend: function(){
        $(".site_loading").show();
      },
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
          $('[data-bs-dismiss="modal"]').click();
        }else {
          $('.Duzenle [name="level"]').val(response.level);
          $('.Duzenle [name="aff_type"]').val(response.aff_type);
          $('.Duzenle [name="aff_value"]').val(response.aff_value);
          $('.Duzenle [name="aff_type2"]').val(response.aff_type2);
          $('.Duzenle [name="aff_value2"]').val(response.aff_value2);
          $('.Duzenle [name="aff_type3"]').val(response.aff_type3);
          $('.Duzenle [name="aff_value3"]').val(response.aff_value3);
          $('.Duzenle [name="aff_type4"]').val(response.aff_type4);
          $('.Duzenle [name="aff_value4"]').val(response.aff_value4);
          $('.Duzenle [name="item_vnum"]').val(response.item_vnum);
          $('.Duzenle [name="item_vnum"]').html('<option value="'+response.item_vnum['vnum']+'">'+response.item_vnum['vnum']+' - '+response.item_vnum['name']+'</option>');
          $('.Duzenle [name="soul_vnum"]').html('<option value="'+response.soul_vnum['vnum']+'">'+response.soul_vnum['vnum']+' - '+response.soul_vnum['name']+'</option>');
          $('.Duzenle [name="req_count"]').val(response.req_count);
          $('.Duzenle [name="cool_time"]').val(response.cool_time);
          $('.Duzenle [name="chance"]').val(response.chance);
          $('.Duzenle [name="mobVnum"]').val(response.mobVnum);
        }
      },
      complete: function(){
        $(".site_loading").hide();
      },
      dataType: "json"
    });
  });
  $(".Duzenle").on("submit", function(e){
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Biyolog/Duzenle",
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
  $(document).on('click','.biyologSil',function(e) {
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
        var mobVnum = $(this).data('id');
        $.ajax({
          type: "post",
          url: url+"/Biyolog/Sil",
          data: {mobVnum},
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
      url: url+"/Biyolog/SunucuyaGonder",
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
