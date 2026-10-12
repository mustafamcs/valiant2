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
  $(document).on('change','.status_update',function(e){
    var id = $(this).data('id');
    $.ajax({
      type: "post",
      url: url+"/NesneMarket/Durum",
      data: {id},
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
          dataTable.ajax.reload();
        }else {
          toastr["success"](response.success);
        }
      },
      dataType: "json"
    });
    e.preventDefault();
  });
  $(".Ekle").on("submit", function(e){
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/NesneMarket/Ekle",
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
      url: url+"/NesneMarket/Detay/"+id,
      beforeSend: function(){
        $(".site_loading").show();
      },
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
          $('[data-bs-dismiss="modal"]').click();
        }else {
          $('.Duzenle [name="category_id"]').html('<option value="'+response.category_id['id']+'">'+response.category_id['name']+'</option>');
          $('.Duzenle [name="vnum"]').html('<option value="'+response.vnum['id']+'">'+response.vnum['name']+'</option>');
          $('.Duzenle [name="item_name"]').val(response.item_name);
          $('.Duzenle [name="price"]').val(response.price);
          $('.Duzenle [name="count"]').val(response.count);
          $('.Duzenle [name="time_type"]').val(response.time_type);
          $('.Duzenle [name="price_type"]').val(response.price_type);
          $('.Duzenle [name="socket0"]').val(response.socket0);
          $('.Duzenle [name="socket1"]').val(response.socket1);
          $('.Duzenle [name="socket2"]').val(response.socket2);
          $('.Duzenle [name="socket3"]').val(response.socket3);
          $('.Duzenle [name="attrtype0"]').val(response.attrtype0).trigger('change');
          $('.Duzenle [name="attrvalue0"]').val(response.attrvalue0);
          $('.Duzenle [name="attrtype1"]').val(response.attrtype1).trigger('change');
          $('.Duzenle [name="attrvalue1"]').val(response.attrvalue1);
          $('.Duzenle [name="attrtype2"]').val(response.attrtype2).trigger('change');
          $('.Duzenle [name="attrvalue2"]').val(response.attrvalue2);
          $('.Duzenle [name="attrtype3"]').val(response.attrtype3).trigger('change');
          $('.Duzenle [name="attrvalue3"]').val(response.attrvalue3);
          $('.Duzenle [name="attrtype4"]').val(response.attrtype4).trigger('change');
          $('.Duzenle [name="attrvalue4"]').val(response.attrvalue4);
          $('.Duzenle [name="attrtype5"]').val(response.attrtype5).trigger('change');
          $('.Duzenle [name="attrvalue5"]').val(response.attrvalue5);
          $('.Duzenle [name="attrtype6"]').val(response.attrtype6).trigger('change');
          $('.Duzenle [name="attrvalue6"]').val(response.attrvalue6);
          $('.Duzenle [name="status"]').val(response.status);
          $('.Duzenle [name="sell_count"]').val(response.sell_count);
          $('.Duzenle [name="id"]').val(response.id);
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
      url: url+"/NesneMarket/Duzenle",
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
        var id = $(this).data('id');
        $.ajax({
          type: "post",
          url: url+"/NesneMarket/Sil",
          data: {id},
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
      url: url+"/NesneMarket/SunucuyaGonder",
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
  }).on('change',function(e){
    var val = e.currentTarget.lastChild.innerText;
    var explode = val.split(" - ");
    $('[name="item_name"]').val(explode[1].trim());
  });
  $('.Kategoriler').select2({
    ajax: {
      url: url+'/NesneMarket/Kategoriler',
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
  $('.EfsunSec').select2();
});
