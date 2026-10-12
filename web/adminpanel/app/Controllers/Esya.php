<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class Esya extends BaseController
{
  public $viewFolder  = "";
  public $esyaModel   = "";

  public function __construct()
  {
    $this->viewFolder = "Esya";
    $this->esyaModel  = model('Esya_model');
    if (!session('user_id')) {
      header('Location: '.base_url('GirisYap'));
      exit;
    }
  }

  public function Index()
  {
    if (!IsAllowedViewModule('esyaGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    $viewData['efsunlar'] = $this->esyaModel->Efsunlar();
    return view("{$this->viewFolder}/Index",$viewData);
  }

  public function Ajax()
  {
    if (!IsAllowedViewModule('esyaGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect('metin2');
    $request  = \Config\Services::request();
    $siralama = ['vnum','locale_name','type','subtype'];
    $query    = "SELECT item_proto.vnum, item_proto.locale_name, item_proto.type, item_proto.subtype FROM player.item_proto ";

    if (
      in_array($request->getPost('searchType'),['vnum','locale_name','type','subtype'])
      && in_array($request->getPost('searchWhere'),['=','!=','%'])
      && !empty($request->getPost('itemSearch'))
    ) {
      if ($request->getPost('searchWhere')=="%") {
        $query  .= " WHERE item_proto.".addslashes(addcslashes($request->getPost('searchType'),'%'))." LIKE '%".mb_convert_encoding(addslashes(addcslashes($request->getPost('itemSearch'),'%')), 'ISO-8859-9' ,"UTF-8")."%'";
      }else {
        $query  .= " WHERE item_proto.".addslashes(addcslashes($request->getPost('searchType'),'%'))." ".addslashes(addcslashes($request->getPost('searchWhere'),'%'))." '".mb_convert_encoding(addslashes(addcslashes($request->getPost('itemSearch'),'%')), 'ISO-8859-9' ,"UTF-8")."'";
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

    $yaz  = $this->esyaModel->AjaxAra($query,$db);
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $itemIcon = $this->esyaModel->ItemIcon($value->vnum);
      if (!empty($itemIcon) && $itemIcon!="-") {
        $sub_array[] = '<img src="'.base_url('assets/img/icon/'.$itemIcon->icon).'" title="'.$value->vnum.'"> '.$value->vnum;
      }else {
        $sub_array[] = $value->vnum;
      }
      $sub_array[] = mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9");
      $sub_array[] = $value->type;
      $sub_array[] = $value->subtype;
      if (IsAllowedViewModule('esyaDuzenleyebilsin')) {
        $sub_array[] = '<a class="btn btn-primary pt-1 pb-1 ps-2 pe-2" data-bs-toggle="modal" data-bs-target="#duzenle" href="javascript:void(0)" data-id="'.$value->vnum.'">
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
    if (!IsAllowedViewModule('esyaDuzenleyebilsin')) {
      responseResult('error',lang('Genel.yetkinYok'));
    }
    $request  = \Config\Services::request();
    $db       = \Config\Database::connect('metin2');
    $kontrol  = $this->esyaModel->ItemProtoKontrol($id,$db);
    if (!$kontrol) {
      responseResult('error',lang('Esya.cikti.esyaYok'));
    }else {
      $returnData['vnum']           = $kontrol->vnum;
      $returnData['locale_name']    = mb_convert_encoding($kontrol->locale_name, 'UTF-8' ,"ISO-8859-9");
      $returnData['type']           = $kontrol->type;
      $returnData['subtype']        = $kontrol->subtype;
      $returnData['weight']         = $kontrol->weight;
      $returnData['antiflag']       = $kontrol->antiflag;
      $returnData['wearflag']       = $kontrol->wearflag;
      $returnData['gold']           = $kontrol->gold;
      $returnData['shop_buy_price'] = $kontrol->shop_buy_price;
      $returnData['magic_pct']      = $kontrol->magic_pct;
      $returnData['specular']       = $kontrol->specular;
      $returnData['socket_pct']     = $kontrol->socket_pct;
      $returnData['addon_type']     = $kontrol->addon_type;

      $returnData['refined_vnum']   = $kontrol->refined_vnum;
      $returnData['refine_set']     = $kontrol->refine_set;

      $returnData['limittype0']     = $kontrol->limittype0;
      $returnData['limitvalue0']    = $kontrol->limitvalue0;
      $returnData['limittype1']     = $kontrol->limittype1;
      $returnData['limitvalue1']    = $kontrol->limitvalue1;

      $returnData['applytype0']     = $kontrol->applytype0;
      $returnData['applyvalue0']    = $kontrol->applyvalue0;
      $returnData['applytype1']     = $kontrol->applytype1;
      $returnData['applyvalue1']    = $kontrol->applyvalue1;
      $returnData['applytype2']     = $kontrol->applytype2;
      $returnData['applyvalue2']    = $kontrol->applyvalue2;

      $returnData['value0']         = $kontrol->value0;
      $returnData['value1']         = $kontrol->value1;
      $returnData['value2']         = $kontrol->value2;
      $returnData['value3']         = $kontrol->value3;
      $returnData['value4']         = $kontrol->value4;
      $returnData['value5']         = $kontrol->value5;

      $returnData['socket0']        = $kontrol->socket0;
      $returnData['socket1']        = $kontrol->socket1;
      $returnData['socket2']        = $kontrol->socket2;
      $returnData['socket3']        = $kontrol->socket3;
      $returnData['socket4']        = $kontrol->socket4;
      $returnData['socket5']        = $kontrol->socket5;
      echo json_encode($returnData, JSON_INVALID_UTF8_SUBSTITUTE);
      exit;
    }
  }

  public function Duzenle()
  {
    if (!IsAllowedViewModule('esyaDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'locale_name' => ['label' => lang('Genel.esya'),  'rules' => "required"],
      'vnum'        => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->esyaModel->ItemProtoKontrol($request->getPost('vnum'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Esya.cikti.esyaYok'));
      }else {
        $data = [
          'locale_name'     =>  mb_convert_encoding($request->getPost('locale_name'), 'ISO-8859-9' ,"UTF-8"),
          'type'            =>  $request->getPost('type'),
          'subtype'         =>  $request->getPost('subtype'),
          'weight'          =>  $request->getPost('weight'),
          'antiflag'        =>  $request->getPost('antiflag'),
          'wearflag'        =>  $request->getPost('wearflag'),
          'gold'            =>  $request->getPost('gold'),
          'shop_buy_price'  =>  $request->getPost('shop_buy_price'),
          'magic_pct'       =>  $request->getPost('magic_pct'),
          'specular'        =>  $request->getPost('specular'),
          'socket_pct'      =>  $request->getPost('socket_pct'),
          'addon_type'      =>  $request->getPost('addon_type'),
          'refined_vnum'    =>  $request->getPost('refined_vnum'),
          'refine_set'      =>  $request->getPost('refine_set'),
          'limittype0'      =>  $request->getPost('limittype0'),
          'limitvalue0'     =>  $request->getPost('limitvalue0'),
          'limittype1'      =>  $request->getPost('limittype1'),
          'limitvalue1'     =>  $request->getPost('limitvalue1'),
          'applytype0'      =>  $request->getPost('applytype0'),
          'applyvalue0'     =>  $request->getPost('applyvalue0'),
          'applytype1'      =>  $request->getPost('applytype1'),
          'applyvalue1'     =>  $request->getPost('applyvalue1'),
          'applytype2'      =>  $request->getPost('applytype2'),
          'applyvalue2'     =>  $request->getPost('applyvalue2'),
          'value0'          =>  $request->getPost('value0'),
          'value1'          =>  $request->getPost('value1'),
          'value2'          =>  $request->getPost('value2'),
          'value3'          =>  $request->getPost('value3'),
          'value4'          =>  $request->getPost('value4'),
          'value5'          =>  $request->getPost('value5'),
          'socket0'         =>  $request->getPost('socket0'),
          'socket1'         =>  $request->getPost('socket1'),
          'socket2'         =>  $request->getPost('socket2'),
          'socket3'         =>  $request->getPost('socket3'),
          'socket4'         =>  $request->getPost('socket4'),
          'socket5'         =>  $request->getPost('socket5'),
        ];
        $result = $this->esyaModel->Guncelle($data,$kontrol->vnum,$db);
        if ($result) {
          LogAdd(lang('Esya.kayit.esyaDuzenlendi',['locale_name' => mb_convert_encoding($kontrol->locale_name, 'UTF-8' ,"ISO-8859-9"), 'vnum' => $kontrol->vnum]),'Esya/Index',session('user_id'));
          responseResult('success',lang('Esya.cikti.esyaDuzenlendi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Droplar($item_vnum = 0)
  {
    if (!IsAllowedViewModule('esyaDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect('metin2');
    $request  = \Config\Services::request();
    $kontrol  = $this->esyaModel->ItemProtoKontrol($item_vnum,$db);
    if (!$kontrol) {
      responseResult('error',lang('Esya.cikti.esyaYok'));
    }
    $siralama = ['mob_vnum','count','prob'];
    $query    = "SELECT drop_default.mob_vnum, drop_default.item_vnum, drop_default.count, drop_default.prob, mob_proto.locale_name FROM player.drop_default ";
    $query    .= "LEFT JOIN player.mob_proto on player.mob_proto.vnum=player.drop_default.mob_vnum ";
    $query    .= " WHERE item_vnum = ".$kontrol->vnum;

    if (
      isset($siralama[$request->getPost('order[0][column]')])
      && in_array($request->getPost('order[0][dir]'),['asc','desc'])
    ) {
      $query  .= " ORDER BY ".$siralama[$request->getPost('order[0][column]')].' '.addslashes(addcslashes($request->getPost('order[0][dir]'),'%'));
    }

    $yaz  = $this->esyaModel->AjaxAra($query,$db);
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->mob_vnum.' - '.mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9");
      $sub_array[] = $value->count;
      $sub_array[] = $value->prob;
      $buttons  =  '<a class="btn btn-primary pt-1 pb-1 ps-2 pe-2" data-bs-toggle="modal" data-bs-target="#dropDuzenle" href="javascript:void(0)" data-locale_name="'.mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9").'" data-mob_vnum="'.$value->mob_vnum.'" data-item_vnum="'.$value->item_vnum.'" data-count="'.$value->count.'" data-prob="'.$value->prob.'">
        <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" style="width:25px;height:25px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 7h-3a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-3" /><path d="M9 15h3l8.5 -8.5a1.5 1.5 0 0 0 -3 -3l-8.5 8.5v3" /><line x1="16" y1="5" x2="19" y2="8" /></svg>
      </a>';
      $buttons .=  '<a class="btn btn-danger pt-1 pb-1 ps-2 pe-2 ms-2 dropSil" href="javascript:void(0)" data-mob_vnum="'.$value->mob_vnum.'" data-item_vnum="'.$value->item_vnum.'" data-count="'.$value->count.'" data-prob="'.$value->prob.'">
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

  public function DropEkle()
  {
    if (!IsAllowedViewModule('esyaDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'item_vnum' => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'count'     => ['label' => lang('Genel.adet'),  'rules' => "required|integer"],
      'prob'      => ['label' => lang('Genel.fiyat'), 'rules' => "required"],
      'mob_vnum'  => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->esyaModel->ItemProtoKontrol($request->getPost('item_vnum'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Esya.cikti.esyaYok'));
      }else {
        $canavarKontrol  = $this->esyaModel->MobProtoKontrol($request->getPost('mob_vnum'),$db);
        if (!$canavarKontrol) {
          responseResult('error',lang('Canavarlar.cikti.canavarYok'));
        }
        $data = [
          'mob_vnum'  =>  $canavarKontrol->vnum,
          'item_vnum' =>  $kontrol->vnum,
          'count'     =>  $request->getPost('count'),
          'prob'      =>  $request->getPost('prob'),
        ];
        $result = $this->esyaModel->DropEkle($data,$db);
        if ($result) {
          LogAdd(lang('Canavar.kayit.dropEklendi',['mob' => mb_convert_encoding($canavarKontrol->locale_name, 'UTF-8' ,"ISO-8859-9"), 'item' => mb_convert_encoding($kontrol->locale_name, 'UTF-8' ,"ISO-8859-9")]),'Esya/Index',session('user_id'));
          responseResult('success',lang('Canavar.cikti.dropEklendi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function DropGuncelle()
  {
    if (!IsAllowedViewModule('esyaDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'drop_item_vnum'  => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'drop_count'      => ['label' => lang('Genel.adet'),  'rules' => "required|integer"],
      'drop_prob'       => ['label' => lang('Genel.fiyat'), 'rules' => "required"],
      'drop_mob_vnum'   => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->esyaModel->DropKontrol($request->getPost('drop_mob_vnum'),$request->getPost('drop_item_vnum'),$request->getPost('drop_count'),$request->getPost('drop_prob'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Esya.cikti.esyaYok'));
      }else {
        $data = [
          'count' =>  $request->getPost('newCount'),
          'prob'  =>  $request->getPost('newProb'),
        ];

        $mobKontrol   = $this->esyaModel->MobProtoKontrol($kontrol->mob_vnum,$db);
        $esyaKontrol  = $this->esyaModel->ItemProtoKontrol($kontrol->item_vnum,$db);

        $result = $this->esyaModel->DropGuncelle($data,$kontrol->mob_vnum,$kontrol->item_vnum,$kontrol->count,$kontrol->prob,$db);
        if ($result) {
          LogAdd(lang('Canavar.kayit.dropGuncellendi',['mob' => mb_convert_encoding((isset($mobKontrol->locale_name)?$mobKontrol->locale_name:$kontrol->mob_vnum), 'UTF-8' ,"ISO-8859-9"), 'item' => mb_convert_encoding((isset($esyaKontrol->locale_name)?$esyaKontrol->locale_name:$kontrol->mob_vnum), 'UTF-8' ,"ISO-8859-9")]),'Esya/Index',session('user_id'));
          responseResult('success',lang('Canavar.cikti.dropGuncellendi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function DropSil()
  {
    if (!IsAllowedViewModule('esyaDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'mob_vnum'  => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'item_vnum' => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'count'     => ['label' => lang('Genel.adet'),  'rules' => "required|integer"],
      'prob'      => ['label' => lang('Genel.fiyat'), 'rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->esyaModel->DropKontrol($request->getPost('mob_vnum'),$request->getPost('item_vnum'),$request->getPost('count'),$request->getPost('prob'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Esya.cikti.esyaYok'));
      }else {
        $mobKontrol   = $this->esyaModel->MobProtoKontrol($kontrol->mob_vnum,$db);
        $esyaKontrol  = $this->esyaModel->ItemProtoKontrol($kontrol->item_vnum,$db);

        $result = $this->esyaModel->DropSil($kontrol->mob_vnum,$kontrol->item_vnum,$kontrol->count,$kontrol->prob,$db);
        if ($result) {
          LogAdd(lang('Canavar.kayit.dropSilindi',['mob' => mb_convert_encoding((isset($mobKontrol->locale_name)?$mobKontrol->locale_name:$kontrol->mob_vnum), 'UTF-8' ,"ISO-8859-9"), 'item' => mb_convert_encoding((isset($esyaKontrol->locale_name)?$esyaKontrol->locale_name:$kontrol->mob_vnum), 'UTF-8' ,"ISO-8859-9")]),'Esya/Index',session('user_id'));
          responseResult('success',lang('Canavar.cikti.dropSilindi'));
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
    if (!IsAllowedViewModule('esyaDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    if (p2pStatus==0) {
      responseResult('error',lang('Genel.p2pKapali'));
    }
    foreach (p2pPorts as $key => $value) {
      SendServer('P',"RELOAD",$value);
    }
    LogAdd(lang('Esya.cikti.sunucuyaGonderildi'),'Esya/Index',session('user_id'));
    responseResult('success',lang('Esya.cikti.sunucuyaGonderildi'));
  }

  public function Ara()
  {
    if (!IsAllowedViewModule('esyaArayabilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    $viewData['efsunlar'] = $this->esyaModel->Efsunlar();
    return view("{$this->viewFolder}/Ara",$viewData);
  }

  public function AjaxAra()
  {
    if (!IsAllowedViewModule('esyaArayabilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect('metin2');
    $request  = \Config\Services::request();
    $siralama = ['item.owner_id','item.id','item.window','item.vnum','item.vnum','item.count'];
    $query    = "SELECT player.name, item.id, item.window, item.vnum, item_proto.locale_name, item.count FROM player.item ";
    $query    .= "LEFT JOIN player.player on player.player.id=player.item.owner_id ";
    $query    .= "LEFT JOIN player.item_proto on player.item_proto.vnum=player.item.vnum ";

    if (is_numeric($request->getPost('vnum')) && $request->getPost('vnum')>0) {
      $query  .= " WHERE item.vnum = ".addslashes(addcslashes($request->getPost('vnum'),'%'));
    }

    if (
      is_numeric($request->getPost('countStart'))
      && is_numeric($request->getPost('countFinish'))
      && $request->getPost('countStart')>=0
      && $request->getPost('countFinish')>=$request->getPost('countStart')
    ) {
      if (!stristr($query,'WHERE')) {
        $query  .= " WHERE ";
      }else {
        $query  .= " AND ";
      }
      $query  .= " item.count >= ".addslashes(addcslashes($request->getPost('countStart'),'%'));
      $query  .= " AND item.count <= ".addslashes(addcslashes($request->getPost('countFinish'),'%'));
    }

    for ($i=0; $i < 6 ; $i++) {
      if (
        is_numeric($request->getPost('socket'.$i))
        && $request->getPost('socket'.$i)>0
      ) {
        if (!stristr($query,'WHERE')) {
          $query  .= " WHERE ";
        }else {
          $query  .= " AND ";
        }
        $query  .= " item.socket".$i." = ".addslashes(addcslashes($request->getPost('socket'.$i),'%'));
      }
    }

    if (
      in_array($request->getPost('window'),['INVENTORY','EQUIPMENT','SAFEBOX','MALL','DRAGON_SOUL_INVENTORY','BELT_INVENTORY','SWITCHBOT','GROUND'])
    ) {
      if (!stristr($query,'WHERE')) {
        $query  .= " WHERE ";
      }else {
        $query  .= " AND ";
      }
      $query  .= " item.window = '".addslashes(addcslashes($request->getPost('window'),'%'))."'";
    }

    for ($i=0; $i < 5 ; $i++) {
      if (
        is_numeric($request->getPost('attrtype'.$i))
        && is_numeric($request->getPost('attrvalue'.$i))
        && in_array($request->getPost('attrequal'.$i),['=','!='])
        && $request->getPost('attrtype'.$i)>=0
      ) {
        if (!stristr($query,'WHERE')) {
          $query  .= " WHERE ";
        }else {
          $query  .= " AND ";
        }
        $query  .= " item.attrtype".$i." ".$request->getPost('attrequal'.$i)." ".addslashes(addcslashes($request->getPost('attrtype'.$i),'%'));
        $query  .= " AND item.attrvalue".$i." ".$request->getPost('attrequal'.$i)." ".addslashes(addcslashes($request->getPost('attrvalue'.$i),'%'));
      }
    }

    if (
      isset($siralama[$request->getPost('order[0][column]')])
      && in_array($request->getPost('order[0][dir]'),['asc','desc'])
    ) {
      $query  .= " ORDER BY ".$siralama[$request->getPost('order[0][column]')].' '.addslashes(addcslashes($request->getPost('order[0][dir]'),'%'));
    }

    if (
      is_numeric($request->getPost('limit'))
      && is_numeric($request->getPost('start'))
      && $request->getPost('limit')>0
      && $request->getPost('start')>=0
    ) {
      $query  .= " LIMIT ".addslashes(addcslashes($request->getPost('limit'),'%')).' OFFSET '.addslashes(addcslashes($request->getPost('start'),'%'));
    }else {
      $query  .= " LIMIT 10";
    }

    $yaz = $this->esyaModel->AjaxAra($query,$db);
    if ($request->getPost('vnum')>0) {
      LogAdd(lang('Esya.kayit.esyaArandi',['vnum' => $request->getPost('vnum')]),'Esya/Ara',session('user_id'));
    }else {
      LogAdd(lang('Esya.kayit.bosEsyaArandi',['vnum' => $request->getPost('vnum')]),'Esya/Ara',session('user_id'));
    }
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->name;
      $sub_array[] = $value->id;
      $sub_array[] = lang('Genel.'.$value->window);
      $sub_array[] = $value->vnum;
      $sub_array[] = mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9");
      $sub_array[] = $value->count;
      $data[] = $sub_array;
    }
    $output = array(
      "draw"            =>  intval($_POST["draw"]),
      "recordsFiltered" =>  (count($yaz)==$request->getPost('limit')?$request->getPost('start')+$request->getPost('limit')+1:0),
      "data"            =>  $data
    );
    echo json_encode($output, JSON_INVALID_UTF8_SUBSTITUTE);
    exit;
  }

  public function Esyalar()
  {
    if (
      IsAllowedViewModule('esyaArayabilsin')
      || IsAllowedViewModule('esyaDuzenleyebilsin')
      || IsAllowedViewModule('yukseltmeEkleyebilsin')
      || IsAllowedViewModule('balikcilikEkleyebilsin')
      || IsAllowedViewModule('carkEkleyebilsin')
      || IsAllowedViewModule('biyologEkleyebilsin')
      || IsAllowedViewModule('sandikEkleyebilsin')
      || IsAllowedViewModule('sandikDuzenleyebilsin')
      || IsAllowedViewModule('nesneMarketEsyaEkleyebilsin')
      || IsAllowedViewModule('karakterEsyaGonderebilsin')
    ) {
      $request  = \Config\Services::request();
      $search   = $request->getGet('q');
      if (!$search) {
        $search = "";
      }
      $esyalar = $this->esyaModel->EsyaAra($search);
      $data[] = [
        'id'    => "",
        'text'  => " - ",
      ];
      foreach ($esyalar as $key => $value) {
        $data[] = [
          'id'    => $value->vnum,
          'text'  => $value->vnum.' - '.mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9")
        ];
      }
      echo json_encode($data);
      exit;
    }
  }
}
