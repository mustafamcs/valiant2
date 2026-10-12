<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none">
    <div class="row align-items-center">
      <div class="col">
        <h1 class="page-title"><?=lang('IslemKayitlari.sayfa.islemKayitlari')?></h1>
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
                <select class="form-select pt-2" name="log_status">
                  <option value=""><?=lang('Genel.hepsi')?></option>
                  <option value="0"><?=lang('Genel.gorulmedi')?></option>
                  <option value="1"><?=lang('Genel.goruldu')?></option>
                </select>
              </div>
            </div>
            <?php if (IsAllowedViewModule('tumBildirimleriGorebilsin')): ?>
              <div class="col-lg-4 pt-3 pt-lg-0">
                <div class="d-flex align-middle">
                  <label class="pt-2 pe-2" style="width:150px;"><?=lang('Genel.kullaniciAdi')?>:</label>
                  <select class="form-select pt-2 log_user_id" name="log_user_id">
                    <option value=""><?=lang('Genel.hepsi')?></option>
                  </select>
                </div>
              </div>
            <?php endif; ?>
            <div class="col-lg-3 pt-3 pb-2 pt-lg-0 pb-lg-0 ms-lg-auto">
              <div class="input-icon">
                <span class="input-icon-addon">
                  <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><circle cx="10" cy="10" r="7"></circle><line x1="21" y1="21" x2="15" y2="15"></line></svg>
                </span>
                <input type="text" class="form-control" autocomplete="off" name="search" placeholder="<?=lang('Genel.arama')?>" aria-label="<?=lang('Genel.arama')?>">
              </div>
            </div>
            <div class="table-responsive mb-0 mt-0">
              <table class="table table-striped table-borderless border-0 text-muted pt-2" data-order='[[0,"desc"]]' data-page-length='10' id="ajax-datatable" data-url="<?=base_url('IslemKayitlari/Ajax')?>">
                <thead>
                  <tr>
                    <th class="ps-2" data-width="2%" data-class="text-left text-truncate">#</th>
                    <?php if (IsAllowedViewModule('tumBildirimleriGorebilsin')): ?>
                      <th class="ps-2" data-width="20%" data-class="text-center text-truncate max-width-300"><?=lang('Genel.kullaniciAdi')?></th>
                    <?php endif; ?>
                    <th class="ps-2" data-orderable="false" data-class="text-truncate max-width-300"><?=lang('Genel.icerik')?></th>
                    <th class="ps-2" data-orderable="false" data-class="text-truncate max-width-300"><?=lang('Genel.link')?></th>
                    <th class="ps-2" data-width="5%" data-class="text-center text-truncate"><?=lang('Genel.durum')?></th>
                    <th class="ps-2" data-width="15%" data-class="text-center text-truncate"><?=lang('Genel.tarih')?></th>
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
