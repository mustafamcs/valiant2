<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none">
    <div class="row align-items-center">
      <div class="col">
        <ol class="breadcrumb breadcrumb-alternate" aria-label="breadcrumbs">
          <li class="breadcrumb-item"><a href="<?=base_url()?>"><?=lang('Efsun.sayfa.efsun')?></a></li>
          <li class="breadcrumb-item active"><a href="<?=base_url('Efsun/Index')?>"><?=lang('Efsun.sayfa.efsunAyarlari')?></a></li>
        </ol>
      </div>
      <?php if (IsAllowedViewModule('efsunDuzenleyebilsin')): ?>
        <div class="col-auto d-md-flex">
          <?php if (p2pStatus==1): ?>
            <form class="SunucuyaGonder">
              <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
              <button type="submit" class="btn btn-primary me-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-server-cog" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><rect x="3" y="4" width="18" height="8" rx="3"></rect><path d="M12 20h-6a3 3 0 0 1 -3 -3v-2a3 3 0 0 1 3 -3h10.5"></path><circle cx="18.001" cy="18" r="2"></circle><path d="M18.001 14.5v1.5"></path><path d="M18.001 20v1.5"></path><path d="M21.032 16.25l-1.299 .75"></path><path d="M16.27 19l-1.3 .75"></path><path d="M14.97 16.25l1.3 .75"></path><path d="M19.733 19l1.3 .75"></path><path d="M7 8v.01"></path><path d="M7 16v.01"></path></svg>
                <?=lang('Genel.sunucuyaGonder')?>
              </button>
            </form>
          <?php endif; ?>
        </div>
      <?php endif; ?>
    </div>
  </div>
  <div class="row row-cards">
    <div class="col-12">
      <div class="card">
        <div class="card-body pb-0">
          <div class="row">
            <div class="col-lg-4 pt-lg-0">
              <div class="d-flex align-middle">
                <label class="pt-2 pe-2 w-25"><?=lang('Efsun.sayfa.efsunAdi')?>:</label>
                <select class="form-select pt-2 select2" name="search">
                  <option value=""><?=lang('Genel.hepsi')?></option>
                  <?php foreach ($efsunlar as $key => $value): ?>
                    <option value="<?=$value->id?>"><?=$value->name?></option>
                  <?php endforeach; ?>
                </select>
              </div>
            </div>
            <div class="table-responsive mb-0 mt-0">
              <table class="table table-striped table-borderless border-0 text-muted pt-2" data-order='[[0,"asc"]]' data-page-length='100' id="ajax-datatable" data-url="<?=base_url('Efsun/Ajax')?>">
                <thead>
                  <tr>
                    <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('Efsun.sayfa.efsunAdi')?></th>
                    <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('Genel.sans')?></th>
                    <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('Genel.deger')?> 1</th>
                    <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('Genel.deger')?> 2</th>
                    <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('Genel.deger')?> 3</th>
                    <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('Genel.deger')?> 4</th>
                    <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('Genel.deger')?> 5</th>
                    <?php if (IsAllowedViewModule('efsunDuzenleyebilsin')): ?>
                      <th class="ps-2" data-width="1%" data-orderable="false" data-class="text-center text-truncate"><?=lang('Genel.islemler')?></th>
                    <?php endif; ?>
                  </tr>
                </thead>
                <tbody></tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<?php if (IsAllowedViewModule('efsunDuzenleyebilsin')): ?>
  <div class="modal modal-blur fade" id="duzenle" role="dialog" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
    <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title"><?=lang('Efsun.sayfa.duzenle')?></h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <form class="Duzenle overflow-auto">
          <div class="modal-body pb-1">
            <div class="mb-2">
              <div class="form-label"><?=lang('Efsun.sayfa.efsunAdi')?></div>
              <input type="text" name="apply" class="form-control" required>
            </div>
            <div class="mb-2">
              <div class="form-label"><?=lang('Genel.sans')?></div>
              <input type="number" name="prob" class="form-control" required>
            </div>
            <div class="row">
              <div class="col">
                <div class="mb-2">
                  <div class="form-label"><?=lang('Genel.deger')?> 1</div>
                  <input type="number" name="lv1" class="form-control" required>
                </div>
              </div>
              <div class="col">
                <div class="mb-2">
                  <div class="form-label"><?=lang('Genel.deger')?> 2</div>
                  <input type="number" name="lv2" class="form-control" required>
                </div>
              </div>
              <div class="col">
                <div class="mb-2">
                  <div class="form-label"><?=lang('Genel.deger')?> 3</div>
                  <input type="number" name="lv3" class="form-control" required>
                </div>
              </div>
              <div class="col">
                <div class="mb-2">
                  <div class="form-label"><?=lang('Genel.deger')?> 4</div>
                  <input type="number" name="lv4" class="form-control" required>
                </div>
              </div>
              <div class="col">
                <div class="mb-2">
                  <div class="form-label"><?=lang('Genel.deger')?> 5</div>
                  <input type="number" name="lv5" class="form-control" required>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-3">
                <div class="mb-2">
                  <div class="form-label">weapon</div>
                  <input type="number" name="weapon" class="form-control" required>
                </div>
              </div>
              <div class="col-3">
                <div class="mb-2">
                  <div class="form-label">body</div>
                  <input type="number" name="body" class="form-control" required>
                </div>
              </div>
              <div class="col-3">
                <div class="mb-2">
                  <div class="form-label">wrist</div>
                  <input type="number" name="wrist" class="form-control" required>
                </div>
              </div>
              <div class="col-3">
                <div class="mb-2">
                  <div class="form-label">foots</div>
                  <input type="number" name="foots" class="form-control" required>
                </div>
              </div>
              <div class="col-3">
                <div class="mb-2">
                  <div class="form-label">neck</div>
                  <input type="number" name="neck" class="form-control" required>
                </div>
              </div>
              <div class="col-3">
                <div class="mb-2">
                  <div class="form-label">head</div>
                  <input type="number" name="head" class="form-control" required>
                </div>
              </div>
              <div class="col-3">
                <div class="mb-2">
                  <div class="form-label">shield</div>
                  <input type="number" name="shield" class="form-control" required>
                </div>
              </div>
              <div class="col-3">
                <div class="mb-2">
                  <div class="form-label">ear</div>
                  <input type="number" name="ear" class="form-control" required>
                </div>
              </div>
              <div class="col-3">
                <div class="mb-2">
                  <div class="form-label">costume_weapon</div>
                  <input type="number" name="costume_weapon" class="form-control" required>
                </div>
              </div>
              <div class="col-3">
                <div class="mb-2">
                  <div class="form-label">belt</div>
                  <input type="number" name="belt" class="form-control" required>
                </div>
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
                <button type="submit" class="btn btn-primary w-100"><?=lang('Efsun.sayfa.duzenle')?></button>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
<?php endif; ?>
<?=view('Static/Footer')?>
