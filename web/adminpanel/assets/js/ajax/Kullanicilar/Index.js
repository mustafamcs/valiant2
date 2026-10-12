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
        d.user_status = $('[name="user_status"]').val()
      },
      type:"POST"
    },
  });
  $('[name="search"]').on('keyup',function(){
    dataTable.ajax.reload();
  });
  $('[name="user_status"]').on('change',function(){
    dataTable.ajax.reload();
  });
  $(document).on('change','.status_update',function(e){
    var id = $(this).data('id');
    $.ajax({
      type: "post",
      url: url+"/Kullanicilar/Durum",
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
});
