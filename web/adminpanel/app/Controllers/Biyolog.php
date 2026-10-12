<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class Biyolog extends BaseController
{
  public $viewFolder    = "";
  public $biyologModel  = "";

  public function __construct()
  {
    $this->viewFolder   = "Biyolog";
    $this->biyologModel = model('Biyolog_model');
    if (!session('user_id')) {
      header('Location: '.base_url('GirisYap'));
      exit;
    }
  }

  public function Index()
  {
    if (!IsAllowedViewModule('biyologGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Index",$viewData);
  }

  public function Ajax()
  {
    if (!IsAllowedViewModule('biyologGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect('metin2');
    $request  = \Config\Services::request();
    $siralama = ['mobVnum','level','item_vnum','soul_vnum'];
    if ($request->getPost('search[value]')) {
      $yaz = $this->biyologModel->AjaxAra($request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }else{
      $yaz = $this->biyologModel->Ajax($request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->mobVnum;
      $sub_array[] = $value->level;
      $item_vnum = $this->biyologModel->ItemProtoKontrol($value->item_vnum);
      $sub_array[] = $value->item_vnum.(isset($item_vnum->locale_name)?' - '.mb_convert_encoding($item_vnum->locale_name, 'UTF-8' ,"ISO-8859-9"):'');
      $soul_vnum = $this->biyologModel->ItemProtoKontrol($value->soul_vnum);
      $sub_array[] = $value->soul_vnum.(isset($soul_vnum->locale_name)?' - '.mb_convert_encoding($soul_vnum->locale_name, 'UTF-8' ,"ISO-8859-9"):'');
      if (IsAllowedViewModule('biyologDuzenleyebilsin') || IsAllowedViewModule('biyologSilebilsin')) {
        $buttons = "";
        if (IsAllowedViewModule('biyologDuzenleyebilsin')) {
          $buttons .= '<a class="btn btn-primary pt-1 pb-1 ps-2 pe-2" data-bs-toggle="modal" data-bs-target="#duzenle" href="javascript:void(0)" data-id="'.$value->mobVnum.'">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" style="width:25px;height:25px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 7h-3a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-3" /><path d="M9 15h3l8.5 -8.5a1.5 1.5 0 0 0 -3 -3l-8.5 8.5v3" /><line x1="16" y1="5" x2="19" y2="8" /></svg>
          </a>';
        }
        if (IsAllowedViewModule('biyologSilebilsin')) {
          $buttons .= '<a class="btn btn-danger pt-1 pb-1 ps-2 pe-2 ms-2 biyologSil" href="javascript:void(0)" data-id="'.$value->mobVnum.'" data-header="'.lang('Genel.silBaslik').'" data-message="'.lang('Genel.buIslemGeriAlinamaz').'" data-yes="'.lang('Genel.evet').'" data-no="'.lang('Genel.hayir').'">
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
    if (!IsAllowedViewModule('biyologEkleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'mobVnum'     => ['label' => lang('Genel.canavar'),             'rules' => "required|integer"],
      'level'       => ['label' => lang('Genel.seviye'),              'rules' => "required|integer"],
      'aff_type'    => ['label' => lang('Biyolog.sayfa.aff_type'),    'rules' => "required|integer"],
      'aff_value'   => ['label' => lang('Biyolog.sayfa.aff_value'),   'rules' => "required|integer"],
      'aff_type2'   => ['label' => lang('Biyolog.sayfa.aff_type2'),   'rules' => "required|integer"],
      'aff_value2'  => ['label' => lang('Biyolog.sayfa.aff_value2'),  'rules' => "required|integer"],
      'aff_type3'   => ['label' => lang('Biyolog.sayfa.aff_type3'),   'rules' => "required|integer"],
      'aff_value3'  => ['label' => lang('Biyolog.sayfa.aff_value3'),  'rules' => "required|integer"],
      'aff_type4'   => ['label' => lang('Biyolog.sayfa.aff_type4'),   'rules' => "required|integer"],
      'aff_value4'  => ['label' => lang('Biyolog.sayfa.aff_value4'),  'rules' => "required|integer"],
      'req_count'   => ['label' => lang('Biyolog.sayfa.req_count'),   'rules' => "required|integer"],
      'cool_time'   => ['label' => lang('Biyolog.sayfa.cool_time'),   'rules' => "required|integer"],
      'chance'      => ['label' => lang('Genel.sans'),                'rules' => "required|integer"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db               = \Config\Database::connect('metin2');
      $kontrol  = $this->biyologModel->Kontrol($request->getPost('mobVnum'),$db);
      if ($kontrol) {
        responseResult('error',lang('Biyolog.cikti.zatenEkli'));
      }
      if ($request->getPost('item_vnum')) {
        $itemKontrol  = $this->biyologModel->ItemProtoKontrol($request->getPost('item_vnum'));
        if (!$itemKontrol) {
          responseResult('error',lang('Esya.cikti.esyaYok'));
        }
      }
      if ($request->getPost('soul_vnum')) {
        $itemKontrol  = $this->biyologModel->ItemProtoKontrol($request->getPost('soul_vnum'));
        if (!$itemKontrol) {
          responseResult('error',lang('Esya.cikti.esyaYok'));
        }
      }
      $data = [
        'mobVnum'     =>  $request->getPost('mobVnum'),
        'level'       =>  $request->getPost('level'),
        'aff_type'    =>  $request->getPost('aff_type'),
        'aff_value'   =>  $request->getPost('aff_value'),
        'aff_type2'   =>  $request->getPost('aff_type2'),
        'aff_value2'  =>  $request->getPost('aff_value2'),
        'aff_type3'   =>  $request->getPost('aff_type3'),
        'aff_value3'  =>  $request->getPost('aff_value3'),
        'aff_type4'   =>  $request->getPost('aff_type4'),
        'aff_value4'  =>  $request->getPost('aff_value4'),
        'item_vnum'   =>  ($request->getPost('item_vnum')?$request->getPost('item_vnum'):0),
        'soul_vnum'   =>  ($request->getPost('soul_vnum')?$request->getPost('soul_vnum'):0),
        'req_count'   =>  $request->getPost('req_count'),
        'cool_time'   =>  $request->getPost('cool_time'),
        'chance'      =>  $request->getPost('chance'),
      ];
      $result = $this->biyologModel->Ekle($data,$db);
      if ($result) {
        LogAdd(lang('Biyolog.kayit.biyologEklendi',[ 'vnum' => $request->getPost('mobVnum') ]),'Biyolog/Index',session('user_id'));
        responseResult('success',lang('Biyolog.cikti.biyologEklendi'));
      }else {
        responseResult('error',lang('Genel.bilinmeyenHata'));
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Detay($id=0)
  {
    if (!IsAllowedViewModule('biyologDuzenleyebilsin')) {
      responseResult('error',lang('Genel.yetkinYok'));
    }
    $request  = \Config\Services::request();
    $db       = \Config\Database::connect('metin2');
    $kontrol  = $this->biyologModel->Kontrol($id,$db);
    if (!$kontrol) {
      responseResult('error',lang('Biyolog.cikti.biyologYok'));
    }else {
      $returnData['level']        = $kontrol->level;
      $returnData['aff_type']     = $kontrol->aff_type;
      $returnData['aff_value']    = $kontrol->aff_value;
      $returnData['aff_type2']    = $kontrol->aff_type2;
      $returnData['aff_value2']   = $kontrol->aff_value2;
      $returnData['aff_type3']    = $kontrol->aff_type3;
      $returnData['aff_value3']   = $kontrol->aff_value3;
      $returnData['aff_type4']    = $kontrol->aff_type4;
      $returnData['aff_value4']   = $kontrol->aff_value4;
      $item_vnum = $this->biyologModel->ItemProtoKontrol($kontrol->item_vnum);
      $returnData['item_vnum']['vnum']  = $kontrol->item_vnum;
      $returnData['item_vnum']['name']  = (isset($item_vnum->locale_name)?mb_convert_encoding($item_vnum->locale_name, 'UTF-8' ,"ISO-8859-9"):'');
      $soul_vnum = $this->biyologModel->ItemProtoKontrol($kontrol->soul_vnum);
      $returnData['soul_vnum']['vnum']  = $kontrol->soul_vnum;
      $returnData['soul_vnum']['name']  = (isset($soul_vnum->locale_name)?mb_convert_encoding($soul_vnum->locale_name, 'UTF-8' ,"ISO-8859-9"):'');
      $returnData['req_count']    = $kontrol->req_count;
      $returnData['cool_time']    = $kontrol->cool_time;
      $returnData['chance']       = $kontrol->chance;
      $returnData['mobVnum']      = $kontrol->mobVnum;
      echo json_encode($returnData);
      exit;
    }
  }

  public function Duzenle()
  {
    if (!IsAllowedViewModule('biyologDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'mobVnum'     => ['label' => lang('Genel.canavar'),             'rules' => "required|integer"],
      'level'       => ['label' => lang('Genel.seviye'),              'rules' => "required|integer"],
      'aff_type'    => ['label' => lang('Biyolog.sayfa.aff_type'),    'rules' => "required|integer"],
      'aff_value'   => ['label' => lang('Biyolog.sayfa.aff_value'),   'rules' => "required|integer"],
      'aff_type2'   => ['label' => lang('Biyolog.sayfa.aff_type2'),   'rules' => "required|integer"],
      'aff_value2'  => ['label' => lang('Biyolog.sayfa.aff_value2'),  'rules' => "required|integer"],
      'aff_type3'   => ['label' => lang('Biyolog.sayfa.aff_type3'),   'rules' => "required|integer"],
      'aff_value3'  => ['label' => lang('Biyolog.sayfa.aff_value3'),  'rules' => "required|integer"],
      'aff_type4'   => ['label' => lang('Biyolog.sayfa.aff_type4'),   'rules' => "required|integer"],
      'aff_value4'  => ['label' => lang('Biyolog.sayfa.aff_value4'),  'rules' => "required|integer"],
      'req_count'   => ['label' => lang('Biyolog.sayfa.req_count'),   'rules' => "required|integer"],
      'cool_time'   => ['label' => lang('Biyolog.sayfa.cool_time'),   'rules' => "required|integer"],
      'chance'      => ['label' => lang('Genel.sans'),                'rules' => "required|integer"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->biyologModel->Kontrol($request->getPost('mobVnum'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Biyolog.cikti.biyologYok'));
      }
      if ($request->getPost('item_vnum')) {
        $itemKontrol  = $this->biyologModel->ItemProtoKontrol($request->getPost('item_vnum'),$db);
        if (!$itemKontrol) {
          responseResult('error',lang('Esya.cikti.esyaYok'));
        }
      }
      if ($request->getPost('soul_vnum')) {
        $itemKontrol  = $this->biyologModel->ItemProtoKontrol($request->getPost('soul_vnum'),$db);
        if (!$itemKontrol) {
          responseResult('error',lang('Esya.cikti.esyaYok'));
        }
      }
      $data = [
        'level'       =>  $request->getPost('level'),
        'aff_type'    =>  $request->getPost('aff_type'),
        'aff_value'   =>  $request->getPost('aff_value'),
        'aff_type2'   =>  $request->getPost('aff_type2'),
        'aff_value2'  =>  $request->getPost('aff_value2'),
        'aff_type3'   =>  $request->getPost('aff_type3'),
        'aff_value3'  =>  $request->getPost('aff_value3'),
        'aff_type4'   =>  $request->getPost('aff_type4'),
        'aff_value4'  =>  $request->getPost('aff_value4'),
        'item_vnum'   =>  ($request->getPost('item_vnum')?$request->getPost('item_vnum'):0),
        'soul_vnum'   =>  ($request->getPost('soul_vnum')?$request->getPost('soul_vnum'):0),
        'req_count'   =>  $request->getPost('req_count'),
        'cool_time'   =>  $request->getPost('cool_time'),
        'chance'      =>  $request->getPost('chance'),
      ];
      $result = $this->biyologModel->Guncelle($data,$kontrol->mobVnum,$db);
      if ($result) {
        LogAdd(lang('Biyolog.kayit.biyologDuzenlendi',[ 'vnum' => $kontrol->mobVnum ]),'Biyolog/Index',session('user_id'));
        responseResult('success',lang('Biyolog.cikti.biyologDuzenlendi'));
      }else {
        responseResult('error',lang('Genel.bilinmeyenHata'));
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Sil()
  {
    if (!IsAllowedViewModule('biyologSilebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'mobVnum'  => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->biyologModel->Kontrol($request->getPost('mobVnum'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Biyolog.cikti.biyologYok'));
      }else {
        $result = $this->biyologModel->Sil($kontrol->mobVnum,$db);
        if ($result) {
          LogAdd(lang('Biyolog.kayit.biyologSilindi',[ 'vnum' => $kontrol->mobVnum ]),'Biyolog/Index',session('user_id'));
          responseResult('success',lang('Biyolog.cikti.biyologSilindi'));
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
    if (!IsAllowedViewModule('biyologDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    if (p2pStatus==0) {
      responseResult('error',lang('Genel.p2pKapali'));
    }
    foreach (p2pPorts as $key => $value) {
      SendServer('P',"RELOAD",$value);
    }
    LogAdd(lang('Biyolog.cikti.sunucuyaGonderildi'),'Biyolog/Index',session('user_id'));
    responseResult('success',lang('Biyolog.cikti.sunucuyaGonderildi'));
  }
}
