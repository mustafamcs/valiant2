<?php
namespace App\Models;
class NPC_model
{
  protected $shopTable      = 'player.shop';
  protected $mobProtoTable  = 'player.mob_proto';
  protected $itemProtoTable = 'player.item_proto';
  protected $shopItemTable  = 'player.shop_item';
  protected $iconTable      = 'item_icon';

  public function AjaxAra($search,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->shopTable)
    ->select($this->mobProtoTable.'.locale_name')
    ->select($this->shopTable.'.*')
    ->join($this->mobProtoTable,$this->mobProtoTable.'.vnum='.$this->shopTable.'.npc_vnum','left')
    ->groupStart()
    ->orLike($this->shopTable.".name",$search)
    ->orLike($this->mobProtoTable.".locale_name",mb_convert_encoding(addslashes(addcslashes($search,'%')), 'ISO-8859-9' ,"UTF-8"))
    ->groupEnd()
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function Ajax($start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->shopTable)
    ->select($this->mobProtoTable.'.locale_name')
    ->select($this->shopTable.'.*')
    ->join($this->mobProtoTable,$this->mobProtoTable.'.vnum='.$this->shopTable.'.npc_vnum','left')
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function Kontrol($vnum,$db)
  {
    return $db->table($this->shopTable)
    ->select($this->mobProtoTable.'.locale_name')
    ->select($this->shopTable.'.*')
    ->join($this->mobProtoTable,$this->mobProtoTable.'.vnum='.$this->shopTable.'.npc_vnum','left')
    ->where($this->shopTable.'.vnum',$vnum)
    ->get()
    ->getRow();
  }

  public function ItemProtoKontrol($vnum)
  {
    if (GetFileCache('ItemProtoKontrol-'.permalink($vnum))) {
      return GetFileCache('ItemProtoKontrol-'.permalink($vnum));
    }else {
      $db   = \Config\Database::connect('metin2');
      $data = $db->table($this->itemProtoTable)
      ->where('vnum',$vnum)
      ->get()
      ->getRow();
      CreateFileCache('ItemProtoKontrol-'.permalink($vnum),$data,600);
      return $data;
    }
  }

  public function MobProtoKontrol($vnum,$db)
  {
    return $db->table($this->mobProtoTable)
    ->where('vnum',$vnum)
    ->get()
    ->getRow();
  }

  public function Ekle($data,$db)
  {
    return $db->table($this->shopTable)->insert($data);
  }

  public function Guncelle($data,$vnum,$db)
  {
    return $db->table($this->shopTable)
    ->where('vnum',$vnum)
    ->update($data);
  }

  public function Sil($vnum,$db)
  {
    return $db->table($this->shopTable)
    ->where('vnum',$vnum)
    ->delete();
  }

  public function Query($query,$db)
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

  public function EsyaEkle($data,$db)
  {
    return $db->table($this->shopItemTable)
    ->insert($data);
  }

  public function EsyaKontrol($shop_vnum,$item_vnum,$count,$db)
  {
    return $db->table($this->shopItemTable)
    ->where('shop_vnum',$shop_vnum)
    ->where('item_vnum',$item_vnum)
    ->where('count',$count)
    ->get()
    ->getRow();
  }

  public function EsyaGuncelle($data,$shop_vnum,$item_vnum,$count,$db)
  {
    return $db->table($this->shopItemTable)
    ->where('shop_vnum',$shop_vnum)
    ->where('item_vnum',$item_vnum)
    ->where('count',$count)
    ->update($data);
  }

  public function EsyaSil($shop_vnum,$item_vnum,$count,$db)
  {
    return $db->table($this->shopItemTable)
    ->where('shop_vnum',$shop_vnum)
    ->where('item_vnum',$item_vnum)
    ->where('count',$count)
    ->delete();
  }
}
