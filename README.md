# VALIANT2

Metin2 private server platform. Client, server, admin panel, autopatcher ve veritabani tek bir repo'da; temiz bir Windows makinesine tek komutla kurulur.

## Proje Yapisi

```
VALIANT2/
├── assets/                     # Client kaynak dosyalari (pack uretimi)
│   └── unpacked/data/          #   Ham veri (root, locale, icon, effect...)
├── database/                   # SQL semalari ve seed verileri
│   ├── bootstrap.sql           #   account/common/log/player DB semasi
│   ├── extra_tables.sql        #   Drop tablolari, biolog, fishevent...
│   └── drop_seed.sql           #   Varsayilan drop verileri
├── patchserver/                # Patch altyapisi kaynaklari
│   ├── src/Patcher.cs          #   Autopatcher (VALIANT2.exe) kaynak kodu
│   ├── file_server.py          #   HTTP dosya sunucusu (8091)
│   └── patch_watch.py          #   Dosya degisiklik izleyici
├── runtime/
│   ├── client/                 # Client calisma ortami
│   │   ├── game/               #   Oyun dosyalari, pack'ler, bin/
│   │   └── VALIANT2.exe        #   Patcher/Launcher
│   ├── server/                 # Sunucu calisma ortami
│   │   └── main/srv1/          #   auth, db, chan/ch1/core1-4, chan/ch99/core99
│   ├── dependencies/           # Otomatik indirilen bagimliliklar (git'e girmez)
│   │   ├── mariadb/            #   MariaDB 11.4 portable
│   │   └── nginx/              #   nginx web sunucusu
│   └── patchserver/            # Patch deploy hedefi (git'e girmez)
├── scripts/windows/            # Tum isletim scriptleri
│   ├── setup.cmd               #   Tek komut kurulum
│   ├── start-server.cmd        #   Oyun sunucusu baslat
│   ├── start-stack.cmd         #   Web/patch altyapisi baslat
│   ├── build-all.cmd           #   Tam derleme
│   └── ...                     #   Diger scriptler (asagida tablo)
├── source/
│   ├── client/                 # Client C++ kaynak kodu + external
│   └── server/                 # Server C++ kaynak kodu + external
├── tools/                      # Yardimci araclar
│   ├── client-config/          #   config.exe (ayar araci)
│   ├── client-launcher/        #   Eski launcher (artik patcher aldigi icin referans)
│   ├── db-manager/             #   DB yonetim araci
│   ├── dump-proto/             #   Proto dosya donusturucu
│   └── pack-maker/             #   FSArchiver pack olusturucu
├── web/adminpanel/             # CodeIgniter 4 admin paneli
├── deploy/certs/               # SSL sertifikalari (git'e girmez)
├── .env                        # Ortam degiskenleri (git'e girmez, setup uretir)
├── AGENTS.md                   # AI/IDE rehberi (tek kaynak)
└── README.md                   # Bu dosya
```

## Gereksinimler

- Windows 10/11 (64-bit)
- Internet baglantisi (ilk kurulumda bagimliliklar indirilir)
- Yonetici (Administrator) yetkisi

Kurulum scripti gereken her seyi otomatik indirir:
Git, Git LFS, VS 2022 Build Tools, VC++ Redistributable, PHP 8.3, Python 3.12, Python 2.7, MariaDB 11.4, nginx.

## Kurulum

```powershell
git clone https://github.com/mustafamcs/valiant2.git
cd valiant2
scripts\windows\setup.cmd
```

`setup.cmd` sirasiyla:

1. Winget ile tum bagimliliklari kurar
2. `.env` dosyasini uretir (rastgele sifreler, otomatik IP algilama)
3. MariaDB portable indirir ve proje icine kurar
4. Git LFS dosyalarini ceker
5. nginx indirir ve yapilandirir (SSL sertifikasi dahil)
6. Veritabani semalarini import eder (oyun + panel)
7. Client, server ve patcher'i derler
8. Patch altyapisini dagitir
9. Firewall kurallarini ekler
10. Tum servisleri baslatir

