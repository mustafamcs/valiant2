<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none mb-2">
    <div class="row align-items-center">
      <div class="mb-1">
        <ol class="breadcrumb breadcrumb-alternate" aria-label="breadcrumbs">
          <li class="breadcrumb-item"><a href="<?=base_url()?>"><?=lang('Ayarlar.sayfa.ayarlar')?></a></li>
          <li class="breadcrumb-item active"><a href="<?=base_url('Ayarlar/LogoYukle')?>"><?=lang('Ayarlar.sayfa.logoYukle')?></a></li>
        </ol>
      </div>
    </div>
  </div>
  <div class="row row-cards">
    <div class="col-md-12">
      <div class="card">
        <?=view('Ayarlar/TabMenu')?>
        <div class="card-body">
          <form class="LogoGuncelle">
            <div class="mb-3">
              <div class="form-label"><?=lang('Ayarlar.sayfa.yukluLogo')?></div>
              <img src="<?=base_url('assets/img/logo.png').'?'.versionKey?>" alt="logo" class="mx-auto d-block">
            </div>
            <div class="mb-1">
              <input type="file" class="form-control mb-1" name="logo" accept="image/jpeg,image/gif,image/png" required />
              <small><?=lang('Ayarlar.sayfa.maksimumDosyaBoyutu')?><span class="text-red">4 MB</span></small>
              -
              <small><?=lang('Ayarlar.sayfa.desteklenenFormatlar')?><span class="text-red">.jpg .png .gif</span></small>
            </div>
            <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
            <div class="form-footer mt-2">
              <button type="submit" class="btn btn-primary w-100"><?=lang('Ayarlar.sayfa.logoyuYukle')?></button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
<?=view('Static/Footer')?>
