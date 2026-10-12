<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class GM extends BaseController
{
  public $viewFolder  = "";
  public $gmModel     = "";

  public function __construct()
  {
    $this->viewFolder = "GM";
    $this->gmModel    = model('GM_model');
    if (!session('user_id')) {
      header('Location: '.base_url('GirisYap'));
      exit;
    }
  }

  public function Index()
  {
    if (!IsAllowedViewModule('gmGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Index",$viewData);
  }

  public function Ajax()
  {
    if (!IsAllowedViewModule('gmGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect('metin2');
    $request  = \Config\Services::request();
    $siralama = ['mID','mAccount','mName','mAuthority'];
    if ($request->getPost('search[value]')) {
      $yaz = $this->gmModel->AjaxAra($request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }else{
      $yaz = $this->gmModel->Ajax($request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->mID;
      $sub_array[] = $value->mAccount;
      $sub_array[] = $value->mName;
      $sub_array[] = $value->mAuthority;
      if (IsAllowedViewModule('gmDuzenleyebilsin') || IsAllowedViewModule('gmSilebilsin')) {
        $buttons = "";
        if (IsAllowedViewModule('gmDuzenleyebilsin')) {
          $buttons .= '<a class="btn btn-primary pt-1 pb-1 ps-2 pe-2" data-bs-toggle="modal" data-bs-target="#duzenle" href="javascript:void(0)" data-id="'.$value->mID.'">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" style="width:25px;height:25px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 7h-3a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-3" /><path d="M9 15h3l8.5 -8.5a1.5 1.5 0 0 0 -3 -3l-8.5 8.5v3" /><line x1="16" y1="5" x2="19" y2="8" /></svg>
          </a>';
        }
        if (IsAllowedViewModule('gmSilebilsin')) {
          $buttons .= '<a class="btn btn-danger pt-1 pb-1 ps-2 pe-2 ms-2 gmSil" href="javascript:void(0)" data-id="'.$value->mID.'" data-header="'.lang('Genel.silBaslik').'" data-message="'.lang('Genel.buIslemGeriAlinamaz').'" data-yes="'.lang('Genel.evet').'" data-no="'.lang('Genel.hayir').'">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" style="width:25px;height:25px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><line x1="4" y1="7" x2="20" y2="7" /><line x1="10" y1="11" x2="10" y2="17" /><line x1="14" y1="11" x2="14" y2="17" /><path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12" /><path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3" /></svg>
          </a>';
        }
        $sub_array[] = $buttons;
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

  public function Ekle()
  {
    if (!IsAllowedViewModule('gmEkleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'mAccount'    => ['label' => lang('Genel.kullaniciAdi'),  'rules' => "required"],
      'mName'       => ['label' => lang('Genel.karakterAdi'),   'rules' => "required"],
      'mAuthority'  => ['label' => lang('Genel.yetki.yetki'),   'rules' => "required|in_list[PLAYER,LOW_WIZARD,GOD,HIGH_WIZARD,IMPLEMENTOR]"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db             = \Config\Database::connect('metin2');
      $oyuncuKontrol  = $this->gmModel->OyuncuKontrol($request->getPost('mAccount'),$request->getPost('mName'),$db);
      if (!$oyuncuKontrol) {
        responseResult('error',lang('GM.cikti.oyuncuYok'));
      }
      $kontrol = $this->gmModel->Kontrol($request->getPost('mAccount'),$request->getPost('mName'),$db);
      if ($kontrol) {
        responseResult('error',lang('GM.cikti.zatenEkli'));
      }
      $data = [
        'mAccount'    =>  $request->getPost('mAccount'),
        'mName'       =>  $request->getPost('mName'),
        'mServerIP'   =>  "ALL",
        'mAuthority'  =>  $request->getPost('mAuthority'),
      ];
      $result = $this->gmModel->Ekle($data,$db);
      if ($result) {
        LogAdd(lang('GM.kayit.gmEklendi',['user' => $request->getPost('mAccount'), 'player' => $request->getPost('mName')]),'GM/Index',session('user_id'));
        responseResult('success',lang('GM.cikti.gmEklendi'));
      }else {
        responseResult('error',lang('Genel.bilinmeyenHata'));
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Detay($id=0)
  {
    if (!IsAllowedViewModule('gmDuzenleyebilsin')) {
      responseResult('error',lang('Genel.yetkinYok'));
    }
    $request  = \Config\Services::request();
    $db       = \Config\Database::connect('metin2');
    $kontrol  = $this->gmModel->KontrolID($id,$db);
    if (!$kontrol) {
      responseResult('error',lang('GM.cikti.gmYok'));
    }else {
      $returnData['mAccount']   = $kontrol->mAccount;
      $returnData['mName']      = $kontrol->mName;
      $returnData['mAuthority'] = $kontrol->mAuthority;
      $returnData['mID']        = $kontrol->mID;
      echo json_encode($returnData);
      exit;
    }
  }

  public function Duzenle()
  {
    if (!IsAllowedViewModule('gmDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'mAccount'    => ['label' => lang('Genel.kullaniciAdi'),  'rules' => "required"],
      'mName'       => ['label' => lang('Genel.karakterAdi'),   'rules' => "required"],
      'mAuthority'  => ['label' => lang('Genel.yetki.yetki'),   'rules' => "required|in_list[PLAYER,LOW_WIZARD,GOD,HIGH_WIZARD,IMPLEMENTOR]"],
      'mID'         => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db             = \Config\Database::connect('metin2');
      $oyuncuKontrol  = $this->gmModel->OyuncuKontrol($request->getPost('mAccount'),$request->getPost('mName'),$db);
      if (!$oyuncuKontrol) {
        responseResult('error',lang('GM.cikti.oyuncuYok'));
      }
      $kontrol  = $this->gmModel->KontrolID($request->getPost('mID'),$db);
      if (!$kontrol) {
        responseResult('error',lang('GM.cikti.gmYok'));
      }else {
        $data = [
          'mAccount'    =>  $request->getPost('mAccount'),
          'mName'       =>  $request->getPost('mName'),
          'mAuthority'  =>  $request->getPost('mAuthority'),
        ];
        $result = $this->gmModel->Guncelle($data,$kontrol->mID,$db);
        if ($result) {
          LogAdd(lang('GM.kayit.gmDuzenlendi',['user' => $kontrol->mAccount, 'player' => $kontrol->mName]),'GM/Index',session('user_id'));
          responseResult('success',lang('GM.cikti.gmDuzenlendi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Sil()
  {
    if (!IsAllowedViewModule('gmSilebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'mID'  => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->gmModel->KontrolID($request->getPost('mID'),$db);
      if (!$kontrol) {
        responseResult('error',lang('GM.cikti.gmYok'));
      }else {
        $result = $this->gmModel->Sil($kontrol->mID,$db);
        if ($result) {
          LogAdd(lang('GM.kayit.gmSilindi',['user' => $kontrol->mAccount, 'player' => $kontrol->mName]),'GM/Index',session('user_id'));
          responseResult('success',lang('GM.cikti.gmSilindi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function SunucuyaGonder()
  {
    if (!IsAllowedViewModule('gmEkleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    if (p2pStatus==0) {
      responseResult('error',lang('Genel.p2pKapali'));
    }
    foreach (p2pPorts as $key => $value) {
      SendServer('A',"RELOAD",$value);
    }
    LogAdd(lang('GM.cikti.sunucuyaGonderildi'),'GM/Index',session('user_id'));
    responseResult('success',lang('GM.cikti.sunucuyaGonderildi'));
  }
}