> Tum bagimliliklar proje klasoru icinde kalir. Proje disinda dosya olusturulmaz.

## Komutlar

Tum komutlar `scripts\windows\` altindadir:

### Sunucu

| Komut | Aciklama |
|---|---|
| `start-server.cmd` | DB + auth + tum core'lari baslatir |
| `stop-server.cmd` | Oyun sunucusunu durdurur |
| `restart-server.cmd` | Durdur + baslat |
| `status-server.cmd` | Suruclerin durumunu gosterir |

### Web / Patch Altyapisi

| Komut | Aciklama |
|---|---|
| `start-stack.cmd` | nginx + PHP panel + patch sunucusu + watcher |
| `stop-stack.cmd` | Web altyapisini durdurur |
| `restart-stack.cmd` | Durdur + baslat |
| `stack-status.cmd` | Tum servislerin saglik tablosu |

### Derleme

| Komut | Aciklama |
|---|---|
| `build-all.cmd` | Client + server + config + launcher + pack'ler |
| `build-patcher.cmd` | Patcher (VALIANT2.exe) derle + dagit |
| `build-client-packs.cmd [isim]` | Client pack'lerini olustur |

### Git

| Komut | Aciklama |
|---|---|
| `git-save.cmd ["mesaj"]` | Degisiklikleri commit'le |
| `git-sync.cmd` | Pull + push |
| `git-info.cmd` | Branch + status + son commit'ler |

### Diger

| Komut | Aciklama |
|---|---|
| `create-account.cmd` | Oyun hesabi olustur + GM yetkisi ver |
| `publish-patch.cmd` | Patch manifestini elle uret |
| `cleanup-project.cmd` | Build/log/gecici dosyalari temizle |

## Mimari

```
Oyuncu  --https-->  nginx (443/80)  --> panel (PHP x4)
                                    --> patch sunucusu (8091)
Oyuncu  --tcp----->  game.exe core'lari (30001, 30003-30010, 30051)
Panel   --socket-->  P2P portlari --> RELOAD / notice / kick
Tum servisler ----->  MariaDB (localhost:3306)
```

### Portlar

| Port | Servis |
|---|---|
| 80, 443 | nginx (panel + patch) |
| 30001 | Auth (client baglantisi) |
| 30003, 30005, 30007, 30009 | CH1 core 1-4 |
| 30051 | CH99 |
| 30000 | DB peer |
| 3306 | MariaDB (sadece localhost) |

### Veritabanlari

| DB | Icerik |
|---|---|
| `account` | Hesaplar, giris bilgileri |
| `common` | GM listesi, oyun ayarlari |
| `log` | Oyun loglari |
| `player` | Karakterler, envanter, drop tablolari |
| Panel DB | Panel kullanicilari, ayarlar, loglar |

## Konfigurasyyon

Tum yapilandirma `.env` dosyasindan okunur. Bu dosya:

- `setup.cmd` tarafindan otomatik olusturulur
- Git'e girmez (`.gitignore`'da)
- Sifreleri rastgele uretir
- Public IP'yi otomatik algilar

Runtime CONFIG dosyalari `.env`'den uretilir (`sync-config.ps1`).
Sunucu durdugunca sifreler `__FROM_ENV__` placeholder'ina doner.

## Patch Sistemi

1. `runtime\client\game\` icinde dosya degisir
2. `patch_watch.py` farki algilar, `runtime\patchserver\patch\files\` altina kopyalar
3. Manifest (`patchlist.json`) guncellenir, versiyon artar
4. Oyuncu `VALIANT2.exe` acar → manifest karsilastirir → sadece farklari indirir → oyunu baslatir

## Detayli Rehber

Tam teknik dokumantasyon icin: [`AGENTS.md`](AGENTS.md)
