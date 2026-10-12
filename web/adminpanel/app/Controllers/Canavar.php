<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class Canavar extends BaseController
{
  public $viewFolder    = "";
  public $canavarModel  = "";

  public function __construct()
  {
    $this->viewFolder   = "Canavar";
    $this->canavarModel = model('Canavar_model');
    if (!session('user_id')) {
      header('Location: '.base_url('GirisYap'));
      exit;
    }
  }

  public function Index()
  {
    if (!IsAllowedViewModule('canavarGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Index",$viewData);
  }

  public function Ajax()
  {
    if (!IsAllowedViewModule('canavarGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect('metin2');
    $request  = \Config\Services::request();
    $siralama = ['vnum','locale_name','rank','type','level','gold_min','exp'];
    $query    = "SELECT * FROM player.mob_proto ";

    if (
      in_array($request->getPost('searchType'),['vnum','locale_name','rank','type','level'])
      && in_array($request->getPost('searchWhere'),['=','!=','%'])
      && !empty($request->getPost('mobSearch'))
    ) {
      if ($request->getPost('searchWhere')=="%") {
        $query  .= " WHERE mob_proto.".addslashes(addcslashes($request->getPost('searchType'),'%'))." LIKE '%".mb_convert_encoding(addslashes(addcslashes($request->getPost('mobSearch'),'%')), 'ISO-8859-9' ,"UTF-8")."%'";
      }else {
        $query  .= " WHERE mob_proto.".addslashes(addcslashes($request->getPost('searchType'),'%'))." ".addslashes(addcslashes($request->getPost('searchWhere'),'%'))." '".mb_convert_encoding(addslashes(addcslashes($request->getPost('mobSearch'),'%')), 'ISO-8859-9' ,"UTF-8")."'";
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

    $yaz  = $this->canavarModel->AjaxAra($query,$db);
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->vnum;
      $sub_array[] = mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9");
      $sub_array[] = $value->rank;
      $sub_array[] = $value->type;
      $sub_array[] = $value->level;
      $sub_array[] = $value->gold_min.' - '.$value->gold_max;
      $sub_array[] = $value->exp;
      if (IsAllowedViewModule('canavarDuzenleyebilsin')) {
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
    if (!IsAllowedViewModule('canavarDuzenleyebilsin')) {
      responseResult('error',lang('Genel.yetkinYok'));
    }
    $request  = \Config\Services::request();
    $db       = \Config\Database::connect('metin2');
    $kontrol  = $this->canavarModel->MobProtoKontrol($id,$db);
    if (!$kontrol) {
      responseResult('error',lang('Canavar.cikti.canavarYok'));
    }else {
      $returnData['vnum']               = $kontrol->vnum;
      $returnData['locale_name']        = mb_convert_encoding($kontrol->locale_name, 'UTF-8' ,"ISO-8859-9");
      $returnData['rank']               = $kontrol->rank;
      $returnData['type']               = $kontrol->type;
      $returnData['battle_type']        = $kontrol->battle_type;
      $returnData['gold_min']           = $kontrol->gold_min;
      $returnData['gold_max']           = $kontrol->gold_max;
      $returnData['exp']                = $kontrol->exp;
      $returnData['level']              = $kontrol->level;
      $returnData['drop_item']          = $kontrol->drop_item;
      $returnData['max_hp']             = $kontrol->max_hp;
      $returnData['damage_min']         = $kontrol->damage_min;
      $returnData['damage_max']         = $kontrol->damage_max;
      $returnData['st']                 = $kontrol->st;
      $returnData['dx']                 = $kontrol->dx;
      $returnData['ht']                 = $kontrol->ht;
      $returnData['iq']                 = $kontrol->iq;
      $returnData['regen_cycle']        = $kontrol->regen_cycle;
      $returnData['regen_percent']      = $kontrol->regen_percent;
      $returnData['def']                = $kontrol->def;
      $returnData['attack_speed']       = $kontrol->attack_speed;
      $returnData['move_speed']         = $kontrol->move_speed;
      $returnData['attack_range']       = $kontrol->attack_range;
      $returnData['ai_flag']            = $kontrol->ai_flag;
      $returnData['setRaceFlag']        = $kontrol->setRaceFlag;
      $returnData['setImmuneFlag']      = $kontrol->setImmuneFlag;
      $returnData['skill_level0']       = $kontrol->skill_level0;
      $returnData['skill_vnum0']        = $kontrol->skill_vnum0;
      $returnData['skill_level1']       = $kontrol->skill_level1;
      $returnData['skill_vnum1']        = $kontrol->skill_vnum1;
      $returnData['skill_level2']       = $kontrol->skill_level2;
      $returnData['skill_vnum2']        = $kontrol->skill_vnum2;
      $returnData['skill_level3']       = $kontrol->skill_level3;
      $returnData['skill_vnum3']        = $kontrol->skill_vnum3;
      $returnData['skill_level4']       = $kontrol->skill_level4;
      $returnData['skill_vnum4']        = $kontrol->skill_vnum4;
      $returnData['enchant_curse']      = $kontrol->enchant_curse;
      $returnData['enchant_slow']       = $kontrol->enchant_slow;
      $returnData['enchant_poison']     = $kontrol->enchant_poison;
      $returnData['enchant_stun']       = $kontrol->enchant_stun;
      $returnData['enchant_critical']   = $kontrol->enchant_critical;
      $returnData['enchant_penetrate']  = $kontrol->enchant_penetrate;
      $returnData['resist_sword']       = $kontrol->resist_sword;
      $returnData['resist_twohand']     = $kontrol->resist_twohand;
      $returnData['resist_dagger']      = $kontrol->resist_dagger;
      $returnData['resist_bell']        = $kontrol->resist_bell;
      $returnData['resist_fan']         = $kontrol->resist_fan;
      $returnData['resist_bow']         = $kontrol->resist_bow;
      $returnData['resist_fire']        = $kontrol->resist_fire;
      $returnData['resist_elect']       = $kontrol->resist_elect;
      $returnData['resist_magic']       = $kontrol->resist_magic;
      $returnData['resist_wind']        = $kontrol->resist_wind;
      $returnData['resist_poison']      = $kontrol->resist_poison;
      echo json_encode($returnData, JSON_INVALID_UTF8_SUBSTITUTE);
      exit;
    }
  }

  public function Duzenle()
  {
    if (!IsAllowedViewModule('canavarDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'locale_name' => ['label' => lang('Canavar.sayfa.canavarAdi'),  'rules' => "required"],
      'vnum'        => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->canavarModel->MobProtoKontrol($request->getPost('vnum'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Canavar.cikti.canavarYok'));
      }else {
        $data = [
          'locale_name'       =>  mb_convert_encoding($request->getPost('locale_name'), 'ISO-8859-9' ,"UTF-8"),
          'rank'              =>  $request->getPost('rank'),
          'type'              =>  $request->getPost('type'),
          'battle_type'       =>  $request->getPost('battle_type'),
          'gold_min'          =>  $request->getPost('gold_min'),
          'gold_max'          =>  $request->getPost('gold_max'),
          'exp'               =>  $request->getPost('exp'),
          'level'             =>  $request->getPost('level'),
          'drop_item'         =>  $request->getPost('drop_item'),
          'max_hp'            =>  $request->getPost('max_hp'),
          'damage_min'        =>  $request->getPost('damage_min'),
          'damage_max'        =>  $request->getPost('damage_max'),
          'st'                =>  $request->getPost('st'),
          'dx'                =>  $request->getPost('dx'),
          'ht'                =>  $request->getPost('ht'),
          'iq'                =>  $request->getPost('iq'),
          'regen_cycle'       =>  $request->getPost('regen_cycle'),
          'regen_percent'     =>  $request->getPost('regen_percent'),
          'def'               =>  $request->getPost('def'),
          'attack_speed'      =>  $request->getPost('attack_speed'),
          'move_speed'        =>  $request->getPost('move_speed'),
          'attack_range'      =>  $request->getPost('attack_range'),
          'ai_flag'           =>  $request->getPost('ai_flag'),
          'setRaceFlag'       =>  $request->getPost('setRaceFlag'),
          'setImmuneFlag'     =>  $request->getPost('setImmuneFlag'),
          'skill_level0'      =>  $request->getPost('skill_level0'),
          'skill_vnum0'       =>  $request->getPost('skill_vnum0'),
          'skill_level1'      =>  $request->getPost('skill_level1'),
          'skill_vnum1'       =>  $request->getPost('skill_vnum1'),
          'skill_level2'      =>  $request->getPost('skill_level2'),
          'skill_vnum2'       =>  $request->getPost('skill_vnum2'),
          'skill_level3'      =>  $request->getPost('skill_level3'),
          'skill_vnum3'       =>  $request->getPost('skill_vnum3'),
          'skill_level4'      =>  $request->getPost('skill_level4'),
          'skill_vnum4'       =>  $request->getPost('skill_vnum4'),
          'enchant_curse'     =>  $request->getPost('enchant_curse'),
          'enchant_slow'      =>  $request->getPost('enchant_slow'),
          'enchant_poison'    =>  $request->getPost('enchant_poison'),
          'enchant_stun'      =>  $request->getPost('enchant_stun'),
          'enchant_critical'  =>  $request->getPost('enchant_critical'),
          'enchant_penetrate' =>  $request->getPost('enchant_penetrate'),
          'resist_sword'      =>  $request->getPost('resist_sword'),
          'resist_twohand'    =>  $request->getPost('resist_twohand'),
          'resist_dagger'     =>  $request->getPost('resist_dagger'),
          'resist_bell'       =>  $request->getPost('resist_bell'),
          'resist_fan'        =>  $request->getPost('resist_fan'),
          'resist_bow'        =>  $request->getPost('resist_bow'),
          'resist_fire'       =>  $request->getPost('resist_fire'),
          'resist_elect'      =>  $request->getPost('resist_elect'),
          'resist_magic'      =>  $request->getPost('resist_magic'),
          'resist_wind'       =>  $request->getPost('resist_wind'),
          'resist_poison'     =>  $request->getPost('resist_poison'),
        ];
        $result = $this->canavarModel->Guncelle($data,$kontrol->vnum,$db);
        if ($result) {
          LogAdd(lang('Canavar.kayit.canavarDuzenlendi',['locale_name' => mb_convert_encoding($kontrol->locale_name, 'UTF-8' ,"ISO-8859-9"), 'vnum' => $kontrol->vnum]),'Canavar/Index',session('user_id'));
          responseResult('success',lang('Canavar.cikti.canavarDuzenlendi'));
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
    if (!IsAllowedViewModule('canavarDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    if (p2pStatus==0) {
      responseResult('error',lang('Genel.p2pKapali'));
    }
    foreach (p2pPorts as $key => $value) {
      SendServer('P',"RELOAD",$value);
    }
    LogAdd(lang('Canavar.cikti.sunucuyaGonderildi'),'Canavar/Index',session('user_id'));
    responseResult('success',lang('Canavar.cikti.sunucuyaGonderildi'));
  }

  public function Droplar($mob_vnum = 0)
  {
    if (!IsAllowedViewModule('canavarDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect('metin2');
    $request  = \Config\Services::request();
    $kontrol  = $this->canavarModel->MobProtoKontrol($mob_vnum,$db);
    if (!$kontrol) {
      responseResult('error',lang('Canavar.cikti.canavarYok'));
    }
    $siralama = ['item_vnum','count','prob'];
    $query    = "SELECT drop_default.mob_vnum, drop_default.item_vnum, drop_default.count, drop_default.prob, item_proto.locale_name FROM player.drop_default ";
    $query    .= "LEFT JOIN player.item_proto on player.item_proto.vnum=player.drop_default.item_vnum ";
    $query    .= " WHERE mob_vnum = ".$kontrol->vnum;

    if (
      isset($siralama[$request->getPost('order[0][column]')])
      && in_array($request->getPost('order[0][dir]'),['asc','desc'])
    ) {
      $query  .= " ORDER BY ".$siralama[$request->getPost('order[0][column]')].' '.addslashes(addcslashes($request->getPost('order[0][dir]'),'%'));
    }

    $yaz  = $this->canavarModel->AjaxAra($query,$db);
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $itemIcon = $this->canavarModel->ItemIcon($value->item_vnum);
      if (!empty($itemIcon) && $itemIcon!="-") {
        $sub_array[] = '<img src="'.base_url('assets/img/icon/'.$itemIcon->icon).'" title="'.$value->item_vnum.'"> '.$value->item_vnum.' - '.mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9");
      }else {
        $sub_array[] = $value->item_vnum.' - '.mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9");
      }
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
    if (!IsAllowedViewModule('canavarDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'item_vnum' => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'count'     => ['label' => lang('Genel.adet'),  'rules' => "required|integer"],
      'prob'      => ['label' => lang('Genel.fiyat'), 'rules' => "required"],
      'vnum'      => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->canavarModel->MobProtoKontrol($request->getPost('vnum'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Canavar.cikti.canavarYok'));
      }else {
        $esyaKontrol  = $this->canavarModel->ItemProtoKontrol($request->getPost('item_vnum'),$db);
        if (!$esyaKontrol) {
          responseResult('error',lang('Esya.cikti.esyaYok'));
        }
        $data = [
          'mob_vnum'  =>  $kontrol->vnum,
          'item_vnum' =>  $esyaKontrol->vnum,
          'count'     =>  $request->getPost('count'),
          'prob'      =>  $request->getPost('prob'),
        ];
        $result = $this->canavarModel->DropEkle($data,$db);
        if ($result) {
          LogAdd(lang('Canavar.kayit.dropEklendi',['mob' => mb_convert_encoding($kontrol->locale_name, 'UTF-8' ,"ISO-8859-9"), 'item' => mb_convert_encoding($esyaKontrol->locale_name, 'UTF-8' ,"ISO-8859-9")]),'Canavar/Index',session('user_id'));
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
    if (!IsAllowedViewModule('canavarDuzenleyebilsin')) {
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
      $kontrol  = $this->canavarModel->DropKontrol($request->getPost('drop_mob_vnum'),$request->getPost('drop_item_vnum'),$request->getPost('drop_count'),$request->getPost('drop_prob'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Esya.cikti.esyaYok'));
      }else {
        $data = [
          'count' =>  $request->getPost('newCount'),
          'prob'  =>  $request->getPost('newProb'),
        ];

        $mobKontrol   = $this->canavarModel->MobProtoKontrol($kontrol->mob_vnum,$db);
        $esyaKontrol  = $this->canavarModel->ItemProtoKontrol($kontrol->item_vnum,$db);

        $result = $this->canavarModel->DropGuncelle($data,$kontrol->mob_vnum,$kontrol->item_vnum,$kontrol->count,$kontrol->prob,$db);
        if ($result) {
          LogAdd(lang('Canavar.kayit.dropGuncellendi',['mob' => mb_convert_encoding((isset($mobKontrol->locale_name)?$mobKontrol->locale_name:$kontrol->mob_vnum), 'UTF-8' ,"ISO-8859-9"), 'item' => mb_convert_encoding((isset($esyaKontrol->locale_name)?$esyaKontrol->locale_name:$kontrol->mob_vnum), 'UTF-8' ,"ISO-8859-9")]),'Canavar/Index',session('user_id'));
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
    if (!IsAllowedViewModule('canavarDuzenleyebilsin')) {
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
      $kontrol  = $this->canavarModel->DropKontrol($request->getPost('mob_vnum'),$request->getPost('item_vnum'),$request->getPost('count'),$request->getPost('prob'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Esya.cikti.esyaYok'));
      }else {
        $mobKontrol   = $this->canavarModel->MobProtoKontrol($kontrol->mob_vnum,$db);
        $esyaKontrol  = $this->canavarModel->ItemProtoKontrol($kontrol->item_vnum,$db);

        $result = $this->canavarModel->DropSil($kontrol->mob_vnum,$kontrol->item_vnum,$kontrol->count,$kontrol->prob,$db);
        if ($result) {
          LogAdd(lang('Canavar.kayit.dropSilindi',['mob' => mb_convert_encoding((isset($mobKontrol->locale_name)?$mobKontrol->locale_name:$kontrol->mob_vnum), 'UTF-8' ,"ISO-8859-9"), 'item' => mb_convert_encoding((isset($esyaKontrol->locale_name)?$esyaKontrol->locale_name:$kontrol->mob_vnum), 'UTF-8' ,"ISO-8859-9")]),'Canavar/Index',session('user_id'));
          responseResult('success',lang('Canavar.cikti.dropSilindi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function DropLevel($mob_vnum = 0)
  {
    if (!IsAllowedViewModule('canavarDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect('metin2');
    $request  = \Config\Services::request();
    $kontrol  = $this->canavarModel->MobProtoKontrol($mob_vnum,$db);
    if (!$kontrol) {
      responseResult('error',lang('Canavar.cikti.canavarYok'));
    }
    $siralama = ['drop_mob_item_level.group_id','drop_mob_group_level.level_start','drop_mob_group_level.level_end','item_vnum','count','prob'];
    $query    = "SELECT drop_mob_item_level.group_id, drop_mob_group_level.level_start, drop_mob_group_level.level_end, drop_mob_item_level.item_vnum, drop_mob_item_level.count, drop_mob_item_level.prob, item_proto.locale_name FROM player.drop_mob_item_level ";
    $query    .= "LEFT JOIN player.drop_mob_group_level on player.drop_mob_group_level.group_id=player.drop_mob_item_level.group_id ";
    $query    .= "LEFT JOIN player.item_proto on player.item_proto.vnum=player.drop_mob_item_level.item_vnum ";
    $query    .= " WHERE drop_mob_group_level.mob_vnum = ".$kontrol->vnum;

    if (
      isset($siralama[$request->getPost('order[0][column]')])
      && in_array($request->getPost('order[0][dir]'),['asc','desc'])
    ) {
      $query  .= " ORDER BY ".$siralama[$request->getPost('order[0][column]')].' '.addslashes(addcslashes($request->getPost('order[0][dir]'),'%'));
    }

    $yaz  = $this->canavarModel->AjaxAra($query,$db);
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->group_id;
      $sub_array[] = $value->level_start;
      $sub_array[] = $value->level_end;
      $itemIcon = $this->canavarModel->ItemIcon($value->item_vnum);
      if (!empty($itemIcon) && $itemIcon!="-") {
        $sub_array[] = '<img src="'.base_url('assets/img/icon/'.$itemIcon->icon).'" title="'.$value->item_vnum.'"> '.$value->item_vnum.' - '.mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9");
      }else {
        $sub_array[] = $value->item_vnum.' - '.mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9");
      }
      $sub_array[] = $value->count;
      $sub_array[] = $value->prob;
      $buttons  =  '<a class="btn btn-primary pt-1 pb-1 ps-2 pe-2" data-bs-toggle="modal" data-bs-target="#dropLevelDuzenle" href="javascript:void(0)" data-level_start="'.$value->level_start.'" data-level_end="'.$value->level_end.'" data-locale_name="'.mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9").'" data-group_id="'.$value->group_id.'" data-item_vnum="'.$value->item_vnum.'" data-count="'.$value->count.'" data-prob="'.$value->prob.'">
      <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" style="width:25px;height:25px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 7h-3a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-3" /><path d="M9 15h3l8.5 -8.5a1.5 1.5 0 0 0 -3 -3l-8.5 8.5v3" /><line x1="16" y1="5" x2="19" y2="8" /></svg>
      </a>';
      $buttons .=  '<a class="btn btn-danger pt-1 pb-1 ps-2 pe-2 ms-2 dropLevelSil" href="javascript:void(0)" data-group_id="'.$value->group_id.'" data-item_vnum="'.$value->item_vnum.'" data-count="'.$value->count.'" data-prob="'.$value->prob.'">
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

  public function DropLevelEkle()
  {
    if (!IsAllowedViewModule('canavarDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'level_group_id'  => ['label' => lang('Canavar.sayfa.group_id'),        'rules' => "required|integer"],
      'level_start'     => ['label' => lang('Canavar.sayfa.levelBaslangic'),  'rules' => "required|integer"],
      'level_end'       => ['label' => lang('Canavar.sayfa.levelBitis'),      'rules' => "required|integer"],
      'level_item_vnum' => ['label' => lang('Genel.esya'),                    'rules' => "required|integer"],
      'level_count'     => ['label' => lang('Genel.adet'),                    'rules' => "required|integer"],
      'level_prob'      => ['label' => lang('Genel.fiyat'),                   'rules' => "required"],
      'vnum'            => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db           = \Config\Database::connect('metin2');
      $grupGenelKontrol  = $this->canavarModel->DropLevelGrupGenelKontrol($request->getPost('level_group_id'),$request->getPost('vnum'),$db);
      if ($grupGenelKontrol) {
        responseResult('error',lang('Canavar.cikti.grupIDKullaniliyor'));
      }
      $grupKontrol  = $this->canavarModel->DropLevelGrupKontrol($request->getPost('level_group_id'),$request->getPost('vnum'),$request->getPost('level_start'),$request->getPost('level_end'),$db);
      $kontrol      = $this->canavarModel->MobProtoKontrol($request->getPost('vnum'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Canavar.cikti.canavarYok'));
      }else {
        $esyaKontrol  = $this->canavarModel->ItemProtoKontrol($request->getPost('level_item_vnum'),$db);
        if (!$esyaKontrol) {
          responseResult('error',lang('Esya.cikti.esyaYok'));
        }
        if (!$grupKontrol) {
          $data = [
            'group_id'    =>  $request->getPost('level_group_id'),
            'mob_vnum'    =>  $kontrol->vnum,
            'level_start' =>  $request->getPost('level_start'),
            'level_end'   =>  $request->getPost('level_end'),
          ];
          $result = $this->canavarModel->DropLevelGrupEkle($data,$db);
          if (!$result) {
            responseResult('error',lang('Genel.bilinmeyenHata'));
          }
        }
        $data = [
          'group_id'  =>  $request->getPost('level_group_id'),
          'item_vnum' =>  $esyaKontrol->vnum,
          'count'     =>  $request->getPost('level_count'),
          'prob'      =>  $request->getPost('level_prob'),
        ];
        $result = $this->canavarModel->DropLevelEkle($data,$db);
        if ($result) {
          LogAdd(lang('Canavar.kayit.dropEklendi',['mob' => mb_convert_encoding($kontrol->locale_name, 'UTF-8' ,"ISO-8859-9"), 'item' => mb_convert_encoding($esyaKontrol->locale_name, 'UTF-8' ,"ISO-8859-9")]),'Canavar/Index',session('user_id'));
          responseResult('success',lang('Canavar.cikti.dropEklendi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function DropLevelGuncelle()
  {
    if (!IsAllowedViewModule('canavarDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'drop_level_item_vnum'  => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'drop_level_count'      => ['label' => lang('Genel.adet'),  'rules' => "required|integer"],
      'drop_level_prob'       => ['label' => lang('Genel.fiyat'), 'rules' => "required"],
      'drop_level_group_id'   => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->canavarModel->DropLevelKontrol($request->getPost('drop_level_group_id'),$request->getPost('drop_level_item_vnum'),$request->getPost('drop_level_count'),$request->getPost('drop_level_prob'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Esya.cikti.esyaYok'));
      }else {
        $data = [
          'count' =>  $request->getPost('levelNewCount'),
          'prob'  =>  $request->getPost('levelNewProb'),
        ];

        $esyaKontrol  = $this->canavarModel->ItemProtoKontrol($kontrol->item_vnum,$db);

        $result = $this->canavarModel->DropLevelGuncelle($data,$kontrol->group_id,$kontrol->item_vnum,$kontrol->count,$kontrol->prob,$db);
        if ($result) {
          LogAdd(lang('Canavar.kayit.dropLevelGuncellendi',['group_id' => $kontrol->group_id, 'item' => mb_convert_encoding((isset($esyaKontrol->locale_name)?$esyaKontrol->locale_name:$kontrol->mob_vnum), 'UTF-8' ,"ISO-8859-9")]),'Canavar/Index',session('user_id'));
          responseResult('success',lang('Canavar.cikti.dropGuncellendi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function DropLevelSil()
  {
    if (!IsAllowedViewModule('canavarDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'group_id'  => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'item_vnum' => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'count'     => ['label' => lang('Genel.adet'),  'rules' => "required|integer"],
      'prob'      => ['label' => lang('Genel.fiyat'), 'rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->canavarModel->DropLevelKontrol($request->getPost('group_id'),$request->getPost('item_vnum'),$request->getPost('count'),$request->getPost('prob'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Esya.cikti.esyaYok'));
      }else {
        $esyaKontrol  = $this->canavarModel->ItemProtoKontrol($kontrol->item_vnum,$db);

        $result = $this->canavarModel->DropLevelSil($kontrol->group_id,$kontrol->item_vnum,$kontrol->count,$kontrol->prob,$db);
        if ($result) {
          $dropLevelEsyalar  = $this->canavarModel->DropLevelEsyalar($request->getPost('group_id'),$db);
          if ($dropLevelEsyalar==0) {
            $this->canavarModel->DropLevelGrupSil($kontrol->group_id,$kontrol->mob_vnum,$kontrol->level_start,$kontrol->level_end,$db);
          }
          LogAdd(lang('Canavar.kayit.dropLevelSilindi',['group_id' => $kontrol->group_id, 'item' => mb_convert_encoding((isset($esyaKontrol->locale_name)?$esyaKontrol->locale_name:$kontrol->mob_vnum), 'UTF-8' ,"ISO-8859-9")]),'Canavar/Index',session('user_id'));
          responseResult('success',lang('Canavar.cikti.dropSilindi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function DropKill($mob_vnum = 0)
  {
    if (!IsAllowedViewModule('canavarDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect('metin2');
    $request  = \Config\Services::request();
    $kontrol  = $this->canavarModel->MobProtoKontrol($mob_vnum,$db);
    if (!$kontrol) {
      responseResult('error',lang('Canavar.cikti.canavarYok'));
    }
    $siralama = ['drop_mob_item_kill.group_id','drop_mob_group_kill.kill_per_drop','item_vnum','count','part_prob'];
    $query    = "SELECT drop_mob_item_kill.group_id, drop_mob_group_kill.kill_per_drop, drop_mob_item_kill.item_vnum, drop_mob_item_kill.count, drop_mob_item_kill.part_prob, item_proto.locale_name FROM player.drop_mob_item_kill ";
    $query    .= "LEFT JOIN player.drop_mob_group_kill on player.drop_mob_group_kill.group_id=player.drop_mob_item_kill.group_id ";
    $query    .= "LEFT JOIN player.item_proto on player.item_proto.vnum=player.drop_mob_item_kill.item_vnum ";
    $query    .= " WHERE drop_mob_group_kill.mob_vnum = ".$kontrol->vnum;

    if (
      isset($siralama[$request->getPost('order[0][column]')])
      && in_array($request->getPost('order[0][dir]'),['asc','desc'])
    ) {
      $query  .= " ORDER BY ".$siralama[$request->getPost('order[0][column]')].' '.addslashes(addcslashes($request->getPost('order[0][dir]'),'%'));
    }

    $yaz  = $this->canavarModel->AjaxAra($query,$db);
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->group_id;
      $sub_array[] = $value->kill_per_drop;
      $itemIcon = $this->canavarModel->ItemIcon($value->item_vnum);
      if (!empty($itemIcon) && $itemIcon!="-") {
        $sub_array[] = '<img src="'.base_url('assets/img/icon/'.$itemIcon->icon).'" title="'.$value->item_vnum.'"> '.$value->item_vnum.' - '.mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9");
      }else {
        $sub_array[] = $value->item_vnum.' - '.mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9");
      }
      $sub_array[] = $value->count;
      $sub_array[] = $value->part_prob;
      $buttons  =  '<a class="btn btn-primary pt-1 pb-1 ps-2 pe-2" data-bs-toggle="modal" data-bs-target="#dropKillDuzenle" href="javascript:void(0)" data-kill_per_drop="'.$value->kill_per_drop.'" data-locale_name="'.mb_convert_encoding($value->locale_name, 'UTF-8' ,"ISO-8859-9").'" data-group_id="'.$value->group_id.'" data-item_vnum="'.$value->item_vnum.'" data-count="'.$value->count.'" data-part_prob="'.$value->part_prob.'">
      <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" style="width:25px;height:25px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 7h-3a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-3" /><path d="M9 15h3l8.5 -8.5a1.5 1.5 0 0 0 -3 -3l-8.5 8.5v3" /><line x1="16" y1="5" x2="19" y2="8" /></svg>
      </a>';
      $buttons .=  '<a class="btn btn-danger pt-1 pb-1 ps-2 pe-2 ms-2 dropKillSil" href="javascript:void(0)" data-group_id="'.$value->group_id.'" data-item_vnum="'.$value->item_vnum.'" data-count="'.$value->count.'" data-part_prob="'.$value->part_prob.'">
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

  public function DropKillEkle()
  {
    if (!IsAllowedViewModule('canavarDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'kill_group_id'       => ['label' => lang('Canavar.sayfa.group_id'),        'rules' => "required|integer"],
      'kill_kill_per_drop'  => ['label' => lang('Canavar.sayfa.killSayisi'),      'rules' => "required|integer"],
      'kill_item_vnum'      => ['label' => lang('Genel.esya'),                    'rules' => "required|integer"],
      'kill_count'          => ['label' => lang('Genel.adet'),                    'rules' => "required|integer"],
      'kill_part_prob'      => ['label' => lang('Genel.sans'),                    'rules' => "required"],
      'vnum'                => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db           = \Config\Database::connect('metin2');
      $grupGenelKontrol  = $this->canavarModel->DropKillGrupGenelKontrol($request->getPost('kill_group_id'),$request->getPost('vnum'),$db);
      if ($grupGenelKontrol) {
        responseResult('error',lang('Canavar.cikti.grupIDKullaniliyor'));
      }
      $grupKontrol  = $this->canavarModel->DropKillGrupKontrol($request->getPost('kill_group_id'),$request->getPost('vnum'),$request->getPost('kill_kill_per_drop'),$db);
      $kontrol      = $this->canavarModel->MobProtoKontrol($request->getPost('vnum'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Canavar.cikti.canavarYok'));
      }else {
        $esyaKontrol  = $this->canavarModel->ItemProtoKontrol($request->getPost('kill_item_vnum'),$db);
        if (!$esyaKontrol) {
          responseResult('error',lang('Esya.cikti.esyaYok'));
        }
        if (!$grupKontrol) {
          $data = [
            'group_id'      =>  $request->getPost('kill_group_id'),
            'mob_vnum'      =>  $kontrol->vnum,
            'kill_per_drop' =>  $request->getPost('kill_kill_per_drop'),
          ];
          $result = $this->canavarModel->DropKillGrupEkle($data,$db);
          if (!$result) {
            responseResult('error',lang('Genel.bilinmeyenHata'));
          }
        }
        $data = [
          'group_id'  =>  $request->getPost('kill_group_id'),
          'item_vnum' =>  $esyaKontrol->vnum,
          'count'     =>  $request->getPost('kill_count'),
          'part_prob' =>  $request->getPost('kill_part_prob'),
        ];
        $result = $this->canavarModel->DropKillEkle($data,$db);
        if ($result) {
          LogAdd(lang('Canavar.kayit.dropEklendi',['mob' => mb_convert_encoding($kontrol->locale_name, 'UTF-8' ,"ISO-8859-9"), 'item' => mb_convert_encoding($esyaKontrol->locale_name, 'UTF-8' ,"ISO-8859-9")]),'Canavar/Index',session('user_id'));
          responseResult('success',lang('Canavar.cikti.dropEklendi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function DropKillGuncelle()
  {
    if (!IsAllowedViewModule('canavarDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'drop_kill_item_vnum'  => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'drop_kill_count'      => ['label' => lang('Genel.adet'),  'rules' => "required|integer"],
      'drop_kill_part_prob'  => ['label' => lang('Genel.fiyat'), 'rules' => "required"],
      'drop_kill_group_id'   => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->canavarModel->DropKillKontrol($request->getPost('drop_kill_group_id'),$request->getPost('drop_kill_item_vnum'),$request->getPost('drop_kill_count'),$request->getPost('drop_kill_part_prob'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Esya.cikti.esyaYok'));
      }else {
        $data = [
          'count'     =>  $request->getPost('killNewCount'),
          'part_prob' =>  $request->getPost('killNewPartProb'),
        ];

        $esyaKontrol  = $this->canavarModel->ItemProtoKontrol($kontrol->item_vnum,$db);

        $result = $this->canavarModel->DropKillGuncelle($data,$kontrol->group_id,$kontrol->item_vnum,$kontrol->count,$kontrol->part_prob,$db);
        if ($result) {
          LogAdd(lang('Canavar.kayit.dropKillGuncellendi',['group_id' => $kontrol->group_id, 'item' => mb_convert_encoding((isset($esyaKontrol->locale_name)?$esyaKontrol->locale_name:$kontrol->mob_vnum), 'UTF-8' ,"ISO-8859-9")]),'Canavar/Index',session('user_id'));
          responseResult('success',lang('Canavar.cikti.dropGuncellendi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function DropKillSil()
  {
    if (!IsAllowedViewModule('canavarDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'group_id'  => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'item_vnum' => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'count'     => ['label' => lang('Genel.adet'),  'rules' => "required|integer"],
      'part_prob' => ['label' => lang('Genel.fiyat'), 'rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->canavarModel->DropKillKontrol($request->getPost('group_id'),$request->getPost('item_vnum'),$request->getPost('count'),$request->getPost('part_prob'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Esya.cikti.esyaYok'));
      }else {
        $esyaKontrol  = $this->canavarModel->ItemProtoKontrol($kontrol->item_vnum,$db);

        $result = $this->canavarModel->DropKillSil($kontrol->group_id,$kontrol->item_vnum,$kontrol->count,$kontrol->part_prob,$db);
        if ($result) {
          $dropKillEsyalar  = $this->canavarModel->DropKillEsyalar($request->getPost('group_id'),$db);
          if ($dropKillEsyalar==0) {
            $this->canavarModel->DropKillGrupSil($kontrol->group_id,$kontrol->mob_vnum,$kontrol->kill_per_drop,$db);
          }
          LogAdd(lang('Canavar.kayit.dropKillSilindi',['group_id' => $kontrol->group_id, 'item' => mb_convert_encoding((isset($esyaKontrol->locale_name)?$esyaKontrol->locale_name:$kontrol->mob_vnum), 'UTF-8' ,"ISO-8859-9")]),'Canavar/Index',session('user_id'));
          responseResult('success',lang('Canavar.cikti.dropSilindi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Canavarlar()
  {
    if (
      IsAllowedViewModule('esyaDuzenleyebilsin')
      || IsAllowedViewModule('npcEkleyebilsin')
    ) {
      $request  = \Config\Services::request();
      $search   = $request->getGet('q');
      if (!$search) {
        $search = "";
      }
      $esyalar = $this->canavarModel->CanavarAra($search);
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
