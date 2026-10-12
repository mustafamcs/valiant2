<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none">
    <div class="row align-items-center">
      <div class="col">
        <ol class="breadcrumb breadcrumb-alternate" aria-label="breadcrumbs">
          <li class="breadcrumb-item"><a href="<?=base_url()?>"><?=lang('Kayitlar.sayfa.kayitlar')?></a></li>
          <li class="breadcrumb-item active"><a href="<?=base_url('Kayitlar/Level')?>"><?=lang('Kayitlar.sayfa.levelKayitlari')?></a></li>
        </ol>
      </div>
    </div>
  </div>
  <div class="row row-cards">
    <div class="col-12">
      <div class="card">
        <div class="card-body pb-0">
          <form class="KayitAra">
            <div class="row">
              <div class="col-lg-5">
                <div class="mb-3 d-flex align-items-center">
                  <select class="form-select" name="searchType">
                    <option value="level"><?=lang('Genel.seviye')?></option>
                    <option value="name" selected><?=lang('Genel.karakterAdi')?></option>
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
                  <input type="text" class="form-control" autocomplete="off" name="logSearch" placeholder="<?=lang('Genel.arama')?>" aria-label="<?=lang('Genel.arama')?>">
                </div>
              </div>
              <div class="col-lg-2">
                <button type="submit" class="btn btn-primary w-100 mb-2"><?=lang('Kayitlar.sayfa.ara')?></button>
              </div>
            </div>
          </form>
          <div class="row">
            <div class="table-responsive mb-0 mt-0">
              <table class="table table-striped table-borderless border-0 text-muted pt-2" data-order='[[3,"desc"]]' data-page-length='10' id="ajax-datatable" data-url="<?=base_url('Kayitlar/AjaxLevel')?>">
                <thead>
                  <tr>
                    <th class="ps-2" data-width="1%" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.karakterAdi')?></th>
                    <th class="ps-2" data-width="1%" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.seviye')?></th>
                    <th class="ps-2" data-width="1%" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.oyunSuresi')?></th>
                    <th class="ps-2" data-width="1%" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.tarih')?></th>
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
