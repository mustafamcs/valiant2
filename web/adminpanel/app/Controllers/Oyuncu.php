<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class Oyuncu extends BaseController
{
  public $viewFolder  = "";
  public $oyuncuModel = "";

  public function __construct()
  {
    $this->viewFolder   = "Oyuncu";
    $this->oyuncuModel  = model('Oyuncu_model');
    if (!session('user_id')) {
      header('Location: '.base_url('GirisYap'));
      exit;
    }
  }

  public function Ara()
  {
    if (!IsAllowedViewModule('oyuncuArayabilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'user_column' => ['rules' => "required|in_list[id,login,mail,name]"],
      'user_search' => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db             = \Config\Database::connect('metin2');
      if ($request->getPost('user_column')=="name") {
        $oyuncuKontrol  = $this->oyuncuModel->KarakterAra($request->getPost('user_column'),$request->getPost('user_search'),$db);
      }else {
        $oyuncuKontrol  = $this->oyuncuModel->OyuncuAra($request->getPost('user_column'),$request->getPost('user_search'),$db);
      }
      if (!$oyuncuKontrol) {
        responseResult('error',lang('Oyuncu.cikti.oyuncuYok'));
      }
      if ($request->getPost('user_column')=="name") {
        $response['link'] = base_url('Oyuncu/Karakter/'.$oyuncuKontrol->id);
      }else {
        $response['link'] = base_url('Oyuncu/Detay/'.$oyuncuKontrol->id);
      }
      responseResult('success',true,$response);
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Detay($id=0)
  {
    if (!IsAllowedViewModule('oyuncuArayabilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $oyuncuKontrol = $this->oyuncuModel->OyuncuDetay($id);
    if (!$oyuncuKontrol) {
      return redirect()->to(base_url('Hata'));
    }else {
      $viewData['oyuncuDetay']  = $oyuncuKontrol;
      $viewData['hesaplar']     = $this->oyuncuModel->OyuncuHesaplari($id);
      $viewData['bayrak']       = $this->oyuncuModel->OyuncuBayrak($id);
      LogAdd(lang('Oyuncu.kayit.oyuncuDetayGirildi',['login' => $oyuncuKontrol->login]),'Oyuncu/Detay/'.$oyuncuKontrol->id,session('user_id'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Detay",$viewData);
  }

  public function EPostaDegistir()
  {
    if (!IsAllowedViewModule('oyuncuEpostaDegistirebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'email' => ['label' => lang('Genel.eposta'),  'rules' => "required|valid_email"],
      'id'    => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->oyuncuModel->OyuncuKontrol($request->getPost('id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Oyuncu.cikti.oyuncuYok'));
      }else {
        if ($kontrol->email==$request->getPost('email')) {
          responseResult('error',lang('Oyuncu.cikti.degisilenVeriAyni'));
        }
        $data = [
          'email' =>  $request->getPost('email'),
        ];
        $result = $this->oyuncuModel->Guncelle($data,$kontrol->id,$db);
        if ($result) {
          DeleteFileCache('OyuncuDetay-'.$kontrol->id);
          LogAdd(lang('Oyuncu.kayit.epostaDegistirildi',['login' => $kontrol->login, 'old_email' => $kontrol->email, 'new_email' => $request->getPost('email')]),'Oyuncu/Detay/'.$kontrol->id,session('user_id'));
          responseResult('success',lang('Oyuncu.cikti.epostaDegistirildi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function TelefonDegistir()
  {
    if (!IsAllowedViewModule('oyuncuTelefonDegistirebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'phone1'  => ['label' => lang('Genel.telefon'),  'rules' => "required|integer"],
      'id'      => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->oyuncuModel->OyuncuKontrol($request->getPost('id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Oyuncu.cikti.oyuncuYok'));
      }else {
        if ($kontrol->phone1==$request->getPost('phone1')) {
          responseResult('error',lang('Oyuncu.cikti.degisilenVeriAyni'));
        }
        $data = [
          'phone1' =>  $request->getPost('phone1'),
        ];
        $result = $this->oyuncuModel->Guncelle($data,$kontrol->id,$db);
        if ($result) {
          DeleteFileCache('OyuncuDetay-'.$kontrol->id);
          LogAdd(lang('Oyuncu.kayit.telefonDegistirildi',['login' => $kontrol->login, 'old_phone' => $kontrol->phone1, 'new_phone' => $request->getPost('phone1')]),'Oyuncu/Detay/'.$kontrol->id,session('user_id'));
          responseResult('success',lang('Oyuncu.cikti.telefonDegistirildi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function SifreDegistir()
  {
    if (!IsAllowedViewModule('oyuncuTelefonDegistirebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'password'  => ['label' => lang('Genel.sifre'),  'rules' => "required|min_length[5]"],
      'id'        => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->oyuncuModel->OyuncuKontrol($request->getPost('id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Oyuncu.cikti.oyuncuYok'));
      }else {
        $data = [
          'password' =>  MysqlPasswordHash($request->getPost('password')),
        ];
        $result = $this->oyuncuModel->Guncelle($data,$kontrol->id,$db);
        if ($result) {
          DeleteFileCache('OyuncuDetay-'.$kontrol->id);
          LogAdd(lang('Oyuncu.kayit.sifreDegistirildi',['login' => $kontrol->login]),'Oyuncu/Detay/'.$kontrol->id,session('user_id'));
          if (p2pStatus==1) {
            foreach (p2pPorts as $key => $value) {
              SendServer($kontrol->login,"DC",$value);
            }
          }
          responseResult('success',lang('Oyuncu.cikti.sifreDegistirildi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function BayrakDegistir()
  {
    if (!IsAllowedViewModule('oyuncuBayrakDegistirebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'empire'  => ['label' => lang('Oyuncu.sayfa.bayrak'),  'rules' => "required|in_list[1,2,3]"],
      'id'      => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->oyuncuModel->OyuncuKontrol($request->getPost('id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Oyuncu.cikti.oyuncuYok'));
      }else {
        $data = [
          'empire' =>  $request->getPost('empire'),
        ];
        $result = $this->oyuncuModel->BayrakGuncelle($data,$kontrol->id,$db);
        if ($result) {
          DeleteFileCache('OyuncuBayrak-'.$kontrol->id);
          LogAdd(lang('Oyuncu.kayit.bayrakDegistirildi',['login' => $kontrol->login]),'Oyuncu/Detay/'.$kontrol->id,session('user_id'));
          responseResult('success',lang('Oyuncu.cikti.bayrakDegistirildi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function AjaxNesneMarket($id=0)
  {
    if (!IsAllowedViewModule('oyuncuNesneMarketKayitGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db             = \Config\Database::connect('metin2');
    $request        = \Config\Services::request();
    $oyuncuKontrol  = $this->oyuncuModel->OyuncuDetay($id);
    if (!$oyuncuKontrol) {
      return redirect()->to(base_url('Hata'));
    }else {
      $hesaplar = $this->oyuncuModel->OyuncuHesaplari($id);
      $hesapId = [];
      foreach ($hesaplar as $key => $value) {
        $hesapId[] = $value->id;
      }
    }
    if (empty($hesapId)) {
      $yaz = [];
    }
    if (!isset($yaz)) {
      $siralama = ['item_vnum','player_pid','item_price','buy_date'];
      if ($request->getPost('search[value]')) {
        $yaz = $this->oyuncuModel->AjaxNesneMarketAra($hesapId,$request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
      }else{
        $yaz = $this->oyuncuModel->AjaxNesneMarket($hesapId,$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
      }
    }
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->item_vnum.' - '.mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9");
      $sub_array[] = $value->player_name;
      $sub_array[] = $value->item_price;
      $sub_array[] = DateDMYHMS($value->buy_date);
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

  public function HesabiBanla()
  {
    if (!IsAllowedViewModule('oyuncuBanlayabilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'ban_sure'  => ['label' => lang('Genel.banSuresi'),  'rules' => "required|in_list[3600,10800,18000,25200,86400,259200,432000,604800,1209600,2592000,86313600]"],
      'id'        => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->oyuncuModel->OyuncuKontrol($request->getPost('id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Oyuncu.cikti.oyuncuYok'));
      }else {
        $banTarihi = date('Y-m-d H:i:s',strtotime('+'.$request->getPost('ban_sure').' seconds'));
        $data = [
          'status'  =>  ($request->getPost('ban_sure')!=86313600?'OK':'BLOCK'),
          'availDt' =>  $banTarihi,
        ];
        $result = $this->oyuncuModel->Guncelle($data,$kontrol->id,$db);
        if ($result) {
          DeleteFileCache('OyuncuDetay-'.$kontrol->id);
          LogAdd(lang('Oyuncu.kayit.oyuncuBanlandi',['login' => $kontrol->login, 'date' => DateDMYHMS($banTarihi)]),'Oyuncu/Detay/'.$kontrol->id,session('user_id'));
          if (p2pStatus==1) {
            foreach (p2pPorts as $key => $value) {
              SendServer($kontrol->login,"DC",$value);
            }
          }
          $alert = [
            'type' => "success",
            'text' => lang('Oyuncu.cikti.oyuncuBanlandi')
          ];
          session()->setFlashdata('alert',$alert);
          responseResult('success',lang('Oyuncu.cikti.oyuncuBanlandi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function HesabiAc()
  {
    if (!IsAllowedViewModule('oyuncuAcabilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'id'  => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->oyuncuModel->OyuncuKontrol($request->getPost('id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Oyuncu.cikti.oyuncuYok'));
      }else {
        $data = [
          'status'  =>  'OK',
          'availDt' =>  date('Y-m-d H:i:00'),
        ];
        $result = $this->oyuncuModel->Guncelle($data,$kontrol->id,$db);
        if ($result) {
          DeleteFileCache('OyuncuDetay-'.$kontrol->id);
          LogAdd(lang('Oyuncu.kayit.oyuncuAcildi',['login' => $kontrol->login]),'Oyuncu/Detay/'.$kontrol->id,session('user_id'));
          $alert = [
            'type' => "success",
            'text' => lang('Oyuncu.cikti.oyuncuAcildi')
          ];
          session()->setFlashdata('alert',$alert);
          responseResult('success',lang('Oyuncu.cikti.oyuncuAcildi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function EPostaGonder()
  {
    if (!IsAllowedViewModule('oyuncuBanlayabilsin') && !IsAllowedViewModule('oyuncuAcabilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'type'  => ['rules' => "required|in_list[ban,ac]"],
      'id'    => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->oyuncuModel->OyuncuKontrol($request->getPost('id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Oyuncu.cikti.oyuncuYok'));
      }else {
        if ($request->getPost('type')=="ban") {
          $info=[
            'to'      => $kontrol->email,
            'subject' => lang('Oyuncu.sayfa.hesabinizBanlandi'),
            'message' => $request->getPost('ban_sebebi')
          ];
        }else {
          $info=[
            'to'      => $kontrol->email,
            'subject' => lang('Oyuncu.sayfa.hesabinizAcildi'),
            'message' => $request->getPost('acilis_sebebi')
          ];
        }
        $result = SendMail($info);
        if ($result) {
          if ($request->getPost('type')=="ban") {
            LogAdd(lang('Oyuncu.kayit.banEpostaGonderildi',['login' => $kontrol->login]),'Oyuncu/Detay/'.$kontrol->id,session('user_id'));
          }else {
            LogAdd(lang('Oyuncu.kayit.acilisEpostaGonderildi',['login' => $kontrol->login]),'Oyuncu/Detay/'.$kontrol->id,session('user_id'));
          }
          responseResult('success',lang('Oyuncu.cikti.epostaGonderildi'));
        }else {
          responseResult('error',lang('Oyuncu.cikti.epostaGonderilemedi'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Karakter($id=0)
  {
    if (!IsAllowedViewModule('karakterDetayGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $karakterKontrol = $this->oyuncuModel->KarakterDetay($id);
    if (!$karakterKontrol) {
      return redirect()->to(base_url('Hata'));
    }else {
      $viewData['karakterDetay']  = $karakterKontrol;
      $viewData['mapIndex']       = $this->oyuncuModel->MapIndex($karakterKontrol->map_index);
      LogAdd(lang('Oyuncu.kayit.karakterDetayGirildi',['name' => $karakterKontrol->name]),'Oyuncu/Karakter/'.$karakterKontrol->id,session('user_id'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Karakter",$viewData);
  }

  public function KarakterKurtar()
  {
    if (!IsAllowedViewModule('karakteKurtarabilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'id'  => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->oyuncuModel->KarakterKontrol($request->getPost('id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Oyuncu.cikti.oyuncuYok'));
      }else {
        if (p2pStatus==1) {
          foreach (p2pPorts as $key => $value) {
            @SendServer($kontrol->login,"DC",$value);
          }
        }
        $data = [
          'map_index'       => 1,
          'x'               => 459770,
          'y'               => 953980,
          'exit_x'          => 0,
          'exit_y'          => 0,
          'exit_map_index'  => 1,
          'horse_riding'    => 0
        ];
        $result = $this->oyuncuModel->KarakterGuncelle($data,$kontrol->id,$db);
        if ($result) {
          DeleteFileCache('KarakterDetay-'.$kontrol->id);
          LogAdd(lang('Oyuncu.kayit.karakterKurtarildi',['name' => $kontrol->name]),'Oyuncu/Karakter/'.$kontrol->id,session('user_id'));
          responseResult('success',lang('Oyuncu.cikti.karakterKurtarildi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function KarakterDusur()
  {
    if (!IsAllowedViewModule('karakterOyundanDusursun')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'id'  => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->oyuncuModel->KarakterKontrol($request->getPost('id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Oyuncu.cikti.oyuncuYok'));
      }else {
        if (p2pStatus==1) {
          foreach (p2pPorts as $key => $value) {
            @SendServer($kontrol->login,"DC",$value);
          }
        }
        LogAdd(lang('Oyuncu.kayit.karakterDusuruldu',['name' => $kontrol->name]),'Oyuncu/Karakter/'.$kontrol->id,session('user_id'));
        responseResult('success',lang('Oyuncu.cikti.karakterDusuruldu'));
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function AjaxKarakterNesneMarket($id=0)
  {
    if (!IsAllowedViewModule('oyuncuNesneMarketKayitGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db               = \Config\Database::connect('metin2');
    $request          = \Config\Services::request();
    $karakterKontrol  = $this->oyuncuModel->KarakterDetay($id);
    if (!$karakterKontrol) {
      return redirect()->to(base_url('Hata'));
    }
    $siralama = ['item_vnum','item_price','buy_date'];
    if ($request->getPost('search[value]')) {
      $yaz = $this->oyuncuModel->AjaxKarakterNesneMarketAra($karakterKontrol->id,$request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }else{
      $yaz = $this->oyuncuModel->AjaxKarakterNesneMarket($karakterKontrol->id,$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->item_vnum.' - '.mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9");
      $sub_array[] = $value->item_price;
      $sub_array[] = DateDMYHMS($value->buy_date);
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

  public function AjaxKarakterPazar($id=0)
  {
    if (!IsAllowedViewModule('oyuncuPazarKayitGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db               = \Config\Database::connect('metin2');
    $request          = \Config\Services::request();
    $karakterKontrol  = $this->oyuncuModel->KarakterDetay($id);
    if (!$karakterKontrol) {
      return redirect()->to(base_url('Hata'));
    }
    $siralama = ['id','item_vnum','item_count','item_price','datetime'];
    if ($request->getPost('search[value]')) {
      $yaz = $this->oyuncuModel->AjaxKarakterPazarAra($karakterKontrol->id,$request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }else{
      $yaz = $this->oyuncuModel->AjaxKarakterPazar($karakterKontrol->id,$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->id;
      $sub_array[] = $value->item_vnum.' - '.mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9");
      $sub_array[] = $value->item_count;
      $sub_array[] = number_format($value->item_price,'0','.','.');
      $sub_array[] = DateDMYHMS(date('Y-m-d H:i:s',$value->datetime));
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

  public function AjaxKarakterGenel($id=0)
  {
    if (!IsAllowedViewModule('karakterGenelKayitGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db               = \Config\Database::connect('metin2');
    $request          = \Config\Services::request();
    $karakterKontrol  = $this->oyuncuModel->KarakterDetay($id);
    if (!$karakterKontrol) {
      return redirect()->to(base_url('Hata'));
    }
    $siralama = ['how','hint','ip','time'];
    $query    = "SELECT log.how, log.hint, log.ip, log.time FROM log.log ";

    $query  .= " WHERE log.who = ".$karakterKontrol->id;

    if (
      in_array($request->getPost('searchType'),['how','hint','ip'])
      && in_array($request->getPost('searchWhere'),['=','!=','%'])
      && !empty($request->getPost('genelSearch'))
    ) {
      if ($request->getPost('searchWhere')=="%") {
        $query  .= " AND log.".addslashes(addcslashes($request->getPost('searchType'),'%'))." LIKE '%".mb_convert_encoding(addslashes(addcslashes($request->getPost('genelSearch'),'%')), 'ISO-8859-9' ,"UTF-8")."%'";
      }else {
        $query  .= " AND log.".addslashes(addcslashes($request->getPost('searchType'),'%'))." ".addslashes(addcslashes($request->getPost('searchWhere'),'%'))." '".mb_convert_encoding(addslashes(addcslashes($request->getPost('genelSearch'),'%')), 'ISO-8859-9' ,"UTF-8")."'";
      }
      $query .= " COLLATE latin5_turkish_ci";
    }

    if (
      isset($siralama[$request->getPost('order[0][column]')])
      && in_array($request->getPost('order[0][dir]'),['asc','desc'])
    ) {
      $query  .= " ORDER BY ".$siralama[$request->getPost('order[0][column]')].' '.addslashes(addcslashes($request->getPost('order[0][dir]'),'%'));
    }

    if (
      is_numeric($request->getPost('length'))
      && is_numeric($request->getPost('start'))
      && $request->getPost('length')>0
      && $request->getPost('start')>=0
    ) {
      $query  .= " LIMIT ".addslashes(addcslashes($request->getPost('length'),'%')).' OFFSET '.addslashes(addcslashes($request->getPost('start'),'%'));
    }else {
      $query  .= " LIMIT 10";
    }

    $yaz  = $this->oyuncuModel->AjaxAra($query,$db);
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->how;
      $sub_array[] = mb_convert_encoding($value->hint, 'UTF-8' ,"ISO-8859-9");
      $sub_array[] = $value->ip;
      $sub_array[] = DateDMYHMS($value->time);
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

  public function Envanter($id=0)
  {
    if (!IsAllowedViewModule('envanterGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }else {
      $karakterKontrol  = $this->oyuncuModel->KarakterDetay($id);
      if (!$karakterKontrol) {
        return redirect()->to(base_url('Hata'));
      }
      $efsunID    = $this->oyuncuModel->EfsunlarID();
      $efsunText  = $this->oyuncuModel->EfsunlarText();
      $data       = $this->oyuncuModel->EnvanterEsyalari($karakterKontrol->id);
      if ($data) {
        foreach ($data as $key => $value) {
          if ($value->window!="MALL") {
            $itemIcon   = $this->oyuncuModel->ItemIcon($value->vnum);
            $response[] = [
              'id'    => $value->id,
              'count' => $value->count,
              'icon'  => (isset($itemIcon->icon)?$itemIcon->icon:'60001.png'),
              'name'  => mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9"),
              'html'  => ItemDetay($value->vnum,$value,(isset($itemIcon->icon)?$itemIcon->icon:'60001.png'),$efsunID,$efsunText),
            ];
          }
        }
      }else {
        $response = [];
      }
      echo json_encode($response);
      exit;
    }
  }

  public function DepoVeNesneMarket($id=0)
  {
    if (!IsAllowedViewModule('envanterGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }else {
      $karakterKontrol  = $this->oyuncuModel->KarakterDetay($id);
      if (!$karakterKontrol) {
        return redirect()->to(base_url('Hata'));
      }
      $efsunID    = $this->oyuncuModel->EfsunlarID();
      $efsunText  = $this->oyuncuModel->EfsunlarText();
      $data       = $this->oyuncuModel->DepoVeNesneMarket($karakterKontrol->account_id);
      if ($data) {
        foreach ($data as $key => $value) {
          $itemIcon   = $this->oyuncuModel->ItemIcon($value->vnum);
          $response[] = [
            'id'    => $value->id,
            'count' => $value->count,
            'icon'  => (isset($itemIcon->icon)?$itemIcon->icon:'60001.png'),
            'name'  => mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9"),
            'html'  => ItemDetay($value->vnum,$value,(isset($itemIcon->icon)?$itemIcon->icon:'60001.png'),$efsunID,$efsunText),
          ];
        }
      }else {
        $response = [];
      }
      echo json_encode($response);
      exit;
    }
  }

  public function EsyaGonder()
  {
    if (!IsAllowedViewModule('karakterEsyaGonderebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'vnum'  => ['label' => lang('Genel.esya'),          'rules' => "required|integer"],
      'count' => ['label' => lang('Genel.adet'),          'rules' => "required|integer"],
      'mall'  => ['label' => lang('Oyuncu.sayfa.nereye'), 'rules' => "required|in_list[0,1]"],
      'id'    => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->oyuncuModel->KarakterKontrol($request->getPost('id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Oyuncu.cikti.oyuncuYok'));
      }else {
        $esya = $this->oyuncuModel->ItemProtoKontrol($request->getPost('vnum'),$db);
        if (!$esya) {
          responseResult('error',lang('Oyuncu.cikti.esyaYok'));
        }
        $data = [
          'pid'         => $kontrol->id,
          'login'       => $kontrol->login,
          'vnum'        => $esya->vnum,
          'count'       => $request->getPost('count'),
          'given_time'  => date('Y-m-d H:i:s'),
          'why'         => esc($request->getPost('why')),
          'mall'        => $request->getPost('mall'),
        ];
        $result = $this->oyuncuModel->EsyaEkle($data,$db);
        if ($result) {
          $text = lang('Oyuncu.kayit.esyaGonderildi',['name' => $kontrol->name, 'item' => mb_convert_encoding($esya->locale_name, 'UTF-8' ,"ISO-8859-9"), 'count' => $request->getPost('count')]);
          LogAdd($text,'Oyuncu/Karakter/'.$kontrol->id,session('user_id'));
          responseResult('success',$text);
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }
}
