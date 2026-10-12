<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class Kullanicilar extends BaseController
{
  public $viewFolder    = "";
  public $kullaniciModel     = "";

  public function __construct()
  {
    $this->viewFolder = "Kullanicilar";
    $this->kullaniciModel = model('Kullanici_model');
    if (!session('user_id')) {
      header('Location: '.base_url('GirisYap'));
      exit;
    }
  }

  public function Index()
  {
    if (!IsAllowedViewModule('kullanicilariGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Index",$viewData);
  }

  public function Ajax()
  {
    if (!IsAllowedViewModule('kullanicilariGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect();
    $request  = \Config\Services::request();
    $siralama = ['user_id','user_name','user_status','user_login_date'];
    if ($request->getPost('search[value]')) {
      if ($request->getPost('user_status')!="") {
        $yaz = $this->kullaniciModel->AjaxAraFiltreleDurum($request->getPost('user_status'),$request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
      }else {
        $yaz = $this->kullaniciModel->AjaxAra($request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
      }
    }else{
      if ($request->getPost('user_status')!="") {
        $yaz = $this->kullaniciModel->AjaxFiltreleDurum($request->getPost('user_status'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
      }else {
        $yaz = $this->kullaniciModel->Ajax($request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
      }
    }
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->user_id;
      $sub_array[] = $value->user_name;
      $sub_array[] = '<label class="form-check form-switch status_update" style="margin-top:2px;" data-id="'.$value->user_id.'"><input class="form-check-input" style="background-size: 1.5rem;" type="checkbox" '.($value->user_status=="1"?'checked':false).'></label>';
      $sub_array[] = DateDMYHM($value->user_login_date)?DateDMYHM($value->user_login_date):lang('Kullanicilar.sayfa.girisYapilmadi');
      if (IsAllowedViewModule('kullaniciDetayiniGorebilsin')) {
        $sub_array[] = '<a class="btn btn-primary pt-1 pb-1 ps-2 pe-2" href="'.base_url('Kullanicilar/Detay/'.$value->user_id).'">
        <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" style="width:25px;height:25px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 7h-3a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-3" /><path d="M9 15h3l8.5 -8.5a1.5 1.5 0 0 0 -3 -3l-8.5 8.5v3" /><line x1="16" y1="5" x2="19" y2="8" /></svg>
        </a>';
      }
      $data[] = $sub_array;
    }
    $output = array(
      "draw"            =>  intval($_POST["draw"]),
      "recordsFiltered" =>  (count($yaz)==$request->getPost('length')?$request->getPost('start')+$request->getPost('length')+1:0),
      "data"            =>  $data
    );
    echo json_encode($output, JSON_INVALID_UTF8_SUBSTITUTE);
    exit;
  }

  public function Durum()
  {
    if (!IsAllowedViewModule('kullaniciDurumunuGuncelleyebilsin')) {
      responseResult('error',lang('Genel.yetkinYok'));
    }
    $validation =  \Config\Services::validation();
    $request    =  \Config\Services::request();
    $validation->setRules([
      'id' => ['rules'=> "required|integer"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db               = \Config\Database::connect();
      $kullaniciKontrol = $this->kullaniciModel->Kontrol($request->getPost('id'),$db);
      if (!$kullaniciKontrol) {
        responseResult('error',lang('Kullanicilar.cikti.boyleBirKullaniciYok'));
      }else {
        if ($kullaniciKontrol->user_rank=="9") {
          responseResult('error',lang('Kullanicilar.cikti.buKullaniciUzerindeIslemYapilamaz'));
        }
        if ($kullaniciKontrol->user_id==session('user_id')) {
          responseResult('error',lang('Kullanicilar.cikti.kendiUzerindeIslemYapamazsin'));
        }
        if ($kullaniciKontrol->user_status=="1") {
          $user_status = "0";
          $text = lang('Kullanicilar.kayit.kullaniciDurumPasif',['user_name' => $kullaniciKontrol->user_name]);
        }else {
          $user_status = "1";
          $text = lang('Kullanicilar.kayit.kullaniciDurumAktif',['user_name' => $kullaniciKontrol->user_name]);
        }
        $data = [
          'user_status' => $user_status,
        ];
        $response = $this->kullaniciModel->Guncelle($data,$kullaniciKontrol->user_id,$db);
        if ($response) {
          DeleteFileCache('KullaniciBilgileri-'.$kullaniciKontrol->user_id);
          LogAdd($text,'Kullanicilar/Index',session('user_id'));
          responseResult('success',$text);
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Ekle()
  {
    if (!IsAllowedViewModule('kullaniciEkleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Ekle",$viewData);
  }

  public function KullaniciEkle()
  {
    if (!IsAllowedViewModule('kullaniciEkleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'name'      => ['label' => lang('Genel.kullaniciAdi'),  'rules' => "required|min_length[2]"],
      'password'  => ['label' => lang('Genel.label.sifre'),   'rules' => "required|min_length[5]"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db      = \Config\Database::connect();
      $kontrol = $this->kullaniciModel->KullaniciAdiKontrol($request->getPost('name'),$db);
      if ($kontrol) {
        responseResult('error',lang('Hesap.cikti.buKullaniciAdiKullaniliyor'));
      }else {
        $data = [
          'user_name'         =>  $request->getPost('name'),
          'user_password'     =>  password_hash($request->getPost('password'),PASSWORD_BCRYPT),
          'user_rank'         =>  "1",
          'user_create_date'  =>  date('Y-m-d H:i:s'),
        ];
        $result = $this->kullaniciModel->Ekle($data,$db);
        if ($result) {
          $insertId = $db->insertID();
          LogAdd(lang('Kullanicilar.kayit.kullaniciEklendi',['user_name' => $request->getPost('name')]),'Kullanicilar/Ekle',session('user_id'));
          $response['url'] = base_url('Kullanicilar/Detay/'.$insertId);
          $alert = [
            'type' => "success",
            'text' => lang('Kullanicilar.cikti.kullaniciEklendi')
          ];
          session()->setFlashdata('alert',$alert);
          responseResult('success',lang('Kullanicilar.cikti.kullaniciEklendi'),$response);
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Detay($id=0)
  {
    if (!IsAllowedViewModule('kullaniciDetayiniGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db               = \Config\Database::connect();
    $kullaniciKontrol = $this->kullaniciModel->Kontrol($id,$db);
    if (!$kullaniciKontrol) {
      return redirect()->to(base_url('Hata'));
    }else {
      $viewData['kullaniciBilgileri'] = $kullaniciKontrol;
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Detay",$viewData);
  }

  public function KullaniciAdi($id=0)
  {
    if (!IsAllowedViewModule('kullaniciAdiniDegistirebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db               = \Config\Database::connect();
    $kullaniciKontrol = $this->kullaniciModel->Kontrol($id,$db);
    if (!$kullaniciKontrol) {
      return redirect()->to(base_url('Hata'));
    }else {
      $viewData['kullaniciBilgileri'] = $kullaniciKontrol;
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/KullaniciAdi",$viewData);
  }

  public function KullaniciAdiDegistir()
  {
    if (!IsAllowedViewModule('kullaniciAdiniDegistirebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'name' => ['label' => lang('Hesap.sayfa.kullaniciAdi'),'rules' => "required|min_length[2]|max_length[25]"],
      'id'   => ['label' => lang('Hesap.sayfa.kullaniciAdi'),'rules' => "required|integer|greater_than[0]"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db               = \Config\Database::connect();
      $kullaniciKontrol = $this->kullaniciModel->Kontrol($request->getPost('id'),$db);
      if (!$kullaniciKontrol) {
        responseResult('error',lang('Genel.kullaniciBulunamadi'));
      }else if ($kullaniciKontrol->user_rank=="9") {
        responseResult('error',lang('Kullanicilar.cikti.buKullaniciUzerindeIslemYapilamaz'));
      }else {
        if ($kullaniciKontrol->user_name==$request->getPost('name')) {
          responseResult('error',lang('Kullanicilar.cikti.buKullaniciAdiniKullaniyorsun'));
        }
        $kullaniciAdiKontrol = $this->kullaniciModel->KullaniciAdiKontrol($request->getPost('name'),$db);
        if ($kullaniciAdiKontrol) {
          responseResult('error',lang('Hesap.cikti.buKullaniciAdiKullaniliyor'));
        }
        $data = [
          'user_name' =>  esc($request->getPost('name'))
        ];
        $result = $this->kullaniciModel->Guncelle($data,$kullaniciKontrol->user_id,$db);
        if ($result) {
          DeleteFileCache('KullaniciBilgileri-'.$kullaniciKontrol->user_id);
          LogAdd(lang('Kullanicilar.kayit.kullaniciAdiDegistirildi',['user_name' => $kullaniciKontrol->user_name,'user_id' => $kullaniciKontrol->user_id,'eski_kullanici_adi' => $kullaniciKontrol->user_name,'yeni_kullanici_adi' => esc($request->getPost('name'))]),'Kullanicilar/KullaniciAdi/'.$kullaniciKontrol->user_id,session('user_id'));
          responseResult('success',lang('Kullanicilar.cikti.kullaniciAdiDegistirildi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Sifre($id=0)
  {
    if (!IsAllowedViewModule('kullaniciSifreDegistirebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db               = \Config\Database::connect();
    $kullaniciKontrol = $this->kullaniciModel->Kontrol($id,$db);
    if (!$kullaniciKontrol) {
      return redirect()->to(base_url('Hata'));
    }else {
      $viewData['kullaniciBilgileri'] = $kullaniciKontrol;
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Sifre",$viewData);
  }

  public function SifreDegistir()
  {
    if (!IsAllowedViewModule('kullaniciSifreDegistirebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'password'  => ['label' => lang('Hesap.sayfa.sifre'),  'rules' => "required|min_length[5]"],
      'id'        => ['label' => lang('Hesap.sayfa.sifre'), 'rules' => "required|integer|greater_than[0]"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db               = \Config\Database::connect();
      $kullaniciKontrol = $this->kullaniciModel->Kontrol($request->getPost('id'),$db);
      if (!$kullaniciKontrol) {
        responseResult('error',lang('Genel.kullaniciBulunamadi'));
      }else if ($kullaniciKontrol->user_rank=="9") {
        responseResult('error',lang('Kullanicilar.cikti.buKullaniciUzerindeIslemYapilamaz'));
      }else {
        $data = [
          'user_password'  =>  password_hash($request->getPost('password'),PASSWORD_BCRYPT)
        ];
        $result = $this->kullaniciModel->Guncelle($data,$kullaniciKontrol->user_id,$db);
        if ($result) {
          DeleteFileCache('KullaniciBilgileri-'.$kullaniciKontrol->user_id);
          LogAdd(lang('Kullanicilar.kayit.sifreDegistirildi',['user_name' => $kullaniciKontrol->user_name,'user_id' => $kullaniciKontrol->user_id]),'Kullanicilar/Sifre/'.$kullaniciKontrol->user_id,session('user_id'));
          responseResult('success',lang('Kullanicilar.cikti.sifreDegistirildi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Yetkilendirme($id=0)
  {
    if (!IsAllowedViewModule('kullaniciYetkiVerebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db               = \Config\Database::connect();
    $kullaniciKontrol = $this->kullaniciModel->Kontrol($id,$db);
    if (!$kullaniciKontrol) {
      return redirect()->to(base_url('Hata'));
    }else {
      $viewData['kullaniciBilgileri'] = $kullaniciKontrol;
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    $yetkiler               = json_decode($kullaniciKontrol->user_role);
    $viewData['yetkiler']   = [
      'genel'           =>  [
        'onBellekTemizleyebilsin'             => (!empty($yetkiler->onBellekTemizleyebilsin)?true:false),
        'anasayfaOnlineGorebilsin'            => (!empty($yetkiler->anasayfaOnlineGorebilsin)?true:false),
      ],
      'islemKayitlari'  =>  [
        'tumBildirimleriGorebilsin'           => (!empty($yetkiler->tumBildirimleriGorebilsin)?true:false),
      ],
      'kullanicilar'  =>  [
        'kullanicilariGorebilsin'                 => (!empty($yetkiler->kullanicilariGorebilsin)?true:false),
        'kullaniciEkleyebilsin'                   => (!empty($yetkiler->kullaniciEkleyebilsin)?true:false),
        'kullaniciDurumunuGuncelleyebilsin'       => (!empty($yetkiler->kullaniciDurumunuGuncelleyebilsin)?true:false),
        'kullaniciDetayiniGorebilsin'             => (!empty($yetkiler->kullaniciDetayiniGorebilsin)?true:false),
        'kullaniciAdiniDegistirebilsin'           => (!empty($yetkiler->kullaniciAdiniDegistirebilsin)?true:false),
        'kullaniciSifreDegistirebilsin'           => (!empty($yetkiler->kullaniciSifreDegistirebilsin)?true:false),
        'kullaniciYetkiVerebilsin'                => (!empty($yetkiler->kullaniciYetkiVerebilsin)?true:false),
        'kullaniciyiSilebilsin'                   => (!empty($yetkiler->kullaniciyiSilebilsin)?true:false),
        'kullaniciOturumunuSonlandırabilsin'      => (!empty($yetkiler->kullaniciOturumunuSonlandırabilsin)?true:false),
        'kullaniciIslemKayitlariniGorebilsin'     => (!empty($yetkiler->kullaniciIslemKayitlariniGorebilsin)?true:false),
      ],
      'ayarlar' =>  [
        'logoyuGuncelleyebilsin'                => (!empty($yetkiler->logoyuGuncelleyebilsin)?true:false),
        'faviconGuncelleyebilsin'               => (!empty($yetkiler->faviconGuncelleyebilsin)?true:false),
        'siteAyarlariniGuncelleyebilsin'        => (!empty($yetkiler->siteAyarlariniGuncelleyebilsin)?true:false),
        'javascriptKodlariniGuncelleyebilsin'   => (!empty($yetkiler->javascriptKodlariniGuncelleyebilsin)?true:false),
        'smtpAyarlariniGuncelleyebilsin'        => (!empty($yetkiler->smtpAyarlariniGuncelleyebilsin)?true:false),
        'p2pAyarlariGuncelleyebilsin'           => (!empty($yetkiler->p2pAyarlariGuncelleyebilsin)?true:false),
        'ikonAyarlariGuncelleyebilsin'          => (!empty($yetkiler->ikonAyarlariGuncelleyebilsin)?true:false),
      ],
      'gm' =>  [
        'gmGorebilsin'                          => (!empty($yetkiler->gmGorebilsin)?true:false),
        'gmEkleyebilsin'                        => (!empty($yetkiler->gmEkleyebilsin)?true:false),
        'gmDuzenleyebilsin'                     => (!empty($yetkiler->gmDuzenleyebilsin)?true:false),
        'gmSilebilsin'                          => (!empty($yetkiler->gmSilebilsin)?true:false),
      ],
      'efsun' =>  [
        'efsunlariGorebilsin'                   => (!empty($yetkiler->efsunlariGorebilsin)?true:false),
        'nadirEfsunlariGorebilsin'              => (!empty($yetkiler->nadirEfsunlariGorebilsin)?true:false),
        'efsunDuzenleyebilsin'                  => (!empty($yetkiler->efsunDuzenleyebilsin)?true:false),
        'nadirEfsunDuzenleyebilsin'             => (!empty($yetkiler->nadirEfsunDuzenleyebilsin)?true:false),
      ],
      'yukseltme' =>  [
        'yukseltmeGorebilsin'                   => (!empty($yetkiler->yukseltmeGorebilsin)?true:false),
        'yukseltmeEkleyebilsin'                 => (!empty($yetkiler->yukseltmeEkleyebilsin)?true:false),
        'yukseltmeDuzenleyebilsin'              => (!empty($yetkiler->yukseltmeDuzenleyebilsin)?true:false),
        'yukseltmeSilebilsin'                   => (!empty($yetkiler->yukseltmeSilebilsin)?true:false),
      ],
      'veriIslemleri' =>  [
        'efsunIsimGorebilsin'                   => (!empty($yetkiler->efsunIsimGorebilsin)?true:false),
        'efsunIsimEkleyebilsin'                 => (!empty($yetkiler->efsunIsimEkleyebilsin)?true:false),
        'efsunIsimDuzenleyebilsin'              => (!empty($yetkiler->efsunIsimDuzenleyebilsin)?true:false),
        'efsunIsimSilebilsin'                   => (!empty($yetkiler->efsunIsimSilebilsin)?true:false),
        'haritaIsimGorebilsin'                  => (!empty($yetkiler->haritaIsimGorebilsin)?true:false),
        'haritaIsimEkleyebilsin'                => (!empty($yetkiler->haritaIsimEkleyebilsin)?true:false),
        'haritaIsimDuzenleyebilsin'             => (!empty($yetkiler->haritaIsimDuzenleyebilsin)?true:false),
        'haritaIsimSilebilsin'                  => (!empty($yetkiler->haritaIsimSilebilsin)?true:false),
      ],
      'esya' =>  [
        'esyaGorebilsin'                        => (!empty($yetkiler->esyaGorebilsin)?true:false),
        'esyaDuzenleyebilsin'                   => (!empty($yetkiler->esyaDuzenleyebilsin)?true:false),
        'esyaArayabilsin'                       => (!empty($yetkiler->esyaArayabilsin)?true:false),
      ],
      'canavar' =>  [
        'canavarGorebilsin'                     => (!empty($yetkiler->canavarGorebilsin)?true:false),
        'canavarDuzenleyebilsin'                => (!empty($yetkiler->canavarDuzenleyebilsin)?true:false),
      ],
      'oyuncu' =>  [
        'oyuncuArayabilsin'                     => (!empty($yetkiler->oyuncuArayabilsin)?true:false),
        'oyuncuEpostaDegistirebilsin'           => (!empty($yetkiler->oyuncuEpostaDegistirebilsin)?true:false),
        'oyuncuTelefonDegistirebilsin'          => (!empty($yetkiler->oyuncuTelefonDegistirebilsin)?true:false),
        'oyuncuSifreDegistirebilsin'            => (!empty($yetkiler->oyuncuSifreDegistirebilsin)?true:false),
        'oyuncuBayrakDegistirebilsin'           => (!empty($yetkiler->oyuncuBayrakDegistirebilsin)?true:false),
        'oyuncuBanlayabilsin'                   => (!empty($yetkiler->oyuncuBanlayabilsin)?true:false),
        'oyuncuAcabilsin'                       => (!empty($yetkiler->oyuncuAcabilsin)?true:false),
        'oyuncuNesneMarketKayitGorebilsin'      => (!empty($yetkiler->oyuncuNesneMarketKayitGorebilsin)?true:false),
        'oyuncuPazarKayitGorebilsin'            => (!empty($yetkiler->oyuncuPazarKayitGorebilsin)?true:false),
        'karakterDetayGorebilsin'               => (!empty($yetkiler->karakterDetayGorebilsin)?true:false),
        'karakteKurtarabilsin'                  => (!empty($yetkiler->karakteKurtarabilsin)?true:false),
        'karakterOyundanDusursun'               => (!empty($yetkiler->karakterOyundanDusursun)?true:false),
        'karakterEsyaGonderebilsin'             => (!empty($yetkiler->karakterEsyaGonderebilsin)?true:false),
        'karakterGenelKayitGorebilsin'          => (!empty($yetkiler->karakterGenelKayitGorebilsin)?true:false),
        'envanterGorebilsin'                    => (!empty($yetkiler->envanterGorebilsin)?true:false),
      ],
      'kayitlar' =>  [
        'bootKayitGorebilsin'                   => (!empty($yetkiler->bootKayitGorebilsin)?true:false),
        'gmKomutKayitGorebilsin'                => (!empty($yetkiler->gmKomutKayitGorebilsin)?true:false),
        'nesneKayitlariGorebilsin'              => (!empty($yetkiler->nesneKayitlariGorebilsin)?true:false),
        'levelKayitlariGorebilsin'              => (!empty($yetkiler->levelKayitlariGorebilsin)?true:false),
        'pazarKayitlariGorebilsin'              => (!empty($yetkiler->pazarKayitlariGorebilsin)?true:false),
      ],
      'balikcilik' =>  [
        'balikcilikGorebilsin'                  => (!empty($yetkiler->balikcilikGorebilsin)?true:false),
        'balikcilikEkleyebilsin'                => (!empty($yetkiler->balikcilikEkleyebilsin)?true:false),
        'balikcilikDuzenleyebilsin'             => (!empty($yetkiler->balikcilikDuzenleyebilsin)?true:false),
        'balikcilikSilebilsin'                  => (!empty($yetkiler->balikcilikSilebilsin)?true:false),
      ],
      'cark' =>  [
        'carkGorebilsin'                        => (!empty($yetkiler->carkGorebilsin)?true:false),
        'carkEkleyebilsin'                      => (!empty($yetkiler->carkEkleyebilsin)?true:false),
        'carkDuzenleyebilsin'                   => (!empty($yetkiler->carkDuzenleyebilsin)?true:false),
        'carkSilebilsin'                        => (!empty($yetkiler->carkSilebilsin)?true:false),
      ],
      'biyolog' =>  [
        'biyologGorebilsin'                     => (!empty($yetkiler->biyologGorebilsin)?true:false),
        'biyologEkleyebilsin'                   => (!empty($yetkiler->biyologEkleyebilsin)?true:false),
        'biyologDuzenleyebilsin'                => (!empty($yetkiler->biyologDuzenleyebilsin)?true:false),
        'biyologSilebilsin'                     => (!empty($yetkiler->biyologSilebilsin)?true:false),
      ],
      'npc' =>  [
        'npcGorebilsin'                         => (!empty($yetkiler->npcGorebilsin)?true:false),
        'npcEkleyebilsin'                       => (!empty($yetkiler->npcEkleyebilsin)?true:false),
        'npcDuzenleyebilsin'                    => (!empty($yetkiler->npcDuzenleyebilsin)?true:false),
        'npcSilebilsin'                         => (!empty($yetkiler->npcSilebilsin)?true:false),
      ],
      'patch' =>  [
        'patchGorebilsin'                       => (!empty($yetkiler->patchGorebilsin)?true:false),
        'patchEkleyebilsin'                    => (!empty($yetkiler->patchEkleyebilsin)?true:false),
        'patchSilebilsin'                      => (!empty($yetkiler->patchSilebilsin)?true:false),
      ],
      'sandik' =>  [
        'sandikGorebilsin'                      => (!empty($yetkiler->sandikGorebilsin)?true:false),
        'sandikEkleyebilsin'                    => (!empty($yetkiler->sandikEkleyebilsin)?true:false),
        'sandikDuzenleyebilsin'                 => (!empty($yetkiler->sandikDuzenleyebilsin)?true:false),
        'sandikSilebilsin'                      => (!empty($yetkiler->sandikSilebilsin)?true:false),
      ],
      'nesneMarket' =>  [
        'nesneMarketKategoriGorebilsin'         => (!empty($yetkiler->nesneMarketKategoriGorebilsin)?true:false),
        'nesneMarketKategoriEkleyebilsin'       => (!empty($yetkiler->nesneMarketKategoriEkleyebilsin)?true:false),
        'nesneMarketKategoriDuzenleyebilsin'    => (!empty($yetkiler->nesneMarketKategoriDuzenleyebilsin)?true:false),
        'nesneMarketKategoriSilebilsin'         => (!empty($yetkiler->nesneMarketKategoriSilebilsin)?true:false),
        'nesneMarketEsyaGorebilsin'             => (!empty($yetkiler->nesneMarketEsyaGorebilsin)?true:false),
        'nesneMarketEsyaEkleyebilsin'           => (!empty($yetkiler->nesneMarketEsyaEkleyebilsin)?true:false),
        'nesneMarketEsyaDuzenleyebilsin'        => (!empty($yetkiler->nesneMarketEsyaDuzenleyebilsin)?true:false),
        'nesneMarketEsyaSilebilsin'             => (!empty($yetkiler->nesneMarketEsyaSilebilsin)?true:false),
      ],
    ];
    return view("{$this->viewFolder}/Yetkilendirme",$viewData);
  }

  public function YetkiGuncelle()
  {
    if (!IsAllowedViewModule('kullaniciYetkiVerebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'id'  => ['label' => lang('Kullanicilar.sayfa.yetkiTipi'), 'rules' => "required|integer|greater_than[0]"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db               = \Config\Database::connect();
      $kullaniciKontrol = $this->kullaniciModel->Kontrol($request->getPost('id'),$db);
      if (!$kullaniciKontrol) {
        responseResult('error',lang('Genel.kullaniciBulunamadi'));
      }else if ($kullaniciKontrol->user_rank=="9") {
        responseResult('error',lang('Kullanicilar.cikti.buKullaniciUzerindeIslemYapilamaz'));
      }else if ($kullaniciKontrol->user_id==session('user_id')) {
        responseResult('error',lang('Kullanicilar.cikti.kendiUzerindeIslemYapamazsin'));
      }else {
        $data = [
          'user_role' =>  json_encode($request->getPost('yetkiler')),
        ];
        $result = $this->kullaniciModel->Guncelle($data,$kullaniciKontrol->user_id,$db);
        if ($result) {
          DeleteFileCache('KullaniciBilgileri-'.$kullaniciKontrol->user_id);
          LogAdd(lang('Kullanicilar.kayit.yetkiGuncellendi',['user_name' => $kullaniciKontrol->user_name,'user_id' => $kullaniciKontrol->user_id]),'Kullanicilar/Yetkilendirme/'.$kullaniciKontrol->user_id,session('user_id'));
          responseResult('success',lang('Kullanicilar.cikti.yetkiGuncellendi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Sil($id=0)
  {
    if (!IsAllowedViewModule('kullaniciyiSilebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db               = \Config\Database::connect();
    $kullaniciKontrol = $this->kullaniciModel->Kontrol($id,$db);
    if (!$kullaniciKontrol) {
      return redirect()->to(base_url('Hata'));
    }else {
      $viewData['kullaniciBilgileri'] = $kullaniciKontrol;
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Sil",$viewData);
  }

  public function KullaniciSil()
  {
    if (!IsAllowedViewModule('kullaniciyiSilebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'onayYazisi'  => ['label' => lang('Hesap.sayfa.onayYazisi'), 'rules' => "required"],
      'id'          => ['label' => lang('Hesap.sayfa.onayYazisi'), 'rules' => "required|integer|greater_than[0]"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db               = \Config\Database::connect();
      $kullaniciKontrol = $this->kullaniciModel->Kontrol($request->getPost('id'),$db);
      if (!$kullaniciKontrol) {
        responseResult('error',lang('Genel.kullaniciBulunamadi'));
      }else if ($kullaniciKontrol->user_rank=="9") {
        responseResult('error',lang('Kullanicilar.cikti.buKullaniciUzerindeIslemYapilamaz'));
      }else if ($kullaniciKontrol->user_id==session('user_id')) {
        responseResult('error',lang('Kullanicilar.cikti.kendiUzerindeIslemYapamazsin'));
      }else if ($request->getPost('onayYazisi')!=$kullaniciKontrol->user_name." hesabını sil") {
        responseResult('error',lang('Kullanicilar.cikti.onayYazisiHatali'));
      }else {
        $result = $this->kullaniciModel->Sil($kullaniciKontrol->user_id,$db);
        if ($result) {
          DeleteFileCache('KullaniciBilgileri-'.$kullaniciKontrol->user_id);
          LogAdd(lang('Kullanicilar.kayit.kullaniciSilindi',['user_name' => $kullaniciKontrol->user_name,'user_id' => $kullaniciKontrol->user_id]),'Kullanicilar/Sil/'.$kullaniciKontrol->user_id,session('user_id'));
          $alert = [
            'type' => "success",
            'text' => lang('Kullanicilar.cikti.kullaniciSilindi')
          ];
          session()->setFlashdata('alert',$alert);
          responseResult('success',lang('Kullanicilar.cikti.kullaniciSilindi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function OturumuSonlandir()
  {
    if (!IsAllowedViewModule('kullaniciOturumunuSonlandırabilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'userId' => ['label' => lang('Hesap.sayfa.kullaniciAdi'),'rules' => "required|integer|greater_than[0]"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db               = \Config\Database::connect();
      $kullaniciKontrol = $this->kullaniciModel->Kontrol($request->getPost('userId'),$db);
      if (!$kullaniciKontrol) {
        responseResult('error',lang('Genel.kullaniciBulunamadi'));
      }else if ($kullaniciKontrol->user_rank=="9") {
        responseResult('error',lang('Kullanicilar.cikti.buKullaniciUzerindeIslemYapilamaz'));
      }else if ($kullaniciKontrol->user_id==session('user_id')) {
        responseResult('error',lang('Kullanicilar.cikti.kendiUzerindeIslemYapamazsin'));
      }else {
        $data = [
          'user_end_session'  =>  "1"
        ];
        $result = $this->kullaniciModel->Guncelle($data,$kullaniciKontrol->user_id,$db);
        if ($result) {
          DeleteFileCache('KullaniciBilgileri-'.$kullaniciKontrol->user_id);
          LogAdd(lang('Kullanicilar.kayit.oturumuSonlandirildi',['user_name' => $kullaniciKontrol->user_name,'user_id' => $kullaniciKontrol->user_id]),'Kullanicilar/Detay/'.$kullaniciKontrol->user_id,session('user_id'));
          responseResult('success',lang('Kullanicilar.cikti.oturumuSonlandirildi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function IslemKayitlari($id=0)
  {
    if (!IsAllowedViewModule('kullaniciIslemKayitlariniGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db               = \Config\Database::connect();
    $kullaniciKontrol = $this->kullaniciModel->Kontrol($id,$db);
    if (!$kullaniciKontrol) {
      return redirect()->to(base_url('Hata'));
    }else {
      $viewData['kullaniciBilgileri'] = $kullaniciKontrol;
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/IslemKayitlari",$viewData);
  }

  public function IslemKayitlariAjax($id=0)
  {
    if (!IsAllowedViewModule('kullaniciIslemKayitlariniGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $refererLink  = \Config\Services::request()->getUserAgent()->getReferrer();
    $refererId    = explode('/',$refererLink);
    $refererId    = end($refererId);
    if ($refererId!=$id) {
      responseResult('error',lang('Genel.bilinmeyenHata'));
    }
    $db       = \Config\Database::connect();
    $request  = \Config\Services::request();
    $siralama = ['log_id','log_content','log_link','log_status','log_date','log_ip'];
    if ($request->getPost('search[value]')) {
      if ($request->getPost('log_status')!="") {
        $yaz = $this->kullaniciModel->IslemKayitlariAjaxAraFiltreleDurum($id,$request->getPost('log_status'),$request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
      }else {
        $yaz = $this->kullaniciModel->IslemKayitlariAjaxAra($id,$request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
      }
    }else{
      if ($request->getPost('log_status')!="") {
        $yaz = $this->kullaniciModel->IslemKayitlariAjaxFiltreleDurum($id,$request->getPost('log_status'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
      }else {
        $yaz = $this->kullaniciModel->IslemKayitlariAjax($id,$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
      }
    }
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->log_id;
      $sub_array[] = strip_tags($value->log_content);
      $sub_array[] = '<a target="_blank" class="text-muted" href="'.base_url($value->log_link).'">'.base_url($value->log_link).'</a>';
      $sub_array[] = ($value->log_status=="0"?lang('Genel.gorulmedi'):lang('Genel.goruldu'));
      $sub_array[] = DateDMYHM($value->log_date);
      $sub_array[] = $value->log_ip;
      $data[] = $sub_array;
    }
    $output = array(
      "draw"            =>  intval($_POST["draw"]),
      "recordsFiltered" =>  (count($yaz)==$request->getPost('length')?$request->getPost('start')+$request->getPost('length')+1:0),
      "data"            =>  $data
    );
    echo json_encode($output, JSON_INVALID_UTF8_SUBSTITUTE);
    exit;
  }
}
