<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none mb-2">
    <div class="row align-items-center">
      <div class="col-auto d-md-flex" style="line-height:40px">
        <ol class="breadcrumb breadcrumb-alternate" aria-label="breadcrumbs">
          <li class="breadcrumb-item"><a href="<?=base_url('Kullanicilar/Index')?>"><?=lang('Kullanicilar.sayfa.kullanicilar')?></a></li>
          <li class="breadcrumb-item"><a href="<?=base_url('Kullanicilar/Detay/'.$kullaniciBilgileri->user_id)?>"><?=lang('Kullanicilar.sayfa.kullaniciDetayi',['user_name' => $kullaniciBilgileri->user_name])?></a></li>
          <li class="breadcrumb-item active"><a href="<?=base_url('Kullanicilar/Yetkilendirme/'.$kullaniciBilgileri->user_id)?>"><?=lang('Kullanicilar.sayfa.yetkilendirme')?></a></li>
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
          <?php if ($kullaniciBilgileri->user_rank!="9"): ?>
            <div class="alert alert-info">
              <?=lang('Kullanicilar.sayfa.yetkilendirmeNot')?>
            </div>
            <form class="YetkiGuncelle">
              <div class="yetkiler row">
                <?php if ($yetkiler): ?>
                  <?php foreach ($yetkiler as $key => $value): ?>
                    <div class="col-12">
                      <h2 class="text-center"><?=lang(''.ucfirst($key).'.yetki.'.$key)?></h2>
                      <hr class="mt-0 mb-2">
                    </div>
                    <?php foreach ($value as $key2 => $value2): ?>
                      <div class="col-10 pt-2">
                        <p><?=lang(''.ucfirst($key).'.yetki.'.$key2)?></p>
                      </div>
                      <div class="col-2">
                        <label class="form-check form-switch" style="margin-top:2px;">
                          <input class="form-check-input" name="yetkiler[<?=$key2?>]" style="background-size: 1.5rem;" type="checkbox" <?=$value2==true?'checked':false?>>
                        </label>
                      </div>
                      <div class="col-12">
                        <hr class="mt-0 mb-2">
                      </div>
                    <?php endforeach; ?>
                  <?php endforeach; ?>
                <?php endif; ?>
              </div>
              <input type="hidden" name="id" value="<?=$kullaniciBilgileri->user_id?>">
              <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
              <div class="form-footer mt-2">
                <button type="submit" class="btn btn-primary w-100"><?=lang('Kullanicilar.sayfa.yetkisiniGuncelle')?></button>
              </div>
            </form>
          <?php else: ?>
            <div class="alert alert-info">
              <?=lang('Kullanicilar.sayfa.yetkilendirmeNotIki')?>
            </div>
          <?php endif; ?>
        </div>
      </div>
    </div>
  </div>
</div>
<?=view('Static/Footer')?>
