<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none mb-2">
    <div class="row align-items-center">
      <div class="mb-1">
        <ol class="breadcrumb breadcrumb-alternate" aria-label="breadcrumbs">
          <li class="breadcrumb-item"><a href="<?=base_url()?>"><?=lang('Hesap.sayfa.hesabim')?></a></li>
          <li class="breadcrumb-item active"><a href="<?=base_url('Hesap/EPosta')?>"><?=lang('Hesap.sayfa.kullaniciAdi')?></a></li>
        </ol>
      </div>
    </div>
  </div>
  <div class="row row-cards">
    <div class="col-md-12">
      <div class="card">
        <?=view('Hesap/TabMenu')?>
        <div class="card-body">
          <div class="alert alert-info">
            <?=lang('Hesap.sayfa.kullaniciAdiNot')?>
          </div>
          <form class="KullaniciAdiDegistir">
            <div class="form-label"><?=lang('Hesap.sayfa.mevcutKullaniciAdi')?></div>
            <div class="input-icon mb-3">
              <span class="input-icon-addon">
                <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><circle cx="12" cy="7" r="4" /><path d="M6 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2" /></svg>
              </span>
              <input type="text" class="form-control" name="kullaniciAdi" minlength="3" maxlength="25" value="<?=$kullaniciBilgileri->user_name?>">
            </div>
            <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
            <div class="form-footer mt-2">
              <button type="submit" class="btn btn-primary w-100"><?=lang('Hesap.sayfa.kullaniciAdiniDegistir')?></button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
<?=view('Static/Footer')?>
