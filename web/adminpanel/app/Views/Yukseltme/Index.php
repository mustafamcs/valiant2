<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none">
    <div class="row align-items-center">
      <div class="col">
        <h1 class="page-title"><?=lang('Yukseltme.sayfa.yukseltme')?></h1>
      </div>
      <div class="col-auto d-md-flex">
        <?php if (IsAllowedViewModule('yukseltmeEkleyebilsin')): ?>
          <a href="javascript:void(0)" class="btn btn-dark me-2" data-bs-toggle="modal" data-bs-target="#ekle">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><rect x="4" y="4" width="6" height="6" rx="1" /><rect x="14" y="4" width="6" height="6" rx="1" /><rect x="4" y="14" width="6" height="6" rx="1" /><path d="M14 17h6m-3 -3v6" /></svg>
            <?=lang('Genel.ekle')?>
          </a>
          <div class="modal modal-blur fade" id="ekle" role="dialog" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
            <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable" role="document">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title"><?=lang('Yukseltme.sayfa.ekle')?></h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form class="Ekle overflow-auto">
                  <div class="modal-body pb-1">
                    <div class="row">
                      <?php for ($i=0; $i < 5 ; $i++) { ?>
                        <div class="col-lg-6">
                          <div class="mb-2">
                            <div class="form-label"><?=lang('Genel.esya')?> <?=$i+1?></div>
                            <select class="form-select Esyalar" name="vnum<?=$i?>">
                              <option value="0">0</option>
                            </select>
                          </div>
                        </div>
                        <div class="col-lg-6">
                          <div class="mb-2">
                            <div class="form-label"><?=lang('Genel.adet')?> <?=$i+1?></div>
                            <input type="number" name="count<?=$i?>" class="form-control" value="0">
                          </div>
                        </div>
                      <?php } ?>
                      <div class="col-lg-6">
                        <div class="mb-2">
                          <div class="form-label">src_vnum</div>
                          <input type="number" name="src_vnum" class="form-control" required value="0">
                        </div>
                      </div>
                      <div class="col-lg-6">
                        <div class="mb-2">
                          <div class="form-label">result_vnum</div>
                          <input type="number" name="result_vnum" class="form-control" required value="0">
                        </div>
                      </div>
                      <div class="col-lg-6">
                        <div class="mb-2">
                          <div class="form-label"><?=lang('Genel.fiyat')?></div>
                          <input type="number" name="cost" class="form-control" required value="0">
                        </div>
                      </div>
                      <div class="col-lg-6">
                        <div class="mb-2">
                          <div class="form-label"><?=lang('Genel.sans')?></div>
                          <input type="number" name="prob" class="form-control" required value="0">
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
                        <button type="submit" class="btn btn-primary w-100"><?=lang('Yukseltme.sayfa.ekle')?></button>
                      </div>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        <?php endif; ?>
        <?php if (p2pStatus==1 && (IsAllowedViewModule('yukseltmeEkleyebilsin') || IsAllowedViewModule('yukseltmeDuzenleyebilsin'))): ?>
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
            <div class="col-lg-4">
              <div class="input-icon">
                <input type="text" class="form-control" autocomplete="off" name="startID" placeholder="<?=lang('Yukseltme.sayfa.baslangic')?>" aria-label="<?=lang('Yukseltme.sayfa.baslangic')?>">
              </div>
            </div>
            <div class="col-lg-4">
              <div class="input-icon">
                <input type="text" class="form-control" autocomplete="off" name="finishID" placeholder="<?=lang('Yukseltme.sayfa.bitis')?>" aria-label="<?=lang('Yukseltme.sayfa.bitis')?>">
              </div>
            </div>
            <div class="col-lg-4">
              <div class="input-icon">
                <button type="button" class="btn btn-primary me-2 w-100 searchButton"><?=lang('Genel.filtrele')?></button>
              </div>
            </div>
            <div class="table-responsive mb-0 mt-0">
              <table class="table table-striped table-borderless border-0 text-muted pt-2" data-order='[[0,"asc"]]' data-page-length='10' id="ajax-datatable" data-url="<?=base_url('Yukseltme/Ajax')?>">
                <thead>
                  <tr>
                    <th class="ps-2" data-width="1%" data-class="text-left text-truncate">#</th>
                    <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('Genel.esyalar')?></th>
                    <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('Genel.fiyat')?></th>
                    <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('Genel.sans')?></th>
                    <?php if (IsAllowedViewModule('yukseltmeDuzenleyebilsin') || IsAllowedViewModule('yukseltmeSilebilsin')): ?>
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
<?php if (IsAllowedViewModule('yukseltmeDuzenleyebilsin')): ?>
  <div class="modal modal-blur fade" id="duzenle" role="dialog" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
    <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title"><?=lang('Yukseltme.sayfa.duzenle')?></h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <form class="Duzenle overflow-auto">
          <div class="modal-body pb-1">
            <div class="row">
              <?php for ($i=0; $i < 5 ; $i++) { ?>
                <div class="col-lg-6">
                  <div class="mb-2">
                    <div class="form-label"><?=lang('Genel.esya')?> <?=$i+1?></div>
                    <input type="number" name="vnum<?=$i?>" class="form-control" required>
                  </div>
                </div>
                <div class="col-lg-6">
                  <div class="mb-2">
                    <div class="form-label"><?=lang('Genel.adet')?> <?=$i+1?></div>
                    <input type="number" name="count<?=$i?>" class="form-control" required>
                  </div>
                </div>
              <?php } ?>
              <div class="col-lg-6">
                <div class="mb-2">
                  <div class="form-label">src_vnum</div>
                  <input type="number" name="src_vnum" class="form-control" required>
                </div>
              </div>
              <div class="col-lg-6">
                <div class="mb-2">
                  <div class="form-label">result_vnum</div>
                  <input type="number" name="result_vnum" class="form-control" required>
                </div>
              </div>
              <div class="col-lg-6">
                <div class="mb-2">
                  <div class="form-label"><?=lang('Genel.fiyat')?></div>
                  <input type="number" name="cost" class="form-control" required>
                </div>
              </div>
              <div class="col-lg-6">
                <div class="mb-2">
                  <div class="form-label"><?=lang('Genel.sans')?></div>
                  <input type="number" name="prob" class="form-control" required>
                </div>
              </div>
            </div>
            <input type="hidden" name="id" value="">
            <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
          </div>
          <div class="modal-footer">
            <div class="row w-100">
              <div class="col-6">
                <button type="button" class="btn w-100" data-bs-dismiss="modal"><?=lang('Genel.iptal')?></button>
              </div>
              <div class="col-6">
                <button type="submit" class="btn btn-primary w-100"><?=lang('Yukseltme.sayfa.duzenle')?></button>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
<?php endif; ?>
<?=view('Static/Footer')?>
