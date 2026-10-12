<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class Ayarlar extends BaseController
{
  public $viewFolder  = "";
  public $ayarModel   = "";

  public function __construct()
  {
    $this->viewFolder = "Ayarlar";
    $this->ayarModel = model('Ayar_model');
    if (!session('user_id')) {
      header('Location: '.base_url('GirisYap'));
      exit;
    }
  }

  public function LogoYukle()
  {
    if (!IsAllowedViewModule('logoyuGuncelleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/LogoYukle",$viewData);
  }

  public function LogoGuncelle()
  {
    if (!IsAllowedViewModule('logoyuGuncelleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $validated = $this->validate([
      'Logo' => [
        'uploaded[logo]',
        'mime_in[logo,image/jpg,image/jpeg,image/gif,image/png]',
        'ext_in[logo,jpg,jpeg,gif,png]',
        'max_size[logo,4096]',
        'is_image[logo]',
      ],
    ]);
    if ($validated) {
      $logo = $this->request->getFile('logo');
      if (file_exists(FCPATH.'assets/img/logo.png')) {
        unlink(FCPATH.'assets/img/logo.png');
      }
      $logo->move(FCPATH,"assets/img/logo.png");
      $response['logo'] = base_url('assets/img/logo.png?'.time());
      LogAdd(lang('Ayarlar.kayit.logoYuklendi'),'Ayarlar/LogoYukle',session('user_id'));
      responseResult('success',lang('Ayarlar.cikti.logoYuklendi'),$response);
    }else {
      responseResult('error',$this->validator->getErrors());
    }
  }

  public function FaviconYukle()
  {
    if (!IsAllowedViewModule('faviconGuncelleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/FaviconYukle",$viewData);
  }

  public function FaviconGuncelle()
  {
    if (!IsAllowedViewModule('faviconGuncelleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $validated = $this->validate([
      'Favicon' => [
        'uploaded[favicon]',
        'mime_in[favicon,image/x-ico,image/x-icon,image/vnd.microsoft.icon]',
        'ext_in[favicon,ico]',
        'max_size[favicon,1024]',
        'is_image[favicon]',
      ],
    ]);
    if ($validated) {
      $logo = $this->request->getFile('favicon');
      if (file_exists(FCPATH.'favicon.ico')) {
        unlink(FCPATH.'favicon.ico');
      }
      $logo->move(FCPATH,"favicon.ico");
      $response['favicon'] = base_url('favicon.ico?'.time());
      LogAdd(lang('Ayarlar.kayit.faviconYuklendi'),'Ayarlar/FaviconYukle',session('user_id'));
      responseResult('success',lang('Ayarlar.cikti.faviconYuklendi'),$response);
    }else {
      responseResult('error',$this->validator->getErrors());
    }
  }

  public function Site()
  {
    if (!IsAllowedViewModule('siteAyarlariniGuncelleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    $db                       = \Config\Database::connect();
    $viewData['siteAdi']      = $this->ayarModel->AyarCek('siteAdi',$db);
    $viewData['footerYazisi'] = $this->ayarModel->AyarCek('footerYazisi',$db);
    return view("{$this->viewFolder}/Site",$viewData);
  }

  public function SiteGuncelle()
  {
    if (!IsAllowedViewModule('siteAyarlariniGuncelleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $validation =  \Config\Services::validation();
    $request    =  \Config\Services::request();
    $validation->setRules([
      'siteAdi'               => ['label' => lang('Ayarlar.sayfa.siteAdi'),              'rules'=> "required"],
      'footerYazisi'          => ['label' => lang('Ayarlar.sayfa.footerYazisi'),         'rules'=> "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db      = \Config\Database::connect();
      $kontrol = [
        'siteAdi'       => $this->ayarModel->AyarCek('siteAdi',$db),
        'footerYazisi'  => $this->ayarModel->AyarCek('footerYazisi',$db),
      ];
      foreach ($kontrol as $key => $value) {
        if (!empty($value)) {
          $data = [
            'setting_content' =>  $request->getPost($key)
          ];
          $result = $this->ayarModel->Guncelle($data,$key,$db);
        }else {
          $data = [
            'setting_name'    =>  $key,
            'setting_content' =>  $request->getPost($key)
          ];
          $result = $this->ayarModel->Ekle($data,$db);
        }
      }
      if ($result) {
        DeleteFileCache('AyarCek-siteAdi');
        DeleteFileCache('AyarCek-footerYazisi');
        LogAdd(lang('Ayarlar.kayit.siteAyarlariGuncellendi'),'Ayarlar/Site',session('user_id'));
        responseResult('success',lang('Ayarlar.cikti.siteAyarlariGuncellendi'));
      }else {
        responseResult('error',lang('Genel.bilinmeyenHata'));
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Javascript()
  {
    if (!IsAllowedViewModule('javascriptKodlariniGuncelleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    $db                            = \Config\Database::connect();
    $viewData['javascriptKodlari'] = $this->ayarModel->AyarCek('javascriptKodlari',$db);
    return view("{$this->viewFolder}/Javascript",$viewData);
  }

  public function JavascriptGuncelle()
  {
    if (!IsAllowedViewModule('javascriptKodlariniGuncelleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $validation =  \Config\Services::validation();
    $request    =  \Config\Services::request();
    $validation->setRules([
      'javascriptKodlari' => ['label' => lang('Ayarlar.sayfa.javascriptKodlari'),'rules'=> "trim"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db      = \Config\Database::connect();
      $kontrol = $this->ayarModel->AyarCek('javascriptKodlari',$db);
      if (!empty($kontrol)) {
        $data = [
          'setting_content'  =>  $request->getPost('javascriptKodlari')
        ];
        $result = $this->ayarModel->Guncelle($data,$kontrol->setting_name,$db);
      }else {
        $data = [
          'setting_name'     =>  'javascriptKodlari',
          'setting_content'  =>  $request->getPost('javascriptKodlari')
        ];
        $result = $this->ayarModel->Ekle($data,$db);
      }
      if ($result) {
        DeleteFileCache('AyarCek-javascriptKodlari');
        LogAdd(lang('Ayarlar.kayit.javascriptKodlariGuncellendi'),'Ayarlar/Javascript',session('user_id'));
        responseResult('success',lang('Ayarlar.cikti.javascriptKodlariGuncellendi'));
      }else {
        responseResult('error',lang('Genel.bilinmeyenHata'));
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function P2P()
  {
    if (!IsAllowedViewModule('p2pAyarlariGuncelleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/P2P",$viewData);
  }

  public function P2PGuncelle()
  {
    if (!IsAllowedViewModule('p2pAyarlariGuncelleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $validation =  \Config\Services::validation();
    $request    =  \Config\Services::request();
    $validation->setRules([
      'p2pStatus'     => ['label' => lang('Genel.durum'),                       'rules' => "required|in_list[0,1]"],
      'p2pHost'       => ['label' => 'IP',                                      'rules' => "required"],
      'p2pPassword'   => ['label' => lang('Genel.sifre'),                       'rules' => "required"],
      'p2pPorts'      => ['label' => lang('Ayarlar.sayfa.portlar'),             'rules' => "required"],
      'p2pStatistics' => ['label' => lang('Ayarlar.sayfa.anasayfaIstatistik'),  'rules' => "required|in_list[0,1]"],
      'p2pChannel'    => ['label' => lang('Ayarlar.sayfa.chPortlar'),           'rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      helper('filesystem');
      $fileContent  = '<?php'.PHP_EOL;
      $fileContent .= 'define(\'p2pStatus\',      '.var_export((int)$request->getPost('p2pStatus'), true).');'.PHP_EOL;
      $fileContent .= 'define(\'p2pHost\',        '.var_export($request->getPost('p2pHost'), true).');'.PHP_EOL;
      $fileContent .= 'define(\'p2pPassword\',    '.var_export($request->getPost('p2pPassword'), true).');'.PHP_EOL;
      $fileContent .= 'define(\'p2pPorts\',       '.var_export(explode(',',$request->getPost('p2pPorts')), true).');'.PHP_EOL;
      $fileContent .= 'define(\'p2pStatistics\',  '.var_export((int)$request->getPost('p2pStatistics'), true).');'.PHP_EOL;
      $fileContent .= 'define(\'p2pChannel\',     '.var_export(explode(',',$request->getPost('p2pChannel')), true).');'.PHP_EOL;
      if (write_file(APPPATH."Config/P2P.php",$fileContent)){
        LogAdd(lang('Ayarlar.kayit.p2pAyarlariGuncellendi'),'Ayarlar/P2P',session('user_id'));
        responseResult('success',lang('Ayarlar.cikti.p2pAyarlariGuncellendi'));
      }else {
        responseResult('error',lang('Ayarlar.cikti.dosyaYazilabilirDegil'));
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function P2PTestEt()
  {
    if (!IsAllowedViewModule('p2pAyarlariGuncelleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $result = SendServer("","USER_COUNT",current(p2pPorts));
    if ($result){
      LogAdd(lang('Ayarlar.cikti.basariylaBaglanildi'),'Ayarlar/P2P',session('user_id'));
      responseResult('success',lang('Ayarlar.cikti.basariylaBaglanildi'));
    }else {
      LogAdd(lang('Ayarlar.cikti.baglanilamadi'),'Ayarlar/P2P',session('user_id'));
      responseResult('error',lang('Ayarlar.cikti.baglanilamadi'));
    }
  }

  public function Ikon()
  {
    if (!IsAllowedViewModule('ikonAyarlariGuncelleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Ikon",$viewData);
  }

  public function ItemListYukle()
  {
    if (!IsAllowedViewModule('ikonAyarlariGuncelleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $validated = $this->validate([
      'txt' => [
        'uploaded[txt]',
        'mime_in[txt,text/plain]',
        'ext_in[txt,txt]',
      ],
    ]);
    if ($validated) {
      $txt      = $this->request->getFile('txt');
      $tempName = $txt->getTempName();
      $file     = fopen($tempName,'r');
      $readFile = fread($file , filesize ($tempName));
      $explode  = explode("\n",$readFile);
      $db = \Config\Database::connect();
      $this->ayarModel->TabloyuBosalt('item_icon',$db);
      $vnums    = [];
      foreach ($explode as $key => $value) {
        $valueExplode =  explode("\t", $value);
        if (isset($valueExplode[2])) {
          $icon = explode('/',$valueExplode[2]);
          $iconName = "";
          if (isset($icon[2])) {
            foreach ($icon as $key => $value) {
              if ($key>=2) {
                $iconName .= trim($value);
                if ($key!=(count($icon)-1)) {
                  $iconName .= '/';
                }
                if ($key==(count($icon)-1)) {
                  $iconName = substr($iconName,0,-4).'.png';
                }
              }
            }
          }else {
            $iconName = 0;
          }
          if (!in_array((isset($valueExplode[0])?$valueExplode[0]:0),$vnums) && ($iconName!=0 || $iconName!=".png")) {
            $vnums[] = (isset($valueExplode[0])?$valueExplode[0]:0);
            $data = [
              'vnum' =>  (isset($valueExplode[0])?$valueExplode[0]:0),
              'icon' => $iconName
            ];
            $this->ayarModel->VeriEkle('item_icon',$data,$db);
          }
        }
      }
      $itemProtoCek = $this->ayarModel->ItemProtoCek();
      $itemProtoCek = array_diff(array_column($itemProtoCek,'vnum'),$vnums);
      foreach ($itemProtoCek as $key => $value) {
        $data = [
          'vnum' =>  $value,
          'icon' => $value.'.png'
        ];
        $this->ayarModel->VeriEkle('item_icon',$data,$db);
      }
      MultiDeleteFileCache('ItemIcon');
      LogAdd(lang('Ayarlar.kayit.itemlistYuklendi'),'Ayarlar/Ikon',session('user_id'));
      responseResult('success',lang('Ayarlar.cikti.itemlistYuklendi'));
    }else {
      responseResult('error',$this->validator->getErrors());
    }
  }

  public function IconZipYukle()
  {
    if (!IsAllowedViewModule('ikonAyarlariGuncelleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $validated = $this->validate([
      'zip' => [
        'uploaded[zip]',
        'mime_in[zip,application/zip,application/octet-stream,application/x-zip-compressed,multipart/x-zip]',
        'ext_in[zip,zip]',
      ],
    ]);
    if ($validated) {
      $zip      = $this->request->getFile('zip');
      $tempName = $zip->getTempName();
      $unzip = new \App\Libraries\Unzip;
      $unzip->allow(array('png','jpeg','jpg'));
      $result = $unzip->extract($tempName, FCPATH.'assets/img/icon/');
      if ($result) {
        MultiDeleteFileCache('ItemIcon');
        LogAdd(lang('Ayarlar.kayit.iconYuklendi'),'Ayarlar/Ikon',session('user_id'));
        responseResult('success',lang('Ayarlar.cikti.iconYuklendi'));
      }else {
        responseResult('error',lang('Genel.bilinmeyenHata'));
      }
    }else {
      responseResult('error',$this->validator->getErrors());
    }
  }

  public function SMTP()
  {
    if (!IsAllowedViewModule('smtpAyarlariniGuncelleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    $db                             = \Config\Database::connect();
    $viewData['smtpGonderenIsim']   = $this->ayarModel->AyarCek('smtpGonderenIsim',$db);
    $viewData['smtpHost']           = $this->ayarModel->AyarCek('smtpHost',$db);
    $viewData['smtpEpostaAdresi']   = $this->ayarModel->AyarCek('smtpEpostaAdresi',$db);
    $viewData['smtpEpostaSifresi']  = $this->ayarModel->AyarCek('smtpEpostaSifresi',$db);
    $viewData['smtpPort']           = $this->ayarModel->AyarCek('smtpPort',$db);
    $viewData['smtpGuvenlik']       = $this->ayarModel->AyarCek('smtpGuvenlik',$db);
    return view("{$this->viewFolder}/SMTP",$viewData);
  }

  public function SMTPGuncelle()
  {
    if (!IsAllowedViewModule('smtpAyarlariniGuncelleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $validation =  \Config\Services::validation();
    $request    =  \Config\Services::request();
    $validation->setRules([
      'smtpGonderenIsim'  => ['label' => lang('Ayarlar.sayfa.smtpGonderenIsim'),  'rules'=> "required"],
      'smtpHost'          => ['label' => "Host",                                  'rules'=> "required"],
      'smtpEpostaAdresi'  => ['label' => lang('Ayarlar.sayfa.smtpEpostaAdresi'),  'rules'=> "required|valid_email"],
      'smtpEpostaSifresi' => ['label' => lang('Ayarlar.sayfa.smtpEpostaSifresi'), 'rules'=> "required"],
      'smtpPort'          => ['label' => "Port",                                  'rules'=> "required|integer"],
      'smtpGuvenlik'      => ['label' => lang('Ayarlar.sayfa.smtpGuvenlik'),      'rules'=> "required|in_list[yok,tls,ssl]"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db      = \Config\Database::connect();
      $kontrol = [
        'smtpGonderenIsim'  => $this->ayarModel->AyarCek('smtpGonderenIsim',$db),
        'smtpHost'          => $this->ayarModel->AyarCek('smtpHost',$db),
        'smtpEpostaAdresi'  => $this->ayarModel->AyarCek('smtpEpostaAdresi',$db),
        'smtpEpostaSifresi' => $this->ayarModel->AyarCek('smtpEpostaSifresi',$db),
        'smtpPort'          => $this->ayarModel->AyarCek('smtpPort',$db),
        'smtpGuvenlik'      => $this->ayarModel->AyarCek('smtpGuvenlik',$db),
      ];
      foreach ($kontrol as $key => $value) {
        if (!empty($value)) {
          $data = [
            'setting_content'  =>  $request->getPost($key)
          ];
          $result = $this->ayarModel->Guncelle($data,$key,$db);
        }else {
          $data = [
            'setting_name'    =>  $key,
            'setting_content' =>  $request->getPost($key)
          ];
          $result = $this->ayarModel->Ekle($data,$db);
        }
      }
      if ($result) {
        LogAdd(lang('Ayarlar.kayit.smtpAyarlariGuncellendi'),'Ayarlar/SMTP',session('user_id'));
        responseResult('success',lang('Ayarlar.cikti.smtpAyarlariGuncellendi'));
      }else {
        responseResult('error',lang('Genel.bilinmeyenHata'));
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function TestEPostaGonder()
  {
    if (!IsAllowedViewModule('smtpAyarlariniGuncelleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $validation =  \Config\Services::validation();
    $request    =  \Config\Services::request();
    $validation->setRules([
      'gonderilecekEPostaAdresi'  => ['label' => lang('Ayarlar.sayfa.gonderilecekEPostaAdresi'),'rules'=> "required|valid_email"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $info=[
        'to' => $request->getPost('gonderilecekEPostaAdresi'),
        'subject' => 'Test E-Posta Gönderimi',
        'message' => "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
      ];
      $response = SendMail($info,true);
      if ($response) {
        LogAdd(lang('Ayarlar.kayit.gondermeIslemiBasarili',["email" => $request->getPost('gonderilecekEPostaAdresi')]),'Ayarlar/SMTP',session('user_id'));
        echo lang('Ayarlar.cikti.gondermeIslemiBasarili');
      }else {
        LogAdd(lang('Ayarlar.kayit.gondermeIslemiBasarisiz',["email" => $request->getPost('gonderilecekEPostaAdresi')]),'Ayarlar/SMTP',session('user_id'));
        echo lang('Ayarlar.cikti.gondermeIslemiBasarisiz');
      }
    }else {
      echo implode($validation->getErrors());
    }
    exit('<br><a href="'.base_url('Ayarlar/SMTP').'">'.lang('Hata.geriDon').'</a>');
  }
}
