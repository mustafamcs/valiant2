<?php
namespace App\Models;
class Biyolog_model
{
  protected $biyologTable   = 'player.biolog_info';
  protected $itemProtoTable = 'player.item_proto';

  public function AjaxAra($search,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->biyologTable)
    ->groupStart()
    ->orLike($this->biyologTable.".mobVnum",$search)
    ->groupEnd()
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function Ajax($start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->biyologTable)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function Kontrol($mobVnum,$db)
  {
    return $db->table($this->biyologTable)
    ->where($this->biyologTable.'.mobVnum',$mobVnum)
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

  public function Ekle($data,$db)
  {
    return $db->table($this->biyologTable)->insert($data);
  }

  public function Guncelle($data,$mobVnum,$db)
  {
    return $db->table($this->biyologTable)
    ->where('mobVnum',$mobVnum)
    ->update($data);
  }

  public function Sil($mobVnum,$db)
  {
    return $db->table($this->biyologTable)
    ->where('mobVnum',$mobVnum)
    ->delete();
  }
}
