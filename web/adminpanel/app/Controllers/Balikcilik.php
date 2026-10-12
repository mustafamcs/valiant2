<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class Balikcilik extends BaseController
{
  public $viewFolder      = "";
  public $balikcilikModel = "";

  public function __construct()
  {
    $this->viewFolder       = "Balikcilik";
    $this->balikcilikModel  = model('Balikcilik_model');
    if (!session('user_id')) {
      header('Location: '.base_url('GirisYap'));
      exit;
    }
  }

  public function Index()
  {
    if (!IsAllowedViewModule('balikcilikGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Index",$viewData);
  }

  public function Ajax()
  {
    if (!IsAllowedViewModule('balikcilikGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect('metin2');
    $request  = \Config\Services::request();
    $siralama = ['vnum','chance'];
    if ($request->getPost('search[value]')) {
      $yaz = $this->balikcilikModel->AjaxAra($request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }else{
      $yaz = $this->balikcilikModel->Ajax($request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->vnum.' - '.mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9");
      $sub_array[] = $value->chance;
      if (IsAllowedViewModule('balikcilikDuzenleyebilsin') || IsAllowedViewModule('balikcilikSilebilsin')) {
        $buttons = "";
        if (IsAllowedViewModule('balikcilikDuzenleyebilsin')) {
          $buttons .= '<a class="btn btn-primary pt-1 pb-1 ps-2 pe-2" data-bs-toggle="modal" data-bs-target="#duzenle" href="javascript:void(0)" data-locale_name="'.mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9").'" data-vnum="'.$value->vnum.'" data-chance="'.$value->chance.'">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" style="width:25px;height:25px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 7h-3a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-3" /><path d="M9 15h3l8.5 -8.5a1.5 1.5 0 0 0 -3 -3l-8.5 8.5v3" /><line x1="16" y1="5" x2="19" y2="8" /></svg>
          </a>';
        }
        if (IsAllowedViewModule('balikcilikSilebilsin')) {
          $buttons .= '<a class="btn btn-danger pt-1 pb-1 ps-2 pe-2 ms-2 esyaSil" href="javascript:void(0)" data-vnum="'.$value->vnum.'" data-chance="'.$value->chance.'" data-header="'.lang('Genel.silBaslik').'" data-message="'.lang('Genel.buIslemGeriAlinamaz').'" data-yes="'.lang('Genel.evet').'" data-no="'.lang('Genel.hayir').'">
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
    if (!IsAllowedViewModule('balikcilikEkleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'vnum'    => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'chance'  => ['label' => lang('Genel.sans'),  'rules' => "required|integer"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db          = \Config\Database::connect('metin2');
      $esyaKontrol = $this->balikcilikModel->ItemProtoKontrol($request->getPost('vnum'),$db);
      if (!$esyaKontrol) {
        responseResult('error',lang('Esya.cikti.esyaYok'));
      }
      $data = [
        'vnum'    =>  $request->getPost('vnum'),
        'chance'  =>  $request->getPost('chance'),
      ];
      $result = $this->balikcilikModel->Ekle($data,$db);
      if ($result) {
        LogAdd(lang('Balikcilik.kayit.balikcilikEklendi',[ 'item' => mb_convert_encoding((isset($esyaKontrol->locale_name)?$esyaKontrol->locale_name:$request->getPost('vnum')), 'UTF-8' ,"ISO-8859-9") ]),'Balikcilik/Index',session('user_id'));
        responseResult('success',lang('Balikcilik.cikti.balikcilikEklendi'));
      }else {
        responseResult('error',lang('Genel.bilinmeyenHata'));
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Duzenle()
  {
    if (!IsAllowedViewModule('balikcilikDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'vnum'      => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'chance'    => ['label' => lang('Genel.sans'),  'rules' => "required|integer"],
      'newChance' => ['label' => lang('Genel.sans'),  'rules' => "required|integer"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db           = \Config\Database::connect('metin2');
      $esyaKontrol  = $this->balikcilikModel->Kontrol($request->getPost('vnum'),$request->getPost('chance'),$db);
      if (!$esyaKontrol) {
        responseResult('error',lang('Esya.cikti.esyaYok'));
      }else {
        $data = [
          'chance'  =>  $request->getPost('newChance'),
        ];
        $result = $this->balikcilikModel->Guncelle($data,$esyaKontrol->vnum,$esyaKontrol->chance,$db);
        if ($result) {
          LogAdd(lang('Balikcilik.kayit.balikcilikDuzenlendi',[ 'item' => mb_convert_encoding((isset($esyaKontrol->locale_name)?$esyaKontrol->locale_name:$esyaKontrol->vnum), 'UTF-8' ,"ISO-8859-9") ]),'Balikcilik/Index',session('user_id'));
          responseResult('success',lang('Balikcilik.cikti.balikcilikDuzenlendi'));
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
    if (!IsAllowedViewModule('balikcilikSilebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'vnum'      => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'chance'    => ['label' => lang('Genel.sans'),  'rules' => "required|integer"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db           = \Config\Database::connect('metin2');
      $esyaKontrol  = $this->balikcilikModel->Kontrol($request->getPost('vnum'),$request->getPost('chance'),$db);
      if (!$esyaKontrol) {
        responseResult('error',lang('Esya.cikti.esyaYok'));
      }else {
        $result = $this->balikcilikModel->Sil($esyaKontrol->vnum,$esyaKontrol->chance,$db);
        if ($result) {
          LogAdd(lang('Balikcilik.kayit.balikcilikSilindi',[ 'item' => mb_convert_encoding((isset($esyaKontrol->locale_name)?$esyaKontrol->locale_name:$esyaKontrol->vnum), 'UTF-8' ,"ISO-8859-9") ]),'Balikcilik/Index',session('user_id'));
          responseResult('success',lang('Balikcilik.cikti.balikcilikSilindi'));
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
    if (!IsAllowedViewModule('balikcilikDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    if (p2pStatus==0) {
      responseResult('error',lang('Genel.p2pKapali'));
    }
    foreach (p2pPorts as $key => $value) {
      SendServer('P',"RELOAD",$value);
    }
    LogAdd(lang('Balikcilik.cikti.sunucuyaGonderildi'),'Balikcilik/Index',session('user_id'));
    responseResult('success',lang('Balikcilik.cikti.sunucuyaGonderildi'));
  }
}
