$(document).ready(function(){
  const url = $('body').data('url');
  $(".EPostaDegistir").on("submit", function(e){
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Oyuncu/EPostaDegistir",
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
  $(".TelefonDegistir").on("submit", function(e){
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Oyuncu/TelefonDegistir",
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
  $(".SifreDegistir").on("submit", function(e){
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Oyuncu/SifreDegistir",
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
          $('[name="password"]').val('');
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
  $(".BayrakDegistir").on("submit", function(e){
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Oyuncu/BayrakDegistir",
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
  $(".HesabiBanla").on("submit", function(e){
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Oyuncu/HesabiBanla",
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
          location.reload();
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
  $(".HesabiAc").on("submit", function(e){
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Oyuncu/HesabiAc",
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
          location.reload();
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
  $(".EPostaGonder").on("submit", function(e){
    var ban_sebebi = $('[name="ban_sebebi"]').val();
    var acilis_sebebi = $('[name="acilis_sebebi"]').val();
    $('.EPostaGonder [name="ban_sebebi"]').val(ban_sebebi);
    $('.EPostaGonder [name="acilis_sebebi"]').val(acilis_sebebi);
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Oyuncu/EPostaGonder",
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
  var dataTableNesneMarket = false;
  $('[href="#nesneMarket"]').on('show.bs.tab',function(e) {
    if (dataTableNesneMarket==false) {
      dataTableNesneMarket = $('#ajax-nesne-market').DataTable({
        "processing":true,
        "serverSide":true,
        "dom": 'tpl',
        "sPaginationType": "simple",
        "language": {
          "url":url+"/assets/js/tr.json"
        },
        "searching": false,
        "ajax":{
          url:$('#ajax-nesne-market').data('url'),
          data: function ( d ) {
            d.search = {
              value : $('[name="nesneMarketSearch"]').val()
            }
          },
          type:"POST"
        },
      });
      $('[name="nesneMarketSearch"]').on('keyup',function(){
        dataTableNesneMarket.ajax.reload();
      });
    }
  });
});
