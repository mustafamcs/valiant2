<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
  <meta http-equiv="X-UA-Compatible" content="ie=edge"/>
  <title><?=lang('GirisYap.sayfa.girisYap').' - '.lang('Genel.yonetimPaneli')?></title>
  <link href="<?=base_url('assets/css/tabler.min.css')?>" rel="stylesheet"/>
  <link rel="icon" href="<?=base_url('favicon.ico')?>">
  <style>
    body{
      background:#0e1420;
      background-image:
        radial-gradient(800px 400px at 85% -10%, rgba(32,107,196,.35), transparent 60%),
        radial-gradient(700px 500px at -10% 110%, rgba(94,142,219,.18), transparent 55%),
        linear-gradient(160deg,#0e1420,#131b2c 60%,#0e1420);
      min-height:100vh;
    }
    .giris-kart{
      border:1px solid rgba(255,255,255,.08);
      border-radius:14px;
      overflow:hidden;
      box-shadow:0 24px 70px rgba(0,0,0,.5);
      background:#fff;
    }
    .giris-marka{
      background:linear-gradient(165deg,#1a5faa 0%,#206bc4 45%,#163e6e 100%);
      color:#fff;
      display:flex;
      flex-direction:column;
      justify-content:center;
      padding:48px 40px;
      position:relative;
      overflow:hidden;
    }
    .giris-marka::after{
      content:"";
      position:absolute;inset:0;
      background:
        radial-gradient(320px 160px at 90% 8%, rgba(255,255,255,.14), transparent 60%),
        radial-gradient(400px 200px at -5% 100%, rgba(0,0,0,.18), transparent 60%);
      pointer-events:none;
    }
    .giris-marka img{filter:drop-shadow(0 3px 10px rgba(0,0,0,.35))}
    .giris-marka h1{font-size:1.6rem;font-weight:800;letter-spacing:-.3px;margin:18px 0 6px}
    .giris-marka p{opacity:.85;font-size:.92rem;margin:0;position:relative;z-index:1}
    .giris-marka .rozet{
      display:inline-flex;align-items:center;gap:8px;
      background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);
      border-radius:99px;padding:6px 14px;font-size:.75rem;font-weight:600;
      position:relative;z-index:1;width:fit-content;
    }
    .giris-form{padding:44px 40px}
    .giris-form h2{font-size:1.25rem;font-weight:700}
    .giris-form .form-control{
      border-radius:8px;
      padding:.65rem .9rem;
      border-color:#e2e8f0;
    }
    .giris-form .form-control:focus{border-color:#206bc4;box-shadow:0 0 0 3px rgba(32,107,196,.15)}
    .giris-form .input-icon .form-control{padding-left:2.4rem}
    .giris-btn{
      border-radius:8px;font-weight:700;font-size:.95rem;
      padding:.7rem;background:linear-gradient(180deg,#2b7fd8,#206bc4);
      border:none;box-shadow:0 6px 18px rgba(32,107,196,.35);
    }
    .giris-btn:hover{background:linear-gradient(180deg,#206bc4,#1a5faa);color:#fff}
    .giris-alt{font-size:.78rem;color:#94a3b8;text-align:center;margin-top:18px}
    @media (max-width:767px){ .giris-marka{display:none} .giris-form{padding:36px 26px} }
  </style>
</head>
<body class="antialiased d-flex flex-column" data-url="<?=base_url()?>">
  <div class="flex-fill d-flex align-items-center justify-content-center py-4">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-12 col-md-10 col-lg-8">
          <div class="giris-kart d-flex">
            <div class="giris-marka col-md-5 d-none d-md-flex">
              <span class="rozet">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><rect x="3" y="4" width="18" height="8" rx="3"/><rect x="3" y="12" width="18" height="8" rx="3"/><line x1="7" y1="8" x2="7.01" y2="8"/><line x1="7" y1="16" x2="7.01" y2="16"/></svg>
                <?=lang('Genel.yonetimPaneli')?>
              </span>
              <img src="<?=base_url('assets/img/logo.png')?>" width="130" alt="logo">
              <h1><?=$ayarSiteAdi ? esc($ayarSiteAdi->setting_content) : lang('Genel.yonetimPaneli')?></h1>
              <p><?=$ayarFooterYazisi ? esc($ayarFooterYazisi->setting_content) : ''?></p>
            </div>
            <div class="giris-form col-12 col-md-7">
              <div class="text-center d-md-none mb-3">
                <img src="<?=base_url('assets/img/logo.png')?>" height="34" alt="logo">
              </div>
              <h2 class="mb-1"><?=lang('GirisYap.sayfa.girisYap')?></h2>
              <div class="text-muted mb-4" style="font-size:.85rem"><?=$ayarSiteAdi ? esc($ayarSiteAdi->setting_content) : ''?></div>
              <form class="GirisYap">
                <div class="mb-3">
                  <label class="form-label"><?=lang('Genel.kullaniciAdi')?></label>
                  <div class="input-icon">
                    <span class="input-icon-addon">
                      <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><circle cx="12" cy="7" r="4"/><path d="M6 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2"/></svg>
                    </span>
                    <input type="text" name="name" class="form-control" placeholder="<?=lang('GirisYap.sayfa.kullaniciAdiGir')?>" autocomplete="username">
                  </div>
                </div>
                <div class="mb-2">
                  <label class="form-label"><?=lang('Genel.sifre')?></label>
                  <div class="input-group input-group-flat">
                    <div class="input-icon flex-fill">
                      <span class="input-icon-addon">
                        <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><rect x="5" y="11" width="14" height="10" rx="2"/><circle cx="12" cy="16" r="1"/><path d="M8 11v-4a4 4 0 0 1 8 0v4"/></svg>
                      </span>
                      <input type="password" name="password" class="form-control" placeholder="<?=lang('GirisYap.sayfa.sifreGiriniz')?>" autocomplete="current-password">
                    </div>
                    <span class="input-group-text">
                      <a href="javascript:void(0)" class="link-secondary sifreyiGoster" title="<?=lang('Genel.sifreyiGoster')?>" data-bs-toggle="tooltip">
                        <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><circle cx="12" cy="12" r="2"/><path d="M22 12c-2.667 4.667 -6 7 -10 7s-7.333 -2.333 -10 -7c2.667 -4.667 6 -7 10 -7s7.333 2.333 10 7"/></svg>
                      </a>
                    </span>
                  </div>
                </div>
                <div class="mt-3">
                  <label class="form-check">
                    <input type="checkbox" name="remember" checked class="form-check-input"/>
                    <span class="form-check-label"><?=lang('GirisYap.sayfa.beniHatirla')?></span>
                  </label>
                </div>
                <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
                <div class="form-footer mt-3">
                  <button type="submit" class="btn btn-primary giris-btn w-100"><?=lang('GirisYap.sayfa.girisYap')?></button>
                </div>
              </form>
              <div class="giris-alt"><?=$ayarFooterYazisi ? esc($ayarFooterYazisi->setting_content) : ''?></div>
            </div>
          </div>
        </div>
      </div>
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
  <script src="<?=base_url('assets/js/jquery.min.js')?>"></script>
  <script src="<?=base_url('assets/js/tabler.min.js')?>"></script>
  <script src="<?=base_url('assets/js/toastr.min.js')?>"></script>
  <script type="text/javascript">
  $(document).ready(function() {
    $('.sifreyiGoster').on('click',function(e) {
      if ($('[name="password"]').attr('type')=="text") {
        $('[name="password"]').attr('type','password');
      }else {
        $('[name="password"]').attr('type','text');
      }
    });
    $('.GirisYap').on('submit', function(e){
      var data = new FormData(this);
      var url = $("body").data("url");
      $.ajax({
        type: "post",
        url: url+"/GirisYap/GirisYap",
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
            window.location.href = url+"/Anasayfa/Index";
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
</body>
</html>
