<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none mb-2">
    <div class="row align-items-center">
      <div class="col-auto d-md-flex" style="line-height:40px">
        <ol class="breadcrumb breadcrumb-alternate" aria-label="breadcrumbs">
          <li class="breadcrumb-item"><a href="<?=base_url('Kullanicilar/Index')?>"><?=lang('Kullanicilar.sayfa.kullanicilar')?></a></li>
          <li class="breadcrumb-item active"><a href="<?=base_url('Kullanicilar/Ekle')?>"><?=lang('Genel.ekle')?></a></li>
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
    <div class="col-md-12">
      <div class="card">
        <div class="card-body">
          <div class="alert alert-info">
            <?=lang('Kullanicilar.sayfa.ekleNot')?>
          </div>
          <form class="KullaniciEkle">
            <div class="mb-2">
              <div class="form-label"><?=lang('Genel.kullaniciAdi')?></div>
              <div class="input-group input-group-flat">
                <span class="input-group-text">
                  <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><circle cx="12" cy="7" r="4" /><path d="M6 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2" /></svg>
                </span>
                <input type="text" name="name" class="form-control" placeholder="example" minlength="2" autocomplete="off" required>
              </div>
            </div>
            <div class="mb-2">
              <div class="form-label"><?=lang('Genel.label.sifre')?></div>
              <div class="input-group input-group-flat">
                <span class="input-group-text">
                  <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><rect x="5" y="11" width="14" height="10" rx="2" /><circle cx="12" cy="16" r="1" /><path d="M8 11v-4a4 4 0 0 1 8 0v4" /></svg>
                </span>
                <input type="password" name="password" class="form-control" placeholder="*********" minlength="5" autocomplete="off" required>
                <span class="input-group-text border-start-0">
                  <a href="javascript:void(0)" class="link-secondary sifreyiGoster" title="<?=lang('Genel.label.sifreyiGoster')?>" data-bs-toggle="tooltip">
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><circle cx="12" cy="12" r="2" /><path d="M22 12c-2.667 4.667 -6 7 -10 7s-7.333 -2.333 -10 -7c2.667 -4.667 6 -7 10 -7s7.333 2.333 10 7" /></svg>
                  </a>
                </span>
              </div>
            </div>
            <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
            <div class="form-footer mt-2">
              <button type="submit" class="btn btn-primary w-100"><?=lang('Kullanicilar.sayfa.kullaniciEkle')?></button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
<?=view('Static/Footer')?>
