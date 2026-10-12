<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none">
    <div class="row align-items-center">
      <div class="col">
        <h1 class="page-title"><?=lang('NPC.sayfa.npc')?></h1>
      </div>
      <div class="col-auto d-md-flex">
        <?php if (IsAllowedViewModule('npcEkleyebilsin')): ?>
          <a href="javascript:void(0)" class="btn btn-dark me-2" data-bs-toggle="modal" data-bs-target="#ekle">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><rect x="4" y="4" width="6" height="6" rx="1" /><rect x="14" y="4" width="6" height="6" rx="1" /><rect x="4" y="14" width="6" height="6" rx="1" /><path d="M14 17h6m-3 -3v6" /></svg>
            <?=lang('Genel.ekle')?>
          </a>
          <div class="modal modal-blur fade" id="ekle" role="dialog" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
            <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable" role="document">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title"><?=lang('NPC.sayfa.ekle')?></h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form class="Ekle overflow-auto">
                  <div class="modal-body pb-1">
                    <div class="row">
                      <div class="col-lg-6 mb-2">
                        <div class="form-label">ID</div>
                        <input type="number" name="vnum" class="form-control" value="0">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label">NPC</div>
                        <select class="form-select Canavarlar" name="npc_vnum"></select>
                      </div>
                      <div class="col-lg-12 mb-2">
                        <div class="form-label"><?=lang('Genel.adi')?></div>
                        <input type="text" name="name" class="form-control">
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
                        <button type="submit" class="btn btn-primary w-100"><?=lang('NPC.sayfa.ekle')?></button>
                      </div>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
          <?php if (p2pStatus==1): ?>
            <form class="SunucuyaGonder">
              <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
              <button type="submit" class="btn btn-primary me-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-server-cog" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><rect x="3" y="4" width="18" height="8" rx="3"></rect><path d="M12 20h-6a3 3 0 0 1 -3 -3v-2a3 3 0 0 1 3 -3h10.5"></path><circle cx="18.001" cy="18" r="2"></circle><path d="M18.001 14.5v1.5"></path><path d="M18.001 20v1.5"></path><path d="M21.032 16.25l-1.299 .75"></path><path d="M16.27 19l-1.3 .75"></path><path d="M14.97 16.25l1.3 .75"></path><path d="M19.733 19l1.3 .75"></path><path d="M7 8v.01"></path><path d="M7 16v.01"></path></svg>
                <?=lang('Genel.sunucuyaGonder')?>
              </button>
            </form>
          <?php endif; ?>
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
              <table class="table table-striped table-borderless border-0 text-muted pt-2" data-order='[[0,"asc"]]' data-page-length='100' id="ajax-datatable" data-url="<?=base_url('NPC/Ajax')?>">
                <thead>
                  <tr>
                    <th class="ps-2" data-width="1%" data-class="text-truncate max-width-300">#</th>
                    <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('Genel.adi')?></th>
                    <th class="ps-2" data-class="text-truncate max-width-300">NPC</th>
                    <?php if (IsAllowedViewModule('npcDuzenleyebilsin') || IsAllowedViewModule('npcSilebilsin')): ?>
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
<?php if (IsAllowedViewModule('npcDuzenleyebilsin')): ?>
  <div class="modal modal-blur fade" id="duzenle" role="dialog" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
    <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title"><?=lang('NPC.sayfa.duzenle')?></h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <form class="Duzenle overflow-auto">
          <div class="modal-body pb-1">
            <ul class="nav nav-tabs" data-bs-toggle="tabs">
              <li class="nav-item">
                <a href="#genel" class="nav-link active" data-bs-toggle="tab"><?=lang('Canavar.sayfa.genel')?></a>
              </li>
              <li class="nav-item">
                <a href="#esyalar" class="nav-link" data-bs-toggle="tab"><?=lang('Genel.esyalar')?></a>
              </li>
            </ul>
            <div class="tab-content p-3">
              <div class="tab-pane active show" id="genel">
                <div class="row">
                  <div class="col-lg-6 mb-2">
                    <div class="form-label">ID</div>
                    <input type="number" name="newVnum" class="form-control" value="0">
                  </div>
                  <div class="col-lg-6 mb-2">
                    <div class="form-label">NPC</div>
                    <select class="form-select Canavarlar" name="npc_vnum"></select>
                  </div>
                  <div class="col-lg-12 mb-2">
                    <div class="form-label"><?=lang('Genel.adi')?></div>
                    <input type="text" name="name" class="form-control">
                  </div>
                </div>
              </div>
              <div class="tab-pane" id="esyalar">
                <div class="row">
                  <div class="col-lg-4 mb-2">
                    <div class="form-label"><?=lang('Genel.esya')?></div>
                    <select class="form-select Esyalar" name="add_item_vnum"></select>
                  </div>
                  <div class="col-lg-4 mb-2">
                    <div class="form-label"><?=lang('Genel.adet')?></div>
                    <input type="number" name="add_count" class="form-control" value="1">
                  </div>
                  <div class="col-lg-4 mb-2">
                    <button type="button" class="btn btn-primary w-100 EsyaEkleButton" style="margin-top:28px;"><?=lang('NPC.sayfa.esyaEkle')?></button>
                  </div>
                </div>
                <hr>
                <div class="table-responsive mb-0 mt-0">
                  <table class="table table-striped table-borderless border-0 text-muted pt-2 w-100" data-order='[[0,"asc"]]' id="esya-datatable">
                    <thead>
                      <tr>
                        <th class="ps-2" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.esya')?></th>
                        <th class="ps-2" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.adet')?></th>
                        <th class="ps-2" data-orderable="false" data-class="text-center align-middle text-truncate"><?=lang('Genel.islemler')?></th>
                      </tr>
                    </thead>
                    <tbody></tbody>
                  </table>
                </div>
                <div class="modal modal-blur fade" id="esyaDuzenle" role="dialog" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
                  <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable" role="document">
                    <div class="modal-content">
                      <div class="modal-header">
                        <h5 class="modal-title"><?=lang('NPC.sayfa.esyaDuzenle')?></h5>
                        <button type="button" class="btn-close" onclick="$('#esyaDuzenle').modal('hide');"></button>
                      </div>
                      <div class="modal-body pb-1">
                        <div class="row">
                          <div class="col-lg-12 mb-2">
                            <div class="form-label"><?=lang('Genel.esya')?></div>
                            <input type="text" name="locale_name" class="form-control" readonly>
                          </div>
                          <div class="col-lg-12 mb-2">
                            <div class="form-label"><?=lang('Genel.adet')?></div>
                            <input type="number" name="new_count" class="form-control">
                          </div>
                        </div>
                        <input type="hidden" name="shop_vnum" value="">
                        <input type="hidden" name="edit_item_vnum" value="">
                        <input type="hidden" name="edit_count" value="">
                        <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
                      </div>
                      <div class="modal-footer">
                        <div class="row w-100">
                          <div class="col-6">
                            <button type="button" class="btn w-100" onclick="$('#esyaDuzenle').modal('hide');"><?=lang('Genel.iptal')?></button>
                          </div>
                          <div class="col-6">
                            <button type="submit" class="btn btn-primary w-100 EsyaGuncelleButon"><?=lang('NPC.sayfa.esyaDuzenle')?></button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <input type="hidden" name="vnum" value="">
            <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
          </div>
          <div class="modal-footer">
            <div class="row w-100">
              <div class="col-6">
                <button type="button" class="btn w-100" data-bs-dismiss="modal"><?=lang('Genel.iptal')?></button>
              </div>
              <div class="col-6">
                <button type="submit" class="btn btn-primary w-100"><?=lang('NPC.sayfa.duzenle')?></button>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
<?php endif; ?>
<?=view('Static/Footer')?>
