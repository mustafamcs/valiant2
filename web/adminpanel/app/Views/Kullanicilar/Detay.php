<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none mb-2">
    <div class="row align-items-center">
      <div class="col-auto d-md-flex" style="line-height:40px">
        <ol class="breadcrumb breadcrumb-alternate" aria-label="breadcrumbs">
          <li class="breadcrumb-item"><a href="<?=base_url('Kullanicilar/Index')?>"><?=lang('Kullanicilar.sayfa.kullanicilar')?></a></li>
          <li class="breadcrumb-item active"><a href="<?=base_url('Kullanicilar/Detay/'.$kullaniciBilgileri->user_id)?>"><?=lang('Kullanicilar.sayfa.kullaniciDetayi',['user_name' => $kullaniciBilgileri->user_name])?></a></li>
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
          <div class="alert alert-info">
            <?=lang('Kullanicilar.sayfa.detayNot')?>
          </div>
          <dl class="row">
            <dt class="col-5"><?=lang('Kullanicilar.sayfa.eklenmeTarihi')?></dt>
            <dd class="col-7"><?=DateDMYHMS($kullaniciBilgileri->user_create_date)?></dd>
            <dt class="col-5"><?=lang('Kullanicilar.sayfa.girisTarihi')?></dt>
            <dd class="col-7"><?=DateDMYHMS($kullaniciBilgileri->user_login_date)?DateDMYHMS($kullaniciBilgileri->user_login_date):lang('Kullanicilar.sayfa.girisYapilmadi')?></dd>
          </dl>
        </div>
      </div>
    </div>
  </div>
</div>
<?=view('Static/Footer')?>
