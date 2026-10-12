<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none mb-2">
    <div class="row align-items-center">
      <div class="mb-1">
        <ol class="breadcrumb breadcrumb-alternate" aria-label="breadcrumbs">
          <li class="breadcrumb-item"><a href="<?=base_url()?>"><?=lang('Ayarlar.sayfa.ayarlar')?></a></li>
          <li class="breadcrumb-item active"><a href="<?=base_url('Ayarlar/P2P')?>"><?=lang('Ayarlar.sayfa.p2pAyarlari')?></a></li>
        </ol>
      </div>
    </div>
  </div>
  <div class="row row-cards">
    <div class="col-md-12">
      <div class="card">
        <?=view('Ayarlar/TabMenu')?>
        <div class="card-body">
          <form class="P2PGuncelle">
            <div class="mb-2">
              <div class="form-label"><?=lang('Genel.durum')?></div>
              <select class="form-control" name="p2pStatus">
                <option value="0" <?=(p2pStatus==0?'selected':'')?>><?=lang('Genel.pasif')?></option>
                <option value="1" <?=(p2pStatus==1?'selected':'')?>><?=lang('Genel.aktif')?></option>
              </select>
            </div>
            <div class="row">
              <div class="col-lg-6">
                <div class="mb-2">
                  <div class="form-label">IP</div>
                  <input type="text" class="form-control" name="p2pHost" value="<?=p2pHost?>" required>
                </div>
              </div>
              <div class="col-lg-6">
                <div class="mb-2">
                  <div class="form-label"><?=lang('Genel.sifre')?></div>
                  <input type="text" class="form-control" name="p2pPassword" value="<?=p2pPassword?>" required>
                </div>
              </div>
            </div>
            <div class="mb-2">
              <div class="form-label"><?=lang('Ayarlar.sayfa.portlar')?></div>
              <input type="text" class="form-control" name="p2pPorts" value="<?=implode(',',p2pPorts)?>" required>
            </div>
            <div class="row">
              <div class="col-lg-6">
                <div class="mb-2">
                  <div class="form-label"><?=lang('Ayarlar.sayfa.anasayfaIstatistik')?></div>
                  <select class="form-control" name="p2pStatistics">
                    <option value="0" <?=(p2pStatistics==0?'selected':'')?>><?=lang('Genel.pasif')?></option>
                    <option value="1" <?=(p2pStatistics==1?'selected':'')?>><?=lang('Genel.aktif')?></option>
                  </select>
                </div>
              </div>
              <div class="col-lg-6">
                <div class="mb-2">
                  <div class="form-label"><?=lang('Ayarlar.sayfa.chPortlar')?></div>
                  <input type="text" class="form-control" name="p2pChannel" value="<?=implode(',',p2pChannel)?>" required>
                </div>
              </div>
            </div>
            <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
            <div class="form-footer mt-2">
              <button type="submit" class="btn btn-primary w-100"><?=lang('Ayarlar.sayfa.p2pAyarlariGuncelle')?></button>
            </div>
          </form>
          <hr>
          <form class="P2PTestEt">
            <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
            <div class="form-footer mt-2">
              <button type="submit" class="btn btn-primary w-100"><?=lang('Ayarlar.sayfa.p2pBaglantisiniTestEt')?></button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
<?=view('Static/Footer')?>
