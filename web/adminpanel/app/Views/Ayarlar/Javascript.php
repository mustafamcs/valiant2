<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none mb-2">
    <div class="row align-items-center">
      <div class="mb-1">
        <ol class="breadcrumb breadcrumb-alternate" aria-label="breadcrumbs">
          <li class="breadcrumb-item"><a href="<?=base_url()?>"><?=lang('Ayarlar.sayfa.ayarlar')?></a></li>
          <li class="breadcrumb-item active"><a href="<?=base_url('Ayarlar/Javascript')?>"><?=lang('Ayarlar.sayfa.javascriptKodlari')?></a></li>
        </ol>
      </div>
    </div>
  </div>
  <div class="row row-cards">
    <div class="col-md-12">
      <div class="card">
        <?=view('Ayarlar/TabMenu')?>
        <div class="card-body">
          <div class="alert alert-info">
            <?=lang('Ayarlar.sayfa.javascriptKodlariNot')?>
          </div>
          <form class="JavascriptGuncelle">
            <div class="mb-1">
              <div class="form-label"><?=lang('Ayarlar.sayfa.javascriptKodlari')?></div>
              <textarea class="form-control" name="javascriptKodlari" rows="20" cols="80"><?=!empty($javascriptKodlari->setting_content)?$javascriptKodlari->setting_content:""?></textarea>
            </div>
            <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
            <div class="form-footer mt-2">
              <button type="submit" class="btn btn-primary w-100"><?=lang('Ayarlar.sayfa.javascriptKodlariGuncelle')?></button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
<?=view('Static/Footer')?>
