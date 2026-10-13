<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class GirisYap extends BaseController
{
  public $viewFolder = "";

  public function __construct()
  {
    $this->viewFolder = "GirisYap";
  }

  public function Index()
  {
    if (session('user_id')) {
      return redirect()->to(base_url('Anasayfa/Index'));
    }
    $anasayfaModel = model('Anasayfa_model');
    $viewData['viewFolder']       = $this->viewFolder;
    $viewData['ayarSiteAdi']      = $anasayfaModel->AyarCek('siteAdi');
    $viewData['ayarFooterYazisi'] = $anasayfaModel->AyarCek('footerYazisi');
    return view("{$this->viewFolder}/Index",$viewData);
  }

  public function GirisYap()
  {
    if (session('user_id')){
      responseResult('error',lang('GirisYap.cikti.girisYapilmisLutfenSayfayiYenile'));
    }
    $validation =  \Config\Services::validation();
    $request    =  \Config\Services::request();
    $validation->setRules([
      'name'      => ['label' => lang('Genel.kullaniciAdi'),  'rules'=> "required"],
      'password'  => ['label' => lang('Genel.sifre'),         'rules'=> "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $girisYapModel  = model('Giris_yap_model');
      $db             = \Config\Database::connect();
      $dbGame         = \Config\Database::connect('metin2');
      $loginName      = $request->getPost('name');
      $loginPass      = $request->getPost('password');
      // 1) Oyun hesabini kontrol et (account.account)
      $accountRow = $girisYapModel->KontrolAccount($loginName,$dbGame);
      if (!$accountRow){
        responseResult('error',lang('GirisYap.cikti.bilgilerHatali'));
      }
      // 2) Sifre dogrulama (MySQL PASSWORD())
      if (!$girisYapModel->SifreDogrula($loginName,$loginPass,$dbGame)){
        responseResult('error',lang('GirisYap.cikti.bilgilerHatali'));
      }
      // 3) Hesap banlı mi?
      if ($accountRow->status !== 'OK'){
        responseResult('error',lang('GirisYap.cikti.hesapBanli'));
      }
      // 4) GM seviyesi IMPLEMENTOR mu? (common.gmlist)
      $gmRow = $girisYapModel->GMKontrol($loginName,$dbGame);
      if (!$gmRow){
        responseResult('error',lang('GirisYap.cikti.yetkisizGiris'));
      }
      // 5) Panel users tablosunda karsilik yoksa otomatik olustur
      $kontrol = $girisYapModel->OtoKayit($loginName,$db);
      // 6) Token + session
      $rememberMeToken = CreateToken('BeniHatirla',$db);
      if ($request->getPost('remember')){
        $data = [
          'user_token'        => $rememberMeToken,
          'user_login_date'   => date('Y-m-d H:i:s'),
          'user_end_session'  => "0",
        ];
        $girisYapModel->Guncelle($data,$kontrol->user_id,$db);
        setcookie(cookieKey,$rememberMeToken,time()+MONTH,'/','');
      }else {
        $data = [
          'user_login_date'  => date('Y-m-d H:i:s'),
          'user_end_session' => "0",
        ];
        $girisYapModel->Guncelle($data,$kontrol->user_id,$db);
      }
      session()->set('user_role',json_decode($kontrol->user_role));
      session()->set('user_id',$kontrol->user_id);
      session()->set('is_admin',true);
      $alert = [
        'type' => "success",
        'text' => lang('GirisYap.cikti.girisBasarili')
      ];
      session()->setFlashdata('alert',$alert);
      LogAdd(lang('GirisYap.kayit.girisBasarili'),'#',$kontrol->user_id);
      responseResult('success',lang('GirisYap.cikti.girisBasarili'));
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function CikisYap()
  {
    if (session('user_id')){
      LogAdd(lang('CikisYap.kayit.cikisYapildi'),'#',session('user_id'));
      session()->removeTempdata('user_role');
      session()->removeTempdata('user_id');
      session()->removeTempdata('is_admin');
      if (get_cookie(cookieKey)){
        setcookie(cookieKey,"",-1,'/','');
      }
      $alert = [
        'type' => "success",
        'text' => lang('CikisYap.cikti.cikisYapildi')
      ];
      session()->setFlashdata('alert',$alert);
      return redirect()->to(base_url('GirisYap'));
    }else {
      return redirect()->to(base_url('GirisYap'));
    }
  }
}
