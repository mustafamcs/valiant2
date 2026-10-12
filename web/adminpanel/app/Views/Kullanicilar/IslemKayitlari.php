<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none mb-2">
    <div class="row align-items-center">
      <div class="col-auto d-md-flex" style="line-height:40px">
        <ol class="breadcrumb breadcrumb-alternate" aria-label="breadcrumbs">
          <li class="breadcrumb-item"><a href="<?=base_url('Kullanicilar/Index')?>"><?=lang('Kullanicilar.sayfa.kullanicilar')?></a></li>
          <li class="breadcrumb-item"><a href="<?=base_url('Kullanicilar/Detay/'.$kullaniciBilgileri->user_id)?>"><?=lang('Kullanicilar.sayfa.kullaniciDetayi',['user_name' => $kullaniciBilgileri->user_name])?></a></li>
          <li class="breadcrumb-item active"><a href="<?=base_url('Kullanicilar/IslemKayitlari/'.$kullaniciBilgileri->user_id)?>"><?=lang('IslemKayitlari.sayfa.islemKayitlari')?></a></li>
        </ol>
      </div>
      <div class="col-auto ms-auto d-md-flex">
        <a href="<?=base_url('Kullanicilar/Index')?>" class="btn btn-dark me-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><line x1="5" y1="12" x2="19" y2="12" /><line x1="5" y1="12" x2="11" y2="18" /><line x1="5" y1="12" x2="11" y2="6" /></svg>
          <?=lang('Hata.geriDon')?>
        </a>
      </div>
    </div>
  </div>
  <div class="row row-cards">
    <?=view('Kullanicilar/LeftMenu')?>
    <div class="col-md-8">
      <div class="card">
        <div class="card-body">
          <div class="alert alert-info d-flex">
            <?=lang('Kullanicilar.sayfa.islemKayitlariNot')?>
          </div>
          <div class="row">
            <div class="col-lg-3 pt-lg-0">
              <div class="d-flex align-middle">
                <label class="pt-2 pe-2"><?=lang('Genel.durum')?>:</label>
                <select class="form-select pt-2" name="log_status">
                  <option value=""><?=lang('Genel.hepsi')?></option>
                  <option value="0"><?=lang('Genel.gorulmedi')?></option>
                  <option value="1"><?=lang('Genel.goruldu')?></option>
                </select>
              </div>
            </div>
            <div class="col-lg-3 pt-3 pb-2 pt-lg-0 pb-lg-0 ms-lg-auto">
              <div class="input-icon">
                <span class="input-icon-addon">
                  <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><circle cx="10" cy="10" r="7"></circle><line x1="21" y1="21" x2="15" y2="15"></line></svg>
                </span>
                <input type="text" class="form-control" autocomplete="off" name="search" placeholder="<?=lang('Genel.arama')?>" aria-label="<?=lang('Genel.arama')?>">
              </div>
            </div>
            <div class="table-responsive mb-0 mt-0">
              <table class="table table-striped table-borderless border-0 text-muted pt-2" data-order='[[0,"desc"]]' data-page-length='10' id="ajax-datatable" data-url="<?=base_url('Kullanicilar/IslemKayitlariAjax/'.$kullaniciBilgileri->user_id)?>">
                <thead>
                  <tr>
                    <th class="ps-2" data-width="2%" data-class="text-left text-truncate">#</th>
                    <th class="ps-2" data-orderable="false" data-class="text-truncate max-width-100"><?=lang('Genel.icerik')?></th>
                    <th class="ps-2" data-orderable="false" data-class="text-truncate max-width-100"><?=lang('Genel.link')?></th>
                    <th class="ps-2" data-width="5%" data-class="text-center text-truncate"><?=lang('Genel.durum')?></th>
                    <th class="ps-2" data-width="15%" data-class="text-center text-truncate max-width-100"><?=lang('Genel.tarih')?></th>
                    <th class="ps-2" data-width="5%" data-class="text-center text-truncate"><?=lang('Genel.ip')?></th>
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
<?=view('Static/Footer')?>
