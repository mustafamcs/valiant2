<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none">
    <div class="row align-items-center">
      <div class="col">
        <h1 class="page-title"><?=lang('Patch.sayfa.patch')?></h1>
        <div class="text-muted mt-1"><?=lang('Patch.sayfa.aciklama')?></div>
      </div>
      <div class="col-auto d-md-flex">
        <span class="badge bg-azure-lt align-self-center me-3 fs-5"><?=lang('Patch.sayfa.surum')?>: v<?=$surum?></span>
        <a href="<?=base_url('Patch/PatcherIndir')?>" class="btn btn-outline-primary me-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2 -2v-2" /><path d="M7 11l5 5l5 -5" /><path d="M12 4l0 12" /></svg>
          <?=lang('Patch.sayfa.patcherIndir')?>
        </a>
        <?php if (IsAllowedViewModule('patchEkleyebilsin')): ?>
          <a href="javascript:void(0)" class="btn btn-dark me-2" data-bs-toggle="modal" data-bs-target="#yukle">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2 -2v-2" /><path d="M7 9l5 -5l5 5" /><path d="M12 4l0 12" /></svg>
            <?=lang('Patch.sayfa.dosyaYukle')?>
          </a>
          <div class="modal modal-blur fade" id="yukle" role="dialog" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
            <div class="modal-dialog modal-lg modal-dialog-centered" role="document">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title"><?=lang('Patch.sayfa.dosyaYukle')?></h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form class="Yukle" enctype="multipart/form-data">
                  <div class="modal-body pb-1">
                    <div class="row">
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Patch.sayfa.sec')?></div>
                        <input type="file" class="form-control" name="dosya" required>
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Patch.sayfa.hedefYol')?></div>
                        <input type="text" class="form-control" name="hedef" placeholder="pack/root.pak">
                      </div>
                    </div>
                    <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
                  </div>
                  <div class="modal-footer">
                    <div class="row w-100">
                      <div class="col-6">
                        <button type="button" class="btn w-100" data-bs-dismiss="modal"><?=lang('Genel.iptal')?></button>
                      </div>
                      <div class="col-6">
                        <button type="submit" class="btn btn-primary w-100"><?=lang('Patch.sayfa.yukle')?></button>
                      </div>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
          <form class="Manifest">
            <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
            <button type="submit" class="btn btn-primary">
              <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M12 5l0 14" /><path d="M16 11l-4 -6l-4 6" /><path d="M5 21l14 0" /></svg>
              <?=lang('Patch.sayfa.manifestOlustur')?>
            </button>
          </form>
        <?php endif; ?>
      </div>
    </div>
  </div>
</div>
<div class="page-body">
  <div class="container-xl">
    <div class="card">
      <div class="card-header">
        <div class="w-50">
          <input type="text" class="form-control" name="search" placeholder="<?=lang('Genel.ara')?>">
        </div>
      </div>
      <div class="card-body">
        <div class="table-responsive">
          <table id="ajax-datatable" class="table table-striped table-borderless border-0 text-muted w-100" data-url="<?=base_url('Patch/Ajax')?>">
            <thead>
              <tr>
                <th><?=lang('Patch.sayfa.dosya')?></th>
                <th data-width="10%"><?=lang('Patch.sayfa.boyut')?></th>
                <th data-width="15%"><?=lang('Patch.sayfa.hash')?></th>
                <?php if (IsAllowedViewModule('patchSilebilsin')): ?>
                  <th data-width="5%" class="text-center"><?=lang('Genel.islemler')?></th>
                <?php endif; ?>
              </tr>
            </thead>
          </table>
        </div>
      </div>
    </div>
  </div>
</div>
<?=view('Static/Footer')?>
