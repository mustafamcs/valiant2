<?php
namespace App\Models;
class Oyuncu_model
{
  protected $accountTable     = 'account.account';
  protected $playerTable      = 'player.player';
  protected $marketLogTable   = 'log.itemshop_log';
  protected $itemProtoTable   = 'player.item_proto';
  protected $mapIndexTable    = 'map_index';
  protected $iconTable        = 'item_icon';
  protected $itemTable        = 'player.item';
  protected $attrIDTable      = 'item_attr_id';
  protected $attrTextTable    = 'item_attr_text';
  protected $offlineShopTable = 'player.offline_shop_sales';
  protected $empireTable      = 'player.player_index';
  protected $awardTable       = 'player.item_award';

  public function OyuncuAra($column,$where,$db)
  {
    return $db->table($this->accountTable)
    ->where($column,$where)
    ->get()
    ->getRow();
  }

  public function OyuncuDetay($id)
  {
    if (GetFileCache('OyuncuDetay-'.Permalink($id))) {
      return GetFileCache('OyuncuDetay-'.Permalink($id));
    }else {
      $db   = \Config\Database::connect('metin2');
      $data = $db->table($this->accountTable)
      ->where('id',$id)
      ->get()
      ->getRow();
      CreateFileCache('OyuncuDetay-'.Permalink($id),$data,600);
      return $data;
    }
  }

  public function OyuncuHesaplari($account_id)
  {
    if (GetFileCache('OyuncuHesaplari-'.Permalink($account_id))) {
      return GetFileCache('OyuncuHesaplari-'.Permalink($account_id));
    }else {
      $db   = \Config\Database::connect('metin2');
      $data = $db->table($this->playerTable)
      ->where('account_id',$account_id)
      ->get()
      ->getResult();
      CreateFileCache('OyuncuHesaplari-'.Permalink($account_id),$data,600);
      return $data;
    }
  }

  public function OyuncuKontrol($id,$db)
  {
    return $db->table($this->accountTable)
    ->where('id',$id)
    ->get()
    ->getRow();
  }

  public function Guncelle($data,$id,$db)
  {
    return $db->table($this->accountTable)
    ->where('id',$id)
    ->update($data);
  }

  public function AjaxNesneMarketAra($player_pid,$search,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->marketLogTable)
    ->join($this->itemProtoTable,$this->itemProtoTable.'.vnum='.$this->marketLogTable.'.item_vnum','left')
    ->whereIn('player_pid',$player_pid)
    ->groupStart()
    ->orLike($this->marketLogTable.".item_vnum",$search)
    ->orLike($this->marketLogTable.".player_name",$search)
    ->groupEnd()
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function AjaxNesneMarket($player_pid,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->marketLogTable)
    ->join($this->itemProtoTable,$this->itemProtoTable.'.vnum='.$this->marketLogTable.'.item_vnum','left')
    ->whereIn('player_pid',$player_pid)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function KarakterAra($column,$where,$db)
  {
    return $db->table($this->playerTable)
    ->where($column,$where)
    ->get()
    ->getRow();
  }

  public function KarakterDetay($id)
  {
    if (GetFileCache('KarakterDetay-'.Permalink($id))) {
      return GetFileCache('KarakterDetay-'.Permalink($id));
    }else {
      $db   = \Config\Database::connect('metin2');
      $data = $db->table($this->playerTable)
      ->where('id',$id)
      ->get()
      ->getRow();
      CreateFileCache('KarakterDetay-'.Permalink($id),$data,600);
      return $data;
    }
  }

  public function MapIndex($id)
  {
    if (GetFileCache('MapIndex-'.Permalink($id))) {
      return GetFileCache('MapIndex-'.Permalink($id));
    }else {
      $db   = \Config\Database::connect();
      $data = $db->table($this->mapIndexTable)
      ->where('id',$id)
      ->get()
      ->getRow();
      CreateFileCache('MapIndex-'.Permalink($id),$data,86400);
      return $data;
    }
  }

  public function KarakterKontrol($id,$db)
  {
    return $db->table($this->playerTable)
    ->select($this->accountTable.'.login')
    ->select($this->playerTable.'.*')
    ->join($this->accountTable,$this->accountTable.'.id='.$this->playerTable.'.account_id','left')
    ->where($this->playerTable.'.id',$id)
    ->get()
    ->getRow();
  }

  public function KarakterGuncelle($data,$id,$db)
  {
    return $db->table($this->playerTable)
    ->where('id',$id)
    ->update($data);
  }

