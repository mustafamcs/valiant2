<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none mb-2">
    <div class="row align-items-center">
      <div class="mb-1">
        <ol class="breadcrumb breadcrumb-alternate" aria-label="breadcrumbs">
          <li class="breadcrumb-item"><a href="<?=base_url()?>"><?=lang('Hesap.sayfa.hesabim')?></a></li>
          <li class="breadcrumb-item active"><a href="<?=base_url('Hesap/Sifre')?>"><?=lang('Hesap.sayfa.sifre')?></a></li>
        </ol>
      </div>
    </div>
  </div>
  <div class="row row-cards">
    <div class="col-md-12">
      <div class="card">
        <?=view('Hesap/TabMenu')?>
        <div class="card-body">
          <div class="alert alert-info">
            <?=lang('Hesap.sayfa.sifremiDegistirNot')?>
          </div>
          <form class="SifreDegistir">
            <div class="mb-2">
              <div class="form-label"><?=lang('Hesap.sayfa.mevcutSifreniz')?></div>
              <div class="input-group input-group-flat">
                <span class="input-group-text">
                  <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><rect x="5" y="11" width="14" height="10" rx="2" /><circle cx="12" cy="16" r="1" /><path d="M8 11v-4a4 4 0 0 1 8 0v4" /></svg>
                </span>
                <input type="password" name="mevcutSifre" class="form-control" placeholder="<?=lang('Hesap.sayfa.mevcutSifreGiriniz')?>" minlength="5" autocomplete="off" required>
                <span class="input-group-text border-start-0">
                  <a href="javascript:void(0)" class="link-secondary mevcutSifreyiGoster" title="<?=lang('Genel.label.sifreyiGoster')?>" data-bs-toggle="tooltip">
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><circle cx="12" cy="12" r="2" /><path d="M22 12c-2.667 4.667 -6 7 -10 7s-7.333 -2.333 -10 -7c2.667 -4.667 6 -7 10 -7s7.333 2.333 10 7" /></svg>
                  </a>
                </span>
              </div>
            </div>
            <div class="mb-2">
              <div class="form-label"><?=lang('Hesap.sayfa.yeniSifreniz')?></div>
              <div class="input-group input-group-flat">
                <span class="input-group-text">
                  <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><rect x="5" y="11" width="14" height="10" rx="2" /><circle cx="12" cy="16" r="1" /><path d="M8 11v-4a4 4 0 0 1 8 0v4" /></svg>
                </span>
                <input type="password" name="yeniSifre" class="form-control" placeholder="<?=lang('Hesap.sayfa.yeniSifreGiriniz')?>" minlength="5" autocomplete="off" required>
                <span class="input-group-text border-start-0">
                  <a href="javascript:void(0)" class="link-secondary yeniSifreyiGoster" title="<?=lang('Genel.label.sifreyiGoster')?>" data-bs-toggle="tooltip">
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><circle cx="12" cy="12" r="2" /><path d="M22 12c-2.667 4.667 -6 7 -10 7s-7.333 -2.333 -10 -7c2.667 -4.667 6 -7 10 -7s7.333 2.333 10 7" /></svg>
                  </a>
                </span>
              </div>
            </div>
            <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
            <div class="form-footer mt-2">
              <button type="submit" class="btn btn-primary w-100"><?=lang('Hesap.sayfa.sifremiDegistir')?></button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
<?=view('Static/Footer')?>
