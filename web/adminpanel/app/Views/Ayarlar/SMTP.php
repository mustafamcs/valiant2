<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none mb-2">
    <div class="row align-items-center">
      <div class="mb-1">
        <ol class="breadcrumb breadcrumb-alternate" aria-label="breadcrumbs">
          <li class="breadcrumb-item"><a href="<?=base_url()?>"><?=lang('Ayarlar.sayfa.ayarlar')?></a></li>
          <li class="breadcrumb-item active"><a href="<?=base_url('Ayarlar/SMTP')?>"><?=lang('Ayarlar.sayfa.smtpAyarlari')?></a></li>
        </ol>
      </div>
    </div>
  </div>
  <div class="row row-cards">
    <div class="col-md-12">
      <div class="card">
        <?=view('Ayarlar/TabMenu')?>
        <div class="card-body">
          <div class="mb-2">
            <div class="form-label"><?=lang('Ayarlar.sayfa.hazirSMTPAyarlari')?></div>
            <select class="form-select" name="hazirAyarlar">
              <option value=""><?=lang('Genel.seciniz')?></option>
              <option value="gmail" data-host="smtp.gmail.com" data-mail="@gmail.com" data-port="465" data-security="ssl">Gmail</option>
              <option value="yandex" data-host="smtp.yandex.com.tr" data-mail="@yandex.com" data-port="465" data-security="ssl">Yandex</option>
            </select>
          </div>
          <form class="SMTPGuncelle row">
            <div class="mb-2 col-lg-4">
              <div class="form-label"><?=lang('Ayarlar.sayfa.gonderenIsim')?></div>
              <input type="text" class="form-control" name="smtpGonderenIsim" value="<?=!empty($smtpGonderenIsim->setting_content)?$smtpGonderenIsim->setting_content:""?>" required>
            </div>
            <div class="mb-2 col-lg-4">
              <div class="form-label"><?=lang('Ayarlar.sayfa.epostaAdresi')?></div>
              <input type="email" class="form-control" name="smtpEpostaAdresi" value="<?=!empty($smtpEpostaAdresi->setting_content)?$smtpEpostaAdresi->setting_content:""?>" required>
            </div>
            <div class="mb-2 col-lg-4">
              <div class="form-label"><?=lang('Ayarlar.sayfa.epostaSifresi')?></div>
              <div class="input-group input-group-flat">
                <input type="password" name="smtpEpostaSifresi" class="form-control" autocomplete="off" value="<?=!empty($smtpEpostaSifresi->setting_content)?$smtpEpostaSifresi->setting_content:""?>" required>
                <span class="input-group-text">
                  <a href="javascript:void(0)" class="link-secondary sifreyiGoster" title="<?=lang('Genel.label.sifreyiGoster')?>" data-bs-toggle="tooltip">
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><circle cx="12" cy="12" r="2" /><path d="M22 12c-2.667 4.667 -6 7 -10 7s-7.333 -2.333 -10 -7c2.667 -4.667 6 -7 10 -7s7.333 2.333 10 7" /></svg>
                  </a>
                </span>
              </div>
            </div>
            <div class="mb-2 col-lg-4">
              <div class="form-label">Host</div>
              <input type="text" class="form-control" name="smtpHost" value="<?=!empty($smtpHost->setting_content)?$smtpHost->setting_content:""?>" required>
            </div>
            <div class="mb-2 col-lg-4">
              <div class="form-label">Port</div>
              <input type="text" class="form-control" name="smtpPort" value="<?=!empty($smtpPort->setting_content)?$smtpPort->setting_content:""?>" required>
            </div>
            <div class="mb-2 col-lg-4">
              <div class="form-label"><?=lang('Ayarlar.sayfa.guvenlikTuru')?></div>
              <select class="form-select" name="smtpGuvenlik">
                <option value="yok" <?=!empty($smtpGuvenlik->setting_content) && $smtpGuvenlik->setting_content=="yok"?'selected':false?>><?=lang('Genel.yok')?></option>
                <option value="tls" <?=!empty($smtpGuvenlik->setting_content) && $smtpGuvenlik->setting_content=="tls"?'selected':false?>>TLS</option>
                <option value="ssl" <?=!empty($smtpGuvenlik->setting_content) && $smtpGuvenlik->setting_content=="ssl"?'selected':false?>>SSL</option>
              </select>
            </div>
            <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
            <div class="form-footer mt-2">
              <button type="submit" class="btn btn-primary w-100"><?=lang('Ayarlar.sayfa.smtpAyarlariGuncelle')?></button>
            </div>
          </form>
          <hr class="mt-3 mb-3">
          <form action="<?=base_url('Ayarlar/TestEPostaGonder')?>" method="post">
            <div class="mb-2">
              <div class="form-label"><?=lang('Ayarlar.sayfa.gonderilecekEPostaAdresi')?></div>
              <input type="email" class="form-control" name="gonderilecekEPostaAdresi" value="<?=!empty($smtpEpostaAdresi->setting_content)?$smtpEpostaAdresi->setting_content:""?>" required>
            </div>
            <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
            <div class="form-footer mt-2">
              <button type="submit" class="btn btn-primary w-100"><?=lang('Ayarlar.sayfa.testEpostasiniGonder')?></button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
<?=view('Static/Footer')?>
