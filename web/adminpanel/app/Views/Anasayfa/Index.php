<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none">
    <div class="row align-items-center">
      <div class="col">
        <h1 class="page-title"><?=lang('Anasayfa.sayfa.anasayfa')?></h1>
      </div>
      <div class="col-auto d-md-flex">
        <span class="text-muted" id="sonGuncelleme" style="line-height:32px;font-size:.8rem"></span>
      </div>
    </div>
  </div>
  <div class="row row-deck row-cards" id="istatistikKartlar">
    <div class="col-6 col-md-4 col-lg-2">
      <div class="card">
        <div class="card-body p-3 text-center">
          <div class="mb-1">
            <span class="avatar avatar-sm" style="background:rgba(32,107,196,.12);color:#206bc4">
              <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><circle cx="9" cy="7" r="4"/><path d="M3 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/><path d="M21 21v-2a4 4 0 0 0 -3 -3.85"/></svg>
            </span>
          </div>
          <div class="h2 mb-0" id="statOnline">0</div>
          <div class="text-muted" style="font-size:.8rem"><?=lang('Anasayfa.sayfa.toplamOyuncuSayisi')?></div>
        </div>
      </div>
    </div>
    <div class="col-6 col-md-4 col-lg-2">
      <div class="card">
        <div class="card-body p-3 text-center">
          <div class="mb-1">
            <span class="avatar avatar-sm" style="background:rgba(47,179,68,.12);color:#2fb344">
              <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><circle cx="12" cy="7" r="4"/><path d="M6 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2"/></svg>
            </span>
          </div>
          <div class="h2 mb-0" id="statHesap">-</div>
          <div class="text-muted" style="font-size:.8rem"><?=lang('Genel.hesap')?></div>
        </div>
      </div>
    </div>
    <div class="col-6 col-md-4 col-lg-2">
      <div class="card">
        <div class="card-body p-3 text-center">
          <div class="mb-1">
            <span class="avatar avatar-sm" style="background:rgba(174,62,201,.12);color:#ae3ec9">
              <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 7h-3a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-3"/><path d="M9 15h3l8.5 -8.5a1.5 1.5 0 0 0 -3 -3l-8.5 8.5v3"/><line x1="16" y1="5" x2="19" y2="8"/></svg>
            </span>
          </div>
          <div class="h2 mb-0" id="statKarakter">-</div>
          <div class="text-muted" style="font-size:.8rem"><?=lang('Genel.karakter')?></div>
        </div>
      </div>
    </div>
    <div class="col-6 col-md-4 col-lg-2">
      <div class="card">
        <div class="card-body p-3 text-center">
          <div class="mb-1">
            <span class="avatar avatar-sm" style="background:rgba(230,162,60,.12);color:#e6a23c">
              <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M3 21l1.65 -3.8a9 9 0 1 1 3.4 2.9l-5.05 .9"/><path d="M9 10l.01 0"/><path d="M15 10l.01 0"/><path d="M9.5 15a3.5 3.5 0 0 0 5 0"/></svg>
            </span>
          </div>
          <div class="h2 mb-0" id="statLonca">-</div>
          <div class="text-muted" style="font-size:.8rem"><?=lang('Genel.lonca')?></div>
        </div>
      </div>
    </div>
    <div class="col-6 col-md-4 col-lg-2">
      <div class="card">
        <div class="card-body p-3 text-center">
          <div class="mb-1">
            <span class="avatar avatar-sm" style="background:rgba(214,57,57,.12);color:#d63939">
              <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M6 21l15 -15l-3 -3l-15 15l3 3"/><path d="M15 6l3 3"/><path d="M9 3a2 2 0 0 1 2 2"/><path d="M14 8l3 3"/><path d="M4 16l4 4"/></svg>
            </span>
          </div>
          <div class="h2 mb-0" id="statEsya">-</div>
          <div class="text-muted" style="font-size:.8rem"><?=lang('Genel.esya')?></div>
        </div>
      </div>
    </div>
    <div class="col-6 col-md-4 col-lg-2">
      <div class="card">
        <div class="card-body p-3 text-center">
          <div class="mb-1">
            <span class="avatar avatar-sm" style="background:rgba(12,166,120,.12);color:#0ca678">
              <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><circle cx="6" cy="19" r="2"/><circle cx="17" cy="19" r="2"/><path d="M17 17h-11v-14h-2"/><path d="M6 5l14 1l-1 7h-13"/></svg>
            </span>
          </div>
          <div class="h2 mb-0" id="statNesne">-</div>
          <div class="text-muted" style="font-size:.8rem"><?=lang('NesneMarket.sayfa.nesneMarket')?></div>
        </div>
      </div>
    </div>
  </div>
  <?php if (IsAllowedViewModule('anasayfaOnlineGorebilsin') && p2pStatus==1 && p2pStatistics==1): ?>
    <div class="row row-cards">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h3 class="card-title">
              <svg xmlns="http://www.w3.org/2000/svg" class="icon me-1" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M3 12h4l3 8l4 -16l3 8h4"/></svg>
              <?=lang('Anasayfa.sayfa.toplamOyuncuSayisi')?>
            </h3>
            <div class="card-actions">
              <span class="badge bg-blue-lt me-2" id="onlineBadge">0</span>
              <button class="btn btn-primary btn-sm IstatistikGetir px-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="icon mx-0" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M20 11a8.1 8.1 0 0 0 -15.5 -2m-.5 -4v4h4"></path><path d="M4 13a8.1 8.1 0 0 0 15.5 2m.5 4v-4h-4"></path></svg>
              </button>
            </div>
          </div>
          <div class="table-responsive">
            <table class="table table-vcenter card-table table-striped">
              <thead>
                <tr>
                  <th><?=lang('Genel.kanal')?></th>
                  <th class="text-center"><span style="color:#d63939">&#9679;</span> Shinsoo</th>
                  <th class="text-center"><span style="color:#f59f00">&#9679;</span> Chunjo</th>
                  <th class="text-center"><span style="color:#206bc4">&#9679;</span> Jinno</th>
                  <th class="text-center"><?=lang('Genel.toplam')?></th>
                </tr>
              </thead>
              <tbody id="onlineCount">
                <tr>
                  <td colspan="5" class="text-center text-muted py-4">-</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  <?php endif; ?>
