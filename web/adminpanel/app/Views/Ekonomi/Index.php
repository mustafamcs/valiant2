<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none">
    <div class="row align-items-center">
      <div class="col">
        <h1 class="page-title">Ekonomi, Dupe Alarmı, 360° Eşya Kaynak Analizi & Anti-Cheat Merkezi</h1>
        <div class="text-muted mt-1">Sunucudaki toplam para arzını, lonca gerçek PC/IP dağılımını, herhangi bir eşyanın tüm kaynaklarını (Keira3 360°) ve canlı hile kayıtlarını izleyin.</div>
      </div>
    </div>
  </div>
</div>

<div class="page-body">
  <div class="container-xl">
    <!-- TOP METRIC CARDS -->
    <div class="row row-cards mb-3">
      <div class="col-sm-6 col-lg-3">
        <div class="card card-sm">
          <div class="card-body">
            <div class="subheader">Dolaşımdaki Toplam Yang</div>
            <div class="h2 mb-0 text-warning"><?=number_format($stats['total_gold'], 0, ',', '.')?> Yang</div>
          </div>
        </div>
      </div>
      <div class="col-sm-6 col-lg-3">
        <div class="card card-sm">
          <div class="card-body">
            <div class="subheader">Kayıtlı Hesap / Karakter</div>
            <div class="h2 mb-0 text-azure"><?=$stats['total_accounts']?> Hesap / <?=$stats['total_chars']?> Karakter</div>
          </div>
        </div>
      </div>
      <div class="col-sm-6 col-lg-3">
        <div class="card card-sm">
          <div class="card-body">
            <div class="subheader">Ortalama Karakter Seviyesi</div>
            <div class="h2 mb-0 text-success">Lv. <?=$stats['avg_level']?></div>
          </div>
        </div>
      </div>
      <div class="col-sm-6 col-lg-3">
        <div class="card card-sm">
          <div class="card-body">
            <div class="subheader">Anti-Cheat İhlal Kaydı</div>
            <div class="h2 mb-0 <?=count($stats['hack_logs'])>0?'text-danger':'text-success'?>"><?=count($stats['hack_logs'])?> Kayıt</div>
          </div>
        </div>
      </div>
    </div>

    <ul class="nav nav-tabs mb-3" data-bs-toggle="tabs">
      <li class="nav-item">
        <a href="#tab-keira-360" class="nav-link active" data-bs-toggle="tab">🔍 1. Keira3 360° Eşya Kaynak & Piyasa Analizörü</a>
      </li>
      <li class="nav-item">
        <a href="#tab-wealth-guilds" class="nav-link" data-bs-toggle="tab">💰 2. En Zengin Karakterler & Lonca PC/Modem Denetimi</a>
      </li>
      <li class="nav-item">
        <a href="#tab-anticheat-discord" class="nav-link" data-bs-toggle="tab">🛡️ 3. Canlı Anti-Cheat (`hack_log`) & Discord Webhook</a>
      </li>
    </ul>

    <div class="tab-content">
      <!-- TAB 1: KEIRA3 360 ITEM SOURCE ANALYZER -->
      <div class="tab-pane active show" id="tab-keira-360">
        <div class="card mb-3">
          <div class="card-header">
            <h3 class="card-title">360° Eşya Kaynak ve Bağlantı Sorgulama (Mob Drop + Sandık + NPC Market + Cube + Envanter Stok)</h3>
          </div>
          <div class="card-body">
            <div class="row g-2 mb-3">
              <div class="col-md-4">
                <input type="number" class="form-control" id="inpAnalyzeVnum" placeholder="Eşya VNUM girin (Örn: 25040, 71084, 19)" value="25040">
              </div>
              <div class="col-md-3">
                <button type="button" class="btn btn-primary w-100" id="btnRunItemAnalysis">🔍 Tüm Kaynakları Çözümle</button>
              </div>
            </div>

            <div id="boxItemAnalysisResult" style="display:none;">
              <div class="alert alert-info d-flex justify-content-between align-items-center">
                <div>
                  <strong id="lblAnItemName" class="fs-3">-</strong>
                  <span class="badge bg-dark ms-2" id="lblAnItemMeta">-</span>
                </div>
                <div class="fs-4">
                  Oyuncu Envanterlerindeki Toplam Stok: <strong id="lblAnInvCount" class="text-warning">0</strong> Adet
                </div>
              </div>

              <div class="row row-cards">
                <div class="col-md-6">
                  <div class="card">
                    <div class="card-header"><h4 class="card-title">👾 Düştüğü Canavarlar (`drop_default`)</h4></div>
                    <div class="card-body p-0">
                      <div class="table-responsive" style="max-height:260px;">
                        <table class="table table-sm table-striped mb-0" id="tblAnMobs">
                          <thead><tr><th>Canavar</th><th>Seviye</th><th>Adet</th><th>Oran</th></tr></thead>
                          <tbody></tbody>
                        </table>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="card">
                    <div class="card-header"><h4 class="card-title">🎁 Çıktığı Sandıklar (`drop_special_items`) & Cube Tarifleri</h4></div>
                    <div class="card-body p-0">
                      <div class="table-responsive" style="max-height:260px;">
                        <table class="table table-sm table-striped mb-0" id="tblAnChestsAndCubes">
                          <thead><tr><th>Kaynak Tipi</th><th>Detay</th><th>Adet / Rol</th></tr></thead>
                          <tbody></tbody>
                        </table>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 2: WEALTH & GUILD MODEM AUDIT -->
      <div class="tab-pane" id="tab-wealth-guilds">
        <div class="row row-cards">
          <div class="col-lg-6">
            <div class="card">
              <div class="card-header"><h3 class="card-title">En Çok Yang Bulunduran 15 Karakter (Dupe / Enflasyon Kontrolü)</h3></div>
              <div class="card-body p-0">
                <div class="table-responsive">
                  <table class="table table-vcenter table-striped mb-0">
                    <thead><tr><th>Karakter</th><th>Seviye</th><th>Yang Miktarı</th><th>Son Giriş</th></tr></thead>
                    <tbody>
                      <?php foreach ($stats['top_rich'] as $p): ?>
                        <tr>
                          <td><a href="<?=base_url('Oyuncu/Karakter/'.$p['id'])?>"><strong><?=htmlspecialchars($p['name'])?></strong></a></td>
                          <td>Lv. <?=$p['level']?></td>
                          <td class="text-warning fw-bold"><?=number_format($p['gold'], 0, ',', '.')?></td>
                          <td class="text-muted small"><?=$p['last_play']?></td>
                        </tr>
                      <?php endforeach; ?>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>

          <div class="col-lg-6">
            <div class="card">
              <div class="card-header"><h3 class="card-title">Lonca Üye & Tekil Modem (IP) Dağılımı</h3></div>
              <div class="card-body p-0">
                <div class="table-responsive">
                  <table class="table table-vcenter table-striped mb-0">
                    <thead><tr><th>Lonca Adı</th><th>Seviye</th><th>Toplam Üye</th><th>Farklı IP (Modem)</th><th>Savaş (G/B/M)</th></tr></thead>
                    <tbody>
                      <?php foreach ($stats['guild_stats'] as $g): ?>
                        <tr>
                          <td><strong><?=htmlspecialchars($g['name'])?></strong></td>
                          <td>Lv. <?=$g['level']?></td>
                          <td><?=$g['member_count']?></td>
                          <td><span class="badge bg-azure-lt"><?=$g['unique_ips']?> Tekil IP</span></td>
                          <td><?=$g['win']?> / <?=$g['draw']?> / <?=$g['loss']?></td>
                        </tr>
                      <?php endforeach; ?>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 3: ANTI-CHEAT & DISCORD WEBHOOK -->
      <div class="tab-pane" id="tab-anticheat-discord">
        <div class="row row-cards">
          <div class="col-lg-4">
            <div class="card">
              <div class="card-header"><h3 class="card-title">🔔 Discord Webhook Bildirim Entegrasyonu</h3></div>
              <div class="card-body">
                <div class="mb-2">
                  <label class="form-label">Discord Kanal Webhook URL</label>
                  <input type="url" class="form-control" id="inpWebhookUrl" value="<?=htmlspecialchars($stats['webhook_url'])?>" placeholder="https://discord.com/api/webhooks/...">
                </div>
                <div class="mb-3">
                  <label class="form-label">Test / Duyuru Mesajı</label>
                  <input type="text" class="form-control" id="inpWebhookMsg" value="VALIANT2 Sunucu ve Ekonomi Gözcüsü aktif!">
                </div>
                <button type="button" class="btn btn-primary w-100" id="btnSaveWebhook">💾 Kaydet ve Discord'a Test Gönder</button>
              </div>
            </div>
          </div>

          <div class="col-lg-8">
            <div class="card">
              <div class="card-header"><h3 class="card-title">🛡️ Canlı Anti-Cheat & Bot Kontrol Kayıtları (`log.hack_log`)</h3></div>
              <div class="card-body p-0">
                <div class="table-responsive" style="max-height:420px;">
                  <table class="table table-vcenter table-striped mb-0">
                    <thead>
                      <tr>
                        <th>Tarih</th>
                        <th>Karakter (PID)</th>
                        <th>Hesap</th>
                        <th>IP Adresi</th>
                        <th>İhlal Tipi</th>
                        <th>Harita / Koordinat</th>
                      </tr>
                    </thead>
                    <tbody>
                      <?php if (empty($stats['hack_logs'])): ?>
                        <tr><td colspan="6" class="text-center text-muted py-4">Henüz kayıtlı hile veya bot ihlali bulunmuyor.</td></tr>
                      <?php else: ?>
                        <?php foreach ($stats['hack_logs'] as $hl): ?>
                          <tr>
                            <td class="small"><?=$hl['log_date']?></td>
                            <td><strong><?=htmlspecialchars($hl['name'])?></strong> (#<?=$hl['pid']?>)</td>
                            <td><?=htmlspecialchars($hl['login'])?></td>
                            <td><code><?=htmlspecialchars($hl['ip'])?></code></td>
                            <td><span class="badge bg-danger"><?=htmlspecialchars($hl['hack_type'])?></span></td>
                            <td>Map <?=$hl['map_index']?> (<?=$hl['x']?>, <?=$hl['y']?>)</td>
                          </tr>
                        <?php endforeach; ?>
                      <?php endif; ?>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const baseUrl = '<?=base_url()?>';

  function runAnalysis() {
    const vnum = document.getElementById('inpAnalyzeVnum').value;
    $.post(baseUrl + '/Ekonomi/KaynakAnalizAjax', { vnum: vnum }, function(res) {
      if (res.status !== 'ok') {
        toastr["error"](res.message || 'Hata');
        return;
      }
      const d = res.data;
      document.getElementById('boxItemAnalysisResult').style.display = '';
      if (d.item) {
        document.getElementById('lblAnItemName').textContent = `${d.item.name} (VNUM #${d.item.vnum})`;
        document.getElementById('lblAnItemMeta').textContent = `Seviye: ${d.item.level} | NPC Fiyat: ${d.item.gold} | Dönüşüm VNUM: ${d.item.refined_vnum}`;
      } else {
        document.getElementById('lblAnItemName').textContent = `Eşya #${vnum} (Proto kaydı bulunamadı)`;
        document.getElementById('lblAnItemMeta').textContent = '-';
      }
      document.getElementById('lblAnInvCount').textContent = (d.inv_count || 0).toLocaleString('tr-TR');

      const tbMobs = document.querySelector('#tblAnMobs tbody');
      tbMobs.innerHTML = '';
      if (!d.mobs || d.mobs.length === 0) {
        tbMobs.innerHTML = '<tr><td colspan="4" class="text-center text-muted">Canavar drop kaydı yok</td></tr>';
      } else {
        d.mobs.forEach(m => {
          tbMobs.innerHTML += `<tr><td><strong>${m.mob_name}</strong> (#${m.mob_vnum})</td><td>Lv.${m.level}</td><td>x${m.count}</td><td><span class="badge bg-green-lt">%${m.prob_pct}</span></td></tr>`;
        });
      }

      const tbOther = document.querySelector('#tblAnChestsAndCubes tbody');
      tbOther.innerHTML = '';
      (d.chests || []).forEach(c => {
        tbOther.innerHTML += `<tr><td><span class="badge bg-purple-lt">Sandık</span></td><td>${c.chest_name} (#${c.chest_vnum})</td><td>x${c.count} (Oran: ${c.prob})</td></tr>`;
      });
      (d.shops || []).forEach(s => {
        tbOther.innerHTML += `<tr><td><span class="badge bg-azure-lt">NPC Market</span></td><td>${s.npc_name} (Shop #${s.shop_id})</td><td>x${s.count}</td></tr>`;
      });
      (d.cubes || []).forEach(cb => {
        tbOther.innerHTML += `<tr><td><span class="badge bg-warning-lt">Cube Arındırma</span></td><td>NPC #${cb.npc} (Ödül #${cb.reward})</td><td>${cb.role}</td></tr>`;
      });
      if (tbOther.innerHTML === '') {
        tbOther.innerHTML = '<tr><td colspan="3" class="text-center text-muted">Sandık, Market veya Cube bağlantısı yok</td></tr>';
      }
    }, 'json');
  }

  document.getElementById('btnRunItemAnalysis').addEventListener('click', runAnalysis);
  document.getElementById('btnSaveWebhook').addEventListener('click', function() {
    $.post(baseUrl + '/Ekonomi/DiscordWebhookAjax', {
      webhook_url: document.getElementById('inpWebhookUrl').value,
      test_message: document.getElementById('inpWebhookMsg').value
    }, function(res) {
      if (res.status === 'ok') toastr["success"](res.message);
      else toastr["error"]("Hata");
    }, 'json');
  });

  runAnalysis();
});
</script>
<?=view('Static/Footer')?>
