$(document).ready(function(){
  const url = $('body').data('url');
  const pid = $('[name="id"]').val();
  $(".KarakterKurtar").on("submit", function(e){
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Oyuncu/KarakterKurtar",
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
  $(".KarakterDusur").on("submit", function(e){
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Oyuncu/KarakterDusur",
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
  function EsyalariYaz(div,response){
    if (response!="") {
      $.each(response, function(index, val) {
        $(div).append('<div class="col-lg-2 text-center p-3" style="height:200px"> \
          <div style="border:1px solid #ccc;height:100%"> \
          <span class="badge badge-danger" style="height:20px;width:20px;line-height:15px;border-radius:10px;position:absolute;top:3px;right:5px">'+val.count+'</span> \
          <br> \
          <div style="height:50px"><img src="'+url+'/assets/img/icon/'+val.icon+'" alt=""></div> \
          <br> \
          <span>ID : '+val.id+'</span><br> \
          <span>'+val.name+'</span><br> \
          <a href="Javascript:void(0)" class="btn btn-primary p-1 mt-1" data-bs-toggle="modal" data-bs-target="#esyaDetay'+val.id+'"> \
            <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M7 7h-1a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-1"></path><path d="M20.385 6.585a2.1 2.1 0 0 0 -2.97 -2.97l-8.415 8.385v3h3l8.385 -8.415z"></path><path d="M16 5l3 3"></path></svg> \
          </a> \
          </div> \
          <div class="modal modal-blur fade" id="esyaDetay'+val.id+'" role="dialog" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="true"> \
            <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable" role="document"> \
              <div class="modal-content"> \
                <div class="modal-header"> \
                  <h5 class="modal-title">'+val.name+'</h5> \
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button> \
                </div> \
                <div class="modal-body pb-1"> \
                  '+val.html+' \
                </div> \
                <div class="modal-footer"> \
                  <button type="button" class="btn w-100" data-bs-dismiss="modal">Kapat</button>  \
                </div> \
              </div> \
            </div> \
          </div> \
        </div>');
      });
    }else {
      $(div).append('<div class="col-lg-12 text-center p-3"> \
        <h3>Eşya bulunamadı.</h3> \
      </div>');
    }
  }
  var envanter = false;
  $('[href="#envanter"]').on('show.bs.tab',function(e) {
    if (envanter==false) {
      $.ajax({
        type: "get",
        url: url+"/Oyuncu/Envanter/"+pid,
        beforeSend: function(){
          $(".site_loading").show();
        },
        success: function(response){
          EsyalariYaz('#envanter>.esyalar',response);
        },
        complete: function(){
          $(".site_loading").hide();
        },
        dataType: "json"
      });
      envanter = true;
    }
  });
  var depoVeNesneMarket = false;
  $('[href="#depoVeNesneMarket"]').on('show.bs.tab',function(e) {
    if (depoVeNesneMarket==false) {
      $.ajax({
        type: "get",
        url: url+"/Oyuncu/DepoVeNesneMarket/"+pid,
        beforeSend: function(){
          $(".site_loading").show();
        },
        success: function(response){
          EsyalariYaz('#depoVeNesneMarket>.esyalar',response);
        },
        complete: function(){
          $(".site_loading").hide();
        },
        dataType: "json"
      });
      depoVeNesneMarket = true;
    }
  });
  $('[name="envanterEsyaAra"]').on("keyup", function() {
    var id    = $(this).data('id');
    var value = this.value.toLowerCase().trim();
    $("#"+id+">.esyalar>.col-lg-2").show().filter(function() {
      return $(this).text().toLowerCase().trim().indexOf(value) == -1;
    }).hide();
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
  var dataTablePazar = false;
  $('[href="#pazar"]').on('show.bs.tab',function(e) {
    if (dataTablePazar==false) {
      dataTablePazar = $('#ajax-pazar-market').DataTable({
        "processing":true,
        "serverSide":true,
        "dom": 'tpl',
        "sPaginationType": "simple",
        "language": {
          "url":url+"/assets/js/tr.json"
        },
        "searching": false,
        "ajax":{
          url:$('#ajax-pazar-market').data('url'),
          data: function ( d ) {
            d.search = {
              value : $('[name="pazarSearch"]').val()
            }
          },
          type:"POST"
        },
      });
      $('[name="pazarSearch"]').on('keyup',function(){
        dataTablePazar.ajax.reload();
      });
    }
  });
  var dataTableGenel = false;
  $('[href="#genel"]').on('show.bs.tab',function(e) {
    if (dataTableGenel==false) {
      dataTableGenel = $('#ajax-genel').DataTable({
        "processing":true,
        "serverSide":true,
        "dom": 'tpl',
        "sPaginationType": "simple",
        "language": {
          "url":url+"/assets/js/tr.json"
        },
        "searching": false,
        "ajax":{
          url:$('#ajax-genel').data('url'),
          data: function ( d ) {
            d.searchType  = $('[name="searchType"]').val(),
            d.searchWhere = $('[name="searchWhere"]').val(),
            d.genelSearch = $('[name="genelSearch"]').val()
          },
          type:"POST"
        },
      });
      $(".GenelAra").on("submit", function(e){
        dataTableGenel.ajax.reload();
        e.preventDefault();
      });
    }
  });
  $(".EsyaGonder").on("submit", function(e){
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Oyuncu/EsyaGonder",
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
