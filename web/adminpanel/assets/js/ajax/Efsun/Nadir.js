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
  $('[name="search"]').on('change',function(){
    dataTable.ajax.reload();
  });
  $(document).on('click','[data-bs-target="#duzenle"]', function(event) {
    var id = $(this).data('id');
    $.ajax({
      type: "get",
      url: url+"/Efsun/NadirDetay/"+id,
      beforeSend: function(){
        $(".site_loading").show();
      },
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
          $('[data-bs-dismiss="modal"]').click();
        }else {
          $('.Duzenle [name="apply"]').val(response.apply);
          $('.Duzenle [name="prob"]').val(response.prob);
          $('.Duzenle [name="lv1"]').val(response.lv1);
          $('.Duzenle [name="lv2"]').val(response.lv2);
          $('.Duzenle [name="lv3"]').val(response.lv3);
          $('.Duzenle [name="lv4"]').val(response.lv4);
          $('.Duzenle [name="lv5"]').val(response.lv5);
          $('.Duzenle [name="weapon"]').val(response.weapon);
          $('.Duzenle [name="body"]').val(response.body);
          $('.Duzenle [name="wrist"]').val(response.wrist);
          $('.Duzenle [name="foots"]').val(response.foots);
          $('.Duzenle [name="neck"]').val(response.neck);
          $('.Duzenle [name="head"]').val(response.head);
          $('.Duzenle [name="shield"]').val(response.shield);
          $('.Duzenle [name="ear"]').val(response.ear);
          $('.Duzenle [name="costume_body"]').val(response.costume_body);
          $('.Duzenle [name="costume_hair"]').val(response.costume_hair);
          $('.Duzenle [name="costume_weapon"]').val(response.costume_weapon);
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
      url: url+"/Efsun/NadirDuzenle",
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
      url: url+"/Efsun/SunucuyaGonder",
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
  $('.select2').select2();
});
