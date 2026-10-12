<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none">
    <div class="row align-items-center">
      <div class="col">
        <ol class="breadcrumb breadcrumb-alternate" aria-label="breadcrumbs">
          <li class="breadcrumb-item"><a href="<?=base_url()?>"><?=lang('Oyuncu.sayfa.oyuncuYonetimi')?></a></li>
          <li class="breadcrumb-item active"><a href="<?=base_url('Oyuncu/Karakter/'.$karakterDetay->id)?>"><?=lang('Oyuncu.sayfa.karakterDetay',['name' => $karakterDetay->name])?></a></li>
        </ol>
      </div>
    </div>
  </div>
  <div class="row row-cards">
    <div class="col-12">
      <div class="card">
        <div class="card-body">
          <div class="row">
            <div class="col-12 mb-2">
              <div class="w-100 text-center mb-2">
                <a class="btn btn-primary" href="<?=base_url('Oyuncu/Detay/'.$karakterDetay->account_id)?>"><?=lang('Oyuncu.sayfa.oyuncuGeriDon')?></a>
              </div>
              <h3 class="text-center bg-dark text-white rounded py-2"><?=lang('Oyuncu.sayfa.karakterBilgileri')?></h3>
            </div>
            <div class="col-lg-6">
              <div class="hesap-bilgi-div">
                <span class="sol"><?=lang('Genel.karakterAdi')?> : </span>
                <span class="sag"><b><?=$karakterDetay->name?> <small>(<?=$karakterDetay->id?>)</small></b></span>
              </div>
              <div class="hesap-bilgi-div">
                <span class="sol"><?=lang('Genel.seviye')?> : </span>
                <span class="sag"><?=$karakterDetay->level?></span>
              </div>
              <div class="hesap-bilgi-div">
                <span class="sol"><?=lang('Oyuncu.sayfa.sinif')?> : </span>
                <span class="sag"><?=KarakterTipi($karakterDetay->job)?></span>
              </div>
              <div class="hesap-bilgi-div">
                <span class="sol"><?=lang('Oyuncu.sayfa.yang')?> : </span>
                <span class="sag"><?=number_format($karakterDetay->gold,0,'.','.')?></span>
              </div>
              <div class="hesap-bilgi-div">
                <span class="sol"><?=lang('Oyuncu.sayfa.pazarYang')?> : </span>
                <span class="sag"><?=number_format($karakterDetay->shop_gold,0,'.','.')?></span>
              </div>
              <div class="hesap-bilgi-div">
                <span class="sol"><?=lang('Oyuncu.sayfa.oyunSuresi')?> : </span>
                <span class="sag"><?=$karakterDetay->playtime?> dakika</span>
              </div>
              <div class="hesap-bilgi-div">
                <span class="sol"><?=lang('Oyuncu.sayfa.sonGiris')?> : </span>
                <span class="sag"><?=DateDMYHMS($karakterDetay->last_play)?></span>
              </div>
              <div class="hesap-bilgi-div">
                <span class="sol"><?=lang('Oyuncu.sayfa.sonKonum')?> : </span>
                <span class="sag"><?=isset($mapIndex->name)?$mapIndex->name.' ('.$karakterDetay->map_index.')':$karakterDetay->map_index?> (<?=$karakterDetay->x.','.$karakterDetay->y?>)</span>
              </div>
              <div class="hesap-bilgi-div">
                <span class="sol"><?=lang('Oyuncu.sayfa.sonIP')?> : </span>
                <span class="sag"><?=$karakterDetay->ip?></span>
              </div>
            </div>
            <div class="col-lg-6">
              <?php if (IsAllowedViewModule('karakteKurtarabilsin')): ?>
                <form class="KarakterKurtar mb-2">
                  <input type="hidden" name="id" value="<?=$karakterDetay->id?>">
                  <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
                  <button type="submit" class="btn btn-primary d-block w-100"><?=lang('Oyuncu.sayfa.karakterKurtar')?></button>
                </form>
              <?php endif; ?>
              <?php if (IsAllowedViewModule('karakterOyundanDusursun')): ?>
                <form class="KarakterDusur mb-2">
                  <input type="hidden" name="id" value="<?=$karakterDetay->id?>">
                  <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
                  <button type="submit" class="btn btn-primary d-block w-100"><?=lang('Oyuncu.sayfa.karakterDusur')?></button>
                </form>
              <?php endif; ?>
              <?php if (IsAllowedViewModule('karakterEsyaGonderebilsin')): ?>
                <button type="submit" class="btn btn-primary d-block w-100" data-bs-toggle="modal" data-bs-target="#esyaGonder"><?=lang('Oyuncu.sayfa.esyaGonder')?></button>
                <div class="modal modal-blur fade" id="esyaGonder" role="dialog" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
                  <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable" role="document">
                    <div class="modal-content">
                      <div class="modal-header">
                        <h5 class="modal-title"><?=lang('Oyuncu.sayfa.esyaGonder')?></h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                      </div>
                      <form class="EsyaGonder overflow-auto">
                        <div class="modal-body pb-1">
                          <div class="row">
                            <div class="col-lg-12 mb-2">
                              <div class="form-label"><?=lang('Genel.esya')?></div>
                              <select class="form-select Esyalar" name="vnum"></select>
                            </div>
                            <div class="col-lg-6 mb-2">
                              <div class="form-label"><?=lang('Genel.adet')?></div>
                              <input type="number" name="count" class="form-control" value="1">
                            </div>
                            <div class="col-lg-6 mb-2">
                              <div class="form-label"><?=lang('Oyuncu.sayfa.nereye')?></div>
                              <select class="form-select" name="mall">
                                <option value="0"><?=lang('Oyuncu.sayfa.depo')?></option>
                                <option value="1"><?=lang('Oyuncu.sayfa.nesneMarket')?></option>
                              </select>
                            </div>
                            <div class="col-lg-12 mb-2">
                              <div class="form-label"><?=lang('Oyuncu.sayfa.nedenVerildi')?></div>
                              <input type="text" name="why" class="form-control">
                            </div>
                          </div>
                          <input type="hidden" name="id" value="<?=$karakterDetay->id?>">
                          <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
                        </div>
                        <div class="modal-footer">
                          <div class="row w-100">
                            <div class="col-6">
                              <button type="button" class="btn w-100" data-bs-dismiss="modal"><?=lang('Genel.iptal')?></button>
                            </div>
                            <div class="col-6">
                              <button type="submit" class="btn btn-primary w-100"><?=lang('Oyuncu.sayfa.esyaGonder')?></button>
                            </div>
                          </div>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>
              <?php endif; ?>
            </div>
          </div>
          <hr>
          <ul class="nav nav-tabs border" data-bs-toggle="tabs">
            <?php if (IsAllowedViewModule('envanterGorebilsin')): ?>
              <li class="nav-item">
                <a href="#envanter" class="nav-link text-dark" data-bs-toggle="tab"><?=lang('Oyuncu.sayfa.envanter')?></a>
              </li>
              <li class="nav-item">
                <a href="#depoVeNesneMarket" class="nav-link text-dark" data-bs-toggle="tab"><?=lang('Oyuncu.sayfa.depoVeNesneMarket')?></a>
              </li>
            <?php endif; ?>
            <?php if (IsAllowedViewModule('oyuncuNesneMarketKayitGorebilsin')): ?>
              <li class="nav-item">
                <a href="#nesneMarket" class="nav-link text-dark" data-bs-toggle="tab"><?=lang('Oyuncu.sayfa.nesneMarketKayitlari')?></a>
              </li>
            <?php endif; ?>
            <?php if (IsAllowedViewModule('oyuncuPazarKayitGorebilsin')): ?>
              <li class="nav-item">
                <a href="#pazar" class="nav-link text-dark" data-bs-toggle="tab"><?=lang('Kayitlar.sayfa.pazarKayitlari')?></a>
              </li>
            <?php endif; ?>
            <?php if (IsAllowedViewModule('karakterGenelKayitGorebilsin')): ?>
              <li class="nav-item">
                <a href="#genel" class="nav-link text-dark" data-bs-toggle="tab"><?=lang('Oyuncu.sayfa.genelKayitlar')?></a>
              </li>
            <?php endif; ?>
          </ul>
          <div class="tab-content p-3">
            <?php if (IsAllowedViewModule('envanterGorebilsin')): ?>
              <div class="tab-pane" id="envanter">
                <div class="row">
                  <input class="form-control m-2" type="text" name="envanterEsyaAra" data-id="envanter" placeholder="<?=lang('Oyuncu.sayfa.esyaAraNot')?>">
                </div>
                <div class="row esyalar"></div>
              </div>
              <div class="tab-pane" id="depoVeNesneMarket">
                <div class="row">
                  <input class="form-control m-2" type="text" name="envanterEsyaAra" data-id="depoVeNesneMarket" placeholder="<?=lang('Oyuncu.sayfa.esyaAraNot')?>">
                </div>
                <div class="row esyalar"></div>
              </div>
            <?php endif; ?>
            <?php if (IsAllowedViewModule('oyuncuNesneMarketKayitGorebilsin')): ?>
              <div class="tab-pane" id="nesneMarket">
                <div class="row">
                  <div class="col-lg-3 pt-3 pb-2 pt-lg-0 pb-lg-0 ms-lg-auto">
                    <div class="input-icon">
                      <span class="input-icon-addon">
                        <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><circle cx="10" cy="10" r="7"></circle><line x1="21" y1="21" x2="15" y2="15"></line></svg>
                      </span>
                      <input type="text" class="form-control" autocomplete="off" name="nesneMarketSearch" placeholder="<?=lang('Genel.arama')?>" aria-label="<?=lang('Genel.arama')?>">
                    </div>
                  </div>
                  <div class="table-responsive mb-0 mt-0">
                    <table class="table table-striped table-borderless border-0 text-muted pt-2" data-order='[[2,"desc"]]' data-page-length='10' id="ajax-nesne-market" data-url="<?=base_url('Oyuncu/AjaxKarakterNesneMarket/'.$karakterDetay->id)?>">
                      <thead>
                        <tr>
                          <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('Genel.esya')?></th>
                          <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('Genel.fiyat')?></th>
                          <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('Genel.tarih')?></th>
                        </tr>
                      </thead>
                      <tbody></tbody>
                    </table>
                  </div>
                </div>
              </div>
            <?php endif; ?>
            <?php if (IsAllowedViewModule('oyuncuPazarKayitGorebilsin')): ?>
              <div class="tab-pane" id="pazar">
                <div class="row">
                  <div class="col-lg-3 pt-3 pb-2 pt-lg-0 pb-lg-0 ms-lg-auto">
                    <div class="input-icon">
                      <span class="input-icon-addon">
                        <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><circle cx="10" cy="10" r="7"></circle><line x1="21" y1="21" x2="15" y2="15"></line></svg>
                      </span>
                      <input type="text" class="form-control" autocomplete="off" name="pazarSearch" placeholder="<?=lang('Genel.arama')?>" aria-label="<?=lang('Genel.arama')?>">
                    </div>
                  </div>
                  <div class="table-responsive mb-0 mt-0">
                    <table class="table table-striped table-borderless border-0 text-muted pt-2" data-order='[[0,"desc"]]' data-page-length='10' id="ajax-pazar-market" data-url="<?=base_url('Oyuncu/AjaxKarakterPazar/'.$karakterDetay->id)?>">
                      <thead>
                        <tr>
                          <th class="ps-2" data-width="1%" data-class="text-truncate align-middle max-width-300">#</th>
                          <th class="ps-2" data-width="1%" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.esya')?></th>
                          <th class="ps-2" data-width="1%" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.adet')?></th>
                          <th class="ps-2" data-width="1%" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.fiyat')?></th>
                          <th class="ps-2" data-width="1%" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.tarih')?></th>
                        </tr>
                      </thead>
                      <tbody></tbody>
                    </table>
                  </div>
                </div>
              </div>
            <?php endif; ?>
            <?php if (IsAllowedViewModule('karakterGenelKayitGorebilsin')): ?>
              <div class="tab-pane" id="genel">
                <form class="GenelAra">
                  <div class="row">
                    <div class="col-lg-5">
                      <div class="mb-3 d-flex align-items-center">
                        <select class="form-select" name="searchType">
                          <option value="how"><?=lang('Genel.tipi')?></option>
                          <option value="hint" selected><?=lang('Genel.icerik')?></option>
                          <option value="ip"><?=lang('Genel.ip')?></option>
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
                        <input type="text" class="form-control" autocomplete="off" name="genelSearch" placeholder="<?=lang('Genel.arama')?>" aria-label="<?=lang('Genel.arama')?>">
                      </div>
                    </div>
                    <div class="col-lg-2">
                      <button type="submit" class="btn btn-primary w-100 mb-2"><?=lang('Oyuncu.sayfa.ara')?></button>
                    </div>
                  </div>
                </form>
                <div class="row">
                  <div class="table-responsive mb-0 mt-0">
                    <table class="table table-striped table-borderless border-0 text-muted pt-2" data-order='[[3,"desc"]]' data-page-length='10' id="ajax-genel" data-url="<?=base_url('Oyuncu/AjaxKarakterGenel/'.$karakterDetay->id)?>">
                      <thead>
                        <tr>
                          <th class="ps-2" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.tipi')?></th>
                          <th class="ps-2" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.icerik')?></th>
                          <th class="ps-2" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.ip')?></th>
                          <th class="ps-2" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.tarih')?></th>
                        </tr>
                      </thead>
                      <tbody></tbody>
                    </table>
                  </div>
                </div>
              </div>
            <?php endif; ?>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<?=view('Static/Footer')?>
