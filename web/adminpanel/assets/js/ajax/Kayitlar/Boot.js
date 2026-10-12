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
        d.logSearch   = $('[name="logSearch"]').val()
      },
      type:"POST"
    },
  });
  $(".KayitAra").on("submit", function(e){
    dataTable.ajax.reload();
    e.preventDefault();
  });
});
