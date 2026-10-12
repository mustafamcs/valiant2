# VALIANT2 çalışma kuralları

- Kullanıcı teknik uygulama, bağımlılık kurulumu, yapılandırma, derleme, test ve hata düzeltmelerinde soru sorulmadan otonom ilerlenmesini ister.
- Geri döndürülemez veri silme, veritabanı DROP/toplu DELETE, force-push ve benzeri yıkıcı işlemler için yine işlem özelinde açık onay alınır.
- Bir özellik bayrağı yalnız client ve server tarafındaki bağımlılıkları birlikte doğrulandıktan sonra değiştirilir.
- `source/client/source/Controls.h` ve `source/server/source/common/Controls.h` bayrakları mümkün olduğunda aynı adla ve aynı davranışla eşleşmelidir.
- Her desteklenen özellik bayrağı hem açık hem kapalı durumda derlenebilir olmalı; paket yapıları veya ağ protokolünü etkileyen bayraklar iki tarafta aynı anda test edilmelidir.
- Değişiklik sonrası ilgili client/server derlemesi, runtime dağıtımı ve temiz `syserr` smoke testi yapılır.
- Hassas bilgiler yalnız kök `.env` dosyasında tutulur ve yanıtlarda açıklanmaz.
- Bekleme gerektiren komutlarda bekleme süresi en fazla 20 saniye tutulur; uzun süren işlemler arka planda çalıştırılıp kısa aralıklarla kontrol edilir.

---

# VALIANT2 Sistem Rehberi (tüm AI IDE'leri için tek kaynak)

Bu dosya tüm altyapının nasıl çalıştığını ve nasıl yönetileceğini anlatır. Başka yere bakma.

## Genel mimari

```
Oyuncu  --https-->  nginx (443/80)  --+--> panel_backend (PHP x4: 8090,8092,8093,8094)  ->  CodeIgniter admin paneli
                                    +--> dosya sunucusu (127.0.0.1:8091 python thread)  ->  C:\patchserver\patch, C:\patchserver\patcher
Oyuncu  --tcp----->  game.exe core'lari (30001, 30003-30009, 30051)
Panel   --socket-->  P2P portlari (30002, 30004, 30006, 30008, 30010, 30052) -> RELOAD/notice/kick
Herkes  --------->  MariaDB 3306 (sadece localhost)
```

- Public IP: `213.254.136.100` (sabit, Turkcell). HTTPS sertifikası: Let's Encrypt IP sertifikası (lego, shortlived ~6 gün, otomatik yenileme: `LegoIPRenew` görevi).
- Cloudflare KULLANILMIYOR, domain kullanılmıyor — her şey IP üzerinden.

## Klasör haritası