</div>
<?=view('Static/Footer')?>
<script type="text/javascript">
$(document).ready(function(){
  const url = $('body').data('url');
  function damga(){
    var d = new Date();
    $('#sonGuncelleme').text(('0'+d.getHours()).slice(-2)+':'+('0'+d.getMinutes()).slice(-2)+':'+('0'+d.getSeconds()).slice(-2));
  }
  $.ajax({
    type: "get",
    url: url+'/Anasayfa/Istatistikler',
    success: function(r){
      $('#statHesap').text(r.hesap);
      $('#statKarakter').text(r.karakter);
      $('#statLonca').text(r.lonca);
      $('#statEsya').text(r.esya);
      $('#statNesne').text(r.nesne);
      damga();
    },
    dataType: "json"
  });
  <?php if (IsAllowedViewModule('anasayfaOnlineGorebilsin') && p2pStatus==1 && p2pStatistics==1): ?>
  $('.IstatistikGetir').on('click',function (e) {
    $.ajax({
      type: "get",
      url: url+'/Anasayfa/OnlineCount',
      success: function(response){
        var m = response.total.match(/(\d+)/);
        if (m) {
          $('#statOnline').text(m[1]);
          $('#onlineBadge').text(m[1]);
        }
        $('#onlineCount').html("");
        $.each(response.chTR, function(index, val) {
          $('#onlineCount').append(val);
        });
        $('#onlineCount').append(response.totalTr);
        damga();
      },
      dataType: "json"
    });
  });
  $('.IstatistikGetir').trigger('click');
  setInterval(function(){ $('.IstatistikGetir').trigger('click'); }, 30000);
  <?php endif; ?>
});
</script>
