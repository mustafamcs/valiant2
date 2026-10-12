<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
  <meta http-equiv="X-UA-Compatible" content="ie=edge"/>
  <title><?php require_once VIEWPATH.'Static/Title.php' ?> - <?=$ayarSiteAdi->setting_content?></title>
  <link href="<?=base_url('assets/css/tabler.min.css').'?'.versionKey?>" rel="stylesheet"/>
  <link href="<?=base_url('assets/css/tabler-vendors.min.css').'?'.versionKey?>" rel="stylesheet"/>
  <link rel="icon" href="<?=base_url('favicon.ico').'?'.versionKey?>">
  <?=$ayarJavascriptKodlari->setting_content?>
</head>
<body class="antialiased d-flex flex-column <?=get_cookie('karanlik_tema')=="acik"?'theme-dark':''?>" data-url="<?=base_url()?>">
  <header class="navbar navbar-expand-md navbar-light d-print-none">
    <div class="container-xl">
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar-menu">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="navbar-brand d-none-navbar-horizontal pe-0 pe-md-3">
        <a href="<?=base_url('Anasayfa/Index')?>">
          <img src="<?=base_url('assets/img/logo.png').'?'.versionKey?>" width="110" height="32" alt="logo" class="navbar-brand-image">
        </a>
      </div>
      <?php if (IsAllowedViewModule('oyuncuArayabilsin')): ?>
        <form class="navbar-nav flex-row align-items-center OyuncuAra">
          <div class="w-50">
            <select class="form-select" name="user_column">
              <option value="id">ID</option>
              <option value="login" selected><?=lang('Genel.hesapAdi')?></option>
              <option value="mail"><?=lang('Genel.eposta')?></option>
              <?php if (IsAllowedViewModule('karakterDetayGorebilsin')): ?>
                <option value="name"><?=lang('Genel.karakterAdi')?></option>
              <?php endif; ?>
            </select>
          </div>
          <div class="w-50">
            <input type="text" class="form-control" autocomplete="off" name="user_search" placeholder="<?=lang('Genel.arama')?>" aria-label="<?=lang('Genel.arama')?>">
          </div>
          <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
          <button type="submit" class="btn btn-primary btn-sm px-2" style="height:36px;">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><circle cx="10" cy="10" r="7"></circle><line x1="21" y1="21" x2="15" y2="15"></line></svg>
          </button>
        </form>
      <?php endif; ?>
      <div class="navbar-nav flex-row order-md-last">
        <?php if (get_cookie('karanlik_tema')=="acik"): ?>
          <div class="nav-item dropdown d-flex me-2">
            <a href="<?=base_url('KaranlikTema/Kapat')?>" class="nav-link px-0">
              <svg xmlns="http://www.w3.org/2000/svg" class="icon text-yellow" style="width:28px;height:28px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><circle cx="12" cy="12" r="4" /><path d="M3 12h1m8 -9v1m8 8h1m-9 8v1m-6.4 -15.4l.7 .7m12.1 -.7l-.7 .7m0 11.4l.7 .7m-12.1 -.7l-.7 .7" /></svg>
            </a>
          </div>
        <?php else: ?>
          <div class="nav-item dropdown d-flex me-2">
            <a href="<?=base_url('KaranlikTema/Ac')?>" class="nav-link px-0">
              <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M12 3c.132 0 .263 0 .393 0a7.5 7.5 0 0 0 7.92 12.446a9 9 0 1 1 -8.313 -12.454z" /></svg>
            </a>
          </div>
        <?php endif; ?>
        <?php if (IsAllowedViewModule('onBellekTemizleyebilsin')): ?>
          <div class="nav-item dropdown d-flex me-2">
            <a href="<?=base_url('OnBellekleriTemizle')?>" class="OnBellekleriTemizle nav-link px-0">
              <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><line x1="4" y1="7" x2="20" y2="7" /><line x1="10" y1="11" x2="10" y2="17" /><line x1="14" y1="11" x2="14" y2="17" /><path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12" /><path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3" /></svg>
            </a>
          </div>
        <?php endif; ?>
        <div class="nav-item dropdown d-flex me-3">
          <a href="javascript:void(0)" class="sonIslemKayitlariGetir nav-link px-0" data-bs-toggle="dropdown">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M10 5a2 2 0 0 1 4 0a7 7 0 0 1 4 6v3a4 4 0 0 0 2 3h-16a4 4 0 0 0 2 -3v-3a7 7 0 0 1 4 -6" /><path d="M9 17v1a3 3 0 0 0 6 0v-1" /></svg>
            <span class="islemKayitiSayisi badge bg-red d-none"></span>
          </a>
          <div class="dropdown-menu dropdown-menu-end dropdown-menu-card" style="width: 320px;">
            <div class="card islemKayitlari" style="max-height:475px;overflow-y:auto"></div>
            <hr class="m-0">
            <div class="card">
              <div class="card-body text-center">
                <a class="text-dark text-decoration-none" href="<?=base_url('IslemKayitlari/Index')?>"><?=lang('IslemKayitlari.sayfa.tumIslemKayitlari')?></a>
              </div>
            </div>
          </div>
        </div>
        <div class="nav-item dropdown">
          <a href="javascript:void(0)" class="nav-link d-flex lh-1 text-reset p-0" data-bs-toggle="dropdown" aria-label="Menu">
            <span class="avatar avatar-sm avatar-rounded adminAvatar" style="background-image: url(<?=base_url('assets/img/avatar.png')?>)"></span>
            <div class="d-none d-xl-block ps-2">
              <div><?=$kullaniciBilgileri->user_name?></div>
            </div>
          </a>
          <div class="dropdown-menu dropdown-menu-end dropdown-menu-arrow">
            <a href="<?=base_url('Hesap/KullaniciAdi')?>" class="dropdown-item"><?=lang('Hesap.sayfa.hesabim')?></a>
            <div class="dropdown-divider"></div>
            <a href="<?=base_url('CikisYap')?>" class="dropdown-item"><?=lang('CikisYap.sayfa.cikisYap')?></a>
          </div>
        </div>
      </div>
    </div>
  </header>
  <?=view('Static/Menu')?>
