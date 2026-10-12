<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none">
    <div class="row align-items-center">
      <div class="col">
        <ol class="breadcrumb breadcrumb-alternate" aria-label="breadcrumbs">
          <li class="breadcrumb-item"><a href="<?=base_url()?>"><?=lang('NesneMarket.sayfa.nesneMarket')?></a></li>
          <li class="breadcrumb-item active"><a href="<?=base_url('NesneMarket/Index')?>"><?=lang('NesneMarket.sayfa.nesneMarketEsya')?></a></li>
        </ol>
      </div>
      <div class="col-auto d-md-flex">
        <?php if (IsAllowedViewModule('nesneMarketEsyaEkleyebilsin')): ?>
          <a href="javascript:void(0)" class="btn btn-dark me-2" data-bs-toggle="modal" data-bs-target="#ekle">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><rect x="4" y="4" width="6" height="6" rx="1" /><rect x="14" y="4" width="6" height="6" rx="1" /><rect x="4" y="14" width="6" height="6" rx="1" /><path d="M14 17h6m-3 -3v6" /></svg>
            <?=lang('Genel.ekle')?>
          </a>
          <div class="modal modal-blur fade" id="ekle" role="dialog" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
            <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable" role="document">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title"><?=lang('NesneMarket.sayfa.esyaEkle')?></h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form class="Ekle overflow-auto">
                  <div class="modal-body pb-1">
                    <div class="row">
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Genel.kategori')?></div>
                        <select class="form-select Kategoriler" name="category_id"></select>
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Genel.esya')?></div>
                        <select class="form-select Esyalar" name="vnum"></select>
                      </div>
                      <div class="col-lg-12 mb-2">
                        <div class="form-label"><?=lang('Genel.esya')?></div>
                        <input type="text" name="item_name" class="form-control">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Genel.fiyat')?></div>
                        <input type="number" name="price" class="form-control" value="0">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Genel.adet')?></div>
                        <input type="number" name="count" class="form-control" value="1">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('NesneMarket.sayfa.time_type')?></div>
                        <input type="number" name="time_type" class="form-control" value="0">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('NesneMarket.sayfa.price_type')?></div>
                        <input type="number" name="price_type" class="form-control" value="0">
                      </div>
                      <?php for ($i=0; $i < 4 ; $i++) { ?>
                        <div class="col-lg-3 mb-2">
                          <div class="form-label">Socket <?=$i?></div>
                          <input type="number" name="socket<?=$i?>" class="form-control" value="0">
                        </div>
                      <?php } ?>
                      <?php for ($i=0; $i < 7 ; $i++) { ?>
                        <div class="col-lg-6 mb-2">
                          <div class="form-label"><?=lang('Genel.efsun').' '.$i?></div>
                          <select class="form-select EfsunSec" name="attrtype<?=$i?>">
                            <option value="0">Yok</option>
                            <?php foreach ($efsunlar as $key => $value): ?>
                              <option value="<?=$value->id?>"><?=$value->name?></option>
                            <?php endforeach; ?>
                          </select>
                        </div>
                        <div class="col-lg-6 mb-2">
                          <div class="form-label"><?=lang('Genel.deger').' '.$i?></div>
                          <input type="number" class="form-control" name="attrvalue<?=$i?>" value="0">
                        </div>
                      <?php } ?>
                      <div class="col-lg-12 mb-2">
                        <div class="form-label"><?=lang('Genel.durum')?></div>
                        <select class="form-select" name="status">
                          <option value="0"><?=lang('Genel.pasif')?></option>
                          <option value="1"><?=lang('Genel.aktif')?></option>
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
                        <button type="submit" class="btn btn-primary w-100"><?=lang('NesneMarket.sayfa.esyaEkle')?></button>
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
              <table class="table table-striped table-borderless border-0 text-muted pt-2" data-order='[[0,"desc"]]' data-page-length='10' id="ajax-datatable" data-url="<?=base_url('NesneMarket/Ajax')?>">
                <thead>
                  <tr>
                    <th class="ps-2" data-width="1%" data-class="text-truncate max-width-300">#</th>
                    <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('Genel.esya')?></th>
                    <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('Genel.fiyat')?></th>
                    <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('NesneMarket.sayfa.kategoriAdi')?></th>
                    <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('NesneMarket.sayfa.sell_count')?></th>
                    <th class="ps-2" data-width="1%" data-class="text-truncate max-width-300"><?=lang('Genel.durum')?></th>
                    <?php if (IsAllowedViewModule('nesneMarketEsyaDuzenleyebilsin') || IsAllowedViewModule('nesneMarketEsyaSilebilsin')): ?>
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
<?php if (IsAllowedViewModule('nesneMarketEsyaDuzenleyebilsin')): ?>
  <div class="modal modal-blur fade" id="duzenle" role="dialog" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
    <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title"><?=lang('NesneMarket.sayfa.esyaDuzenle')?></h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <form class="Duzenle overflow-auto">
          <div class="modal-body pb-1">
            <div class="row">
              <div class="col-lg-6 mb-2">
                <div class="form-label"><?=lang('Genel.kategori')?></div>
                <select class="form-select Kategoriler" name="category_id"></select>
              </div>
              <div class="col-lg-6 mb-2">
                <div class="form-label"><?=lang('Genel.esya')?></div>
                <select class="form-select Esyalar" name="vnum"></select>
              </div>
              <div class="col-lg-12 mb-2">
                <div class="form-label"><?=lang('Genel.esya')?></div>
                <input type="text" name="item_name" class="form-control">
              </div>
              <div class="col-lg-6 mb-2">
                <div class="form-label"><?=lang('Genel.fiyat')?></div>
                <input type="number" name="price" class="form-control" value="0">
              </div>
              <div class="col-lg-6 mb-2">
                <div class="form-label"><?=lang('Genel.adet')?></div>
                <input type="number" name="count" class="form-control" value="1">
              </div>
              <div class="col-lg-6 mb-2">
                <div class="form-label"><?=lang('NesneMarket.sayfa.time_type')?></div>
                <input type="number" name="time_type" class="form-control" value="0">
              </div>
              <div class="col-lg-6 mb-2">
                <div class="form-label"><?=lang('NesneMarket.sayfa.price_type')?></div>
                <input type="number" name="price_type" class="form-control" value="0">
              </div>
              <?php for ($i=0; $i < 4 ; $i++) { ?>
                <div class="col-lg-3 mb-2">
                  <div class="form-label">Socket <?=$i?></div>
                  <input type="number" name="socket<?=$i?>" class="form-control" value="0">
                </div>
              <?php } ?>
              <?php for ($i=0; $i < 7 ; $i++) { ?>
                <div class="col-lg-6 mb-2">
                  <div class="form-label"><?=lang('Genel.efsun').' '.$i?></div>
                  <select class="form-select EfsunSec" name="attrtype<?=$i?>">
                    <option value="0">Yok</option>
                    <?php foreach ($efsunlar as $key => $value): ?>
                      <option value="<?=$value->id?>"><?=$value->name?></option>
                    <?php endforeach; ?>
                  </select>
                </div>
                <div class="col-lg-6 mb-2">
                  <div class="form-label"><?=lang('Genel.deger').' '.$i?></div>
                  <input type="number" class="form-control" name="attrvalue<?=$i?>" value="0">
                </div>
              <?php } ?>
              <div class="col-lg-6 mb-2">
                <div class="form-label"><?=lang('NesneMarket.sayfa.sell_count')?></div>
                <input type="number" name="sell_count" class="form-control" value="0">
              </div>
              <div class="col-lg-6 mb-2">
                <div class="form-label"><?=lang('Genel.durum')?></div>
                <select class="form-select" name="status">
                  <option value="0"><?=lang('Genel.pasif')?></option>
                  <option value="1"><?=lang('Genel.aktif')?></option>
                </select>
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
                <button type="submit" class="btn btn-primary w-100"><?=lang('NesneMarket.sayfa.esyaDuzenle')?></button>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
<?php endif; ?>
<?=view('Static/Footer')?>
