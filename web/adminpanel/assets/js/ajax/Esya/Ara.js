$(document).ready(function(){
  const url = $('body').data('url');
  var dataTable = "";
  $(".EsyaAra").on("submit", function(e){
    if (dataTable==="") {
      dataTable = $('#ajax-datatable').DataTable({
        "processing":true,
        "serverSide":true,
        "dom": 'tp',
        "sPaginationType": "simple",
        "language": {
          "url":url+"/assets/js/tr.json"
        },
        "searching": false,
        "ajax":{
          url:$('#ajax-datatable').data('url'),
          data: function ( d ) {
            d.vnum        = $('[name="vnum"]').val(),
            d.countStart  = $('[name="countStart"]').val(),
            d.countFinish = $('[name="countFinish"]').val(),
            d.socket0     = $('[name="socket0"]').val(),
            d.socket1     = $('[name="socket1"]').val(),
            d.socket2     = $('[name="socket2"]').val(),
            d.socket3     = $('[name="socket3"]').val(),
            d.socket4     = $('[name="socket4"]').val(),
            d.socket5     = $('[name="socket5"]').val(),
            d.window      = $('[name="window"]').val(),
            d.limit       = $('[name="limit"]').val(),
            d.attrtype0   = $('[name="attrtype0"]').val(),
            d.attrvalue0  = $('[name="attrvalue0"]').val(),
            d.attrequal0  = $('[name="attrequal0"]').val(),
            d.attrtype1   = $('[name="attrtype1"]').val(),
            d.attrvalue1  = $('[name="attrvalue1"]').val(),
            d.attrequal1  = $('[name="attrequal1"]').val(),
            d.attrtype2   = $('[name="attrtype2"]').val(),
            d.attrvalue2  = $('[name="attrvalue2"]').val(),
            d.attrequal2  = $('[name="attrequal2"]').val(),
            d.attrtype3   = $('[name="attrtype3"]').val(),
            d.attrvalue3  = $('[name="attrvalue3"]').val(),
            d.attrequal3  = $('[name="attrequal3"]').val(),
            d.attrtype4   = $('[name="attrtype4"]').val(),
            d.attrvalue4  = $('[name="attrvalue4"]').val(),
            d.attrequal4  = $('[name="attrequal4"]').val()
          },
          type:"POST"
        },
      });
    }else {
      dataTable.ajax.reload();
    }
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
  $('.EfsunSec').select2();
});
