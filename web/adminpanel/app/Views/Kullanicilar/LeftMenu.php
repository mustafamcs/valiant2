<div class="col-md-4">
  <div class="card">
    <div class="card-body">
      <div class="row g-2 align-items-center">
        <div class="col">
          <h4 class="card-title m-0 user_name">
            <?=$kullaniciBilgileri->user_name?>
          </h4>
          <div class="small mt-1">
            <?php if ((strtotime($kullaniciBilgileri->user_login_date)+600)>time()): ?>
              <span class="badge bg-green"></span> <?=lang('Genel.cevrimici')?>
            <?php else: ?>
              <span class="badge bg-grey"></span> <?=lang('Genel.cevrimDisi')?>
            <?php endif; ?>
          </div>
        </div>
        <div class="col-auto">
          <label class="form-check form-switch status_update" style="margin-top:2px;" data-id="<?=$kullaniciBilgileri->user_id?>">
            <input class="form-check-input" style="background-size: 1.5rem;" type="checkbox" <?=$kullaniciBilgileri->user_status=="1"?'checked':false?>>
          </label>
        </div>
      </div>
    </div>
    <?php if (IsAllowedViewModule('kullaniciDetayiniGorebilsin')): ?>
      <div class="accordion-item">
        <h2 class="accordion-header">
          <a href="<?=base_url('Kullanicilar/Detay/'.$kullaniciBilgileri->user_id)?>" class="accordion-button text-decoration-none <?=WebTitle('Detay')?'':'collapsed'?>">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon me-1" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><line x1="12" y1="8" x2="12.01" y2="8" /><rect x="4" y="4" width="16" height="16" rx="2" /><polyline points="11 12 12 12 12 16 13 16" /></svg>
            <?=lang('Genel.detay')?>
          </a>
        </h2>
      </div>
    <?php endif; ?>
    <?php if (IsAllowedViewModule('kullaniciAdiniDegistirebilsin')): ?>
      <div class="accordion-item">
        <h2 class="accordion-header">
          <a href="<?=base_url('Kullanicilar/KullaniciAdi/'.$kullaniciBilgileri->user_id)?>" class="accordion-button text-decoration-none <?=WebTitle('KullaniciAdi')?'':'collapsed'?>">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon me-1" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><circle cx="12" cy="7" r="4" /><path d="M6 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2" /></svg>
            <?=lang('Hesap.sayfa.kullaniciAdi')?>
          </a>
        </h2>
      </div>
    <?php endif; ?>
    <?php if (IsAllowedViewModule('kullaniciSifreDegistirebilsin')): ?>
      <div class="accordion-item">
        <h2 class="accordion-header">
          <a href="<?=base_url('Kullanicilar/Sifre/'.$kullaniciBilgileri->user_id)?>" class="accordion-button text-decoration-none <?=WebTitle('Sifre')?'':'collapsed'?>">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon me-1" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><rect x="5" y="11" width="14" height="10" rx="2" /><circle cx="12" cy="16" r="1" /><path d="M8 11v-4a4 4 0 0 1 8 0v4" /></svg>
            <?=lang('Hesap.sayfa.sifre')?>
          </a>
        </h2>
      </div>
    <?php endif; ?>
    <?php if (IsAllowedViewModule('kullaniciYetkiVerebilsin')): ?>
      <div class="accordion-item">
        <h2 class="accordion-header">
          <a href="<?=base_url('Kullanicilar/Yetkilendirme/'.$kullaniciBilgileri->user_id)?>" class="accordion-button text-decoration-none <?=WebTitle('Yetkilendirme')?'':'collapsed'?>">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon me-1" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><circle cx="12" cy="12" r="9" /><path d="M10 16.5l2 -3l2 3m-2 -3v-2l3 -1m-6 0l3 1" /><circle cx="12" cy="7.5" r=".5" fill="currentColor" /></svg>
            <?=lang('Kullanicilar.sayfa.yetkilendirme')?>
          </a>
        </h2>
      </div>
    <?php endif; ?>
    <?php if (IsAllowedViewModule('kullaniciyiSilebilsin')): ?>
      <div class="accordion-item">
        <h2 class="accordion-header">
          <a href="<?=base_url('Kullanicilar/Sil/'.$kullaniciBilgileri->user_id)?>" class="accordion-button text-decoration-none <?=WebTitle('Sil')?'':'collapsed'?>">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon me-1" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><circle cx="9" cy="7" r="4" /><path d="M3 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2" /><path d="M17 9l4 4m0 -4l-4 4" /></svg>
            <?=lang('Genel.sil')?>
          </a>
        </h2>
      </div>
    <?php endif; ?>
    <?php if (IsAllowedViewModule('kullaniciOturumunuSonlandırabilsin')): ?>
      <div class="accordion-item">
        <h2 class="accordion-header">
          <a href="javascript:void(0)" class="accordion-button text-decoration-none oturumuSonlandir" data-header="<?=lang('Kullanicilar.sayfa.oturumuSonlandir')?>" data-message="<?=lang('Kullanicilar.sayfa.oturumuSonlandirNot')?>" data-yes="<?=lang('Genel.evet')?>" data-no="<?=lang('Genel.hayir')?>" data-id="<?=$kullaniciBilgileri->user_id?>">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon me-1" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M14 8v-2a2 2 0 0 0 -2 -2h-7a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h7a2 2 0 0 0 2 -2v-2" /><path d="M7 12h14l-3 -3m0 6l3 -3" /></svg>
            <?=lang('Kullanicilar.sayfa.oturumuSonlandir')?>
          </a>
        </h2>
      </div>
    <?php endif; ?>
    <?php if (IsAllowedViewModule('kullaniciIslemKayitlariniGorebilsin')): ?>
      <div class="accordion-item">
        <h2 class="accordion-header">
          <a href="<?=base_url('Kullanicilar/IslemKayitlari/'.$kullaniciBilgileri->user_id)?>" class="accordion-button text-decoration-none <?=WebTitle('IslemKayitlari')?'':'collapsed'?>">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon me-1" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M10 5a2 2 0 0 1 4 0a7 7 0 0 1 4 6v3a4 4 0 0 0 2 3h-16a4 4 0 0 0 2 -3v-3a7 7 0 0 1 4 -6" /><path d="M9 17v1a3 3 0 0 0 6 0v-1" /></svg>
            <?=lang('IslemKayitlari.sayfa.islemKayitlari')?>
          </a>
        </h2>
      </div>
    <?php endif; ?>
  </div>
</div>
