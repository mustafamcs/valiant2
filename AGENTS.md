# VALIANT2 çalışma kuralları

- Kullanıcı teknik uygulama, bağımlılık kurulumu, yapılandırma, derleme, test ve hata düzeltmelerinde soru sorulmadan otonom ilerlenmesini ister.
- Geri döndürülemez veri silme, veritabanı DROP/toplu DELETE, force-push ve benzeri yıkıcı işlemler için yine işlem özelinde açık onay alınır.
- Bir özellik bayrağı yalnız client ve server tarafındaki bağımlılıkları birlikte doğrulandıktan sonra değiştirilir.
- `source/client/source/Controls.h` ve `source/server/source/common/Controls.h` bayrakları mümkün olduğunda aynı adla ve aynı davranışla eşleşmelidir.
- Her desteklenen özellik bayrağı hem açık hem kapalı durumda derlenebilir olmalı; paket yapıları veya ağ protokolünü etkileyen bayraklar iki tarafta aynı anda test edilmelidir.
- Değişiklik sonrası ilgili client/server derlemesi, runtime dağıtımı ve temiz `syserr` smoke testi yapılır.
- Hassas bilgiler yalnız kök `.env` dosyasında tutulur ve yanıtlarda açıklanmaz.
