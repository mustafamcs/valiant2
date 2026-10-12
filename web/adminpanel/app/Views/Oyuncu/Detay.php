<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none">
    <div class="row align-items-center">
      <div class="col">
        <ol class="breadcrumb breadcrumb-alternate" aria-label="breadcrumbs">
          <li class="breadcrumb-item"><a href="<?=base_url()?>"><?=lang('Oyuncu.sayfa.oyuncuYonetimi')?></a></li>
          <li class="breadcrumb-item active"><a href="<?=base_url('Oyuncu/Detay/'.$oyuncuDetay->id)?>"><?=lang('Oyuncu.sayfa.oyuncuDetay',['login' => $oyuncuDetay->login])?></a></li>
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
              <h3 class="text-center bg-dark text-white rounded py-2"><?=lang('Oyuncu.sayfa.hesapBilgileri')?></h3>
            </div>
            <div class="col-lg-5">
              <div class="hesap-bilgi-div">
                <span class="sol"><?=lang('Genel.hesapAdi')?> : </span>
                <span class="sag"><b><?=$oyuncuDetay->login?> <small>(<?=$oyuncuDetay->id?>)</small></b></span>
              </div>
              <div class="hesap-bilgi-div">
                <span><?=lang('Genel.eposta')?> : </span>
                <span>
                  <form class="EPostaDegistir d-flex">
                    <input type="email" name="email" class="form-control" value="<?=$oyuncuDetay->email?>">
                    <input type="hidden" name="id" value="<?=$oyuncuDetay->id?>">
                    <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
                    <?php if (IsAllowedViewModule('oyuncuEpostaDegistirebilsin')): ?>
                      <button type="submit" class="btn btn-primary btn-sm ms-2"><?=lang('Genel.degistir')?></button>
                    <?php endif; ?>
                  </form>
                </span>
              </div>
              <div class="hesap-bilgi-div">
                <span><?=lang('Genel.telefon')?> : </span>
                <span>
                  <form class="TelefonDegistir d-flex">
                    <input type="number" name="phone1" class="form-control" value="<?=$oyuncuDetay->phone1?>">
                    <input type="hidden" name="id" value="<?=$oyuncuDetay->id?>">
                    <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
                    <?php if (IsAllowedViewModule('oyuncuTelefonDegistirebilsin')): ?>
                      <button type="submit" class="btn btn-primary btn-sm ms-2"><?=lang('Genel.degistir')?></button>
                    <?php endif; ?>
                  </form>
                </span>
              </div>
              <div class="hesap-bilgi-div">
                <span><?=lang('Genel.sifre')?> : </span>
                <span>
                  <form class="SifreDegistir d-flex">
                    <input type="text" name="password" class="form-control" placeholder="<?=lang('Oyuncu.sayfa.yeniSifre')?>">
                    <input type="hidden" name="id" value="<?=$oyuncuDetay->id?>">
                    <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
                    <?php if (IsAllowedViewModule('oyuncuSifreDegistirebilsin')): ?>
                      <button type="submit" class="btn btn-primary btn-sm ms-2"><?=lang('Genel.degistir')?></button>
                    <?php endif; ?>
                  </form>
                </span>
              </div>
              <div class="hesap-bilgi-div">
                <span><?=lang('Oyuncu.sayfa.bayrak')?> : </span>
                <span>
                  <form class="BayrakDegistir d-flex">
                    <select class="form-select" name="empire">
                      <option value="1" <?=(isset($bayrak->empire) && $bayrak->empire=="1"?'selected':'')?>><?=lang('Oyuncu.sayfa.kirmizi')?></option>
                      <option value="2" <?=(isset($bayrak->empire) && $bayrak->empire=="2"?'selected':'')?>><?=lang('Oyuncu.sayfa.sari')?></option>
                      <option value="3" <?=(isset($bayrak->empire) && $bayrak->empire=="3"?'selected':'')?>><?=lang('Oyuncu.sayfa.mavi')?></option>
                    </select>
                    <input type="hidden" name="id" value="<?=$oyuncuDetay->id?>">
                    <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
                    <?php if (IsAllowedViewModule('oyuncuBayrakDegistirebilsin')): ?>
                      <button type="submit" class="btn btn-primary btn-sm ms-2"><?=lang('Genel.degistir')?></button>
                    <?php endif; ?>
                  </form>
                </span>
              </div>
              <div class="hesap-bilgi-div">
                <span><?=lang('Genel.ep')?> : </span>
                <span><?=$oyuncuDetay->cash?></span>
              </div>
              <div class="hesap-bilgi-div">
                <span><?=lang('Genel.durum')?> : </span>
                <?php if ($oyuncuDetay->status!="OK" || strtotime($oyuncuDetay->availDt)>time()): ?>
                  <span><?=lang('Genel.pasif')?></span>
                <?php else: ?>
                  <span><?=lang('Genel.aktif')?></span>
                <?php endif; ?>
              </div>
            </div>
            <div class="col-lg-7">
              <table class="table table-striped">
                <thead>
                  <tr>
                    <th><?=lang('Genel.karakter')?></th>
                    <th><?=lang('Genel.seviye')?></th>
                    <th><?=lang('Genel.tur')?></th>
                    <th>Yang</th>
                  </tr>
                </thead>
                <tbody>
                  <?php if (!empty($hesaplar) && $hesaplar!="-"): ?>
                    <?php foreach ($hesaplar as $key => $value): ?>
                      <tr>
                        <?php if (IsAllowedViewModule('karakterDetayGorebilsin')): ?>
                          <td><a href="<?=base_url('Oyuncu/Karakter/'.$value->id)?>" class="text-dark"><b><?=$value->name?> <small>(<?=$value->id?>)</small> </b></a></td>
                        <?php else: ?>
                          <td><a href="javascript:void(0)" class="text-dark"><b><?=$value->name?> <small>(<?=$value->id?>)</small> </b></a></td>
                        <?php endif; ?>
                        <td><?=$value->level?> Lv.</td>
                        <td><?=KarakterTipi($value->job)?></td>
                        <td><?=number_format($value->gold,0,'.','.')?> Yang</td>
                      </tr>
                    <?php endforeach; ?>
                  <?php else: ?>
                    <tr>
                      <td colspan="6" class="text-center"><?=lang('Oyuncu.sayfa.karakterYok')?></td>
                    </tr>
                  <?php endif; ?>
                </tbody>
              </table>
            </div>
          </div>
          <hr>
          <ul class="nav nav-tabs border" data-bs-toggle="tabs">
            <?php if (IsAllowedViewModule('oyuncuBanlayabilsin') || IsAllowedViewModule('oyuncuAcabilsin')): ?>
              <li class="nav-item">
                <a href="#ban" class="nav-link text-dark" data-bs-toggle="tab"><?=lang('Oyuncu.sayfa.banIslemleri')?></a>
              </li>
            <?php endif; ?>
            <?php if (IsAllowedViewModule('oyuncuNesneMarketKayitGorebilsin')): ?>
              <li class="nav-item">
                <a href="#nesneMarket" class="nav-link text-dark" data-bs-toggle="tab"><?=lang('Oyuncu.sayfa.nesneMarketKayitlari')?></a>
              </li>
            <?php endif; ?>
          </ul>
          <div class="tab-content p-3">
            <?php if (IsAllowedViewModule('oyuncuBanlayabilsin') || IsAllowedViewModule('oyuncuAcabilsin')): ?>
              <div class="tab-pane" id="ban">
                <div class="row">
                  <div class="col-lg-6">
                    <div class="row">
                      <div class="col-12 mb-2">
                        <div class="form-label"><?=lang('Oyuncu.sayfa.banSebebi')?></div>
                        <textarea name="ban_sebebi" class="form-control" rows="4" cols="80"></textarea>
                      </div>
                      <div class="col-12 mb-2">
                        <div class="form-label"><?=lang('Oyuncu.sayfa.acilisSebebi')?></div>
                        <textarea name="acilis_sebebi" class="form-control" rows="4" cols="80"></textarea>
                      </div>
                    </div>
                  </div>
                  <div class="col-lg-6">
                    <div class="hesap-bilgi-div">
                      <span><?=lang('Genel.banTarihi')?> : </span>
                      <?php if ($oyuncuDetay->availDt!=0): ?>
                        <span><?=DateDMYHMS($oyuncuDetay->availDt)?></span>
                      <?php else: ?>
                        <span>-</span>
                      <?php endif; ?>
                    </div>
                    <?php if ($oyuncuDetay->status!="OK" || strtotime($oyuncuDetay->availDt)>time()): ?>
                      <form class="HesabiAc">
                        <input type="hidden" name="id" value="<?=$oyuncuDetay->id?>">
                        <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
                        <div class="hesap-bilgi-div">
                          <button type="submit" class="btn btn-primary w-100"><?=lang('Oyuncu.sayfa.hesabiAc')?></button>
                        </div>
                      </form>
                    <?php else: ?>
                      <form class="HesabiBanla">
                        <div class="hesap-bilgi-div">
                          <span><?=lang('Genel.banSuresi')?> : </span>
                          <span>
                            <select class="form-select" name="ban_sure" style="width:300px">
                              <option value=""><?=lang('Genel.seciniz')?></option>
                              <option value="<?=3600?>">1 <?=lang('Genel.saat')?></option>
                              <option value="<?=10800?>">3 <?=lang('Genel.saat')?></option>
                              <option value="<?=18000?>">5 <?=lang('Genel.saat')?></option>
                              <option value="<?=25200?>">7 <?=lang('Genel.saat')?></option>
                              <option value="<?=86400?>">1 <?=lang('Genel.gun')?></option>
                              <option value="<?=259200?>">3 <?=lang('Genel.gun')?></option>
                              <option value="<?=432000?>">5 <?=lang('Genel.gun')?></option>
                              <option value="<?=604800?>">7 <?=lang('Genel.gun')?></option>
                              <option value="<?=1209600?>">14 <?=lang('Genel.gun')?></option>
                              <option value="<?=2592000?>">30 <?=lang('Genel.gun')?></option>
                              <option value="<?=86313600?>"><?=lang('Genel.sinirsiz')?></option>
                            </select>
                          </span>
                        </div>
                        <input type="hidden" name="id" value="<?=$oyuncuDetay->id?>">
                        <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
                        <div class="hesap-bilgi-div">
                          <button type="submit" class="btn btn-primary w-100"><?=lang('Oyuncu.sayfa.hesabiBanla')?></button>
                        </div>
                      </form>
                    <?php endif; ?>
                    <form class="EPostaGonder">
                      <input type="hidden" name="ban_sebebi" value="">
                      <input type="hidden" name="type" value="ban">
                      <input type="hidden" name="id" value="<?=$oyuncuDetay->id?>">
                      <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
                      <div class="hesap-bilgi-div">
                        <button type="submit" class="btn btn-primary w-100"><?=lang('Oyuncu.sayfa.hesabiBanMail')?></button>
                      </div>
                    </form>
                    <form class="EPostaGonder">
                      <input type="hidden" name="acilis_sebebi" value="">
                      <input type="hidden" name="type" value="ac">
                      <input type="hidden" name="id" value="<?=$oyuncuDetay->id?>">
                      <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
                      <div class="hesap-bilgi-div border-0">
                        <button type="submit" class="btn btn-primary w-100"><?=lang('Oyuncu.sayfa.hesabiAcilisMail')?></button>
                      </div>
                    </form>
                  </div>
                </div>
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
                    <table class="table table-striped table-borderless border-0 text-muted pt-2" data-order='[[3,"desc"]]' data-page-length='10' id="ajax-nesne-market" data-url="<?=base_url('Oyuncu/AjaxNesneMarket/'.$oyuncuDetay->id)?>">
                      <thead>
                        <tr>
                          <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('Genel.esya')?></th>
                          <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('Genel.karakterAdi')?></th>
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
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<?=view('Static/Footer')?>
