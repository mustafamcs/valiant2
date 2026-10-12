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
      url: url+"/NPC/Ekle",
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
      url: url+"/NPC/Detay/"+id,
      beforeSend: function(){
        $(".site_loading").show();
      },
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
          $('[data-bs-dismiss="modal"]').click();
        }else {
          $('.Duzenle [name="npc_vnum"]').html('<option value="'+response.npc_vnum['vnum']+'">'+response.npc_vnum['vnum']+' - '+response.npc_vnum['name']+'</option>');
          $('.Duzenle [name="newVnum"]').val(response.vnum);
          $('.Duzenle [name="name"]').val(response.name);
          $('.Duzenle [name="vnum"]').val(response.vnum);
          $('.Duzenle [name="shop_vnum"]').val(response.vnum);
          $('[href="#genel"]').tab('show');
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
      url: url+"/NPC/Duzenle",
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
          $('#duzenle').modal('hide');
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
  $(document).on('click','.npcSil',function(e) {
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
        var vnum = $(this).data('id');
        $.ajax({
          type: "post",
          url: url+"/NPC/Sil",
          data: {vnum},
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
      url: url+"/NPC/SunucuyaGonder",
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
  $('.Canavarlar').select2({
    ajax: {
      url: url+'/Canavar/Canavarlar',
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
    $('[name="name"]').val(explode[1].trim());
  });
  $(".EsyaEkleButton").on("click", function(e){
    var shop_vnum   = $('[name="shop_vnum"]').val()
    var item_vnum   = $('[name="add_item_vnum"]').val()
    var count       = $('[name="add_count"]').val()
    $.ajax({
      type: "post",
      url: url+"/NPC/EsyaEkle",
      data: {shop_vnum,item_vnum,count},
      beforeSend: function(){
        $(".site_loading").show();
      },
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
        }else {
          toastr["success"](response.success);
          dataTableEsyalar.ajax.reload();
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
  $(document).on('click','[data-bs-target="#esyaDuzenle"]', function(event) {
    $('#esyaDuzenle [name="locale_name"]').val($(this).data('locale_name'));
    $('#esyaDuzenle [name="new_count"]').val($(this).data('count'));
    $('#esyaDuzenle [name="edit_item_vnum"]').val($(this).data('item_vnum'));
    $('#esyaDuzenle [name="edit_count"]').val($(this).data('count'));
  });
  $(".EsyaGuncelleButon").on("click", function(e){
    var new_item_vnum   = $('[name="new_item_vnum"]').val()
    var new_count       = $('[name="new_count"]').val()
    var shop_vnum       = $('[name="shop_vnum"]').val()
    var edit_item_vnum  = $('[name="edit_item_vnum"]').val()
    var edit_count      = $('[name="edit_count"]').val()
    $.ajax({
      type: "post",
      url: url+"/NPC/EsyaGuncelle",
      data: {new_item_vnum,new_count,shop_vnum,edit_item_vnum,edit_count},
      beforeSend: function(){
        $(".site_loading").show();
      },
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
        }else {
          toastr["success"](response.success);
          dataTableEsyalar.ajax.reload();
          $('#esyaDuzenle').modal('hide');
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
  var dataTableEsyalar = false;
  $('[href="#esyalar"]').on('show.bs.tab',function(e) {
    var vnum  = $('.Duzenle [name="vnum"]').val()
    if (dataTableEsyalar!=false) {
      dataTableEsyalar.destroy();
    }
    if (vnum!=undefined) {
      dataTableEsyalar = $('#esya-datatable').DataTable({
        "processing":true,
        "serverSide":true,
        "dom": '',
        "sPaginationType": "simple",
        "language": {
          "url":url+"/assets/js/tr.json"
        },
        "searching": false,
        "ajax":{
          url: url+'/NPC/Esyalar/'+vnum,
          type:"POST"
        },
      });
    }
  });
  $(document).on('click','.esyaSil',function(e) {
    var shop_vnum = $(this).data('shop_vnum');
    var item_vnum = $(this).data('item_vnum');
    var count     = $(this).data('count');
    $.ajax({
      type: "post",
      url: url+"/NPC/EsyaSil",
      data: {shop_vnum,item_vnum,count},
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
        }else {
          toastr["success"](response.success);
          dataTableEsyalar.ajax.reload();
        }
      },
      dataType: "json"
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
