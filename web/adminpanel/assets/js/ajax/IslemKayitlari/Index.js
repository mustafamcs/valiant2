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
        },
        d.log_status  = $('[name="log_status"]').val(),
        d.log_user_id = $('[name="log_user_id"]').val()
      },
      type:"POST"
    },
  });
  $('[name="search"]').on('keyup',function(){
    dataTable.ajax.reload();
  });
  $('[name="log_status"]').on('change',function(){
    dataTable.ajax.reload();
  });
  $('[name="log_user_id"]').on('change',function(){
    dataTable.ajax.reload();
  });
  $('.log_user_id').select2({
    ajax: {
      url: url+'/IslemKayitlari/Kullanicilar',
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
