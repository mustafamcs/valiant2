<footer class="footer footer-transparent d-print-none">
  <div class="container">
    <div class="row text-center align-items-center flex-row-reverse">
      <div class="col-12 mt-3 mt-lg-0">
        <ul class="list-inline list-inline-dots mb-0">
          <li class="list-inline-item">
            <?=$ayarFooterYazisi->setting_content?>
          </li>
        </ul>
      </div>
    </div>
  </div>
</footer>
</div>
</div>
<div class="site_loading">
  <div class="sk-chase">
    <div class="sk-chase-dot"></div>
    <div class="sk-chase-dot"></div>
    <div class="sk-chase-dot"></div>
    <div class="sk-chase-dot"></div>
    <div class="sk-chase-dot"></div>
    <div class="sk-chase-dot"></div>
  </div>
</div>
<script src="<?=base_url('assets/js/jquery.min.js').'?'.versionKey?>"></script>
<script src="<?=base_url('assets/js/jquery.dataTables.min.js').'?'.versionKey?>"></script>
<script src="<?=base_url('assets/js/dataTables.bootstrap5.min.js').'?'.versionKey?>"></script>
<script src="<?=base_url('assets/js/tabler.min.js').'?'.versionKey?>"></script>
<script src="<?=base_url('assets/js/toastr.min.js').'?'.versionKey?>"></script>
<script src="<?=base_url('assets/js/sweetalert2.min.js').'?'.versionKey?>"></script>
<script src="<?=base_url('assets/js/select2.min.js').'?'.versionKey?>"></script>
<script src="<?=base_url('assets/js/jquery.fancybox.min.js').'?'.versionKey?>"></script>
<script src="<?=base_url('assets/js/jquery.nestable.min.js').'?'.versionKey?>"></script>
<script src="<?=base_url('assets/libs/choices.js/public/assets/scripts/choices.js').'?'.versionKey?>"></script>
<script src="<?=base_url('assets/libs/ckeditor/ckeditor.js').'?'.versionKey?>"></script>
<script type="text/javascript">
$(document).ready(function() {
  const url = $('body').data('url');
  IslemKayitiSayisi();
  setInterval(IslemKayitiSayisi,30000);
  function IslemKayitiSayisi() {
    $.ajax({
      type: "get",
      url: url+"/IslemKayitlari/IslemKayitiSayisi",
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
        }else {
          if (response.islemKayitiSayisi) {
            $('.islemKayitiSayisi').text(response.islemKayitiSayisi);
            $('.islemKayitiSayisi').removeClass('d-none');
          }else {
            $('.islemKayitiSayisi').addClass('d-none');
          }
        }
      },
      dataType: "json"
    });
  }
  $('.sonIslemKayitlariGetir').on('show.bs.dropdown',function(e){
    $.ajax({
      type: "get",
      url: url+"/IslemKayitlari/SonIslemKayitlari",
      success: function(response){
        if (response.sonIslemKayitlari==null) {
          $('.islemKayitlari').html('<div class="card-body text-center"><?=lang('Genel.henuzIslemKaydiYok')?></div>');
        }else {
          $('.islemKayitlari').html('');
          $.each(response.sonIslemKayitlari, function(index, val) {
            $('.islemKayitlari').append('<div class="card-body p-3 pb-2 pt-2"> \
            <a class="text-dark text-decoration-none" href="'+val.link+'" target="_blank">'+val.text+'</a> \
            <br><small class="text-secondary mt-2 mb-0" style="font-size:11px">'+val.time+'</small> \
            </div>');
          });
          $('.islemKayitiSayisi').addClass('d-none');
        }
      },
      dataType: "json"
    });
  });
  $('.OnBellekleriTemizle').on('click',function(e) {
    Swal.fire({
      title: "<?=lang('Genel.onBellekleriTemizle')?>",
      text:"<?=lang('Genel.onBellekleriTemizleNot')?>",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: "<?=lang('Genel.temizle')?>",
      cancelButtonText: "<?=lang('Genel.iptal')?>",
      closeOnConfirm: !1,
      closeOnCancel: !1
    })
    .then((result) => {
      if (result.value) {
        window.location.href = $(this).attr('href');
      }
    });
    e.preventDefault();
  });
  $(".OyuncuAra").on("submit", function(e){
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Oyuncu/Ara",
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
          window.location.href = response.link;
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
});
<?php $alert = session()->getFlashdata('alert')  ?>
<?php if ($alert): ?>
toastr["<?=$alert['type']?>"]("<?=$alert['text']?>");
<?php endif; ?>
</script>
<?php $uri = 'assets/js/ajax/'.$viewFolder.'/'.service('router')->methodName().'.js' ?>
<?php if (isset($viewFolder) && file_exists(FCPATH.'/'.$uri)): ?>
  <script src="<?=base_url($uri).'?'.versionKey?>"></script>
<?php endif; ?>
<script type="text/javascript">
$(document).ready(function() {
  var liveSearchTimer = null;
  $(document).on('input change', '.CanavarAra input, .CanavarAra select, .EsyaAra input, .EsyaAra select, .GenelAra input, .GenelAra select, .KayitAra input, .KayitAra select', function() {
    var form = $(this).closest('form');
    clearTimeout(liveSearchTimer);
    liveSearchTimer = setTimeout(function() { form.trigger('submit'); }, 400);
  });
});
</script>
<script type="text/javascript">
$(document).ready(function() {
  var hash = window.location.hash;
  hash && $('ul.nav a[href="' + hash + '"]').tab('show');

  $('.nav-tabs a').click(function (e) {
    if (
      window.location.pathname.indexOf('Canavar/Index')==-1
      && window.location.pathname.indexOf('Esya/Index')==-1
      && window.location.pathname.indexOf('NPC/Index')==-1
    ) {
      $(this).tab('show');
      var scrollmem = $('body').scrollTop();
      window.location.hash = this.hash;
      $('html,body').scrollTop(scrollmem);
    }
  });
});
</script>
</body>
</html>
