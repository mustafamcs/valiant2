<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
  <meta http-equiv="X-UA-Compatible" content="ie=edge"/>
  <title><?=lang('Hata.sayfaBulunamadi').' - '.lang('Genel.yonetimPaneli')?></title>
  <link href="<?=base_url('assets/css/tabler.min.css')?>" rel="stylesheet"/>
  <link rel="icon" href="<?=base_url('favicon.ico')?>">
</head>
<body class="antialiased d-flex flex-column <?=get_cookie('karanlik_tema')=="acik"?'theme-dark':''?>" data-url="<?=base_url()?>">
  <div class="flex-fill d-flex align-items-center justify-content-center">
    <div class="container-tight py-6">
      <div class="empty">
        <div class="empty-header mb-2">404</div>
        <p class="empty-title"><?=lang('Hata.sayfaBulunamadi')?></p>
        <p class="empty-subtitle text-muted">
          <?=lang('Hata.sayfaBulunamadiAciklama')?>
        </p>
        <div class="empty-action mt-2">
          <a href="<?=$link?>" class="btn btn-primary">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><line x1="5" y1="12" x2="19" y2="12" /><line x1="5" y1="12" x2="11" y2="18" /><line x1="5" y1="12" x2="11" y2="6" /></svg>
            <?=lang('Hata.geriDon')?>
          </a>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
