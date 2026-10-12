<?php
namespace App\Models;
class Yukseltme_model
{
  protected $refineTable  = 'player.refine_proto';
  protected $iconTable    = 'item_icon';

  public function AjaxFiltrele($startID,$finishID,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->refineTable)
    ->where($this->refineTable.".id >=",$startID)
    ->where($this->refineTable.".id <=",$finishID)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function Ajax($start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->refineTable)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function Kontrol($id,$db)
  {
    return $db->table($this->refineTable)
    ->where('id',$id)
    ->get()
    ->getRow();
  }

  public function Ekle($data,$db)
  {
    return $db->table($this->refineTable)->insert($data);
  }

  public function Guncelle($data,$where,$db)
  {
    return $db->table($this->refineTable)
    ->where('id',$where)
    ->update($data);
  }

  public function Sil($where,$db)
  {
    return $db->table($this->refineTable)
    ->where('id',$where)
    ->delete();
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
}
