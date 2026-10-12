$(document).ready(function(){
  const url = $('body').data('url');
  var currentGroup = 0;
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
      url: url+"/Sandik/GrupEkle",
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
  function renderItems(items){
    var html = '';
    items.forEach(function(it){
      html += '<tr data-id="'+it.id+'">'
        +'<td class="text-truncate max-width-300"><img src="'+url+'/assets/img/icon/'+it.icon+'" width="32" height="32" alt=""> '+it.item_vnum+(it.name?' - '+it.name:'')+'</td>'
        +'<td><input type="number" class="form-control form-control-sm item-count" value="'+it.count+'" min="1" style="width:90px"></td>'
        +'<td><input type="number" class="form-control form-control-sm item-prob" value="'+it.prob+'" min="0" style="width:90px"></td>'
        +'<td><input type="number" class="form-control form-control-sm item-rare" value="'+it.rare+'" min="0" style="width:90px"></td>'
        +'<td class="text-muted">'+it.idx+'</td>'
        +'<td class="text-center">'
        +'<a class="btn btn-primary pt-1 pb-1 ps-2 pe-2 itemKaydet" href="javascript:void(0)" data-id="'+it.id+'"><svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" style="width:22px;height:22px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M6 4h10l4 4v10a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2v-12a2 2 0 0 1 2 -2" /><circle cx="12" cy="14" r="2" /><polyline points="14 4 14 8 8 8 8 4" /></svg></a>'
        +'<a class="btn btn-danger pt-1 pb-1 ps-2 pe-2 ms-2 itemSil" href="javascript:void(0)" data-id="'+it.id+'"><svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" style="width:22px;height:22px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><line x1="4" y1="7" x2="20" y2="7" /><line x1="10" y1="11" x2="10" y2="17" /><line x1="14" y1="11" x2="14" y2="17" /><path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12" /><path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3" /></svg></a>'
        +'</td></tr>';
    });
    if (!items.length) {
      html = '<tr><td colspan="6" class="text-center text-muted">-</td></tr>';
    }
    $('#sandikIcerik').html(html);
  }
  function loadDetay(id){
    $.ajax({
      type: "get",
      url: url+"/Sandik/Detay/"+id,
      beforeSend: function(){
        $(".site_loading").show();
      },
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
          $('[data-bs-dismiss="modal"]').click();
        }else {
          currentGroup = response.vnum;
          $('#sandikBaslik').text('('+response.vnum+(response.name?' - '+response.name:'')+')');
          $('.GrupDuzenle [name="vnum"]').val(response.vnum);
          $('.GrupDuzenle [name="type"]').val(response.type);
          $('.ItemEkle [name="group_vnum"]').val(response.vnum);
          renderItems(response.items);
        }
      },
      complete: function(){
        $(".site_loading").hide();
      },
      dataType: "json"
    });
  }
  $(document).on('click','[data-bs-target="#duzenle"]', function() {
    loadDetay($(this).data('id'));
  });
  $(".GrupDuzenle").on("submit", function(e){
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Sandik/GrupDuzenle",
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
  $(".ItemEkle").on("submit", function(e){
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Sandik/ItemEkle",
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
          loadDetay(currentGroup);
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
  $(document).on('click','.itemKaydet', function(e){
    var tr = $(this).closest('tr');
    var data = new FormData();
    data.append('id', $(this).data('id'));
    data.append('count', tr.find('.item-count').val());
    data.append('prob', tr.find('.item-prob').val());
    data.append('rare', tr.find('.item-rare').val());
    $.ajax({
      type: "post",
      url: url+"/Sandik/ItemDuzenle",
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
  $(document).on('click','.itemSil', function(e){
    var id = $(this).data('id');
    $.ajax({
      type: "post",
      url: url+"/Sandik/ItemSil",
      data: {id},
      beforeSend: function(){
        $(".site_loading").show();
      },
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
        }else {
          toastr["success"](response.success);
          loadDetay(currentGroup);
          dataTable.ajax.reload();
        }
      },
      complete: function(){
        $(".site_loading").hide();
      },
      dataType: "json"
    });
    e.preventDefault();
  });
  $(document).on('click','.sandikSil',function(e) {
    var el = $(this);
    Swal.fire({
      title: el.data('header'),
      html: el.data('message'),
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: el.data('yes'),
      cancelButtonText: el.data('no'),
      closeOnConfirm: !1,
      closeOnCancel: !1
    })
    .then((result) => {
      if (result.value) {
        var vnum = el.data('id');
        $.ajax({
          type: "post",
          url: url+"/Sandik/Sil",
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
      url: url+"/Sandik/SunucuyaGonder",
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
  $('#duzenle').on('shown.bs.modal', function () {
    $('.ItemEkle .Esyalar').select2({
      dropdownParent: $('#duzenle'),
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
  $('.Ekle .Esyalar, #ekle .Esyalar').select2({
    dropdownParent: $('#ekle'),
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