| Yol | İçerik |
|---|---|
| `C:\Users\Administrator\Desktop\VALIANT2` | Proje kökü (git repo) |
| `runtime\client\game` | Canlı client dosyaları (patch kaynağı, watcher bunu izler) |
| `runtime\client\VALIANT2.exe` | Patcher = launcher (oyunculara dağıtılan exe) |
| `runtime\server\main\srv1\{auth,chan\ch1\core1-4,chan\ch99\core99,db}` | Oyun sunucusu süreç dizinleri; her birinde `CONFIG`, `syslog.txt`, `syserr.txt` |
| `runtime\server\.state` | Süreç pid dosyaları |
| `web\adminpanel` | CodeIgniter 4 panel |
| `assets\unpacked\data` | Client kaynak dosyaları (pack'ler buradan üretilir) |
| `assets\unpacked\create_*.bat` | FSArchiver ile .pak üretimi (örn. `create_root.bat` → `root.pak`) |
| `tools\client-config` | `config.exe` kaynağı (game\bin\config.exe) |
| `tools\client-launcher` | Eski launcher (artık kullanılmıyor, patcher aldı) |
| `patchserver\` | Patch altyapısı kaynakları (Patcher.cs `Cfg.BASE_URL` kullanır — derleme anında `.env`'den üretilir; file_server.py, patch_watch.py `patchserver.json` okur). `setup.ps1`/`start-stack` PATCH_ROOT'a dağıtır |
| `deploy\certs\` | setup.ps1'in ürettiği self-signed sertifika (git'e girmez) |
| `C:\patchserver` | Patch deploy hedefi (`.env` PATCH_ROOT — `patchserver.json` burada, .py'ler ayarları ondan okur) |
| `C:\patchserver\patch\files` | Oyunculara dağıtılan oyun dosyaları |
| `C:\patchserver\patch\patchlist.json` | Manifest (version, base, files[path,size,sha256]) |
| `C:\patchserver\patch\patcher.json` | Patcher self-update manifesti |
| `C:\patchserver\patch\hashcache.json` | Panel hash önbelleği |
| `C:\patchserver\src\Patcher.cs` | Patcher kaynak kodu |
| `C:\patchserver\file_server.py` | /update ve /patcher için threaded dosya sunucusu (127.0.0.1:8091) |
| `C:\patchserver\patch_watch.py` | Watcher: game klasörünü izler → patch/files senkron + manifest bump |
| `C:\nginx-1.27.5` | Web sunucusu; conf: `conf\nginx.conf` |

## Portlar

| Port | Servis | Dışarıya |
|---|---|---|
| 80/443 | nginx → panel + patch | Açık (gerekli) |
| 30001 | Auth | Açık |
| 30003/05/07/09 | CH1 core1-4 | Açık |
| 30051 | CH99 | Açık |
| 30000, 30002, 30004, 30006, 30008, 30010, 30052 | DB peer + P2P | Açık ama admin komutları sadece `ADMINPAGE_IP1` beyaz listesinden (127.0.0.1) |
| 3306 | MariaDB | Kapalı (localhost) |
| 8090-8094 | PHP panel worker'ları | Kapalı (nginx arkası) |
| 8091 | Patch dosya sunucusu | Kapalı (nginx arkası) |
| 135/139/445/3389 | SMB/RDP | Firewall ile kapalı (`VALIANT-Block-*` kuralları) |

## Scheduled Tasks (boot'ta otomatik)

- `VALIANT2-AdminPanel` → `web\adminpanel\start_panel.vbs` (4 PHP worker'ı gizli başlatır)
- `VALIANT2-Nginx` → nginx
- `VALIANT2-PatchFiles` → `file_server.py` (pythonw)
- `VALIANT2-PatchWatch` → `patch_watch.py` (pythonw)
- `LegoIPRenew` → sertifika otomatik yenileme
- Oyun sunucusu için görev YOK — `start-server.cmd` ile başlatılır.

## Scriptler (scripts\windows)

| Komut | Ne yapar |
|---|---|
| `common.ps1` | Paylaşılan yardımcılar — tüm scriptler `.env` okuma, php/pythonw/nginx bulma, PATCH_ROOT/PUBLIC_IP çözümü için bunu dot-source eder. Yeni script yazarken bunu kullan |
| `setup.cmd` | **İlk kurulum** (yeni makine, tek komut): winget bağımlılıkları (Git/LFS/VS2022/PHP8.3/Python3.12/MariaDB), `.env` üretimi, nginx indir+conf+sertifika, patchserver dağıtımı, scheduled task `VALIANT2-Stack`, firewall kuralları, DB şema (oyun + panel), `build-all` + `build-patcher` |
| `build-all.ps1 [-SkipPacks]` | config.exe + client sln + launcher + server sln + tüm pack'ler (MSBuild 2022) |
| `build-client-packs.ps1` | `assets\unpacked\data` → runtime pack'leri (FSArchiver) |
| `build-patcher.cmd` | `Patcher.cs` → VALIANT2.exe; runtime/client + patchserver'a kopyalar, patcher.json hash günceller |
| `sync-config.ps1` | .env'den runtime CONFIG dosyalarını üretir (build-all içinde otomatik çağrılır) |
| `start-server.cmd [-Minimal]` | MariaDB kontrol + db + auth + core'ları başlatır (pid .state'e yazar) |
| `stop-server.cmd` | pid dosyalarından hepsini durdurur |
| `restart-server.cmd` | stop + start |
| `status-server.cmd` | pid'lere göre durum tablosu |
| `start-stack.cmd` | nginx + 4 PHP worker + file_server + patch_watch (hepsi gizli) |
| `stop-stack.cmd` | yukarıdakileri durdurur (oyuna dokunmaz) |
| `restart-stack.cmd` | stack restart |
| `stack-status.cmd` | TÜM servislerin sağlık tablosu (port + http kontrol) |
| `publish-patch.cmd` | manifest'i elle üret + version bump (watcher zaten otomatik yapar) |
| `git-save.cmd ["mesaj"]` | `git add -A` + commit (mesaj yoksa tarihli otomatik mesaj) |
| `git-sync.cmd` | `git pull --rebase` + `git push` (origin: github.com/mustafamcs/valiant2) |
| `git-info.cmd` | branch + status + son 10 commit özeti |
| `setup-database.ps1` | DB şema kurulumu |
| `test-feature-flags.ps1` | bayrak açık/kapalı derleme testi |

## Patch sistemi akışı

1. `runtime\client\game` içinde dosya değişir → `patch_watch.py` (5sn poll + 10sn debounce) fark eder
2. Değişen kopyalanır `patch\files\` altına → manifest üretilir, version +1
3. Oyuncu `VALIANT2.exe` (patcher) açar → patcher.json ile kendini günceller → patchlist.json ile dosya SHA256 karşılaştır → sadece farkları indirir → doğrular → OYNA ile `game\bin\M2Client.exe` başlatır (WorkingDirectory=game)
4. Panel "Patch Yönetimi" sayfası: dosya yükle/sil/listele, "Patchlist Oluştur" elle yayın, "Patcher İndir".

**Hariç tutulanlar** (patch'e girmez — hem watcher hem panel): `UserData` (ama `lang.cfg`, `loca.cfg` dahil!), `logs`, `upload`, `syserr`, `screenshot`, `metin2.cfg`, `mouse.cfg`.

**metin2.cfg:** manifest'te YOK. Patcher ilk açılışta dosya yoksa varsayılanı yazar (1280×1024, 32bit, 120Hz, WINDOWED 1, MUSIC 1.0, VOICE 3). Kullanıcı ayarları asla ezilmez. `config.exe` kök `game\metin2.cfg` okur (`..\metin2.cfg`), ikinci cfg dosyası yok.

## Bilinen kritik noktalar / tuzaklar

- **`BIND_IP: 213.254.136.100`** her core CONFIG'inde zorunlu — yoksa core ilk public adaptörü duyurur (Radmin gibi sanal IP'ler oyuncuları yanlış yere warp eder; "karakter seçiminden sonra login'e atma" belirtisi).
- `serverinfo.py`: `SERVER_IP=213.254.136.100` (public), `SERVER_IP_2=127.0.0.1` (DevServer). Değişince `create_root.bat` ile root.pak yeniden paketlenir — patch watcher bunu otomatik dağıtır.
- `common.game_settings.version` = client version (`1000138964`). Client version değişirse bu satır güncellenmeli yoksa "client out of date". Server 60sn'de bir tabloyu yeniden okur.
- PHP panel worker'ları `php -S` × 4 — Windows'ta `PHP_CLI_SERVER_WORKERS` çalışmaz, ayrı süreç + nginx upstream kullanılıyor.
- nginx `limit_req_zone` 50r/s burst=100 — patch listeleme eskiden her istekte sha256 hesaplıyordu, artık `hashcache.json` cache'li.
- P2P/admin portları dışarıya açık ama `@` komutları `ADMINPAGE_IP1` (127.0.0.1) + parola korumalı.
- Cloudflare Tunnel (`cloudflared`) ve Playit artık gerekmiyor — devre dışı bırakılabilir ama kurulu duruyor.
- `C:\testclient` = izolasyonlu test client klasörü (sadece VALIANT2.exe koy, çalıştır → sıfırdan kurar).

## Panel notları

- Yetkiler granüler: `IsAllowedViewModule('<yetki>')`. Patch için: `patchGorebilsin`, `patchEkleyebilsin`, `patchSilebilsin`.
- Sayfa başlıkları `app/Views/Static/Title.php` içinde `WebTitle()` zinciri — yeni controller eklersen oraya da ekle (yoksa sekmede "Sayfa Bulunamadı" yazar).
- CSRF: POST'larda `csrf_token` alanı zorunlu; yeni controller'ları `app/Config/Filters.php`'deki CSRF whitelist'e gerekirse ekle.
- `Routes.php` içinde `/` → `GirisYap::Index` açık.
- Tüm panel işlemleri `LogAdd(...)` ile işlem kayıtlarına düşer.

## Taşınabilirlik kuralları

- Hiçbir script'te mutlak kullanıcı yolu veya sabit IP yazma: `common.ps1`'deki `Get-EnvSettings`/`Get-PublicBase`/`Get-PatchRoot`/`Get-PhpExe`/`Get-PythonwExe`/`Get-NginxExe` kullan.
- `.env` değişkenleri: `PUBLIC_IP` (dış adres — panel/patch/BIND_IP için), `CLIENT_SERVER_IP` (client'ın bağlandığı), `PATCH_ROOT` (patch deploy dizini), `PANEL_BASE_URL`, `PANEL_DB_*`. `.env` git'e girmez; setup her makinede kendisi üretir (IP'yi api.ipify/ifconfig/icanhazip'ten otomatik algılar, şifreleri rastgele basar). Sablon/örnek dosya YOK — her şey canlı üretilir.
- Patcher `Cfg.BASE_URL` kullanır; `build-patcher.ps1` derleme anında bu sınıfı `.env`'den üretir — kaynak dosyada IP yok.
- `sync-config.ps1` CONFIG'lere `BIND_IP: <PUBLIC_IP>` yazar (yoksa ekler) — IP değişince `sync-config` + `restart-server` yeterli.
- Panel `PatchRoot` sabitini `Settings.php`'deki `PATCH_ROOT`'tan okur — controller'larda `PatchRoot . "/patch"` kullan.

## Veritabanı

- MariaDB (servis `MariaDB`), sadece localhost:3306. Bağlantı bilgileri `.env`'de.
- DB'ler: `account`, `common`, `log`, `player` + panel DB (`PANEL_DB_DATABASE`).
- `database/bootstrap.sql` = 4 oyun DB'sinin şema+seed'i; `database/extra_tables.sql` = drop tabloları (drop_default 1542, drop_special_* 700+, drop_mob_*), biolog/fishevent/itemshop/offline_shop_sales view; `database/drop_seed.sql` = drop_default seed. Hepsi `setup-database.ps1` tarafından import edilir.
- Panel DB (`valiant_panel`) `web\adminpanel\sql.sql`'den kurulur (users/settings/logs/item_icon vb.).
- item_proto/mob_proto MySQL'de (txt değil).

## Tipik iş akışları

- **Kod değişti, rebuild:** `build-all.cmd` (veya sadece ilgili parça), sonra `restart-server.cmd` ve client'a yeniden paket.
- **Client dosyası değişti:** hiçbir şey yapma — watcher ~15sn içinde manifest'i günceller; ya da `publish-patch.cmd`.
- **Patcher UI/kod değişti:** `build-patcher.cmd` (otomatik dağıtır + self-update hash'ini günceller).
- **Sunucu çöktü/dondu:** `restart-server.cmd` sonra `stack-status.cmd`.
- **Dışarıdan erişim sorunu:** önce `stack-status.cmd` → kapalı port varsa start scriptlerini çalıştır.
