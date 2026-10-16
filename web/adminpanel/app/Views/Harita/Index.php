<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none">
    <div class="row align-items-center">
      <div class="col">
        <h1 class="page-title">Görsel Harita, Regen / Metin Taşı, Yang Isı Haritası & Atlas Stüdyosu</h1>
        <div class="text-muted mt-1">Harita üzerinde tıklayarak Metin/Boss/Mob yerleştirin, Zindan <code>d.purge_area</code> seçin, Saatlik Yang ısı haritasını ve <code>atlasinfo.txt</code> sektörlerini inceleyin.</div>
      </div>
    </div>
  </div>
</div>

<div class="page-body">
  <div class="container-xl">
    <ul class="nav nav-tabs mb-3" data-bs-toggle="tabs">
      <li class="nav-item">
        <a href="#tab-regen-studio" class="nav-link active" data-bs-toggle="tab">1. İnteraktif Harita & Regen / Yang Isı Haritası</a>
      </li>
      <li class="nav-item">
        <a href="#tab-atlas-viewer" class="nav-link" data-bs-toggle="tab">2. AtlasInfo Dünya Sektör & Çakışma Haritası (<?=count($atlas)?> Harita)</a>
      </li>
    </ul>

    <div class="tab-content">
      <!-- TAB 1: REGEN STUDIO -->
      <div class="tab-pane active show" id="tab-regen-studio">
        <div class="row row-cards">
          <div class="col-lg-7">
            <div class="card">
              <div class="card-header d-flex justify-content-between align-items-center">
                <h3 class="card-title" id="canvasHeaderTitle">Harita Kanvası (Tıkla Ekle / Sağ Tıkla Sil / Sürükle d.purge_area)</h3>
                <div class="btn-group btn-group-sm">
                  <button type="button" class="btn btn-outline-warning" id="btnToggleHeatmap">🔥 Yang Isı Haritası: AÇIK</button>
                  <button type="button" class="btn btn-outline-info" id="btnCopyPurge">📋 d.purge_area Kopyala</button>
                </div>
              </div>
              <div class="card-body text-center bg-dark p-2">
                <canvas id="mapCanvas" width="600" height="600" style="border:2px solid #d4af37; cursor:crosshair; max-width:100%; background:#0e1318;"></canvas>
                <div class="d-flex justify-content-between text-light small mt-2 px-2">
                  <span id="lblHoverCoord">Koordinat: (X: 0, Y: 0)</span>
                  <span id="lblPurgeCode" class="text-warning">Alan seçmek için Shift + Sol Tık sürükleyin</span>
                  <span id="lblTotalYangHour" class="text-success fw-bold">Tahmini Kapasite: 0 Yang/saat</span>
                </div>
              </div>
            </div>
          </div>

          <div class="col-lg-5">
            <div class="card mb-3">
              <div class="card-header">
                <h3 class="card-title">Harita Seçimi & Hızlı Ekleme / Izgara Dağıtıcı</h3>
              </div>
              <div class="card-body">
                <div class="row g-2 mb-2">
                  <div class="col-7">
                    <label class="form-label">Harita Klasörü</label>
                    <select class="form-select" id="selMapName">
                      <?php foreach ($maps as $m): ?>
                        <option value="<?=htmlspecialchars($m['name'])?>" <?=($m['name']==='metin2_map_a1'?'selected':'')?>>
                          <?=htmlspecialchars($m['name'])?> (<?=$m['width']?>x<?=$m['height']?>)
                        </option>
                      <?php endforeach; ?>
                    </select>
                  </div>
                  <div class="col-5">
                    <label class="form-label">Spawn Dosyası</label>
                    <select class="form-select" id="selFileType">
                      <option value="stone.txt">stone.txt (Metin)</option>
                      <option value="boss.txt">boss.txt (Boss)</option>
                      <option value="regen.txt" selected>regen.txt (Slot/Grup)</option>
                      <option value="npc.txt">npc.txt (NPC)</option>
                    </select>
                  </div>
                </div>

                <div class="row g-2 mb-2">
                  <div class="col-4">
                    <label class="form-label">Tıkla-Ekle VNUM</label>
                    <input type="number" class="form-control" id="inpSpawnVnum" value="8001">
                  </div>
                  <div class="col-4">
                    <label class="form-label">Süre (15s/10m/1h)</label>
                    <input type="text" class="form-control" id="inpSpawnTime" value="60s">
                  </div>
                  <div class="col-4">
                    <label class="form-label">Izgara Adet</label>
                    <div class="input-group">
                      <input type="number" class="form-control" id="inpGridCount" value="15" min="1" max="200">
                      <button class="btn btn-warning" type="button" id="btnGridDistribute" title="Tüm haritaya otomatik dağıt">Dağıt</button>
                    </div>
                  </div>
                </div>

                <div class="mb-2">
                  <label class="form-label d-flex justify-content-between">
                    <span>Ham Dosya İçeriği (<span id="lblActiveFile">regen.txt</span>)</span>
                    <span class="badge bg-green-lt" id="lblSpawnCount">0 Kayıt</span>
                  </label>
                  <textarea class="form-control font-monospace" id="txtRawRegen" rows="12" style="font-size:12px;"></textarea>
                </div>

                <button type="button" class="btn btn-primary w-100" id="btnSaveRegen">
                  💾 Kaydet ve Canlı Sunucuya Gönder (@RELOAD regen)
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 2: ATLASINFO VIEWER -->
      <div class="tab-pane" id="tab-atlas-viewer">
        <div class="row row-cards">
          <div class="col-lg-7">
            <div class="card">
              <div class="card-header">
                <h3 class="card-title">AtlasInfo 2D Dünya Sektör Haritası (Kırmızı = Çakışan Sektör)</h3>
              </div>
              <div class="card-body text-center bg-dark">
                <canvas id="atlasCanvas" width="620" height="520" style="border:1px solid #444; max-width:100%; background:#090d12;"></canvas>
              </div>
            </div>
          </div>
          <div class="col-lg-5">
            <div class="card">
              <div class="card-header">
                <h3 class="card-title">Sektör Listesi & 25600 Hiza Kontrolü</h3>
              </div>
              <div class="card-body p-0">
                <div class="table-responsive" style="max-height:520px;">
                  <table class="table table-sm table-striped mb-0">
                    <thead>
                      <tr>
                        <th>Harita</th>
                        <th>Base X, Y</th>
                        <th>Boyut</th>
                        <th>25600 Hiza</th>
                      </tr>
                    </thead>
                    <tbody>
                      <?php foreach ($atlas as $a): ?>
                        <tr>
                          <td><code><?=htmlspecialchars($a['name'])?></code></td>
                          <td><?=$a['bx']?>, <?=$a['by']?></td>
                          <td><?=$a['wx']?>x<?=$a['wy']?></td>
                          <td>
                            <?php if ($a['aligned']): ?>
                              <span class="badge bg-success">Tam Hizalı</span>
                            <?php else: ?>
                              <span class="badge bg-warning">Kayık</span>
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
        </div>
      </div>
    </div>
  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const baseUrl = '<?=base_url()?>';
  const canvas = document.getElementById('mapCanvas');
  const ctx = canvas.getContext('2d');
  let mapSetting = { width: 4, height: 5, base_x: 0, base_y: 0 };
  let mapSpawns = [];
  let showHeatmap = true;
  let dragStart = null;
  let purgeRect = null;

  function loadMapData() {
    const map = document.getElementById('selMapName').value;
    const type = document.getElementById('selFileType').value;
    document.getElementById('lblActiveFile').textContent = type;
    $.post(baseUrl + '/Harita/DetayAjax', { map: map, type: type }, function(res) {
      if (res.status === 'ok') {
        mapSetting = res.setting;
        mapSpawns = res.spawns || [];
        document.getElementById('txtRawRegen').value = res.raw || '';
        document.getElementById('lblSpawnCount').textContent = mapSpawns.length + ' Toplam Nokta';
        let totalYang = 0;
        mapSpawns.forEach(s => { if (s.file === 'regen.txt') totalYang += (s.yang_h || 0); });
        document.getElementById('lblTotalYangHour').textContent = 'Harita Kapasitesi: ' + totalYang.toLocaleString('tr-TR') + ' Yang/saat';
        drawMapCanvas();
      }
    }, 'json');
  }

  function drawMapCanvas() {
    const maxW = Math.max(256, mapSetting.width * 256);
    const maxH = Math.max(256, mapSetting.height * 256);
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Grid lines per 256 sector
    ctx.strokeStyle = 'rgba(212, 175, 55, 0.18)';
    ctx.lineWidth = 1;
    for (let x = 0; x <= mapSetting.width; x++) {
      let px = (x / mapSetting.width) * canvas.width;
      ctx.beginPath(); ctx.moveTo(px, 0); ctx.lineTo(px, canvas.height); ctx.stroke();
    }
    for (let y = 0; y <= mapSetting.height; y++) {
      let py = (y / mapSetting.height) * canvas.height;
      ctx.beginPath(); ctx.moveTo(0, py); ctx.lineTo(canvas.width, py); ctx.stroke();
    }

    // Heatmap circles
    if (showHeatmap) {
      mapSpawns.forEach(s => {
        if (s.file !== 'regen.txt') return;
        let px = (s.x / maxW) * canvas.width;
        let py = (s.y / maxH) * canvas.height;
        let grad = ctx.createRadialGradient(px, py, 2, px, py, 28);
        grad.addColorStop(0, 'rgba(255, 90, 0, 0.28)');
        grad.addColorStop(1, 'rgba(255, 90, 0, 0)');
        ctx.fillStyle = grad;
        ctx.beginPath(); ctx.arc(px, py, 28, 0, Math.PI * 2); ctx.fill();
      });
    }

    // Spawn dots
    mapSpawns.forEach(s => {
      let px = (s.x / maxW) * canvas.width;
      let py = (s.y / maxH) * canvas.height;
      if (s.file === 'stone.txt') ctx.fillStyle = '#38bdf8';
      else if (s.file === 'boss.txt') ctx.fillStyle = '#f43f5e';
      else if (s.file === 'npc.txt') ctx.fillStyle = '#facc15';
      else ctx.fillStyle = '#4ade80';

      ctx.beginPath();
      ctx.arc(px, py, s.file === 'boss.txt' ? 6 : (s.file === 'stone.txt' ? 4.5 : 3), 0, Math.PI * 2);
      ctx.fill();
    });

    // Purge Area rectangle
    if (purgeRect) {
      ctx.strokeStyle = '#f43f5e';
      ctx.fillStyle = 'rgba(244, 63, 94, 0.2)';
      ctx.lineWidth = 2;
      ctx.fillRect(purgeRect.x1, purgeRect.y1, purgeRect.x2 - purgeRect.x1, purgeRect.y2 - purgeRect.y1);
      ctx.strokeRect(purgeRect.x1, purgeRect.y1, purgeRect.x2 - purgeRect.x1, purgeRect.y2 - purgeRect.y1);
    }
  }

  canvas.addEventListener('mousemove', function(e) {
    const rect = canvas.getBoundingClientRect();
    const cx = (e.clientX - rect.left) * (canvas.width / rect.width);
    const cy = (e.clientY - rect.top) * (canvas.height / rect.height);
    const maxW = Math.max(256, mapSetting.width * 256);
    const maxH = Math.max(256, mapSetting.height * 256);
    const mapX = Math.round((cx / canvas.width) * maxW);
    const mapY = Math.round((cy / canvas.height) * maxH);
    document.getElementById('lblHoverCoord').textContent = `Harita: (${mapX}, ${mapY}) | Dünya: (${mapSetting.base_x + mapX * 100}, ${mapSetting.base_y + mapY * 100})`;

    if (dragStart) {
      purgeRect = { x1: Math.min(dragStart.x, cx), y1: Math.min(dragStart.y, cy), x2: Math.max(dragStart.x, cx), y2: Math.max(dragStart.y, cy) };
      const wx1 = mapSetting.base_x + Math.round((purgeRect.x1 / canvas.width) * maxW) * 100;
      const wy1 = mapSetting.base_y + Math.round((purgeRect.y1 / canvas.height) * maxH) * 100;
      const wx2 = mapSetting.base_x + Math.round((purgeRect.x2 / canvas.width) * maxW) * 100;
      const wy2 = mapSetting.base_y + Math.round((purgeRect.y2 / canvas.height) * maxH) * 100;
      document.getElementById('lblPurgeCode').textContent = `d.purge_area(${wx1}, ${wy1}, ${wx2}, ${wy2})`;
      drawMapCanvas();
    }
  });

  canvas.addEventListener('mousedown', function(e) {
    const rect = canvas.getBoundingClientRect();
    const cx = (e.clientX - rect.left) * (canvas.width / rect.width);
    const cy = (e.clientY - rect.top) * (canvas.height / rect.height);
    if (e.shiftKey) {
      dragStart = { x: cx, y: cy };
      return;
    }
    if (e.button === 0) {
      const maxW = Math.max(256, mapSetting.width * 256);
      const maxH = Math.max(256, mapSetting.height * 256);
      const mapX = Math.round((cx / canvas.width) * maxW);
      const mapY = Math.round((cy / canvas.height) * maxH);
      const fileType = document.getElementById('selFileType').value;
      const vnum = parseInt(document.getElementById('inpSpawnVnum').value || '8001', 10);
      const resp = document.getElementById('inpSpawnTime').value || '60s';
      const kind = (fileType === 'regen.txt') ? 'r' : 'm';
      const line = `${kind}\t${mapX}\t${mapY}\t10\t10\t0\t0\t${resp}\t100\t1\t${vnum}`;
      const area = document.getElementById('txtRawRegen');
      area.value = (area.value.trim() ? area.value.trim() + "\n" : "") + line + "\n";
      mapSpawns.push({ file: fileType, kind: kind, x: mapX, y: mapY, vnum: vnum, count: 1, yang_h: 5000 });
      drawMapCanvas();
    }
  });

  window.addEventListener('mouseup', function() { dragStart = null; });

  document.getElementById('btnToggleHeatmap').addEventListener('click', function() {
    showHeatmap = !showHeatmap;
    this.textContent = showHeatmap ? '🔥 Yang Isı Haritası: AÇIK' : '🔥 Yang Isı Haritası: KAPALI';
    drawMapCanvas();
  });

  document.getElementById('btnCopyPurge').addEventListener('click', function() {
    const code = document.getElementById('lblPurgeCode').textContent;
    navigator.clipboard.writeText(code);
    toastr["success"]("Panoya kopyalandı: " + code);
  });

  document.getElementById('selMapName').addEventListener('change', loadMapData);
  document.getElementById('selFileType').addEventListener('change', loadMapData);

  document.getElementById('btnSaveRegen').addEventListener('click', function() {
    const map = document.getElementById('selMapName').value;
    const type = document.getElementById('selFileType').value;
    const content = document.getElementById('txtRawRegen').value;
    $.post(baseUrl + '/Harita/KaydetAjax', { map: map, type: type, content: content }, function(res) {
      if (res.status === 'ok') {
        toastr["success"](res.message);
        loadMapData();
      } else {
        toastr["error"](res.message || 'Hata oluştu');
      }
    }, 'json');
  });

  document.getElementById('btnGridDistribute').addEventListener('click', function() {
    const map = document.getElementById('selMapName').value;
    const type = document.getElementById('selFileType').value;
    const vnum = document.getElementById('inpSpawnVnum').value;
    const adet = document.getElementById('inpGridCount').value;
    const sure = document.getElementById('inpSpawnTime').value;
    $.post(baseUrl + '/Harita/IzgaraDagitAjax', { map: map, type: type, vnum: vnum, adet: adet, sure: sure }, function(res) {
      if (res.status === 'ok') {
        toastr["success"](res.message);
        loadMapData();
      } else {
        toastr["error"](res.message || 'Hata');
      }
    }, 'json');
  });

  // Draw AtlasInfo Canvas
  const atlasData = <?=json_encode($atlas)?>;
  const aCanvas = document.getElementById('atlasCanvas');
  if (aCanvas && atlasData.length > 0) {
    const aCtx = aCanvas.getContext('2d');
    let maxCoordX = 1, maxCoordY = 1;
    atlasData.forEach(s => {
      maxCoordX = Math.max(maxCoordX, s.bx + s.wx * 25600);
      maxCoordY = Math.max(maxCoordY, s.by + s.wy * 25600);
    });
    atlasData.forEach((s, idx) => {
      const rx = (s.bx / maxCoordX) * (aCanvas.width - 20) + 10;
      const ry = (s.by / maxCoordY) * (aCanvas.height - 20) + 10;
      const rw = Math.max(6, (s.wx * 25600 / maxCoordX) * (aCanvas.width - 20));
      const rh = Math.max(6, (s.wy * 25600 / maxCoordY) * (aCanvas.height - 20));
      const hue = (idx * 47) % 360;
      aCtx.fillStyle = `hsla(${hue}, 70%, 50%, 0.45)`;
      aCtx.strokeStyle = s.aligned ? `hsl(${hue}, 80%, 65%)` : '#ff4444';
      aCtx.fillRect(rx, ry, rw, rh);
      aCtx.strokeRect(rx, ry, rw, rh);
    });
  }

  loadMapData();
});
</script>
<?=view('Static/Footer')?>
