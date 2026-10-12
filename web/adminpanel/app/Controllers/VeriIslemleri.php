<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class VeriIslemleri extends BaseController
{
  public $viewFolder  = "";
  public $veriModel   = "";

  public function __construct()
  {
    $this->viewFolder = "VeriIslemleri";
    $this->veriModel  = model('Veri_islem_model');
    if (!session('user_id')) {
      header('Location: '.base_url('GirisYap'));
      exit;
    }
  }

  public function ID()
  {
    if (!IsAllowedViewModule('efsunIsimGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/ID",$viewData);
  }

  public function AjaxID()
  {
    if (!IsAllowedViewModule('efsunIsimGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect();
    $request  = \Config\Services::request();
    $siralama = ['id','name'];
    if ($request->getPost('search[value]')) {
      $yaz = $this->veriModel->AjaxAraID($request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }else{
      $yaz = $this->veriModel->AjaxID($request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->id;
      $sub_array[] = $value->name;
      if (IsAllowedViewModule('efsunIsimDuzenleyebilsin') || IsAllowedViewModule('efsunIsimSilebilsin')) {
        $buttons = "";
        if (IsAllowedViewModule('efsunIsimDuzenleyebilsin')) {
          $buttons .= '<a class="btn btn-primary pt-1 pb-1 ps-2 pe-2" data-bs-toggle="modal" data-bs-target="#duzenle" href="javascript:void(0)" data-id="'.$value->id.'">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" style="width:25px;height:25px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 7h-3a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-3" /><path d="M9 15h3l8.5 -8.5a1.5 1.5 0 0 0 -3 -3l-8.5 8.5v3" /><line x1="16" y1="5" x2="19" y2="8" /></svg>
          </a>';
        }
        if (IsAllowedViewModule('efsunIsimSilebilsin')) {
          $buttons .= '<a class="btn btn-danger pt-1 pb-1 ps-2 pe-2 ms-2 isimSil" href="javascript:void(0)" data-id="'.$value->id.'" data-header="'.lang('Genel.silBaslik').'" data-message="'.lang('Genel.buIslemGeriAlinamaz').'" data-yes="'.lang('Genel.evet').'" data-no="'.lang('Genel.hayir').'">
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

  public function EkleID()
  {
    if (!IsAllowedViewModule('efsunIsimEkleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'id'    => ['label' => lang('Genel.id'),    'rules' => "required|integer"],
      'name'  => ['label' => lang('Genel.isim'),  'rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db      = \Config\Database::connect();
      $kontrol = $this->veriModel->KontrolID($request->getPost('id'),$db);
      if ($kontrol) {
        responseResult('error',lang('VeriIslemleri.cikti.zatenEkli'));
      }
      $data = [
        'id'    =>  $request->getPost('id'),
        'name'  =>  $request->getPost('name'),
      ];
      $result = $this->veriModel->EkleID($data,$db);
      if ($result) {
        DeleteFileCache('EfsunlarID');
        LogAdd(lang('VeriIslemleri.kayit.isimEklendi',['id' => $request->getPost('id'), 'name' => $request->getPost('name')]),'VeriIslemleri/ID',session('user_id'));
        responseResult('success',lang('VeriIslemleri.cikti.isimEklendi'));
      }else {
        responseResult('error',lang('Genel.bilinmeyenHata'));
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function DetayID($id=0)
  {
    if (!IsAllowedViewModule('efsunIsimDuzenleyebilsin')) {
      responseResult('error',lang('Genel.yetkinYok'));
    }
    $request  = \Config\Services::request();
    $db       = \Config\Database::connect();
    $kontrol  = $this->veriModel->KontrolID($id,$db);
    if (!$kontrol) {
      responseResult('error',lang('VeriIslemleri.cikti.isimYok'));
    }else {
      $returnData['id']   = $kontrol->id;
      $returnData['name'] = $kontrol->name;
      echo json_encode($returnData);
      exit;
    }
  }

  public function DuzenleID()
  {
    if (!IsAllowedViewModule('efsunIsimDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'id'    => ['label' => lang('Genel.id'),    'rules' => "required|integer"],
      'name'  => ['label' => lang('Genel.isim'),  'rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect();
      $kontrol  = $this->veriModel->KontrolID($request->getPost('id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('VeriIslemleri.cikti.isimYok'));
      }else {
        $data = [
          'id'    =>  $request->getPost('id'),
          'name'  =>  $request->getPost('name'),
        ];
        $result = $this->veriModel->GuncelleID($data,$kontrol->id,$db);
        if ($result) {
          DeleteFileCache('EfsunlarID');
          LogAdd(lang('VeriIslemleri.kayit.isimDuzenlendi',['id' => $kontrol->id, 'name' => $kontrol->name]),'VeriIslemleri/ID',session('user_id'));
          responseResult('success',lang('VeriIslemleri.cikti.isimDuzenlendi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function SilID()
  {
    if (!IsAllowedViewModule('efsunIsimSilebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'id'  => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect();
      $kontrol  = $this->veriModel->KontrolID($request->getPost('id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('VeriIslemleri.cikti.isimYok'));
      }else {
        $result = $this->veriModel->SilID($kontrol->id,$db);
        if ($result) {
          DeleteFileCache('EfsunlarID');
          LogAdd(lang('VeriIslemleri.kayit.isimSilindi',['id' => $kontrol->id, 'name' => $kontrol->name]),'VeriIslemleri/ID',session('user_id'));
          responseResult('success',lang('VeriIslemleri.cikti.isimSilindi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Text()
  {
    if (!IsAllowedViewModule('efsunIsimGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Text",$viewData);
  }

  public function AjaxText()
  {
    if (!IsAllowedViewModule('efsunIsimGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect();
    $request  = \Config\Services::request();
    $siralama = ['id','name'];
    if ($request->getPost('search[value]')) {
      $yaz = $this->veriModel->AjaxAraText($request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }else{
      $yaz = $this->veriModel->AjaxText($request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->id;
      $sub_array[] = $value->name;
      if (IsAllowedViewModule('efsunIsimDuzenleyebilsin') || IsAllowedViewModule('efsunIsimSilebilsin')) {
        $buttons = "";
        if (IsAllowedViewModule('efsunIsimDuzenleyebilsin')) {
          $buttons .= '<a class="btn btn-primary pt-1 pb-1 ps-2 pe-2" data-bs-toggle="modal" data-bs-target="#duzenle" href="javascript:void(0)" data-id="'.$value->id.'">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" style="width:25px;height:25px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 7h-3a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-3" /><path d="M9 15h3l8.5 -8.5a1.5 1.5 0 0 0 -3 -3l-8.5 8.5v3" /><line x1="16" y1="5" x2="19" y2="8" /></svg>
          </a>';
        }
        if (IsAllowedViewModule('efsunIsimSilebilsin')) {
          $buttons .= '<a class="btn btn-danger pt-1 pb-1 ps-2 pe-2 ms-2 isimSil" href="javascript:void(0)" data-id="'.$value->id.'" data-header="'.lang('Genel.silBaslik').'" data-message="'.lang('Genel.buIslemGeriAlinamaz').'" data-yes="'.lang('Genel.evet').'" data-no="'.lang('Genel.hayir').'">
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

  public function EkleText()
  {
    if (!IsAllowedViewModule('efsunIsimEkleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'id'    => ['label' => lang('Genel.id'),    'rules' => "required"],
      'name'  => ['label' => lang('Genel.isim'),  'rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db      = \Config\Database::connect();
      $kontrol = $this->veriModel->KontrolText($request->getPost('id'),$db);
      if ($kontrol) {
        responseResult('error',lang('VeriIslemleri.cikti.zatenEkli'));
      }
      $data = [
        'id'    =>  $request->getPost('id'),
        'name'  =>  $request->getPost('name'),
      ];
      $result = $this->veriModel->EkleText($data,$db);
      if ($result) {
        DeleteFileCache('EfsunlarText');
        LogAdd(lang('VeriIslemleri.kayit.isimEklendi',['id' => $request->getPost('id'), 'name' => $request->getPost('name')]),'VeriIslemleri/Text',session('user_id'));
        responseResult('success',lang('VeriIslemleri.cikti.isimEklendi'));
      }else {
        responseResult('error',lang('Genel.bilinmeyenHata'));
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function DetayText($id=0)
  {
    if (!IsAllowedViewModule('efsunIsimDuzenleyebilsin')) {
      responseResult('error',lang('Genel.yetkinYok'));
    }
    $request  = \Config\Services::request();
    $db       = \Config\Database::connect();
    $kontrol  = $this->veriModel->KontrolText($id,$db);
    if (!$kontrol) {
      responseResult('error',lang('VeriIslemleri.cikti.isimYok'));
    }else {
      $returnData['id']   = $kontrol->id;
      $returnData['name'] = $kontrol->name;
      echo json_encode($returnData);
      exit;
    }
  }

  public function DuzenleText()
  {
    if (!IsAllowedViewModule('efsunIsimDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'id'    => ['label' => lang('Genel.id'),    'rules' => "required"],
      'name'  => ['label' => lang('Genel.isim'),  'rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect();
      $kontrol  = $this->veriModel->KontrolText($request->getPost('id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('VeriIslemleri.cikti.isimYok'));
      }else {
        $data = [
          'id'    =>  $request->getPost('id'),
          'name'  =>  $request->getPost('name'),
        ];
        $result = $this->veriModel->GuncelleText($data,$kontrol->id,$db);
        if ($result) {
          DeleteFileCache('EfsunlarText');
          LogAdd(lang('VeriIslemleri.kayit.isimDuzenlendi',['id' => $kontrol->id, 'name' => $kontrol->name]),'VeriIslemleri/Text',session('user_id'));
          responseResult('success',lang('VeriIslemleri.cikti.isimDuzenlendi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function SilText()
  {
    if (!IsAllowedViewModule('efsunIsimSilebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'id'  => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect();
      $kontrol  = $this->veriModel->KontrolText($request->getPost('id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('VeriIslemleri.cikti.isimYok'));
      }else {
        $result = $this->veriModel->SilText($kontrol->id,$db);
        if ($result) {
          DeleteFileCache('EfsunlarText');
          LogAdd(lang('VeriIslemleri.kayit.isimSilindi',['id' => $kontrol->id, 'name' => $kontrol->name]),'VeriIslemleri/Text',session('user_id'));
          responseResult('success',lang('VeriIslemleri.cikti.isimSilindi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Harita()
  {
    if (!IsAllowedViewModule('haritaIsimGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Harita",$viewData);
  }

  public function AjaxHarita()
  {
    if (!IsAllowedViewModule('haritaIsimGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect();
    $request  = \Config\Services::request();
    $siralama = ['id','name'];
    if ($request->getPost('search[value]')) {
      $yaz = $this->veriModel->AjaxAraHarita($request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }else{
      $yaz = $this->veriModel->AjaxHarita($request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->id;
      $sub_array[] = $value->name;
      if (IsAllowedViewModule('haritaIsimDuzenleyebilsin') || IsAllowedViewModule('haritaIsimSilebilsin')) {
        $buttons = "";
        if (IsAllowedViewModule('haritaIsimDuzenleyebilsin')) {
          $buttons .= '<a class="btn btn-primary pt-1 pb-1 ps-2 pe-2" data-bs-toggle="modal" data-bs-target="#duzenle" href="javascript:void(0)" data-id="'.$value->id.'">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" style="width:25px;height:25px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 7h-3a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-3" /><path d="M9 15h3l8.5 -8.5a1.5 1.5 0 0 0 -3 -3l-8.5 8.5v3" /><line x1="16" y1="5" x2="19" y2="8" /></svg>
          </a>';
        }
        if (IsAllowedViewModule('haritaIsimSilebilsin')) {
          $buttons .= '<a class="btn btn-danger pt-1 pb-1 ps-2 pe-2 ms-2 haritaSil" href="javascript:void(0)" data-id="'.$value->id.'" data-header="'.lang('Genel.silBaslik').'" data-message="'.lang('Genel.buIslemGeriAlinamaz').'" data-yes="'.lang('Genel.evet').'" data-no="'.lang('Genel.hayir').'">
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

  public function EkleHarita()
  {
    if (!IsAllowedViewModule('haritaIsimEkleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'id'    => ['label' => lang('Genel.id'),    'rules' => "required"],
      'name'  => ['label' => lang('Genel.isim'),  'rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db      = \Config\Database::connect();
      $kontrol = $this->veriModel->KontrolHarita($request->getPost('id'),$db);
      if ($kontrol) {
        responseResult('error',lang('VeriIslemleri.cikti.zatenEkli'));
      }
      $data = [
        'id'    =>  $request->getPost('id'),
        'name'  =>  $request->getPost('name'),
      ];
      $result = $this->veriModel->EkleHarita($data,$db);
      if ($result) {
        LogAdd(lang('VeriIslemleri.kayit.haritaEklendi',['id' => $request->getPost('id'), 'name' => $request->getPost('name')]),'VeriIslemleri/Harita',session('user_id'));
        responseResult('success',lang('VeriIslemleri.cikti.haritaEklendi'));
      }else {
        responseResult('error',lang('Genel.bilinmeyenHata'));
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function DetayHarita($id=0)
  {
    if (!IsAllowedViewModule('haritaIsimDuzenleyebilsin')) {
      responseResult('error',lang('Genel.yetkinYok'));
    }
    $request  = \Config\Services::request();
    $db       = \Config\Database::connect();
    $kontrol  = $this->veriModel->KontrolHarita($id,$db);
    if (!$kontrol) {
      responseResult('error',lang('VeriIslemleri.cikti.isimYok'));
    }else {
      $returnData['id']   = $kontrol->id;
      $returnData['name'] = $kontrol->name;
      echo json_encode($returnData);
      exit;
    }
  }

  public function DuzenleHarita()
  {
    if (!IsAllowedViewModule('haritaIsimDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'id'    => ['label' => lang('Genel.id'),    'rules' => "required"],
      'name'  => ['label' => lang('Genel.isim'),  'rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect();
      $kontrol  = $this->veriModel->KontrolHarita($request->getPost('id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('VeriIslemleri.cikti.isimYok'));
      }else {
        $data = [
          'id'    =>  $request->getPost('id'),
          'name'  =>  $request->getPost('name'),
        ];
        $result = $this->veriModel->GuncelleHarita($data,$kontrol->id,$db);
        if ($result) {
          LogAdd(lang('VeriIslemleri.kayit.haritaDuzenlendi',['id' => $kontrol->id, 'name' => $kontrol->name]),'VeriIslemleri/Harita',session('user_id'));
          responseResult('success',lang('VeriIslemleri.cikti.haritaDuzenlendi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function SilHarita()
  {
    if (!IsAllowedViewModule('efsunIsimSilebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'id'  => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect();
      $kontrol  = $this->veriModel->KontrolHarita($request->getPost('id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('VeriIslemleri.cikti.isimYok'));
      }else {
        $result = $this->veriModel->SilHarita($kontrol->id,$db);
        if ($result) {
          LogAdd(lang('VeriIslemleri.kayit.haritaSilindi',['id' => $kontrol->id, 'name' => $kontrol->name]),'VeriIslemleri/Harita',session('user_id'));
          responseResult('success',lang('VeriIslemleri.cikti.haritaSilindi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }
}
