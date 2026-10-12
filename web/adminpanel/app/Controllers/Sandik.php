<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class Sandik extends BaseController
{
  public $viewFolder   = "";
  public $sandikModel  = "";

  public function __construct()
  {
    $this->viewFolder   = "Sandik";
    $this->sandikModel  = model('Sandik_model');
    if (!session('user_id')) {
      header('Location: '.base_url('GirisYap'));
      exit;
    }
  }

  public function Index()
  {
    if (!IsAllowedViewModule('sandikGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Index",$viewData);
  }

  public function Ajax()
  {
    if (!IsAllowedViewModule('sandikGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect('metin2');
    $request  = \Config\Services::request();
    $siralama = ['vnum','locale_name','type','item_count'];
    if ($request->getPost('search[value]')) {
      $yaz = $this->sandikModel->AjaxAra($request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }else{
      $yaz = $this->sandikModel->Ajax($request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $icon      = $this->sandikModel->Ikon($value->vnum,$db);
      $name      = isset($value->locale_name)?mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9"):'';
      $sub_array[] = '<img src="'.base_url('assets/img/icon/'.$icon).'" width="32" height="32" alt=""> '.$value->vnum.($name?' - '.$name:'');
      $sub_array[] = $value->type;
      $sub_array[] = $value->item_count;
      if (IsAllowedViewModule('sandikDuzenleyebilsin') || IsAllowedViewModule('sandikSilebilsin')) {
        $buttons = "";
        if (IsAllowedViewModule('sandikDuzenleyebilsin')) {
          $buttons .= '<a class="btn btn-primary pt-1 pb-1 ps-2 pe-2" data-bs-toggle="modal" data-bs-target="#duzenle" href="javascript:void(0)" data-id="'.$value->vnum.'">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" style="width:25px;height:25px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 7h-3a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-3" /><path d="M9 15h3l8.5 -8.5a1.5 1.5 0 0 0 -3 -3l-8.5 8.5v3" /><line x1="16" y1="5" x2="19" y2="8" /></svg>
          </a>';
        }
        if (IsAllowedViewModule('sandikSilebilsin')) {
          $buttons .= '<a class="btn btn-danger pt-1 pb-1 ps-2 pe-2 ms-2 sandikSil" href="javascript:void(0)" data-id="'.$value->vnum.'" data-header="'.lang('Genel.silBaslik').'" data-message="'.lang('Genel.buIslemGeriAlinamaz').'" data-yes="'.lang('Genel.evet').'" data-no="'.lang('Genel.hayir').'">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" style="width:25px;height:25px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><line x1="4" y1="7" x2="20" y2="7" /><line x1="10" y1="11" x2="10" y2="17" /><line x1="14" y1="11" x2="14" y2="17" /><path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12" /><path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3" /></svg>
          </a>';
        }
        $sub_array[] = $buttons;
      }
      $data[] = $sub_array;
    }
    $output = array(
      "draw"            =>  intval($_POST["draw"]),
      "recordsFiltered" =>  $this->sandikModel->Sayi($db),
      "data"            =>  $data
    );
    echo json_encode($output, JSON_INVALID_UTF8_SUBSTITUTE);
    exit;
  }

  public function Detay($id=0)
  {
    if (!IsAllowedViewModule('sandikDuzenleyebilsin')) {
      responseResult('error',lang('Genel.yetkinYok'));
    }
    $db       = \Config\Database::connect('metin2');
    $kontrol  = $this->sandikModel->GrupKontrol($id,$db);
    if (!$kontrol) {
      responseResult('error',lang('Sandik.cikti.sandikYok'));
    }else {
      $returnData['vnum'] = $kontrol->vnum;
      $returnData['type'] = $kontrol->type;
      $item = $this->sandikModel->ItemProtoKontrol($kontrol->vnum);
      $returnData['name'] = (isset($item->locale_name)?mb_convert_encoding($item->locale_name, 'UTF-8' ,"ISO-8859-9"):'');
      $icerikler = $this->sandikModel->Icerikler($kontrol->vnum,$db);
      $returnData['items'] = [];
      foreach ($icerikler as $value) {
        $returnData['items'][] = [
          'id'        => $value->id,
          'item_vnum' => $value->item_vnum,
          'name'      => (isset($value->locale_name)?mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9"):''),
          'icon'      => (isset($value->icon)&&$value->icon?$value->icon:'noicon.png'),
          'count'     => $value->count,
          'prob'      => $value->prob,
          'rare'      => $value->rare,
          'idx'       => $value->idx,
        ];
      }
      echo json_encode($returnData, JSON_INVALID_UTF8_SUBSTITUTE);
      exit;
    }
  }

  public function GrupEkle()
  {
    if (!IsAllowedViewModule('sandikEkleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'vnum' => ['label' => lang('Genel.esya'),  'rules' => "required|integer|greater_than[0]"],
      'type' => ['label' => lang('Sandik.sayfa.tip'), 'rules' => "required|in_list[norm,const,newpct,pct,stone,quest,special]"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db      = \Config\Database::connect('metin2');
      $kontrol = $this->sandikModel->GrupKontrol($request->getPost('vnum'),$db);
      if ($kontrol) {
        responseResult('error',lang('Sandik.cikti.zatenEkli'));
      }
      if (!$this->sandikModel->ItemProtoKontrol($request->getPost('vnum'))) {
        responseResult('error',lang('Esya.cikti.esyaYok'));
      }
      $result = $this->sandikModel->GrupEkle([
        'vnum' => $request->getPost('vnum'),
        'type' => $request->getPost('type'),
      ],$db);
      if ($result) {
        LogAdd(lang('Sandik.kayit.sandikEklendi',[ 'vnum' => $request->getPost('vnum') ]),'Sandik/Index',session('user_id'));
        responseResult('success',lang('Sandik.cikti.sandikEklendi'));
      }else {
        responseResult('error',lang('Genel.bilinmeyenHata'));
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function GrupDuzenle()
  {
    if (!IsAllowedViewModule('sandikDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'vnum' => ['label' => lang('Genel.esya'),           'rules' => "required|integer"],
      'type' => ['label' => lang('Sandik.sayfa.tip'),     'rules' => "required|in_list[norm,const,newpct,pct,stone,quest,special]"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db      = \Config\Database::connect('metin2');
      $kontrol = $this->sandikModel->GrupKontrol($request->getPost('vnum'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Sandik.cikti.sandikYok'));
      }
      $result = $this->sandikModel->GrupGuncelle(['type'=>$request->getPost('type')],$kontrol->vnum,$db);
      if ($result) {
        LogAdd(lang('Sandik.kayit.sandikDuzenlendi',[ 'vnum' => $kontrol->vnum ]),'Sandik/Index',session('user_id'));
        responseResult('success',lang('Sandik.cikti.sandikDuzenlendi'));
      }else {
        responseResult('error',lang('Genel.bilinmeyenHata'));
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function ItemEkle()
  {
    if (!IsAllowedViewModule('sandikDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'group_vnum' => ['label' => lang('Sandik.sayfa.sandik'), 'rules' => "required|integer"],
      'item_vnum'  => ['label' => lang('Genel.esya'),          'rules' => "required|integer|greater_than[0]"],
      'count'      => ['label' => lang('Genel.adet'),          'rules' => "required|integer|greater_than[0]"],
      'prob'       => ['label' => lang('Genel.sans'),          'rules' => "required|integer"],
      'rare'       => ['label' => lang('Sandik.sayfa.rare'),   'rules' => "required|integer"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db      = \Config\Database::connect('metin2');
      $kontrol = $this->sandikModel->GrupKontrol($request->getPost('group_vnum'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Sandik.cikti.sandikYok'));
      }
      if (!$this->sandikModel->ItemProtoKontrol($request->getPost('item_vnum'))) {
        responseResult('error',lang('Esya.cikti.esyaYok'));
      }
      $maxIdx = $db->table('player.drop_special_item')->selectMax('idx')->where('group_vnum',$kontrol->vnum)->get()->getRow();
      $result = $this->sandikModel->ItemEkle([
        'group_vnum' => $kontrol->vnum,
        'item_vnum'  => $request->getPost('item_vnum'),
        'count'      => $request->getPost('count'),
        'prob'       => $request->getPost('prob'),
        'rare'       => $request->getPost('rare'),
        'idx'        => ($maxIdx && $maxIdx->idx!==null ? $maxIdx->idx+1 : 1),
      ],$db);
      if ($result) {
        LogAdd(lang('Sandik.kayit.itemEklendi',[ 'vnum' => $kontrol->vnum, 'item' => $request->getPost('item_vnum') ]),'Sandik/Index',session('user_id'));
        responseResult('success',lang('Sandik.cikti.itemEklendi'));
      }else {
        responseResult('error',lang('Genel.bilinmeyenHata'));
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function ItemDuzenle()
  {
    if (!IsAllowedViewModule('sandikDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'id'    => ['label' => 'ID',                          'rules' => "required|integer|greater_than[0]"],
      'count' => ['label' => lang('Genel.adet'),            'rules' => "required|integer|greater_than[0]"],
      'prob'  => ['label' => lang('Genel.sans'),            'rules' => "required|integer"],
      'rare'  => ['label' => lang('Sandik.sayfa.rare'),     'rules' => "required|integer"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db      = \Config\Database::connect('metin2');
      $kontrol = $this->sandikModel->ItemKontrol($request->getPost('id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Sandik.cikti.itemYok'));
      }
      $result = $this->sandikModel->ItemGuncelle([
        'count' => $request->getPost('count'),
        'prob'  => $request->getPost('prob'),
        'rare'  => $request->getPost('rare'),
      ],$kontrol->id,$db);
      if ($result) {
        LogAdd(lang('Sandik.kayit.itemDuzenlendi',[ 'vnum' => $kontrol->group_vnum, 'item' => $kontrol->item_vnum ]),'Sandik/Index',session('user_id'));
        responseResult('success',lang('Sandik.cikti.itemDuzenlendi'));
      }else {
        responseResult('error',lang('Genel.bilinmeyenHata'));
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function ItemSil()
  {
    if (!IsAllowedViewModule('sandikDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'id'  => ['rules' => "required|integer|greater_than[0]"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db      = \Config\Database::connect('metin2');
      $kontrol = $this->sandikModel->ItemKontrol($request->getPost('id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Sandik.cikti.itemYok'));
      }
      $result = $this->sandikModel->ItemSil($kontrol->id,$db);
      if ($result) {
        LogAdd(lang('Sandik.kayit.itemSilindi',[ 'vnum' => $kontrol->group_vnum, 'item' => $kontrol->item_vnum ]),'Sandik/Index',session('user_id'));
        responseResult('success',lang('Sandik.cikti.itemSilindi'));
      }else {
        responseResult('error',lang('Genel.bilinmeyenHata'));
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Sil()
  {
    if (!IsAllowedViewModule('sandikSilebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'vnum'  => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db      = \Config\Database::connect('metin2');
      $kontrol = $this->sandikModel->GrupKontrol($request->getPost('vnum'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Sandik.cikti.sandikYok'));
      }else {
        $result = $this->sandikModel->GrupSil($kontrol->vnum,$db);
        if ($result) {
          LogAdd(lang('Sandik.kayit.sandikSilindi',[ 'vnum' => $kontrol->vnum ]),'Sandik/Index',session('user_id'));
          responseResult('success',lang('Sandik.cikti.sandikSilindi'));
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
    if (!IsAllowedViewModule('sandikDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    if (p2pStatus==0) {
      responseResult('error',lang('Genel.p2pKapali'));
    }
    foreach (p2pPorts as $key => $value) {
      SendServer('P',"RELOAD",$value);
    }
    LogAdd(lang('Sandik.cikti.sunucuyaGonderildi'),'Sandik/Index',session('user_id'));
    responseResult('success',lang('Sandik.cikti.sunucuyaGonderildi'));
  }
}
