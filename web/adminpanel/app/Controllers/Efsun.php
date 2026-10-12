<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class Efsun extends BaseController
{
  public $viewFolder  = "";
  public $efsunModel  = "";

  public function __construct()
  {
    $this->viewFolder = "Efsun";
    $this->efsunModel = model('Efsun_model');
    if (!session('user_id')) {
      header('Location: '.base_url('GirisYap'));
      exit;
    }
  }

  public function Index()
  {
    if (!IsAllowedViewModule('efsunlariGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    $viewData['efsunlar'] = $this->efsunModel->Efsunlar();
    return view("{$this->viewFolder}/Index",$viewData);
  }

  public function Ajax()
  {
    if (!IsAllowedViewModule('efsunlariGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect('metin2');
    $request  = \Config\Services::request();
    $siralama = ['apply','prob','lv1','lv2','lv3','lv4','lv5'];
    if ($request->getPost('search[value]')) {
      $yaz = $this->efsunModel->AjaxAra($request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }else{
      $yaz = $this->efsunModel->Ajax($request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }
    $efsunlar = $this->efsunModel->Efsunlar();
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $applySearch = array_search($value->apply,array_column($efsunlar, 'id'));
      if (isset($efsunlar[$applySearch]->name)) {
        $sub_array[] = $efsunlar[$applySearch]->name;
      }else {
        $sub_array[] = '*'.$value->apply.'*';
      }
      $sub_array[] = $value->prob;
      $sub_array[] = $value->lv1;
      $sub_array[] = $value->lv2;
      $sub_array[] = $value->lv3;
      $sub_array[] = $value->lv4;
      $sub_array[] = $value->lv5;
      if (IsAllowedViewModule('efsunDuzenleyebilsin')) {
        $sub_array[] = '<a class="btn btn-primary pt-1 pb-1 ps-2 pe-2" data-bs-toggle="modal" data-bs-target="#duzenle" href="javascript:void(0)" data-id="'.$value->apply.'">
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

  public function Detay($id=0)
  {
    if (!IsAllowedViewModule('efsunDuzenleyebilsin')) {
      responseResult('error',lang('Genel.yetkinYok'));
    }
    $request  = \Config\Services::request();
    $db       = \Config\Database::connect('metin2');
    $kontrol  = $this->efsunModel->Kontrol($id,$db);
    if (!$kontrol) {
      responseResult('error',lang('Efsun.cikti.efsunYok'));
    }else {
      $returnData['apply']          = $kontrol->apply;
      $returnData['prob']           = $kontrol->prob;
      $returnData['lv1']            = $kontrol->lv1;
      $returnData['lv2']            = $kontrol->lv2;
      $returnData['lv3']            = $kontrol->lv3;
      $returnData['lv4']            = $kontrol->lv4;
      $returnData['lv5']            = $kontrol->lv5;
      $returnData['weapon']         = $kontrol->weapon;
      $returnData['body']           = $kontrol->body;
      $returnData['wrist']          = $kontrol->wrist;
      $returnData['foots']          = $kontrol->foots;
      $returnData['neck']           = $kontrol->neck;
      $returnData['head']           = $kontrol->head;
      $returnData['shield']         = $kontrol->shield;
      $returnData['ear']            = $kontrol->ear;
      $returnData['costume_weapon'] = $kontrol->costume_weapon;
      $returnData['belt']           = $kontrol->belt;
      echo json_encode($returnData);
      exit;
    }
  }

  public function Duzenle()
  {
    if (!IsAllowedViewModule('efsunDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $efsunlar   = $this->efsunModel->Efsunlar();
    $validation->setRules([
      'apply'           => ['label' => lang('Efsun.sayfa.efsunAdi'),   'rules' => "required|in_list[".implode(',',array_column($efsunlar,'id'))."]"],
      'prob'            => ['label' => lang('Genel.sans'),    'rules' => "required|integer"],
      'lv1'             => ['label' => lang('Genel.deger'),   'rules' => "required|integer"],
      'lv2'             => ['label' => lang('Genel.deger'),   'rules' => "required|integer"],
      'lv3'             => ['label' => lang('Genel.deger'),   'rules' => "required|integer"],
      'lv4'             => ['label' => lang('Genel.deger'),   'rules' => "required|integer"],
      'lv5'             => ['label' => lang('Genel.deger'),   'rules' => "required|integer"],
      'weapon'          => ['rules' => "required|integer"],
      'body'            => ['rules' => "required|integer"],
      'wrist'           => ['rules' => "required|integer"],
      'foots'           => ['rules' => "required|integer"],
      'neck'            => ['rules' => "required|integer"],
      'head'            => ['rules' => "required|integer"],
      'shield'          => ['rules' => "required|integer"],
      'ear'             => ['rules' => "required|integer"],
      'costume_weapon'  => ['rules' => "required|integer"],
      'belt'            => ['rules' => "required|integer"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->efsunModel->Kontrol($request->getPost('apply'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Efsun.cikti.efsunYok'));
      }else {
        $data = [
          'prob'            =>  $request->getPost('prob'),
          'lv1'             =>  $request->getPost('lv1'),
          'lv2'             =>  $request->getPost('lv2'),
          'lv3'             =>  $request->getPost('lv3'),
          'lv4'             =>  $request->getPost('lv4'),
          'lv5'             =>  $request->getPost('lv5'),
          'weapon'          =>  $request->getPost('weapon'),
          'body'            =>  $request->getPost('body'),
          'wrist'           =>  $request->getPost('wrist'),
          'foots'           =>  $request->getPost('foots'),
          'neck'            =>  $request->getPost('neck'),
          'head'            =>  $request->getPost('head'),
          'shield'          =>  $request->getPost('shield'),
          'ear'             =>  $request->getPost('ear'),
          'costume_weapon'  =>  $request->getPost('costume_weapon'),
          'belt'            =>  $request->getPost('belt'),
        ];
        $result = $this->efsunModel->Guncelle($data,$kontrol->apply,$db);
        if ($result) {
          LogAdd(lang('Efsun.kayit.efsunDuzenlendi',['name' => $kontrol->apply]),'Efsun/Index',session('user_id'));
          responseResult('success',lang('Efsun.cikti.efsunDuzenlendi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Nadir()
  {
    if (!IsAllowedViewModule('nadirEfsunlariGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    $viewData['efsunlar'] = $this->efsunModel->Efsunlar();
    return view("{$this->viewFolder}/Nadir",$viewData);
  }

  public function NadirAjax()
  {
    if (!IsAllowedViewModule('nadirEfsunlariGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect('metin2');
    $request  = \Config\Services::request();
    $siralama = ['apply','prob','lv1','lv2','lv3','lv4','lv5'];
    if ($request->getPost('search[value]')) {
      $yaz = $this->efsunModel->NadirAjaxAra($request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }else{
      $yaz = $this->efsunModel->NadirAjax($request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }
    $data = [];
    $efsunlar = $this->efsunModel->Efsunlar();
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $applySearch = array_search($value->apply,array_column($efsunlar, 'id'));
      if (isset($efsunlar[$applySearch]->name)) {
        $sub_array[] = $efsunlar[$applySearch]->name;
      }else {
        $sub_array[] = '*'.$value->apply.'*';
      }
      $sub_array[] = $value->prob;
      $sub_array[] = $value->lv1;
      $sub_array[] = $value->lv2;
      $sub_array[] = $value->lv3;
      $sub_array[] = $value->lv4;
      $sub_array[] = $value->lv5;
      if (IsAllowedViewModule('efsunDuzenleyebilsin')) {
        $sub_array[] = '<a class="btn btn-primary pt-1 pb-1 ps-2 pe-2" data-bs-toggle="modal" data-bs-target="#duzenle" href="javascript:void(0)" data-id="'.$value->apply.'">
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

  public function NadirDetay($id=0)
  {
    if (!IsAllowedViewModule('nadirEfsunDuzenleyebilsin')) {
      responseResult('error',lang('Genel.yetkinYok'));
    }
    $request  = \Config\Services::request();
    $db       = \Config\Database::connect('metin2');
    $kontrol  = $this->efsunModel->NadirKontrol($id,$db);
    if (!$kontrol) {
      responseResult('error',lang('Efsun.cikti.efsunYok'));
    }else {
      $returnData['apply']          = $kontrol->apply;
      $returnData['prob']           = $kontrol->prob;
      $returnData['lv1']            = $kontrol->lv1;
      $returnData['lv2']            = $kontrol->lv2;
      $returnData['lv3']            = $kontrol->lv3;
      $returnData['lv4']            = $kontrol->lv4;
      $returnData['lv5']            = $kontrol->lv5;
      $returnData['weapon']         = $kontrol->weapon;
      $returnData['body']           = $kontrol->body;
      $returnData['wrist']          = $kontrol->wrist;
      $returnData['foots']          = $kontrol->foots;
      $returnData['neck']           = $kontrol->neck;
      $returnData['head']           = $kontrol->head;
      $returnData['shield']         = $kontrol->shield;
      $returnData['ear']            = $kontrol->ear;
      $returnData['costume_body']   = $kontrol->costume_body;
      $returnData['costume_hair']   = $kontrol->costume_hair;
      $returnData['costume_weapon'] = $kontrol->costume_weapon;
      echo json_encode($returnData);
      exit;
    }
  }

  public function NadirDuzenle()
  {
    if (!IsAllowedViewModule('nadirEfsunDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $efsunlar   = $this->efsunModel->Efsunlar();
    $validation->setRules([
      'apply'           => ['label' => lang('Efsun.sayfa.efsunAdi'),   'rules' => "required|in_list[".implode(',',array_column($efsunlar,'id'))."]"],
      'prob'            => ['label' => lang('Genel.sans'),    'rules' => "required|integer"],
      'lv1'             => ['label' => lang('Genel.deger'),   'rules' => "required|integer"],
      'lv2'             => ['label' => lang('Genel.deger'),   'rules' => "required|integer"],
      'lv3'             => ['label' => lang('Genel.deger'),   'rules' => "required|integer"],
      'lv4'             => ['label' => lang('Genel.deger'),   'rules' => "required|integer"],
      'lv5'             => ['label' => lang('Genel.deger'),   'rules' => "required|integer"],
      'weapon'          => ['rules' => "required|integer"],
      'body'            => ['rules' => "required|integer"],
      'wrist'           => ['rules' => "required|integer"],
      'foots'           => ['rules' => "required|integer"],
      'neck'            => ['rules' => "required|integer"],
      'head'            => ['rules' => "required|integer"],
      'shield'          => ['rules' => "required|integer"],
      'ear'             => ['rules' => "required|integer"],
      'costume_body'    => ['rules' => "required|integer"],
      'costume_hair'    => ['rules' => "required|integer"],
      'costume_weapon'  => ['rules' => "required|integer"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->efsunModel->NadirKontrol($request->getPost('apply'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Efsun.cikti.efsunYok'));
      }else {
        $data = [
          'prob'            =>  $request->getPost('prob'),
          'lv1'             =>  $request->getPost('lv1'),
          'lv2'             =>  $request->getPost('lv2'),
          'lv3'             =>  $request->getPost('lv3'),
          'lv4'             =>  $request->getPost('lv4'),
          'lv5'             =>  $request->getPost('lv5'),
          'weapon'          =>  $request->getPost('weapon'),
          'body'            =>  $request->getPost('body'),
          'wrist'           =>  $request->getPost('wrist'),
          'foots'           =>  $request->getPost('foots'),
          'neck'            =>  $request->getPost('neck'),
          'head'            =>  $request->getPost('head'),
          'shield'          =>  $request->getPost('shield'),
          'ear'             =>  $request->getPost('ear'),
          'costume_body'    =>  $request->getPost('costume_body'),
          'costume_hair'    =>  $request->getPost('costume_hair'),
          'costume_weapon'  =>  $request->getPost('costume_weapon'),
        ];
        $result = $this->efsunModel->NadirGuncelle($data,$kontrol->apply,$db);
        if ($result) {
          LogAdd(lang('Efsun.kayit.nadirEfsunDuzenlendi',['name' => $kontrol->apply]),'Efsun/Nadir',session('user_id'));
          responseResult('success',lang('Efsun.cikti.nadirEfsunDuzenlendi'));
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
    if (!IsAllowedViewModule('efsunDuzenleyebilsin') && !IsAllowedViewModule('nadirEfsunDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    if (p2pStatus==0) {
      responseResult('error',lang('Genel.p2pKapali'));
    }
    foreach (p2pPorts as $key => $value) {
      SendServer('P',"RELOAD",$value);
    }
    LogAdd(lang('Efsun.cikti.sunucuyaGonderildi'),'Efsun/Index',session('user_id'));
    responseResult('success',lang('Efsun.cikti.sunucuyaGonderildi'));
  }
}
