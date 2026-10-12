<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none mb-2">
    <div class="row align-items-center">
      <div class="mb-1">
        <ol class="breadcrumb breadcrumb-alternate" aria-label="breadcrumbs">
          <li class="breadcrumb-item"><a href="<?=base_url()?>"><?=lang('Ayarlar.sayfa.ayarlar')?></a></li>
          <li class="breadcrumb-item active"><a href="<?=base_url('Ayarlar/Ikon')?>"><?=lang('Ayarlar.sayfa.ikonAyarlari')?></a></li>
        </ol>
      </div>
    </div>
  </div>
  <div class="row row-cards">
    <div class="col-md-12">
      <div class="card">
        <?=view('Ayarlar/TabMenu')?>
        <div class="card-body">
          <div class="row">
            <div class="col-lg-6">
              <form class="ItemListYukle">
                <div class="mb-2">
                  <div class="form-label">item_list.txt</div>
                  <input type="file" class="form-control" name="txt" accept="text/plain" required>
                </div>
                <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
                <div class="form-footer mt-2">
                  <button type="submit" class="btn btn-primary w-100"><?=lang('Ayarlar.sayfa.itemlistYukle')?></button>
                </div>
              </form>
            </div>
            <div class="col-lg-6">
              <form class="IconZipYukle">
                <div class="mb-2">
                  <div class="form-label">icon.zip</div>
                  <input type="file" class="form-control" name="zip" accept="application/zip, application/octet-stream, application/x-zip-compressed, multipart/x-zip" required>
                </div>
                <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
                <div class="form-footer mt-2">
                  <button type="submit" class="btn btn-primary w-100"><?=lang('Ayarlar.sayfa.iconYukle')?></button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<?=view('Static/Footer')?>
