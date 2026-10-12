<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class NPC extends BaseController
{
  public $viewFolder  = "";
  public $npcModel    = "";

  public function __construct()
  {
    $this->viewFolder = "NPC";
    $this->npcModel   = model('NPC_model');
    if (!session('user_id')) {
      header('Location: '.base_url('GirisYap'));
      exit;
    }
  }

  public function Index()
  {
    if (!IsAllowedViewModule('npcGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Index",$viewData);
  }

  public function Ajax()
  {
    if (!IsAllowedViewModule('npcGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect('metin2');
    $request  = \Config\Services::request();
    $siralama = ['vnum','name','npc_vnum'];
    if ($request->getPost('search[value]')) {
      $yaz = $this->npcModel->AjaxAra($request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }else{
      $yaz = $this->npcModel->Ajax($request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->vnum;
      $sub_array[] = $value->name;
      $sub_array[] = $value->npc_vnum.' - '.mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9");
      if (IsAllowedViewModule('npcDuzenleyebilsin') || IsAllowedViewModule('npcSilebilsin')) {
        $buttons = "";
        if (IsAllowedViewModule('npcDuzenleyebilsin')) {
          $buttons .= '<a class="btn btn-primary pt-1 pb-1 ps-2 pe-2" data-bs-toggle="modal" data-bs-target="#duzenle" href="javascript:void(0)" data-id="'.$value->vnum.'">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" style="width:25px;height:25px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 7h-3a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-3" /><path d="M9 15h3l8.5 -8.5a1.5 1.5 0 0 0 -3 -3l-8.5 8.5v3" /><line x1="16" y1="5" x2="19" y2="8" /></svg>
          </a>';
        }
        if (IsAllowedViewModule('npcSilebilsin')) {
          $buttons .= '<a class="btn btn-danger pt-1 pb-1 ps-2 pe-2 ms-2 npcSil" href="javascript:void(0)" data-id="'.$value->vnum.'" data-header="'.lang('Genel.silBaslik').'" data-message="'.lang('Genel.buIslemGeriAlinamaz').'" data-yes="'.lang('Genel.evet').'" data-no="'.lang('Genel.hayir').'">
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
    if (!IsAllowedViewModule('npcEkleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'vnum'      => ['label' => 'ID',              'rules' => "required|integer"],
      'name'      => ['label' => lang('Genel.adi'), 'rules' => "required"],
      'npc_vnum'  => ['label' => 'NPC',             'rules' => "required|integer"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->npcModel->Kontrol($request->getPost('vnum'),$db);
      if ($kontrol) {
        responseResult('error',lang('NPC.cikti.zatenEkli'));
      }
      if ($request->getPost('npc_vnum')) {
        $canavarKontrol  = $this->npcModel->MobProtoKontrol($request->getPost('npc_vnum'),$db);
        if (!$canavarKontrol) {
          responseResult('error',lang('Canavar.cikti.canavarYok'));
        }
      }
      $data = [
        'vnum'      =>  $request->getPost('vnum'),
        'name'      =>  mb_convert_encoding($request->getPost('name'), 'ISO-8859-9' ,"UTF-8"),
        'npc_vnum'  =>  ($request->getPost('npc_vnum')?$request->getPost('npc_vnum'):0),
      ];
      $result = $this->npcModel->Ekle($data,$db);
      if ($result) {
        LogAdd(lang('NPC.kayit.npcEklendi',[ 'name' => $request->getPost('name') ]),'NPC/Index',session('user_id'));
        responseResult('success',lang('NPC.cikti.npcEklendi'));
      }else {
        responseResult('error',lang('Genel.bilinmeyenHata'));
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Detay($id=0)
  {
    if (!IsAllowedViewModule('npcDuzenleyebilsin')) {
      responseResult('error',lang('Genel.yetkinYok'));
    }
    $request  = \Config\Services::request();
    $db       = \Config\Database::connect('metin2');
    $kontrol  = $this->npcModel->Kontrol($id,$db);
    if (!$kontrol) {
      responseResult('error',lang('NPC.cikti.npcYok'));
    }else {
      $returnData['vnum']             = $kontrol->vnum;
      $returnData['name']             = mb_convert_encoding($kontrol->name, 'UTF-8' ,"ISO-8859-9");
      $returnData['npc_vnum']['vnum'] = $kontrol->npc_vnum;
      $returnData['npc_vnum']['name'] = mb_convert_encoding($kontrol->locale_name, 'UTF-8' ,"ISO-8859-9");
      echo json_encode($returnData);
      exit;
    }
  }

  public function Duzenle()
  {
    if (!IsAllowedViewModule('npcDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'newVnum'   => ['label' => 'ID',              'rules' => "required|integer"],
      'name'      => ['label' => lang('Genel.adi'), 'rules' => "required"],
      'npc_vnum'  => ['label' => 'NPC',             'rules' => "required|integer"],
      'vnum'      => ['label' => 'ID',              'rules' => "required|integer"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->npcModel->Kontrol($request->getPost('vnum'),$db);
      if (!$kontrol) {
        responseResult('error',lang('NPC.cikti.npcYok'));
      }
      if ($request->getPost('npc_vnum')) {
        $canavarKontrol  = $this->npcModel->MobProtoKontrol($request->getPost('npc_vnum'),$db);
        if (!$canavarKontrol) {
          responseResult('error',lang('Canavar.cikti.canavarYok'));
        }
      }
      $data = [
        'vnum'      =>  $request->getPost('newVnum'),
        'name'      =>  mb_convert_encoding($request->getPost('name'), 'ISO-8859-9' ,"UTF-8"),
        'npc_vnum'  =>  ($request->getPost('npc_vnum')?$request->getPost('npc_vnum'):0),
      ];
      $result = $this->npcModel->Guncelle($data,$kontrol->vnum,$db);
      if ($result) {
        LogAdd(lang('NPC.kayit.npcDuzenlendi',[ 'name' => mb_convert_encoding($kontrol->name, 'UTF-8' ,"ISO-8859-9") ]),'NPC/Index',session('user_id'));
        responseResult('success',lang('NPC.cikti.npcDuzenlendi'));
      }else {
        responseResult('error',lang('Genel.bilinmeyenHata'));
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Sil()
  {
    if (!IsAllowedViewModule('npcSilebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'vnum'  => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->npcModel->Kontrol($request->getPost('vnum'),$db);
      if (!$kontrol) {
        responseResult('error',lang('NPC.cikti.npcYok'));
      }else {
        $result = $this->npcModel->Sil($kontrol->vnum,$db);
        if ($result) {
          LogAdd(lang('NPC.kayit.npcSilindi',[ 'name' => mb_convert_encoding($kontrol->name, 'UTF-8' ,"ISO-8859-9") ]),'NPC/Index',session('user_id'));
          responseResult('success',lang('NPC.cikti.npcSilindi'));
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
    if (!IsAllowedViewModule('npcEkleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    if (p2pStatus==0) {
      responseResult('error',lang('Genel.p2pKapali'));
    }
    foreach (p2pPorts as $key => $value) {
      SendServer('P',"RELOAD",$value);
    }
    LogAdd(lang('NPC.cikti.sunucuyaGonderildi'),'NPC/Index',session('user_id'));
    responseResult('success',lang('NPC.cikti.sunucuyaGonderildi'));
  }

  public function Esyalar($shop_vnum = 0)
  {
    if (!IsAllowedViewModule('npcDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect('metin2');
    $request  = \Config\Services::request();
    $kontrol  = $this->npcModel->Kontrol($shop_vnum,$db);
    if (!$kontrol) {
      responseResult('error',lang('NPC.cikti.npcYok'));
    }
    $siralama = ['item_vnum','count'];
    $query    = "SELECT shop_item.shop_vnum, shop_item.item_vnum, shop_item.count, item_proto.locale_name FROM player.shop_item ";
    $query    .= "LEFT JOIN player.item_proto on player.item_proto.vnum=player.shop_item.item_vnum ";
    $query    .= " WHERE shop_vnum = ".$kontrol->vnum;

    if (
      isset($siralama[$request->getPost('order[0][column]')])
      && in_array($request->getPost('order[0][dir]'),['asc','desc'])
    ) {
      $query  .= " ORDER BY ".$siralama[$request->getPost('order[0][column]')].' '.addslashes(addcslashes($request->getPost('order[0][dir]'),'%'));
    }

    $yaz  = $this->npcModel->Query($query,$db);
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $itemIcon = $this->npcModel->ItemIcon($value->item_vnum);
      if (!empty($itemIcon) && $itemIcon!="-") {
        $sub_array[] = '<img src="'.base_url('assets/img/icon/'.$itemIcon->icon).'" title="'.$value->item_vnum.'"> '.$value->item_vnum.' - '.mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9");
      }else {
        $sub_array[] = $value->item_vnum.' - '.mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9");
      }
      $sub_array[] = $value->count;
      $buttons  =  '<a class="btn btn-primary pt-1 pb-1 ps-2 pe-2" data-bs-toggle="modal" data-bs-target="#esyaDuzenle" href="javascript:void(0)" data-locale_name="'.mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9").'" data-item_vnum="'.$value->item_vnum.'" data-count="'.$value->count.'">
        <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" style="width:25px;height:25px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 7h-3a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-3" /><path d="M9 15h3l8.5 -8.5a1.5 1.5 0 0 0 -3 -3l-8.5 8.5v3" /><line x1="16" y1="5" x2="19" y2="8" /></svg>
      </a>';
      $buttons .=  '<a class="btn btn-danger pt-1 pb-1 ps-2 pe-2 ms-2 esyaSil" href="javascript:void(0)" data-shop_vnum="'.$value->shop_vnum.'" data-item_vnum="'.$value->item_vnum.'" data-count="'.$value->count.'">
        <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" style="width:25px;height:25px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><line x1="4" y1="7" x2="20" y2="7" /><line x1="10" y1="11" x2="10" y2="17" /><line x1="14" y1="11" x2="14" y2="17" /><path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12" /><path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3" /></svg>
      </a>';
      $sub_array[] = $buttons;
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

  public function EsyaEkle()
  {
    if (!IsAllowedViewModule('npcDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'item_vnum' => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'count'     => ['label' => lang('Genel.adet'),  'rules' => "required|integer"],
      'shop_vnum' => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->npcModel->Kontrol($request->getPost('shop_vnum'),$db);
      if (!$kontrol) {
        responseResult('error',lang('NPC.cikti.npcYok'));
      }else {
        $esyaKontrol  = $this->npcModel->ItemProtoKontrol($request->getPost('item_vnum'),$db);
        if (!$esyaKontrol) {
          responseResult('error',lang('Esya.cikti.esyaYok'));
        }
        $ekliMi  = $this->npcModel->EsyaKontrol($kontrol->vnum,$esyaKontrol->vnum,$request->getPost('count'),$db);
        if ($ekliMi) {
          responseResult('error',lang('NPC.cikti.esyaZatenEkli'));
        }
        $data = [
          'shop_vnum' =>  $kontrol->vnum,
          'item_vnum' =>  $esyaKontrol->vnum,
          'count'     =>  $request->getPost('count'),
        ];
        $result = $this->npcModel->EsyaEkle($data,$db);
        if ($result) {
          LogAdd(lang('NPC.kayit.esyaEklendi',['name' => mb_convert_encoding($kontrol->name, 'UTF-8' ,"ISO-8859-9"), 'item' => mb_convert_encoding($esyaKontrol->locale_name, 'UTF-8' ,"ISO-8859-9")]),'NPC/Index',session('user_id'));
          responseResult('success',lang('NPC.cikti.esyaEklendi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function EsyaGuncelle()
  {
    if (!IsAllowedViewModule('npcDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'edit_item_vnum'  => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'edit_count'      => ['label' => lang('Genel.adet'),  'rules' => "required|integer"],
      'shop_vnum'       => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->npcModel->EsyaKontrol($request->getPost('shop_vnum'),$request->getPost('edit_item_vnum'),$request->getPost('edit_count'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Esya.cikti.esyaYok'));
      }else {
        $data = [
          'count' =>  $request->getPost('new_count'),
        ];

        $npcKontrol   = $this->npcModel->Kontrol($kontrol->shop_vnum,$db);
        $esyaKontrol  = $this->npcModel->ItemProtoKontrol($kontrol->item_vnum,$db);

        $result = $this->npcModel->EsyaGuncelle($data,$kontrol->shop_vnum,$kontrol->item_vnum,$kontrol->count,$db);
        if ($result) {
          LogAdd(lang('NPC.kayit.esyaDuzenlendi',['name' => mb_convert_encoding((isset($npcKontrol->name)?$npcKontrol->name:$kontrol->shop_vnum), 'UTF-8' ,"ISO-8859-9"), 'item' => mb_convert_encoding((isset($esyaKontrol->locale_name)?$esyaKontrol->locale_name:$kontrol->item_vnum), 'UTF-8' ,"ISO-8859-9")]),'NPC/Index',session('user_id'));
          responseResult('success',lang('NPC.cikti.esyaDuzenlendi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function EsyaSil()
  {
    if (!IsAllowedViewModule('npcDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'item_vnum'   => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'count'       => ['label' => lang('Genel.adet'),  'rules' => "required|integer"],
      'shop_vnum'   => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->npcModel->EsyaKontrol($request->getPost('shop_vnum'),$request->getPost('item_vnum'),$request->getPost('count'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Esya.cikti.esyaYok'));
      }else {
        $npcKontrol   = $this->npcModel->Kontrol($kontrol->shop_vnum,$db);
        $esyaKontrol  = $this->npcModel->ItemProtoKontrol($kontrol->item_vnum,$db);

        $result = $this->npcModel->EsyaSil($kontrol->shop_vnum,$kontrol->item_vnum,$kontrol->count,$db);
        if ($result) {
          LogAdd(lang('NPC.kayit.esyaSilindi',['name' => mb_convert_encoding((isset($npcKontrol->name)?$npcKontrol->name:$kontrol->shop_vnum), 'UTF-8' ,"ISO-8859-9"), 'item' => mb_convert_encoding((isset($esyaKontrol->locale_name)?$esyaKontrol->locale_name:$kontrol->item_vnum), 'UTF-8' ,"ISO-8859-9")]),'NPC/Index',session('user_id'));
          responseResult('success',lang('NPC.cikti.esyaSilindi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }
}
