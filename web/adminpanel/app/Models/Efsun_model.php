<?php
namespace App\Models;
class Efsun_model
{
  protected $attrTable      = 'player.item_attr';
  protected $rareAttrTable  = 'player.item_attr_rare';
  protected $attrTextTable  = 'item_attr_text';

  public function AjaxAra($search,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->attrTable)
    ->groupStart()
    ->orLike($this->attrTable.".apply",$search)
    ->groupEnd()
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function Ajax($start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->attrTable)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function Kontrol($apply,$db)
  {
    return $db->table($this->attrTable)
    ->where('apply',$apply)
    ->get()
    ->getRow();
  }

  public function Guncelle($data,$where,$db)
  {
    return $db->table($this->attrTable)
    ->where('apply',$where)
    ->update($data);
  }

  public function NadirAjaxAra($search,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->rareAttrTable)
    ->groupStart()
    ->orLike($this->rareAttrTable.".apply",$search)
    ->groupEnd()
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function NadirAjax($start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->rareAttrTable)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function NadirKontrol($apply,$db)
  {
    return $db->table($this->rareAttrTable)
    ->where('apply',$apply)
    ->get()
    ->getRow();
  }

  public function NadirGuncelle($data,$where,$db)
  {
    return $db->table($this->rareAttrTable)
    ->where('apply',$where)
    ->update($data);
  }

  public function Efsunlar()
  {
    if (GetFileCache('EfsunlarText')) {
      return GetFileCache('EfsunlarText');
    }else {
      $db   = \Config\Database::connect();
      $data = $db->table($this->attrTextTable)
      ->get()
      ->getResult();
      CreateFileCache('EfsunlarText',$data,86400);
      return $data;
    }
  }
}
