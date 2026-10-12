<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none">
    <div class="row align-items-center">
      <div class="col">
        <h1 class="page-title"><?=lang('Sandik.sayfa.sandik')?></h1>
      </div>
      <div class="col-auto d-md-flex">
        <?php if (IsAllowedViewModule('sandikEkleyebilsin')): ?>
          <a href="javascript:void(0)" class="btn btn-dark me-2" data-bs-toggle="modal" data-bs-target="#ekle">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><rect x="4" y="4" width="6" height="6" rx="1" /><rect x="14" y="4" width="6" height="6" rx="1" /><rect x="4" y="14" width="6" height="6" rx="1" /><path d="M14 17h6m-3 -3v6" /></svg>
            <?=lang('Genel.ekle')?>
          </a>
          <div class="modal modal-blur fade" id="ekle" role="dialog" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
            <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable" role="document">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title"><?=lang('Sandik.sayfa.ekle')?></h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form class="Ekle overflow-auto">
                  <div class="modal-body pb-1">
                    <div class="row">
                      <div class="col-lg-8 mb-2">
                        <div class="form-label"><?=lang('Genel.esya')?></div>
                        <select class="form-control Esyalar" name="vnum"></select>
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Sandik.sayfa.tip')?></div>
                        <select class="form-control" name="type">
                          <option value="norm"><?=lang('Sandik.sayfa.tipNorm')?></option>
                          <option value="const"><?=lang('Sandik.sayfa.tipConst')?></option>
                          <option value="newpct"><?=lang('Sandik.sayfa.tipNewpct')?></option>
                          <option value="pct"><?=lang('Sandik.sayfa.tipPct')?></option>
                          <option value="stone"><?=lang('Sandik.sayfa.tipStone')?></option>
                          <option value="quest"><?=lang('Sandik.sayfa.tipQuest')?></option>
                          <option value="special"><?=lang('Sandik.sayfa.tipSpecial')?></option>
                        </select>
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
                        <button type="submit" class="btn btn-primary w-100"><?=lang('Sandik.sayfa.ekle')?></button>
                      </div>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        <?php endif; ?>
        <?php if (IsAllowedViewModule('sandikDuzenleyebilsin') && p2pStatus==1): ?>
          <form class="SunucuyaGonder">
            <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
            <button type="submit" class="btn btn-primary me-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-server-cog" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><rect x="3" y="4" width="18" height="8" rx="3"></rect><path d="M12 20h-6a3 3 0 0 1 -3 -3v-2a3 3 0 0 1 3 -3h10.5"></path><circle cx="18.001" cy="18" r="2"></circle><path d="M18.001 14.5v1.5"></path><path d="M18.001 20v1.5"></path><path d="M21.032 16.25l-1.299 .75"></path><path d="M16.27 19l-1.3 .75"></path><path d="M14.97 16.25l1.3 .75"></path><path d="M19.733 19l1.3 .75"></path><path d="M7 8v.01"></path><path d="M7 16v.01"></path></svg>
              <?=lang('Genel.sunucuyaGonder')?>
            </button>
          </form>
        <?php endif; ?>
      </div>
    </div>
  </div>
  <div class="row row-cards">
    <div class="col-12">
      <div class="card">
        <div class="card-body pb-0">
          <div class="row">
            <div class="col-lg-3 pt-3 pb-2 pt-lg-0 pb-lg-0 ms-lg-auto">
              <div class="input-icon">
                <span class="input-icon-addon">
                  <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><circle cx="10" cy="10" r="7"></circle><line x1="21" y1="21" x2="15" y2="15"></line></svg>
                </span>
                <input type="text" class="form-control" autocomplete="off" name="search" placeholder="<?=lang('Genel.arama')?>" aria-label="<?=lang('Genel.arama')?>">
              </div>
            </div>
            <div class="table-responsive mb-0 mt-0">
              <table class="table table-striped table-borderless border-0 text-muted pt-2" data-order='[[0,"asc"]]' data-page-length='25' id="ajax-datatable" data-url="<?=base_url('Sandik/Ajax')?>">
                <thead>
                  <tr>
                    <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('Sandik.sayfa.sandik')?></th>
                    <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('Sandik.sayfa.tip')?></th>
                    <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('Sandik.sayfa.esyaSayisi')?></th>
                    <?php if (IsAllowedViewModule('sandikDuzenleyebilsin') || IsAllowedViewModule('sandikSilebilsin')): ?>
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
<?php if (IsAllowedViewModule('sandikDuzenleyebilsin')): ?>
  <div class="modal modal-blur fade" id="duzenle" role="dialog" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
    <div class="modal-dialog modal-xl modal-dialog-centered modal-dialog-scrollable" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title"><?=lang('Sandik.sayfa.duzenle')?> <span id="sandikBaslik" class="text-muted"></span></h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body pb-1">
          <form class="GrupDuzenle">
            <div class="row align-items-end">
              <input type="hidden" name="vnum">
              <div class="col-lg-3 mb-2">
                <div class="form-label"><?=lang('Sandik.sayfa.tip')?></div>
                <select class="form-control" name="type">
                  <option value="norm"><?=lang('Sandik.sayfa.tipNorm')?></option>
                  <option value="const"><?=lang('Sandik.sayfa.tipConst')?></option>
                  <option value="newpct"><?=lang('Sandik.sayfa.tipNewpct')?></option>
                  <option value="pct"><?=lang('Sandik.sayfa.tipPct')?></option>
                  <option value="stone"><?=lang('Sandik.sayfa.tipStone')?></option>
                  <option value="quest"><?=lang('Sandik.sayfa.tipQuest')?></option>
                  <option value="special"><?=lang('Sandik.sayfa.tipSpecial')?></option>
                </select>
              </div>
              <div class="col-lg-3 mb-2">
                <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
                <button type="submit" class="btn btn-primary w-100"><?=lang('Sandik.sayfa.duzenle')?></button>
              </div>
            </div>
          </form>
          <hr class="my-2">
          <div class="form-label"><?=lang('Sandik.sayfa.icerik')?></div>
          <form class="ItemEkle">
            <input type="hidden" name="group_vnum">
            <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
            <div class="row align-items-end">
              <div class="col-lg-5 mb-2">
                <div class="form-label"><?=lang('Genel.esya')?></div>
                <select class="form-control Esyalar" name="item_vnum"></select>
              </div>
              <div class="col-lg-2 mb-2">
                <div class="form-label"><?=lang('Genel.adet')?></div>
                <input type="number" name="count" class="form-control" value="1" min="1">
              </div>
              <div class="col-lg-2 mb-2">
                <div class="form-label"><?=lang('Genel.sans')?></div>
                <input type="number" name="prob" class="form-control" value="100" min="0">
              </div>
              <div class="col-lg-2 mb-2">
                <div class="form-label"><?=lang('Sandik.sayfa.rare')?></div>
                <input type="number" name="rare" class="form-control" value="0" min="0">
              </div>
              <div class="col-lg-1 mb-2">
                <button type="submit" class="btn btn-primary w-100" title="<?=lang('Sandik.sayfa.itemEkle')?>">
                  <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" /></svg>
                </button>
              </div>
            </div>
          </form>
          <div class="table-responsive">
            <table class="table table-striped table-borderless border-0 text-muted">
              <thead>
                <tr>
                  <th><?=lang('Genel.esya')?></th>
                  <th data-width="1%"><?=lang('Genel.adet')?></th>
                  <th data-width="1%"><?=lang('Genel.sans')?></th>
                  <th data-width="1%"><?=lang('Sandik.sayfa.rare')?></th>
                  <th data-width="1%"><?=lang('Sandik.sayfa.sira')?></th>
                  <th data-width="1%" class="text-center"><?=lang('Genel.islemler')?></th>
                </tr>
              </thead>
              <tbody id="sandikIcerik"></tbody>
            </table>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn w-100" data-bs-dismiss="modal"><?=lang('Genel.iptal')?></button>
        </div>
      </div>
    </div>
  </div>
<?php endif; ?>
<?=view('Static/Footer')?>
