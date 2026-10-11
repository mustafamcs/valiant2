# VALIANT2

Windows üzerinde client, server, quest compiler ve client pack bileşenlerini kaynak koddan oluşturan proje.

## Temiz kurulum

Windows 10/11 üzerinde PowerShell'i açın ve proje kökünde çalıştırın:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\setup.ps1
```

Kurulum yönetici izni ister ve şunları otomatik olarak gerçekleştirir:

- Git ve Git LFS kurulumu
- Visual Studio 2022 C++ Build Tools kurulumu
- 32-bit Visual C++ runtime kurulumu
- MariaDB kurulumu ve veritabanlarının hazırlanması
- Yerel `.env` oluşturulması
- Client, server ve `qc.exe` Release build'leri
- Client pack arşivlerinin oluşturulması

Gizli bilgiler içeren `.env` Git tarafından izlenmez. Yeni kurulumda güvenli yerel parolalar otomatik üretilir.

## Çalıştırma

Sunucuyu başlatmak için:

```powershell
.\scripts\windows\start-server.cmd
```

Durumu görüntülemek için:

```powershell
.\scripts\windows\status-server.cmd
```

Sunucuyu durdurmak için:

```powershell
.\scripts\windows\stop-server.cmd
```

Client launcher:

```text
runtime\client\VALIANT2.exe
```

Launcher üzerinden oyun başlatılabilir ve client ayarları açılabilir. Tüm oyun dosyaları düzenli biçimde `runtime\client\game\` altında tutulur. Ayar aracı `metin2.cfg` içindeki tüm client ayarlarını düzenler ve her build sırasında kaynak koddan yeniden üretilir.

## Yeniden build

Tüm Release hedefleri ve pack'ler:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\windows\build-all.ps1
```

Tek bir pack:

```powershell
.\scripts\windows\build-client-packs.cmd root
```

Build çıktıları GitHub'a yüklenmez. Client, server, QC ve pack çıktıları kurulum sırasında doğrudan ilgili runtime klasörlerinde üretilir.
