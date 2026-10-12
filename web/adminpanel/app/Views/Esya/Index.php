<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none">
    <div class="row align-items-center">
      <div class="col">
        <ol class="breadcrumb breadcrumb-alternate" aria-label="breadcrumbs">
          <li class="breadcrumb-item"><a href="<?=base_url()?>"><?=lang('Esya.sayfa.esyaYonetimi')?></a></li>
          <li class="breadcrumb-item active"><a href="<?=base_url('Esya/Index')?>"><?=lang('Esya.sayfa.esyalar')?></a></li>
        </ol>
      </div>
      <?php if (IsAllowedViewModule('esyaDuzenleyebilsin')): ?>
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
          <form class="EsyaAra">
            <div class="row">
              <div class="col-lg-5">
                <div class="mb-3 d-flex align-items-center">
                  <select class="form-select" name="searchType">
                    <option value="vnum">vnum</option>
                    <option value="locale_name" selected><?=lang('Esya.sayfa.esyaAdi')?></option>
                    <option value="type"><?=lang('Esya.sayfa.type')?></option>
                    <option value="subtype"><?=lang('Esya.sayfa.subtype')?></option>
                  </select>
                </div>
              </div>
              <div class="col-lg-1">
                <div class="mb-3 d-flex align-items-center">
                  <select class="form-select" name="searchWhere">
                    <option value="=">=</option>
                    <option value="!=">!=</option>
                    <option value="%" selected>%%</option>
                  </select>
                </div>
              </div>
              <div class="col-lg-4">
                <div class="input-icon">
                  <span class="input-icon-addon">
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><circle cx="10" cy="10" r="7"></circle><line x1="21" y1="21" x2="15" y2="15"></line></svg>
                  </span>
                  <input type="text" class="form-control" autocomplete="off" name="itemSearch" placeholder="<?=lang('Genel.arama')?>" aria-label="<?=lang('Genel.arama')?>">
                </div>
              </div>
              <div class="col-lg-2">
                <button type="submit" class="btn btn-primary w-100 mb-2"><?=lang('Esya.sayfa.ara')?></button>
              </div>
            </div>
          </form>
          <div class="row">
            <div class="table-responsive mb-0 mt-0">
              <table class="table table-striped table-borderless border-0 text-muted pt-2" data-order='[[0,"asc"]]' data-page-length='10' id="ajax-datatable" data-url="<?=base_url('Esya/Ajax')?>">
                <thead>
                  <tr>
                    <th class="ps-2" data-width="1%" data-class="text-left align-middle text-truncate">#</th>
                    <th class="ps-2" data-width="1%" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.esya')?></th>
                    <th class="ps-2" data-width="1%" data-class="text-truncate align-middle max-width-300"><?=lang('Esya.sayfa.type')?></th>
                    <th class="ps-2" data-width="1%" data-class="text-truncate align-middle max-width-300"><?=lang('Esya.sayfa.subtype')?></th>
                    <?php if (IsAllowedViewModule('esyaDuzenleyebilsin')): ?>
                      <th class="ps-2" data-width="1%" data-orderable="false" data-class="text-center align-middle text-truncate"><?=lang('Genel.islemler')?></th>
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
<?php if (IsAllowedViewModule('esyaDuzenleyebilsin')): ?>
  <div class="modal modal-blur fade" id="duzenle" role="dialog" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
    <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title"><?=lang('Esya.sayfa.esyaDuzenle')?></h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <form class="Duzenle overflow-auto">
          <div class="modal-body pb-3">
            <div class="card">
              <div class="card-body p-0">
                <ul class="nav nav-tabs" data-bs-toggle="tabs">
                  <li class="nav-item">
                    <a href="#genel" class="nav-link active" data-bs-toggle="tab"><?=lang('Esya.sayfa.genel')?></a>
                  </li>
                  <li class="nav-item">
                    <a href="#yukseltme" class="nav-link" data-bs-toggle="tab"><?=lang('Esya.sayfa.yukseltme')?></a>
                  </li>
                  <li class="nav-item">
                    <a href="#sure" class="nav-link" data-bs-toggle="tab"><?=lang('Esya.sayfa.sure')?></a>
                  </li>
                  <li class="nav-item">
                    <a href="#efsun" class="nav-link" data-bs-toggle="tab"><?=lang('Esya.sayfa.efsun')?></a>
                  </li>
                  <li class="nav-item">
                    <a href="#deger" class="nav-link" data-bs-toggle="tab"><?=lang('Esya.sayfa.deger')?></a>
                  </li>
                  <li class="nav-item">
                    <a href="#socket" class="nav-link" data-bs-toggle="tab"><?=lang('Esya.sayfa.socket')?></a>
                  </li>
                  <li class="nav-item">
                    <a href="#drop" class="nav-link" data-bs-toggle="tab"><?=lang('Canavar.sayfa.drop')?></a>
                  </li>
                </ul>
                <div class="tab-content p-3">
                  <div class="tab-pane active show" id="genel">
                    <div class="row">
                      <div class="col-lg-12 mb-2">
                        <div class="form-label"><?=lang('Genel.esya')?></div>
                        <input type="text" name="locale_name" class="form-control">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Esya.sayfa.type')?></div>
                        <input type="number" name="type" class="form-control">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Esya.sayfa.subtype')?></div>
                        <input type="number" name="subtype" class="form-control">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Esya.sayfa.weight')?></div>
                        <input type="number" name="weight" class="form-control">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Esya.sayfa.antiflag')?></div>
                        <input type="number" name="antiflag" class="form-control">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Esya.sayfa.wearflag')?></div>
                        <input type="number" name="wearflag" class="form-control">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Esya.sayfa.addon_type')?></div>
                        <input type="number" name="addon_type" class="form-control">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Esya.sayfa.gold')?></div>
                        <input type="number" name="gold" class="form-control">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Esya.sayfa.shop_buy_price')?></div>
                        <input type="number" name="shop_buy_price" class="form-control">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Esya.sayfa.magic_pct')?></div>
                        <input type="number" name="magic_pct" class="form-control">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Esya.sayfa.socket_pct')?></div>
                        <input type="number" name="socket_pct" class="form-control">
                      </div>
                      <div class="col-lg-12 mb-2">
                        <div class="form-label"><?=lang('Esya.sayfa.specular')?></div>
                        <input type="number" name="specular" class="form-control">
                      </div>
                    </div>
                  </div>
                  <div class="tab-pane" id="yukseltme">
                    <div class="row">
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Esya.sayfa.refined_vnum')?></div>
                        <input type="number" name="refined_vnum" class="form-control">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Esya.sayfa.refine_set')?></div>
                        <input type="number" name="refine_set" class="form-control">
                      </div>
                    </div>
                  </div>
                  <div class="tab-pane" id="sure">
                    <div class="row">
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Esya.sayfa.limittype0')?></div>
                        <input type="number" name="limittype0" class="form-control">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Esya.sayfa.limitvalue0')?></div>
                        <input type="number" name="limitvalue0" class="form-control">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Esya.sayfa.limittype1')?></div>
                        <input type="number" name="limittype1" class="form-control">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Esya.sayfa.limitvalue1')?></div>
                        <input type="number" name="limitvalue1" class="form-control">
                      </div>
                    </div>
                  </div>
                  <div class="tab-pane" id="efsun">
                    <div class="row">
                      <?php for ($i=0; $i < 3 ; $i++) { ?>
                        <div class="col-lg-6 mb-2">
                          <div class="form-label"><?=lang('Esya.sayfa.applytype'.$i)?></div>
                          <input type="number" name="applytype<?=$i?>" class="form-control">
                        </div>
                        <div class="col-lg-6 mb-2">
                          <div class="form-label"><?=lang('Esya.sayfa.applyvalue'.$i)?></div>
                          <input type="number" name="applyvalue<?=$i?>" class="form-control">
                        </div>
                      <?php } ?>
                    </div>
                  </div>
                  <div class="tab-pane" id="deger">
                    <div class="row">
                      <?php for ($i=0; $i < 6 ; $i++) { ?>
                        <div class="col-lg-6 mb-2">
                          <div class="form-label"><?=lang('Esya.sayfa.value'.$i)?></div>
                          <input type="number" name="value<?=$i?>" class="form-control">
                        </div>
                      <?php } ?>
                    </div>
                  </div>
                  <div class="tab-pane" id="socket">
                    <div class="row">
                      <?php for ($i=0; $i < 6 ; $i++) { ?>
                        <div class="col-lg-6 mb-2">
                          <div class="form-label"><?=lang('Esya.sayfa.socket'.$i)?></div>
                          <input type="number" name="socket<?=$i?>" class="form-control">
                        </div>
                      <?php } ?>
                    </div>
                  </div>
                  <div class="tab-pane" id="drop">
                    <div class="row">
                      <div class="col-lg-3 mb-2">
                        <div class="form-label"><?=lang('Genel.canavar')?></div>
                        <select class="form-select Canavarlar" name="mob_vnum"></select>
                      </div>
                      <div class="col-lg-3 mb-2">
                        <div class="form-label"><?=lang('Genel.adet')?></div>
                        <input type="number" name="count" class="form-control" value="1">
                      </div>
                      <div class="col-lg-3 mb-2">
                        <div class="form-label"><?=lang('Genel.sans')?></div>
                        <input type="text" name="prob" class="form-control" value="0">
                      </div>
                      <input type="hidden" name="item_vnum" value="">
                      <div class="col-lg-3 mb-2">
                        <button type="button" class="btn btn-primary w-100 DropEkleButton" style="margin-top:28px;"><?=lang('Canavar.sayfa.dropEkle')?></button>
                      </div>
                    </div>
                    <hr>
                    <div class="table-responsive mb-0 mt-0">
                      <table class="table table-striped table-borderless border-0 text-muted pt-2 w-100" data-order='[[0,"asc"]]' id="drop-datatable">
                        <thead>
                          <tr>
                            <th class="ps-2" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.canavar')?></th>
                            <th class="ps-2" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.adet')?></th>
                            <th class="ps-2" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.sans')?></th>
                            <th class="ps-2" data-orderable="false" data-class="text-center align-middle text-truncate"><?=lang('Genel.islemler')?></th>
                          </tr>
                        </thead>
                        <tbody></tbody>
                      </table>
                    </div>
                    <div class="modal modal-blur fade" id="dropDuzenle" role="dialog" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
                      <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable" role="document">
                        <div class="modal-content">
                          <div class="modal-header">
                            <h5 class="modal-title"><?=lang('Canavar.sayfa.dropDuzenle')?></h5>
                            <button type="button" class="btn-close" onclick="$('#dropDuzenle').modal('hide');"></button>
                          </div>
                          <div class="modal-body pb-1">
                            <div class="row">
                              <div class="col-lg-12 mb-2">
                                <div class="form-label"><?=lang('Genel.canavar')?></div>
                                <input type="text" name="locale_name" class="form-control" disabled>
                              </div>
                              <div class="col-lg-6 mb-2">
                                <div class="form-label"><?=lang('Genel.adet')?></div>
                                <input type="number" name="newCount" class="form-control">
                              </div>
                              <div class="col-lg-6 mb-2">
                                <div class="form-label"><?=lang('Genel.sans')?></div>
                                <input type="text" name="newProb" class="form-control">
                              </div>
                            </div>
                            <input type="hidden" name="drop_item_vnum" value="">
                            <input type="hidden" name="drop_count" value="">
                            <input type="hidden" name="drop_prob" value="">
                            <input type="hidden" name="drop_mob_vnum" value="">
                            <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
                          </div>
                          <div class="modal-footer">
                            <div class="row w-100">
                              <div class="col-6">
                                <button type="button" class="btn w-100" onclick="$('#dropDuzenle').modal('hide');"><?=lang('Genel.iptal')?></button>
                              </div>
                              <div class="col-6">
                                <button type="submit" class="btn btn-primary w-100 DropGuncelleButon"><?=lang('Canavar.sayfa.dropDuzenle')?></button>
                              </div>
                            </div>
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
          <div class="modal-footer px-2">
            <div class="row w-100">
              <div class="col-6">
                <button type="button" class="btn w-100" data-bs-dismiss="modal"><?=lang('Genel.iptal')?></button>
              </div>
              <div class="col-6">
                <button type="submit" class="btn btn-primary w-100"><?=lang('Esya.sayfa.esyaDuzenle')?></button>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
<?php endif; ?>
<?=view('Static/Footer')?>
