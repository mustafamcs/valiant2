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
                                    +--> dosya sunucusu (127.0.0.1:8091 python thread)  ->  runtime\patchserver\patch
Oyuncu  --tcp----->  game.exe core'lari (30001, 30003-30009, 30051)
Panel   --socket-->  P2P portlari (30002, 30004, 30006, 30008, 30010, 30052) -> RELOAD/notice/kick
Herkes  --------->  MariaDB 3306 (sadece localhost)
```

- Public IP `.env`'deki `PUBLIC_IP` değerinden okunur. setup.ps1 IP'yi otomatik algılar.
- HTTPS sertifikası: setup.ps1 self-signed üretir; production'da Let's Encrypt kullanılabilir.
- Domain gerekli değil — her şey IP üzerinden çalışır.

## Klasör haritası

```
VALIANT2/                                       Proje kökü (git repo)
├── assets/unpacked/data/                       Client kaynak dosyaları (pack üretimi)
├── database/                                   SQL şema + seed dosyaları
├── runtime/
│   ├── client/game/                            Canlı client dosyaları
│   ├── client/VALIANT2.exe                     Patcher/Launcher
│   ├── server/main/srv1/                       Sunucu süreç dizinleri
│   │   ├── auth/                                 Auth core
│   │   ├── chan/ch1/core{1-4}/                    CH1 core'ları
│   │   ├── chan/ch99/core99/                      CH99 core
│   │   ├── db/                                   DB peer
│   │   └── share/                                Paylaşılan conf/data/bin
│   ├── server/.state/                          PID dosyaları
│   ├── dependencies/mariadb/                   MariaDB 11.4 portable (git'e girmez)
│   ├── dependencies/nginx/                     nginx + SSL sertifikaları (git'e girmez)
│   └── patchserver/                            Patch deploy hedefi (git'e girmez)
├── scripts/windows/                            Tüm işletim scriptleri
├── source/
│   ├── client/                                 Client C++ kaynak + external
│   ├── server/                                 Server C++ kaynak + external
│   └── patchserver/                            Patch altyapısı kaynakları
│       ├── src/Patcher.cs                        Autopatcher (C#) kaynak kodu
│       ├── file_server.py                        HTTP dosya sunucusu (Python)
│       └── patch_watch.py                        Dosya değişiklik izleyici (Python)
├── tools/                                      Yardımcı araçlar
│   ├── client-config/                            config.exe kaynağı
│   ├── control-center/                           VALIANT2-ControlCenter.exe kaynağı (C# WinForms)
│   ├── db-manager/                               DB yönetim aracı
│   ├── dump-proto/                               Proto dönüştürücü
│   └── pack-maker/                               Pack oluşturucu
├── web/adminpanel/                             CodeIgniter 4 admin paneli
├── VALIANT2-ControlCenter.exe                  Masaüstü tümleşik yönetim ve kurulum paneli
├── .env                                        Ortam değişkenleri (git'e girmez)
├── AGENTS.md                                   Bu rehber
└── README.md                                   Proje tanıtımı
```

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

- `VALIANT2-Stack` → `start-stack.cmd` (oturum açılışında: nginx + 4 PHP worker + patch sunucusu + watcher)
- Oyun sunucusu için görev YOK — `start-server.cmd` ile elle başlatılır.

## Scriptler (scripts\windows)

| Komut | Ne yapar |
|---|---|
| `common.ps1` | Paylaşılan yardımcılar — tüm scriptler `.env` okuma, php/pythonw/nginx bulma, PATCH_ROOT/PUBLIC_IP çözümü için bunu dot-source eder. Yeni script yazarken bunu kullan |
| `create-account.cmd` | İnteraktif: oyun hesabı açar (account.account, MySQL PASSWORD hash) + karaktere IMPLEMENTOR yetkisi (common.gmlist). setup.cmd içinde de sorulur |
| `setup.cmd` | **İlk kurulum** (yeni makine, tek komut): winget bağımlılıkları (Git/LFS/VS2022/PHP8.3/Python3.12/MariaDB), `.env` üretimi, nginx indir+conf+sertifika, patchserver dağıtımı, scheduled task `VALIANT2-Stack`, firewall kuralları, DB şema (oyun + panel), `build-all` + `build-patcher` |
| `build-all.ps1 [-SkipPacks]` | config.exe + client sln + launcher + server sln + tüm pack'ler (MSBuild 2022) |
| `build-client-packs.ps1` | `assets\unpacked\data` → runtime pack'leri (FSArchiver) |
| `build-patcher.cmd` | `Patcher.cs` → VALIANT2.exe; runtime/client + patchserver'a kopyalar, patcher.json hash günceller |
| `build-control-center.cmd` | `tools\control-center` → kök dizine `VALIANT2-ControlCenter.exe` derler (dahili .NET 4 `csc.exe` kullanır) |
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
| `git-sanitize.ps1` | `.env`'den üretilen dosyaları (CONFIG'ler, conf.txt, start_panel.vbs) `git update-index --skip-worktree` ile diff'lerden gizler. `sync-config` ve `setup` otomatik çağırır — bu dosyaların değişiklik göstermesi NORMAL ve git'te görünmez |
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

- **`BIND_IP`** her core CONFIG'inde zorunlu — `sync-config.ps1` makinenin internal adapter IP'sini otomatik yazar. `0.0.0.0` KULLANMA: game.exe `g_szPublicIP[0]=='0'` kontrolü ile `exit(1)` yapar. NAT public IP de yerel adaptörde olmadığı için bind başarısız olur.
- `serverinfo.py`: `SERVER_IP=<PUBLIC_IP>`, `SERVER_IP_2=127.0.0.1`. `sync-config.ps1` IP'yi `.env`'den günceller. Değişince `create_root.bat` ile root.pak yeniden paketlenir — patch watcher bunu otomatik dağıtır.
- `common.game_settings.version` = client version (`1000138964`). Client version değişirse bu satır güncellenmeli yoksa "client out of date". Server 60sn'de bir tabloyu yeniden okur.
- PHP panel worker'ları `php -S` × 4 — Windows'ta `PHP_CLI_SERVER_WORKERS` çalışmaz, ayrı süreç + nginx upstream kullanılıyor.
- nginx `limit_req_zone` 50r/s burst=100 — patch listeleme eskiden her istekte sha256 hesaplıyordu, artık `hashcache.json` cache'li.
- P2P/admin portları dışarıya açık ama `@` komutları `ADMINPAGE_IP1` (127.0.0.1) + parola korumalı.
- Cloudflare Tunnel (`cloudflared`) ve Playit artık gerekmiyor.
- **Linux symlink → Windows dosya sorunu**: git clone'da `CMD`, `CRC`, `PTS`, `VERSION`, `BANIP`, `data`, `locale`, `log` gibi dosyalar Linux'ta symlink ama Windows'ta düz metin (hedef yolu içerik olarak) olarak oluşur. game.exe bunları parse edince crash/exit yapar (ör. CMD içindeki `../share/conf/CMD` metni komut olarak parse edilip `exit(1)` çağrılır). `sync-config.ps1` her çağrıda bu dosyaları otomatik düzeltir.

## Panel notları

- Yetkiler granüler: `IsAllowedViewModule('<yetki>')`. Patch için: `patchGorebilsin`, `patchEkleyebilsin`, `patchSilebilsin`.
- Sayfa başlıkları `app/Views/Static/Title.php` içinde `WebTitle()` zinciri — yeni controller eklersen oraya da ekle (yoksa sekmede "Sayfa Bulunamadı" yazar).
- CSRF: POST'larda `csrf_token` alanı zorunlu; yeni controller'ları `app/Config/Filters.php`'deki CSRF whitelist'e gerekirse ekle.
- `Routes.php` içinde `/` → `GirisYap::Index` açık.
- Tüm panel işlemleri `LogAdd(...)` ile işlem kayıtlarına düşer.

## Taşınabilirlik kuralları

- **Tüm bağımlılıklar proje içinde**: MariaDB → `runtime\dependencies\mariadb`, nginx → `runtime\dependencies\nginx`, patchserver → `runtime\patchserver`. Proje dışında dosya oluşturulmaz. `common.ps1`'deki `Get-MariaDbDir`/`Get-NginxDir`/`Get-PatchRoot` bu yolları verir.
- Hiçbir script'te mutlak kullanıcı yolu veya sabit IP yazma: `common.ps1`'deki `Get-EnvSettings`/`Get-PublicBase`/`Get-PatchRoot`/`Get-PhpExe`/`Get-PythonwExe`/`Get-NginxExe`/`Get-MariaDbDir`/`Get-NginxDir` kullan.
- `.env` değişkenleri: `PUBLIC_IP` (dış adres — panel/patch/BIND_IP için), `CLIENT_SERVER_IP` (client'ın bağlandığı), `PATCH_ROOT` (patch deploy dizini), `PANEL_BASE_URL`, `PANEL_DB_*`. `.env` git'e girmez; setup her makinede kendisi üretir (IP'yi api.ipify/ifconfig/icanhazip'ten otomatik algılar, şifreleri rastgele basar). Sablon/örnek dosya YOK — her şey canlı üretilir.
- Patcher `Cfg.BASE_URL` kullanır; `build-patcher.ps1` derleme anında bu sınıfı `.env`'den üretir — kaynak dosyada IP yok.
- `sync-config.ps1` CONFIG'lere `BIND_IP: <internal_adapter_IP>` yazar (yoksa ekler), runtime dizinlerindeki Linux semlink referans dosyalarını (CMD, CRC, PTS, VERSION, BANIP vb.) düzeltir, `log` dizini + `data`/`locale` junction'larını oluşturur. IP değişince `sync-config` + `restart-server` yeterli.
- Runtime CONFIG'ler repo'da `__FROM_ENV__` placeholder'ıyla durur; start/build'da `.env`'den gerçek değerler yazılır, stop'ta tekrar placeholder'a çekilir. `git-sanitize` (skip-worktree) sayesinde bu dosyalar git diff'inde görünmez — commit'leme.
- Panel `PatchRoot` sabitini `Settings.php`'deki `PATCH_ROOT`'tan okur — controller'larda `PatchRoot . "/patch"` kullan.

## Veritabanı

- MariaDB (servis `MariaDB`), sadece localhost:3306. Bağlantı bilgileri `.env`'de.
- DB'ler: `account`, `common`, `log`, `player` + panel DB (`PANEL_DB_DATABASE`).
- `database/bootstrap.sql` = 4 oyun DB'sinin şema+seed'i; `database/extra_tables.sql` = drop tabloları (drop_default 1542, drop_special_* 700+, drop_mob_*), biolog/fishevent/itemshop/offline_shop_sales view; `database/drop_seed.sql` = drop_default seed. Hepsi `setup-database.ps1` tarafından import edilir.
- Panel DB (`valiant_panel`) `web\adminpanel\sql.sql`'den kurulur (users/settings/logs/item_icon vb.).
- item_proto/mob_proto MySQL'de **player** DB'sinde (db.exe DirectQuery varsayılan slot = SQL_PLAYER). skill_proto, refine_proto, item_attr, item_attr_rare, banword da player'da.

## Tipik iş akışları

- **Kod değişti, rebuild:** `build-all.cmd` (veya sadece ilgili parça), sonra `restart-server.cmd` ve client'a yeniden paket.
- **Client dosyası değişti:** hiçbir şey yapma — watcher ~15sn içinde manifest'i günceller; ya da `publish-patch.cmd`.
- **Patcher UI/kod değişti:** `build-patcher.cmd` (otomatik dağıtır + self-update hash'ini günceller).
- **Sunucu çöktü/dondu:** `restart-server.cmd` sonra `stack-status.cmd`.
- **Dışarıdan erişim sorunu:** önce `stack-status.cmd` → kapalı port varsa start scriptlerini çalıştır.
