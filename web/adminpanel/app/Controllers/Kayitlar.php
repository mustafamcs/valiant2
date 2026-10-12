<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class Kayitlar extends BaseController
{
  public $viewFolder  = "";
  public $kayitModel  = "";

  public function __construct()
  {
    $this->viewFolder = "Kayitlar";
    $this->kayitModel = model('Kayit_model');
    if (!session('user_id')) {
      header('Location: '.base_url('GirisYap'));
      exit;
    }
  }

  public function Boot()
  {
    if (!IsAllowedViewModule('bootKayitGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Boot",$viewData);
  }

  public function AjaxBoot()
  {
    if (!IsAllowedViewModule('bootKayitGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect('metin2');
    $request  = \Config\Services::request();
    $siralama = ['hostname','channel','time'];
    $query    = "SELECT * FROM log.bootlog ";

    if (
      in_array($request->getPost('searchType'),['hostname','channel'])
      && in_array($request->getPost('searchWhere'),['=','!=','%'])
      && !empty($request->getPost('logSearch'))
    ) {
      if ($request->getPost('searchWhere')=="%") {
        $query  .= " WHERE ".addslashes(addcslashes($request->getPost('searchType'),'%'))." LIKE '%".mb_convert_encoding(addslashes(addcslashes($request->getPost('logSearch'),'%')), 'ISO-8859-9' ,"UTF-8")."%'";
      }else {
        $query  .= " WHERE ".addslashes(addcslashes($request->getPost('searchType'),'%'))." ".addslashes(addcslashes($request->getPost('searchWhere'),'%'))." '".mb_convert_encoding(addslashes(addcslashes($request->getPost('logSearch'),'%')), 'ISO-8859-9' ,"UTF-8")."'";
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

    $yaz  = $this->kayitModel->AjaxAra($query,$db);
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->hostname;
      $sub_array[] = $value->channel;
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

  public function GM()
  {
    if (!IsAllowedViewModule('gmKomutKayitGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/GM",$viewData);
  }

  public function AjaxGM()
  {
    if (!IsAllowedViewModule('gmKomutKayitGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect('metin2');
    $request  = \Config\Services::request();
    $siralama = ['username','command','ip','date'];
    $query    = "SELECT * FROM log.command_log ";

    if (
      in_array($request->getPost('searchType'),['username','command','ip'])
      && in_array($request->getPost('searchWhere'),['=','!=','%'])
      && !empty($request->getPost('logSearch'))
    ) {
      if ($request->getPost('searchWhere')=="%") {
        $query  .= " WHERE ".addslashes(addcslashes($request->getPost('searchType'),'%'))." LIKE '%".mb_convert_encoding(addslashes(addcslashes($request->getPost('logSearch'),'%')), 'ISO-8859-9' ,"UTF-8")."%'";
      }else {
        $query  .= " WHERE ".addslashes(addcslashes($request->getPost('searchType'),'%'))." ".addslashes(addcslashes($request->getPost('searchWhere'),'%'))." '".mb_convert_encoding(addslashes(addcslashes($request->getPost('logSearch'),'%')), 'ISO-8859-9' ,"UTF-8")."'";
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

    $yaz  = $this->kayitModel->AjaxAra($query,$db);
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->username;
      $sub_array[] = mb_convert_encoding($value->command, 'UTF-8' ,"ISO-8859-9");
      $sub_array[] = $value->ip;
      $sub_array[] = DateDMYHMS($value->date);
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

  public function NesneMarket()
  {
    if (!IsAllowedViewModule('nesneKayitlariGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/NesneMarket",$viewData);
  }

  public function AjaxNesneMarket()
  {
    if (!IsAllowedViewModule('nesneKayitlariGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect('metin2');
    $request  = \Config\Services::request();
    $siralama = ['item_vnum','player_name','item_price','buy_date'];
    $query    = "SELECT * FROM log.itemshop_log ";
    $query    .= "LEFT JOIN player.item_proto on player.item_proto.vnum=log.itemshop_log.item_vnum ";

    if (
      in_array($request->getPost('searchType'),['vnum','player_name'])
      && in_array($request->getPost('searchWhere'),['=','!=','%'])
      && !empty($request->getPost('logSearch'))
    ) {
      if ($request->getPost('searchWhere')=="%") {
        $query  .= " WHERE ".addslashes(addcslashes($request->getPost('searchType'),'%'))." LIKE '%".mb_convert_encoding(addslashes(addcslashes($request->getPost('logSearch'),'%')), 'ISO-8859-9' ,"UTF-8")."%'";
      }else {
        $query  .= " WHERE ".addslashes(addcslashes($request->getPost('searchType'),'%'))." ".addslashes(addcslashes($request->getPost('searchWhere'),'%'))." '".mb_convert_encoding(addslashes(addcslashes($request->getPost('logSearch'),'%')), 'ISO-8859-9' ,"UTF-8")."'";
      }
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

    $yaz  = $this->kayitModel->AjaxAra($query,$db);
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

  public function Level()
  {
    if (!IsAllowedViewModule('levelKayitlariGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Level",$viewData);
  }

  public function AjaxLevel()
  {
    if (!IsAllowedViewModule('levelKayitlariGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect('metin2');
    $request  = \Config\Services::request();
    $siralama = ['name','level','playtime','time'];
    $query    = "SELECT * FROM log.levellog ";

    if (
      in_array($request->getPost('searchType'),['name','level'])
      && in_array($request->getPost('searchWhere'),['=','!=','%'])
      && !empty($request->getPost('logSearch'))
    ) {
      if ($request->getPost('searchWhere')=="%") {
        $query  .= " WHERE ".addslashes(addcslashes($request->getPost('searchType'),'%'))." LIKE '%".mb_convert_encoding(addslashes(addcslashes($request->getPost('logSearch'),'%')), 'ISO-8859-9' ,"UTF-8")."%'";
      }else {
        $query  .= " WHERE ".addslashes(addcslashes($request->getPost('searchType'),'%'))." ".addslashes(addcslashes($request->getPost('searchWhere'),'%'))." '".mb_convert_encoding(addslashes(addcslashes($request->getPost('logSearch'),'%')), 'ISO-8859-9' ,"UTF-8")."'";
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

    $yaz  = $this->kayitModel->AjaxAra($query,$db);
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->name;
      $sub_array[] = $value->level.' Lv.';
      $sub_array[] = $value->playtime.' dakika';
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

  public function Pazar()
  {
    if (!IsAllowedViewModule('pazarKayitlariGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Pazar",$viewData);
  }

  public function AjaxPazar()
  {
    if (!IsAllowedViewModule('pazarKayitlariGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect('metin2');
    $request  = \Config\Services::request();
    $siralama = ['id','buyer_name','item_vnum','item_count','item_price','datetime'];
    $query    = "SELECT * FROM player.offline_shop_sales ";
    $query    .= "LEFT JOIN player.item_proto on player.item_proto.vnum=player.offline_shop_sales.item_vnum ";

    if (
      in_array($request->getPost('searchType'),['item_vnum','buyer_name','item_price'])
      && in_array($request->getPost('searchWhere'),['=','!=','%'])
      && !empty($request->getPost('logSearch'))
    ) {
      if ($request->getPost('searchWhere')=="%") {
        $query  .= " WHERE ".addslashes(addcslashes($request->getPost('searchType'),'%'))." LIKE '%".mb_convert_encoding(addslashes(addcslashes($request->getPost('logSearch'),'%')), 'ISO-8859-9' ,"UTF-8")."%'";
      }else {
        $query  .= " WHERE ".addslashes(addcslashes($request->getPost('searchType'),'%'))." ".addslashes(addcslashes($request->getPost('searchWhere'),'%'))." '".mb_convert_encoding(addslashes(addcslashes($request->getPost('logSearch'),'%')), 'ISO-8859-9' ,"UTF-8")."'";
      }
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

    $yaz  = $this->kayitModel->AjaxAra($query,$db);
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->id;
      $sub_array[] = $value->buyer_name;
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
}
