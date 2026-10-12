<?php
if (WebTitle('Anasayfa')) {
  echo lang('Anasayfa.sayfa.anasayfa');
}else if (WebTitle('IslemKayitlari') && !WebTitle('Kullanicilar')) {
  echo lang('IslemKayitlari.sayfa.islemKayitlari');
}else if (WebTitle('Ayarlar') && WebTitle('LogoYukle')) {
  echo lang('Ayarlar.sayfa.logoYukle').' - '.lang('Ayarlar.sayfa.ayarlar');
}else if (WebTitle('Ayarlar') && WebTitle('FaviconYukle')) {
  echo lang('Ayarlar.sayfa.faviconYukle').' - '.lang('Ayarlar.sayfa.ayarlar');
}else if (WebTitle('Ayarlar') && WebTitle('Site')) {
  echo lang('Ayarlar.sayfa.siteAyarlari').' - '.lang('Ayarlar.sayfa.ayarlar');
}else if (WebTitle('Ayarlar') && WebTitle('Javascript')) {
  echo lang('Ayarlar.sayfa.javascriptKodlari').' - '.lang('Ayarlar.sayfa.ayarlar');
}else if (WebTitle('Ayarlar') && WebTitle('SMTP')) {
  echo lang('Ayarlar.sayfa.smtpAyarlari').' - '.lang('Ayarlar.sayfa.ayarlar');
}else if (WebTitle('Ayarlar') && WebTitle('P2P')) {
  echo lang('Ayarlar.sayfa.p2pAyarlari').' - '.lang('Ayarlar.sayfa.ayarlar');
}else if (WebTitle('Ayarlar') && WebTitle('Ikon')) {
  echo lang('Ayarlar.sayfa.ikonAyarlari').' - '.lang('Ayarlar.sayfa.ayarlar');
}else if (WebTitle('Hesap') && WebTitle('KullaniciAdi')) {
  echo lang('Hesap.sayfa.kullaniciAdi').' - '.lang('Hesap.sayfa.hesabim');
}else if (WebTitle('Hesap') && WebTitle('Sifre')) {
  echo lang('Hesap.sayfa.sifre').' - '.lang('Hesap.sayfa.hesabim');
}else if (WebTitle('Kullanicilar') && WebTitle('Ekle')) {
  echo lang('Genel.ekle').' - '.lang('Kullanicilar.sayfa.kullanicilar');
}else if (WebTitle('Kullanicilar') && WebTitle('Detay')) {
  echo lang('Kullanicilar.sayfa.kullaniciDetayi',['user_name' => $kullaniciBilgileri->user_name]).' - '.lang('Kullanicilar.sayfa.kullanicilar');
}else if (WebTitle('Kullanicilar') && WebTitle('KullaniciAdi')) {
  echo lang('Hesap.sayfa.kullaniciAdi').' - '.lang('Kullanicilar.sayfa.kullaniciDetayi',['user_name' => $kullaniciBilgileri->user_name]).' - '.lang('Kullanicilar.sayfa.kullanicilar');
}else if (WebTitle('Kullanicilar') && WebTitle('Sifre')) {
  echo lang('Hesap.sayfa.sifre').' - '.lang('Kullanicilar.sayfa.kullaniciDetayi',['user_name' => $kullaniciBilgileri->user_name]).' - '.lang('Kullanicilar.sayfa.kullanicilar');
}else if (WebTitle('Kullanicilar') && WebTitle('Yetkilendirme')) {
  echo lang('Kullanicilar.sayfa.yetkilendirme').' - '.lang('Kullanicilar.sayfa.kullaniciDetayi',['user_name' => $kullaniciBilgileri->user_name]).' - '.lang('Kullanicilar.sayfa.kullanicilar');
}else if (WebTitle('Kullanicilar') && WebTitle('Sil')) {
  echo lang('Genel.sil').' - '.lang('Kullanicilar.sayfa.kullaniciDetayi',['user_name' => $kullaniciBilgileri->user_name]).' - '.lang('Kullanicilar.sayfa.kullanicilar');
}else if (WebTitle('Kullanicilar') && WebTitle('IslemKayitlari')) {
  echo lang('IslemKayitlari.sayfa.islemKayitlari').' - '.lang('Kullanicilar.sayfa.kullaniciDetayi',['user_name' => $kullaniciBilgileri->user_name]).' - '.lang('Kullanicilar.sayfa.kullanicilar');
}else if (WebTitle('Kullanicilar')) {
  echo lang('Kullanicilar.sayfa.kullanicilar');
}else if (WebTitle('Efsun') && WebTitle('Index')) {
  echo lang('Efsun.sayfa.efsunAyarlari').' - '.lang('Efsun.sayfa.efsun');
}else if (WebTitle('Efsun') && WebTitle('Nadir')) {
  echo lang('Efsun.sayfa.nadirEfsunAyarlari').' - '.lang('Efsun.sayfa.efsun');
}else if (WebTitle('Yukseltme')) {
  echo lang('Yukseltme.sayfa.yukseltme');
}else if (WebTitle('Kayitlar') && WebTitle('Boot')) {
  echo lang('Kayitlar.sayfa.bootKayitlari').' - '.lang('Kayitlar.sayfa.kayitlar');
}else if (WebTitle('Kayitlar') && WebTitle('GM')) {
  echo lang('Kayitlar.sayfa.gmKomutKayitlari').' - '.lang('Kayitlar.sayfa.kayitlar');
}else if (WebTitle('Kayitlar') && WebTitle('NesneMarket')) {
  echo lang('Kayitlar.sayfa.nesneMarketKayitlari').' - '.lang('Kayitlar.sayfa.kayitlar');
}else if (WebTitle('Kayitlar') && WebTitle('Level')) {
  echo lang('Kayitlar.sayfa.levelKayitlari').' - '.lang('Kayitlar.sayfa.kayitlar');
}else if (WebTitle('Kayitlar') && WebTitle('Pazar')) {
  echo lang('Kayitlar.sayfa.pazarKayitlari').' - '.lang('Kayitlar.sayfa.kayitlar');
}else if (WebTitle('GM')) {
  echo lang('GM.sayfa.gm');
}else if (WebTitle('VeriIslemleri') && WebTitle('Harita')) {
  echo lang('VeriIslemleri.sayfa.haritaIsimleri').' - '.lang('VeriIslemleri.sayfa.veriIslemleri');
}else if (WebTitle('VeriIslemleri') && WebTitle('Text')) {
  echo lang('VeriIslemleri.sayfa.efsunIsimleriText').' - '.lang('VeriIslemleri.sayfa.veriIslemleri');
}else if (WebTitle('VeriIslemleri') && WebTitle('ID')) {
  echo lang('VeriIslemleri.sayfa.efsunIsimleriID').' - '.lang('VeriIslemleri.sayfa.veriIslemleri');
}else if (WebTitle('Esya') && WebTitle('Index')) {
  echo lang('Esya.sayfa.esyalar').' - '.lang('Esya.sayfa.esyaYonetimi');
}else if (WebTitle('Esya') && WebTitle('Ara')) {
  echo lang('Esya.sayfa.ara').' - '.lang('Esya.sayfa.esyaYonetimi');
}else if (WebTitle('Oyuncu') && WebTitle('Karakter') && isset($karakterDetay->name)) {
  echo lang('Oyuncu.sayfa.karakterDetay',['name' => $karakterDetay->name]).' - '.lang('Oyuncu.sayfa.oyuncuYonetimi');
}else if (WebTitle('Oyuncu') && WebTitle('Detay') && isset($oyuncuDetay->login)) {
  echo lang('Oyuncu.sayfa.oyuncuDetay',['login' => $oyuncuDetay->login]).' - '.lang('Oyuncu.sayfa.oyuncuYonetimi');
}else if (WebTitle('Canavar') && WebTitle('Index')) {
  echo lang('Canavar.sayfa.canavarlar').' - '.lang('Canavar.sayfa.canavar');
}else if (WebTitle('Balikcilik')) {
  echo lang('Balikcilik.sayfa.balikcilik');
}else if (WebTitle('Cark')) {
  echo lang('Cark.sayfa.cark');
}else if (WebTitle('Biyolog')) {
  echo lang('Biyolog.sayfa.biyolog');
}else if (WebTitle('NPC')) {
  echo lang('NPC.sayfa.npc');
}else if (WebTitle('NesneMarket') && WebTitle('Index')) {
  echo lang('NesneMarket.sayfa.nesneMarketEsya').' - '.lang('NesneMarket.sayfa.nesneMarket');
}else if (WebTitle('NesneMarket') && WebTitle('Kategori')) {
  echo lang('NesneMarket.sayfa.kategoriler').' - '.lang('NesneMarket.sayfa.nesneMarket');
}else {
  echo lang('Hata.sayfaBulunamadi');
}
?>