  public function AjaxKarakterNesneMarketAra($player_pid,$search,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->marketLogTable)
    ->join($this->itemProtoTable,$this->itemProtoTable.'.vnum='.$this->marketLogTable.'.item_vnum','left')
    ->where('player_pid',$player_pid)
    ->groupStart()
    ->orLike($this->marketLogTable.".item_vnum",$search)
    ->groupEnd()
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function AjaxKarakterNesneMarket($player_pid,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->marketLogTable)
    ->join($this->itemProtoTable,$this->itemProtoTable.'.vnum='.$this->marketLogTable.'.item_vnum','left')
    ->where('player_pid',$player_pid)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function AjaxAra($query,$db)
  {
    header('Content-Type: text/html; charset=latin5');
    return $db->query($query)->getResult();
  }

  public function ItemIcon($vnum)
  {
    if (GetFileCache('ItemIcon-'.$vnum)) {
      return GetFileCache('ItemIcon-'.$vnum);
    }else {
      $db   = \Config\Database::connect();
      $data = $db->table($this->iconTable)
      ->where('vnum',$vnum)
      ->get()
      ->getRow();
      CreateFileCache('ItemIcon-'.$vnum,$data,86400);
      return $data;
    }
  }

  public function EnvanterEsyalari($id)
  {
    if (GetFileCache('EnvanterEsyalari-'.Permalink($id))) {
      return GetFileCache('EnvanterEsyalari-'.Permalink($id));
    }else {
      $db   = \Config\Database::connect('metin2');
      $data = $db->table($this->itemTable)
      ->join($this->itemProtoTable,$this->itemProtoTable.'.vnum='.$this->itemTable.'.vnum','left')
      ->where('owner_id',$id)
      ->get()
      ->getResult();
      CreateFileCache('EnvanterEsyalari-'.Permalink($id),$data,600);
      return $data;
    }
  }

  public function EfsunlarID()
  {
    if (GetFileCache('EfsunlarID')) {
      return GetFileCache('EfsunlarID');
    }else {
      $db   = \Config\Database::connect();
      $data = $db->table($this->attrIDTable)
      ->get()
      ->getResult();
      CreateFileCache('EfsunlarID',$data,86400);
      return $data;
    }
  }

  public function EfsunlarText()
  {
    if (GetFileCache('EfsunlarID')) {
      return GetFileCache('EfsunlarID');
    }else {
      $db   = \Config\Database::connect();
      $data = $db->table($this->attrTextTable)
      ->get()
      ->getResult();
      CreateFileCache('EfsunlarID',$data,86400);
      return $data;
    }
  }

  public function DepoVeNesneMarket($id)
  {
    if (GetFileCache('DepoVeNesneMarket-'.Permalink($id))) {
      return GetFileCache('DepoVeNesneMarket-'.Permalink($id));
    }else {
      $db   = \Config\Database::connect('metin2');
      $data = $db->table($this->itemTable)
      ->join($this->itemProtoTable,$this->itemProtoTable.'.vnum='.$this->itemTable.'.vnum','left')
      ->where('owner_id',$id)
      ->whereIn('window',['SAFEBOX','MALL'])
      ->get()
      ->getResult();
      CreateFileCache('DepoVeNesneMarket-'.Permalink($id),$data,600);
      return $data;
    }
  }

  public function AjaxKarakterPazarAra($buyer_id,$search,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->offlineShopTable)
    ->join($this->itemProtoTable,$this->itemProtoTable.'.vnum='.$this->offlineShopTable.'.item_vnum','left')
    ->where('buyer_id',$buyer_id)
    ->groupStart()
    ->orLike($this->offlineShopTable.".item_vnum",$search)
    ->groupEnd()
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function AjaxKarakterPazar($buyer_id,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->offlineShopTable)
    ->join($this->itemProtoTable,$this->itemProtoTable.'.vnum='.$this->offlineShopTable.'.item_vnum','left')
    ->where('buyer_id',$buyer_id)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function OyuncuBayrak($id)
  {
    if (GetFileCache('OyuncuBayrak-'.Permalink($id))) {
      return GetFileCache('OyuncuBayrak-'.Permalink($id));
    }else {
      $db   = \Config\Database::connect('metin2');
      $data = $db->table($this->empireTable)
      ->where('id',$id)
      ->get()
      ->getRow();
      CreateFileCache('OyuncuBayrak-'.Permalink($id),$data,600);
      return $data;
    }
  }

  public function BayrakGuncelle($data,$id,$db)
  {
    return $db->table($this->empireTable)
    ->where('id',$id)
    ->update($data);
  }

  public function EsyaEkle($data,$db)
  {
    return $db->table($this->awardTable)->insert($data);
  }

  public function ItemProtoKontrol($vnum,$db)
  {
    return $db->table($this->itemProtoTable)
    ->where('vnum',$vnum)
    ->get()
    ->getRow();
  }
}
