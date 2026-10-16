<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none">
    <div class="row align-items-center">
      <div class="col">
        <h1 class="page-title">Görsel Arındırma (Cube) & Üretim Tarifleri Stüdyosu</h1>
        <div class="text-muted mt-1">Sunucu (<code>common/cube.txt</code>) ve İstemci Wikipedia (<code>wikipedia/cube.txt</code>) dosyalarını eşzamanlı yönetin. Toplam <strong><?=count($recipes)?></strong> aktif tarif.</div>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#modalCubeEkle">
          ➕ Yeni Arındırma Tarifi Ekle
        </button>
      </div>
    </div>
  </div>
</div>

<div class="page-body">
  <div class="container-xl">
    <?php if (!empty($conflicts)): ?>
      <div class="alert alert-warning mb-3">
        <h4 class="alert-title">⚠️ Çakışan Tarif Uyarısı (<?=count($conflicts)?>)</h4>
        <ul class="mb-0">
          <?php foreach ($conflicts as $c): ?>
            <li><?=htmlspecialchars($c)?></li>
          <?php endforeach; ?>
        </ul>
      </div>
    <?php endif; ?>

    <div class="card">
      <div class="card-header d-flex justify-content-between">
        <h3 class="card-title">Kayıtlı Cube Üretim Tarifleri</h3>
        <input type="text" id="inpCubeFilter" class="form-control w-25" placeholder="NPC, Eşya veya Kategori ara...">
      </div>
      <div class="card-body p-0">
        <div class="table-responsive" style="max-height:620px;">
          <table class="table table-vcenter table-striped mb-0" id="tblCubeRecipes">
            <thead>
              <tr>
                <th>#</th>
                <th>NPC</th>
                <th>İstenen Malzemeler</th>
                <th>Üretilen Ödül</th>
                <th>Maliyet (Yang)</th>
                <th>Şans</th>
                <th>Kategori</th>
                <th class="text-center">İşlem</th>
              </tr>
            </thead>
            <tbody>
              <?php foreach ($recipes as $r): ?>
                <tr>
                  <td><?=$r['idx'] + 1?></td>
                  <td>
                    <strong><?=htmlspecialchars($r['npc_name'])?></strong>
                    <div class="text-muted small">VNUM: <?=$r['npc']?></div>
                  </td>
                  <td>
                    <?php foreach ($r['items'] as $m): ?>
                      <span class="badge bg-azure-lt me-1 mb-1">
                        <?=htmlspecialchars($m['name'])?> (<?=$m['vnum']?>) <strong>x<?=$m['count']?></strong>
                      </span>
                    <?php endforeach; ?>
                  </td>
                  <td>
                    <span class="badge bg-green-lt fs-6">
                      🎁 <?=htmlspecialchars($r['reward']['name'])?> (<?=$r['reward']['vnum']?>) <strong>x<?=$r['reward']['count']?></strong>
                    </span>
                  </td>
                  <td><?=number_format($r['gold'], 0, ',', '.')?> Yang</td>
                  <td>
                    <span class="badge <?=($r['percent']>=80?'bg-success':($r['percent']>=40?'bg-warning':'bg-danger'))?>">
                      %<?=$r['percent']?>
                    </span>
                  </td>
                  <td><code><?=htmlspecialchars($r['category'])?></code></td>
                  <td class="text-center">
                    <button type="button" class="btn btn-sm btn-danger btnDeleteCube" data-idx="<?=$r['idx']?>">Sil</button>
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

<!-- MODAL: YENİ CUBE TARİFİ EKLE -->
<div class="modal modal-blur fade" id="modalCubeEkle" tabindex="-1" role="dialog" aria-hidden="true">
  <div class="modal-dialog modal-lg modal-dialog-centered" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Yeni Arındırma (Cube) Tarifi Oluştur</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <form id="frmCubeAdd">
          <div class="row g-2 mb-3">
            <div class="col-md-4">
              <label class="form-label">NPC VNUM</label>
              <input type="number" class="form-control" name="npc" value="20016" required>
            </div>
            <div class="col-md-4">
              <label class="form-label">Ödül Eşya VNUM</label>
              <input type="number" class="form-control" name="reward_vnum" placeholder="Örn: 24600" required>
            </div>
            <div class="col-md-4">
              <label class="form-label">Ödül Adet</label>
              <input type="number" class="form-control" name="reward_count" value="1" required>
            </div>
          </div>

          <div class="row g-2 mb-3">
            <div class="col-md-4">
              <label class="form-label">Yang Maliyeti</label>
              <input type="number" class="form-control" name="gold" value="50000000">
            </div>
            <div class="col-md-4">
              <label class="form-label">Başarı Şansı (%1 - %100)</label>
              <input type="number" class="form-control" name="percent" value="100" min="1" max="100">
            </div>
            <div class="col-md-4">
              <label class="form-label">Kategori</label>
              <select class="form-select" name="category">
                <option value="UPGRADE">UPGRADE (Yükseltme)</option>
                <option value="WEAPON">WEAPON (Silah)</option>
                <option value="ARMOR">ARMOR (Zırh)</option>
                <option value="UNIQUE">UNIQUE (Özel/Takı)</option>
                <option value="ACCESSORY">ACCESSORY (Aksesuar)</option>
                <option value="BELT">BELT (Kemer)</option>
                <option value="ETC">ETC (Diğer)</option>
              </select>
            </div>
          </div>

          <h4 class="mb-2">Gerekli Malzemeler (En az 1, en fazla 5 slot)</h4>
          <?php for ($i = 1; $i <= 5; $i++): ?>
            <div class="row g-2 mb-2">
              <div class="col-md-6">
                <input type="number" class="form-control" name="mat_vnum_<?=$i?>" placeholder="<?=$i?>. Malzeme Eşya VNUM">
              </div>
              <div class="col-md-6">
                <input type="number" class="form-control" name="mat_count_<?=$i?>" placeholder="<?=$i?>. Malzeme Adet">
              </div>
            </div>
          <?php endfor; ?>
        </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn me-auto" data-bs-dismiss="modal">İptal</button>
        <button type="button" class="btn btn-primary" id="btnSubmitCube">💾 Tarifi Kaydet & Canlı Yükle</button>
      </div>
    </div>
  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const baseUrl = '<?=base_url()?>';

  document.getElementById('inpCubeFilter').addEventListener('input', function() {
    const q = this.value.toLowerCase();
    document.querySelectorAll('#tblCubeRecipes tbody tr').forEach(tr => {
      tr.style.display = tr.textContent.toLowerCase().includes(q) ? '' : 'none';
    });
  });

  document.getElementById('btnSubmitCube').addEventListener('click', function() {
    const data = $('#frmCubeAdd').serialize();
    $.post(baseUrl + '/Arindirma/EkleAjax', data, function(res) {
      if (res.status === 'ok') {
        toastr["success"](res.message);
        setTimeout(() => location.reload(), 700);
      } else {
        toastr["error"](res.message || 'Hata');
      }
    }, 'json');
  });

  document.querySelectorAll('.btnDeleteCube').forEach(btn => {
    btn.addEventListener('click', function() {
      const idx = this.getAttribute('data-idx');
      if (!confirm('Bu arındırma tarifini silmek istediğinize emin misiniz?')) return;
      $.post(baseUrl + '/Arindirma/SilAjax', { idx: idx }, function(res) {
        if (res.status === 'ok') {
          toastr["success"](res.message);
          setTimeout(() => location.reload(), 500);
        } else {
          toastr["error"](res.message || 'Hata');
        }
      }, 'json');
    });
  });
});
</script>
<?=view('Static/Footer')?>
