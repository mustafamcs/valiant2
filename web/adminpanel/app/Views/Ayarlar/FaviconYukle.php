<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none mb-2">
    <div class="row align-items-center">
      <div class="mb-1">
        <ol class="breadcrumb breadcrumb-alternate" aria-label="breadcrumbs">
          <li class="breadcrumb-item"><a href="<?=base_url()?>"><?=lang('Ayarlar.sayfa.ayarlar')?></a></li>
          <li class="breadcrumb-item active"><a href="<?=base_url('Ayarlar/FaviconYukle')?>"><?=lang('Ayarlar.sayfa.faviconYukle')?></a></li>
        </ol>
      </div>
    </div>
  </div>
  <div class="row row-cards">
    <div class="col-md-12">
      <div class="card">
        <?=view('Ayarlar/TabMenu')?>
        <div class="card-body">
          <form class="FaviconGuncelle">
            <div class="mb-3">
              <div class="form-label"><?=lang('Ayarlar.sayfa.yukluFavicon')?></div>
              <img src="<?=base_url('favicon.ico').'?'.versionKey?>" alt="favicon">
            </div>
            <div class="mb-1">
              <input type="file" class="form-control mb-1" name="favicon" accept="image/x-icon" required />
              <small><?=lang('Ayarlar.sayfa.maksimumDosyaBoyutu')?><span class="text-red">1 MB</span></small>
              -
              <small><?=lang('Ayarlar.sayfa.desteklenenFormatlar')?><span class="text-red">.ico</span></small>
            </div>
            <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
            <div class="form-footer mt-2">
              <button type="submit" class="btn btn-primary w-100"><?=lang('Ayarlar.sayfa.faviconuYukle')?></button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
<?=view('Static/Footer')?>
