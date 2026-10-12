<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none">
    <div class="row align-items-center">
      <div class="col">
        <h1 class="page-title"><?=lang('Kullanicilar.sayfa.kullanicilar')?></h1>
      </div>
      <div class="col-auto d-md-flex">
        <?php if (IsAllowedViewModule('kullaniciEkleyebilsin')): ?>
          <a href="<?=base_url('Kullanicilar/Ekle')?>" class="btn btn-dark me-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><rect x="4" y="4" width="6" height="6" rx="1" /><rect x="14" y="4" width="6" height="6" rx="1" /><rect x="4" y="14" width="6" height="6" rx="1" /><path d="M14 17h6m-3 -3v6" /></svg>
            <?=lang('Genel.ekle')?>
          </a>
        <?php endif; ?>
      </div>
    </div>
  </div>
  <div class="row row-cards">
    <div class="col-12">
      <div class="card">
        <div class="card-body pb-0">
          <div class="row">
            <div class="col-lg-3 pt-lg-0">
              <div class="d-flex align-middle">
                <label class="pt-2 pe-2"><?=lang('Genel.durum')?>:</label>
                <select class="form-select pt-2" name="user_status">
                  <option value=""><?=lang('Genel.hepsi')?></option>
                  <option value="0"><?=lang('Genel.pasif')?></option>
                  <option value="1"><?=lang('Genel.aktif')?></option>
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
              <table class="table table-striped table-borderless border-0 text-muted pt-2" data-order='[[0,"desc"]]' data-page-length='10' id="ajax-datatable" data-url="<?=base_url('Kullanicilar/Ajax')?>">
                <thead>
                  <tr>
                    <th class="ps-2" data-width="1%" data-class="text-left text-truncate">#</th>
                    <th class="ps-2" data-orderable="false" data-class="text-truncate max-width-300"><?=lang('Genel.kullaniciAdi')?></th>
                    <th class="ps-2" data-width="1%"><?=lang('Genel.durum')?></th>
                    <th class="ps-2" data-width="5%" data-class="text-truncate"><?=lang('Kullanicilar.sayfa.girisTarihi')?></th>
                    <?php if (IsAllowedViewModule('kullaniciDetayiniGorebilsin')): ?>
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
<?=view('Static/Footer')?>
