<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class Hesap extends BaseController
{
  public $viewFolder  = "";
  public $hesapModel  = "";

  public function __construct()
  {
    $this->viewFolder = "Hesap";
    $this->hesapModel = model('Hesap_model');
    if (!session('user_id')) {
      header('Location: '.base_url('GirisYap'));
      exit;
    }
  }

  public function KullaniciAdi()
  {
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/KullaniciAdi",$viewData);
  }

  public function KullaniciAdiDegistir()
  {
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'kullaniciAdi' => ['label' => lang('Hesap.sayfa.mevcutKullaniciAdi'),'rules' => "required|min_length[2]|max_length[25]"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db      = \Config\Database::connect();
      $kontrol = $this->hesapModel->KullaniciBilgileri(session('user_id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Genel.kullaniciBulunamadi'));
      }else {
        if ($kontrol->user_name==$request->getPost('kullaniciAdi')) {
          responseResult('error',lang('Hesap.cikti.buKullaniciAdiniKullaniyorsun'));
        }
        $kullaniciAdiKontrol = $this->hesapModel->KullaniciAdiKontrol($request->getPost('kullaniciAdi'),$db);
        if ($kullaniciAdiKontrol) {
          responseResult('error',lang('Hesap.cikti.buKullaniciAdiKullaniliyor'));
        }
        $data = [
          'user_name' =>  esc($request->getPost('kullaniciAdi'))
        ];
        $result = $this->hesapModel->Guncelle($data,$kontrol->user_id,$db);
        if ($result) {
          DeleteFileCache('KullaniciBilgileri-'.session('user_id'));
          LogAdd(lang('Hesap.kayit.kullaniciAdiDegistirildi',["eski_kullanici_adi" => $kontrol->user_name,"yeni_kullanici_adi" => esc($request->getPost('kullaniciAdi'))]),'Hesap/KullaniciAdi',session('user_id'));
          session()->removeTempdata('user_role');
          session()->removeTempdata('user_id');
          session()->removeTempdata('is_admin');
          if (get_cookie(cookieKey)){
            setcookie(cookieKey,"",-1,'/','');
          }
          $alert = [
            'type' => "success",
            'text' => lang('Hesap.cikti.kullaniciAdiDegistirildi')
          ];
          session()->setFlashdata('alert',$alert);
          responseResult('success',lang('Hesap.cikti.kullaniciAdiDegistirildi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Sifre()
  {
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Sifre",$viewData);
  }

  public function SifreDegistir()
  {
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'mevcutSifre' => ['label' => lang('Hesap.sayfa.mevcutSifreniz'), 'rules' => "required|min_length[5]"],
      'yeniSifre'   => ['label' => lang('Hesap.sayfa.yeniSifreniz'),   'rules' => "required|min_length[5]"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db      = \Config\Database::connect();
      $kontrol = $this->hesapModel->KullaniciBilgileri(session('user_id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Genel.kullaniciBulunamadi'));
      }else {
        if (!password_verify($request->getPost('mevcutSifre'),$kontrol->user_password)) {
          responseResult('error',lang('Hesap.cikti.mevcutSifreHatali'));
        }
        if (password_verify($request->getPost('yeniSifre'),$kontrol->user_password)) {
          responseResult('error',lang('Hesap.cikti.buSifreyiKullaniyorsun'));
        }
        $data = [
          'user_password' =>  password_hash($request->getPost('yeniSifre'),PASSWORD_BCRYPT)
        ];
        $result = $this->hesapModel->Guncelle($data,$kontrol->user_id,$db);
        if ($result) {
          LogAdd(lang('Hesap.kayit.sifreDegistirildi'),'Hesap/Sifre',session('user_id'));
          session()->removeTempdata('user_role');
          session()->removeTempdata('user_id');
          session()->removeTempdata('is_admin');
          if (get_cookie(cookieKey)){
            setcookie(cookieKey,"",-1,'/','');
          }
          $alert = [
            'type' => "success",
            'text' => lang('Hesap.cikti.sifreDegistirildi')
          ];
          session()->setFlashdata('alert',$alert);
          responseResult('success',lang('Hesap.cikti.sifreDegistirildi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }
}
