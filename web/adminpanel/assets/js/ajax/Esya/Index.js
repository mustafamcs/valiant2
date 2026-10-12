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
        d.searchType  = $('[name="searchType"]').val(),
        d.searchWhere = $('[name="searchWhere"]').val(),
        d.itemSearch  = $('[name="itemSearch"]').val()
      },
      type:"POST"
    },
  });
  $(".EsyaAra").on("submit", function(e){
    dataTable.ajax.reload();
    e.preventDefault();
  });
  $(document).on('click','[data-bs-target="#duzenle"]', function(event) {
    var id = $(this).data('id');
    $.ajax({
      type: "get",
      url: url+"/Esya/Detay/"+id,
      beforeSend: function(){
        $(".site_loading").show();
      },
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
          $('[data-bs-dismiss="modal"]').click();
        }else {
          $('.Duzenle [name="vnum"]').val(response.vnum);
          $('.Duzenle [name="locale_name"]').val(response.locale_name);
          $('.Duzenle [name="type"]').val(response.type);
          $('.Duzenle [name="subtype"]').val(response.subtype);
          $('.Duzenle [name="weight"]').val(response.weight);
          $('.Duzenle [name="antiflag"]').val(response.antiflag);
          $('.Duzenle [name="wearflag"]').val(response.wearflag);
          $('.Duzenle [name="gold"]').val(response.gold);
          $('.Duzenle [name="shop_buy_price"]').val(response.shop_buy_price);
          $('.Duzenle [name="magic_pct"]').val(response.magic_pct);
          $('.Duzenle [name="specular"]').val(response.specular);
          $('.Duzenle [name="socket_pct"]').val(response.socket_pct);
          $('.Duzenle [name="addon_type"]').val(response.addon_type);
          $('.Duzenle [name="refined_vnum"]').val(response.refined_vnum);
          $('.Duzenle [name="refine_set"]').val(response.refine_set);
          $('.Duzenle [name="limittype0"]').val(response.limittype0);
          $('.Duzenle [name="limitvalue0"]').val(response.limitvalue0);
          $('.Duzenle [name="limittype1"]').val(response.limittype1);
          $('.Duzenle [name="limitvalue1"]').val(response.limitvalue1);
          $('.Duzenle [name="applytype0"]').val(response.applytype0);
          $('.Duzenle [name="applyvalue0"]').val(response.applyvalue0);
          $('.Duzenle [name="applytype1"]').val(response.applytype1);
          $('.Duzenle [name="applyvalue1"]').val(response.applyvalue1);
          $('.Duzenle [name="applytype2"]').val(response.applytype2);
          $('.Duzenle [name="applyvalue2"]').val(response.applyvalue2);
          $('.Duzenle [name="value0"]').val(response.value0);
          $('.Duzenle [name="value1"]').val(response.value1);
          $('.Duzenle [name="value2"]').val(response.value2);
          $('.Duzenle [name="value3"]').val(response.value3);
          $('.Duzenle [name="value4"]').val(response.value4);
          $('.Duzenle [name="value5"]').val(response.value5);
          $('.Duzenle [name="socket0"]').val(response.socket0);
          $('.Duzenle [name="socket1"]').val(response.socket1);
          $('.Duzenle [name="socket2"]').val(response.socket2);
          $('.Duzenle [name="socket3"]').val(response.socket3);
          $('.Duzenle [name="socket4"]').val(response.socket4);
          $('.Duzenle [name="socket5"]').val(response.socket5);
          $('.Duzenle [name="item_vnum"]').val(response.vnum);
          $('[href="#genel"]').tab('show');
        }
      },
      complete: function(){
        $(".site_loading").hide();
      },
      dataType: "json"
    });
  });
  $('.EfsunSec').select2();
  $(".Duzenle").on("submit", function(e){
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Esya/Duzenle",
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
  $(".SunucuyaGonder").on("submit", function(e){
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Esya/SunucuyaGonder",
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
  $(".DropEkleButton").on("click", function(e){
    var mob_vnum  = $('[name="mob_vnum"]').val()
    var item_vnum = $('[name="item_vnum"]').val()
    var count     = $('[name="count"]').val()
    var prob      = $('[name="prob"]').val()
    $.ajax({
      type: "post",
      url: url+"/Esya/DropEkle",
      data: {mob_vnum,item_vnum,count,prob},
      beforeSend: function(){
        $(".site_loading").show();
      },
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
        }else {
          toastr["success"](response.success);
          dataTableDroplar.ajax.reload();
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
  $(document).on('click','[data-bs-target="#dropDuzenle"]', function(event) {
    $('#dropDuzenle [name="locale_name"]').val($(this).data('locale_name'));
    $('#dropDuzenle [name="newCount"]').val($(this).data('count'));
    $('#dropDuzenle [name="newProb"]').val($(this).data('prob'));
    $('#dropDuzenle [name="drop_item_vnum"]').val($(this).data('item_vnum'));
    $('#dropDuzenle [name="drop_count"]').val($(this).data('count'));
    $('#dropDuzenle [name="drop_prob"]').val($(this).data('prob'));
    $('#dropDuzenle [name="drop_mob_vnum"]').val($(this).data('mob_vnum'));
  });
  $(".DropGuncelleButon").on("click", function(e){
    var drop_mob_vnum   = $('[name="drop_mob_vnum"]').val()
    var drop_item_vnum = $('[name="drop_item_vnum"]').val()
    var drop_count     = $('[name="drop_count"]').val()
    var drop_prob      = $('[name="drop_prob"]').val()
    var newCount       = $('[name="newCount"]').val()
    var newProb        = $('[name="newProb"]').val()
    $.ajax({
      type: "post",
      url: url+"/Esya/DropGuncelle",
      data: {drop_mob_vnum,drop_item_vnum,drop_count,drop_prob,newCount,newProb},
      beforeSend: function(){
        $(".site_loading").show();
      },
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
        }else {
          toastr["success"](response.success);
          dataTableDroplar.ajax.reload();
          $('#dropDuzenle').modal('hide');
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
  var dataTableDroplar = false;
  $('[href="#drop"]').on('show.bs.tab',function(e) {
    var vnum  = $('[name="vnum"]').val()
    if (dataTableDroplar!=false) {
      dataTableDroplar.destroy();
    }
    if (vnum>0) {
      dataTableDroplar = $('#drop-datatable').DataTable({
        "processing":true,
        "serverSide":true,
        "dom": '',
        "sPaginationType": "simple",
        "language": {
          "url":url+"/assets/js/tr.json"
        },
        "searching": false,
        "ajax":{
          url: url+'/Esya/Droplar/'+vnum,
          type:"POST"
        },
      });
    }
  });
  $(document).on('click','.dropSil',function(e) {
    var mob_vnum  = $(this).data('mob_vnum');
    var item_vnum = $(this).data('item_vnum');
    var count     = $(this).data('count');
    var prob      = $(this).data('prob');
    $.ajax({
      type: "post",
      url: url+"/Esya/DropSil",
      data: {mob_vnum,item_vnum,count,prob},
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
        }else {
          toastr["success"](response.success);
          dataTableDroplar.ajax.reload();
        }
      },
      dataType: "json"
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
  });
});
