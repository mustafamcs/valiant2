<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none">
    <div class="row align-items-center">
      <div class="col">
        <h1 class="page-title">Oyun Sistemleri (`Controls.h` `#define`), Sunucu Profilleri & Başlangıç Paketi</h1>
        <div class="text-muted mt-1">Client ve Server <code>Controls.h</code> içindeki tüm <code>#ifdef / #else</code> özellik bayraklarını tek tıkla açıp kapatın, sunucu profilini seçin ve başlangıç eşyalarını düzenleyin.</div>
      </div>
    </div>
  </div>
</div>

<div class="page-body">
  <div class="container-xl">
    <!-- SERVER PROFILE CARDS (MsmPanel / IrisPanel Style) -->
    <div class="row row-cards mb-3">
      <div class="col-md-3">
        <div class="card">
          <div class="card-body">
            <h3 class="card-title text-warning">⚔️ 1 - 99 Classic Emek</h3>
            <p class="text-muted small">Geleneksel düşük Yang/EXP dengesi, değerli düşen BK ve Ruh Taşı ekonomisi.</p>
            <button class="btn btn-outline-warning w-100 btnApplyProfile" data-profile="1_99_emek">Bu Profili Uygula</button>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card">
          <div class="card-body">
            <h3 class="card-title text-azure">🛡️ 1 - 105 Orta Emek</h3>
            <p class="text-muted small">Dengeli metin/zindan farmı, Kuşak, Simya ve Evrimli Pet odaklı orta ölçekli yapı.</p>
            <button class="btn btn-outline-info w-100 btnApplyProfile" data-profile="1_105_orta">Bu Profili Uygula</button>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card">
          <div class="card-body">
            <h3 class="card-title text-success">🐉 65 - 250 Bol Dönüşüm PvM</h3>
            <p class="text-muted small">Yüksek Yang/Hasar ölçeği, çoklu zindan döngüsü ve hızlı dönüşüm zinciri.</p>
            <button class="btn btn-outline-success w-100 btnApplyProfile" data-profile="65_250_pvm">Bu Profili Uygula</button>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card">
          <div class="card-body">
            <h3 class="card-title text-danger">👑 98 - 99 WS'lik Düello</h3>
            <p class="text-muted small">Hazır ekipman, tek tık Biyolog ve doğrudan Lonca / 1v1 turnuva odaklı yapı.</p>
            <button class="btn btn-outline-danger w-100 btnApplyProfile" data-profile="98_99_wslik">Bu Profili Uygula</button>
          </div>
        </div>
      </div>
    </div>

    <ul class="nav nav-tabs mb-3" data-bs-toggle="tabs">
      <li class="nav-item">
        <a href="#tab-controls-flags" class="nav-link active" data-bs-toggle="tab">⚙️ 1. C++ `Controls.h` Özellik Bayrakları (<?=count($flags)?> Sistem)</a>
      </li>
      <li class="nav-item">
        <a href="#tab-starter-quest" class="nav-link" data-bs-toggle="tab">🎒 2. Başlangıç Seviye / Ekipman Paketi (`give_basic_weapon.lua`)</a>
      </li>
    </ul>

    <div class="tab-content">
      <!-- TAB 1: CONTROLS.H FLAGS -->
      <div class="tab-pane active show" id="tab-controls-flags">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h3 class="card-title">Client & Server `Controls.h` Senkronize Sistem Yöneticisi</h3>
            <input type="text" id="inpFlagSearch" class="form-control w-25" placeholder="ENABLE_... bayrağı ara...">
          </div>
          <div class="card-body p-0">
            <div class="table-responsive" style="max-height:580px;">
              <table class="table table-vcenter table-striped mb-0" id="tblFeatureFlags">
                <thead>
                  <tr>
                    <th>Özellik Bayrağı (`#define`)</th>
                    <th>Client Durumu</th>
                    <th>Server Durumu</th>
                    <th>Senkron</th>
                    <th class="text-end">Durum Değiştir (Aç / Kapat)</th>
                  </tr>
                </thead>
                <tbody>
                  <?php foreach ($flags as $f): ?>
                    <tr>
                      <td><code><?=htmlspecialchars($f['name'])?></code></td>
                      <td>
                        <?php if (!$f['in_client']): ?>
                          <span class="text-muted">-</span>
                        <?php elseif ($f['client_on']): ?>
                          <span class="badge bg-success">AÇIK</span>
                        <?php else: ?>
                          <span class="badge bg-secondary">KAPALI</span>
                        <?php endif; ?>
                      </td>
                      <td>
                        <?php if (!$f['in_server']): ?>
                          <span class="text-muted">-</span>
                        <?php elseif ($f['server_on']): ?>
                          <span class="badge bg-success">AÇIK</span>
                        <?php else: ?>
                          <span class="badge bg-secondary">KAPALI</span>
                        <?php endif; ?>
                      </td>
                      <td>
                        <?php if ($f['synced']): ?>
                          <span class="badge bg-azure-lt">Eşit</span>
                        <?php else: ?>
                          <span class="badge bg-warning">Farklı</span>
                        <?php endif; ?>
                      </td>
                      <td class="text-end">
                        <?php if ($f['active']): ?>
                          <button class="btn btn-sm btn-outline-danger btnToggleFlag" data-flag="<?=htmlspecialchars($f['name'])?>" data-enable="0">Kapat (`//#define`)</button>
                        <?php else: ?>
                          <button class="btn btn-sm btn-outline-success btnToggleFlag" data-flag="<?=htmlspecialchars($f['name'])?>" data-enable="1">Aç (`#define`)</button>
                        <?php endif; ?>
                      </td>
                    </tr>
                  <?php endforeach; ?>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 2: STARTER QUEST -->
      <div class="tab-pane" id="tab-starter-quest">
        <div class="card">
          <div class="card-header">
            <h3 class="card-title">Yeni Karakter Başlangıç Paketi (`collection/special/give_basic_weapon.lua`)</h3>
          </div>
          <div class="card-body">
            <textarea class="form-control font-monospace mb-3" id="txtStarterQuest" rows="18"><?=htmlspecialchars($startQuest)?></textarea>
            <button type="button" class="btn btn-primary" id="btnSaveStarterQuest">💾 Başlangıç Paketini Kaydet</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const baseUrl = '<?=base_url()?>';

  document.getElementById('inpFlagSearch').addEventListener('input', function() {
    const q = this.value.toLowerCase();
    document.querySelectorAll('#tblFeatureFlags tbody tr').forEach(tr => {
      tr.style.display = tr.textContent.toLowerCase().includes(q) ? '' : 'none';
    });
  });

  document.querySelectorAll('.btnToggleFlag').forEach(btn => {
    btn.addEventListener('click', function() {
      const flag = this.getAttribute('data-flag');
      const enable = this.getAttribute('data-enable');
      $.post(baseUrl + '/Sistemler/BayrakDegistirAjax', { flag: flag, enable: enable }, function(res) {
        if (res.status === 'ok') {
          toastr["success"](res.message);
          setTimeout(() => location.reload(), 600);
        } else {
          toastr["error"](res.message || 'Hata');
        }
      }, 'json');
    });
  });

  document.querySelectorAll('.btnApplyProfile').forEach(btn => {
    btn.addEventListener('click', function() {
      const profile = this.getAttribute('data-profile');
      $.post(baseUrl + '/Sistemler/ProfilUygulaAjax', { profile: profile }, function(res) {
        if (res.status === 'ok') toastr["success"](res.message);
        else toastr["error"](res.message || 'Hata');
      }, 'json');
    });
  });

  document.getElementById('btnSaveStarterQuest').addEventListener('click', function() {
    const content = document.getElementById('txtStarterQuest').value;
    $.post(baseUrl + '/Sistemler/BaslangicKaydetAjax', { content: content }, function(res) {
      if (res.status === 'ok') toastr["success"](res.message);
      else toastr["error"](res.message || 'Hata');
    }, 'json');
  });
});
</script>
<?=view('Static/Footer')?>
