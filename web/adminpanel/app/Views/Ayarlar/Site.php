<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none mb-2">
    <div class="row align-items-center">
      <div class="mb-1">
        <ol class="breadcrumb breadcrumb-alternate" aria-label="breadcrumbs">
          <li class="breadcrumb-item"><a href="<?=base_url()?>"><?=lang('Ayarlar.sayfa.ayarlar')?></a></li>
          <li class="breadcrumb-item active"><a href="<?=base_url('Ayarlar/Site')?>"><?=lang('Ayarlar.sayfa.siteAyarlari')?></a></li>
        </ol>
      </div>
    </div>
  </div>
  <div class="row row-cards">
    <div class="col-md-12">
      <div class="card">
        <?=view('Ayarlar/TabMenu')?>
        <div class="card-body">
          <form class="SiteGuncelle">
            <div class="mb-2">
              <div class="form-label"><?=lang('Ayarlar.sayfa.siteAdi')?></div>
              <input type="text" class="form-control" name="siteAdi" value="<?=!empty($siteAdi->setting_content)?$siteAdi->setting_content:""?>" required>
            </div>
            <div class="mb-2">
              <div class="form-label"><?=lang('Ayarlar.sayfa.footerYazisi')?></div>
              <textarea class="form-control" name="footerYazisi" rows="2" cols="80" required><?=!empty($footerYazisi->setting_content)?$footerYazisi->setting_content:""?></textarea>
            </div>
            <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
            <div class="form-footer mt-2">
              <button type="submit" class="btn btn-primary w-100"><?=lang('Ayarlar.sayfa.siteAyarlariniGuncelle')?></button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
<?=view('Static/Footer')?>
