<?php
namespace App\Models;
class Veri_islem_model
{
  protected $attrIdTable    = 'item_attr_id';
  protected $attrTextTable  = 'item_attr_text';
  protected $mapTable       = 'map_index';

  public function AjaxAraID($search,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->attrIdTable)
    ->groupStart()
    ->orLike($this->attrIdTable.".id",$search)
    ->orLike($this->attrIdTable.".name",$search)
    ->groupEnd()
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function AjaxID($start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->attrIdTable)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function KontrolID($id,$db)
  {
    return $db->table($this->attrIdTable)
    ->where('id',$id)
    ->get()
    ->getRow();
  }

  public function EkleID($data,$db)
  {
    return $db->table($this->attrIdTable)->insert($data);
  }

  public function GuncelleID($data,$where,$db)
  {
    return $db->table($this->attrIdTable)
    ->where('id',$where)
    ->update($data);
  }

  public function SilID($where,$db)
  {
    return $db->table($this->attrIdTable)
    ->where('id',$where)
    ->delete();
  }

  public function AjaxAraText($search,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->attrTextTable)
    ->groupStart()
    ->orLike($this->attrTextTable.".id",$search)
    ->orLike($this->attrTextTable.".name",$search)
    ->groupEnd()
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function AjaxText($start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->attrTextTable)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function KontrolText($id,$db)
  {
    return $db->table($this->attrTextTable)
    ->where('id',$id)
    ->get()
    ->getRow();
  }

  public function EkleText($data,$db)
  {
    return $db->table($this->attrTextTable)->insert($data);
  }

  public function GuncelleText($data,$where,$db)
  {
    return $db->table($this->attrTextTable)
    ->where('id',$where)
    ->update($data);
  }

  public function SilText($where,$db)
  {
    return $db->table($this->attrTextTable)
    ->where('id',$where)
    ->delete();
  }

  public function AjaxAraHarita($search,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->mapTable)
    ->groupStart()
    ->orLike($this->mapTable.".id",$search)
    ->orLike($this->mapTable.".name",$search)
    ->groupEnd()
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function AjaxHarita($start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->mapTable)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function KontrolHarita($id,$db)
  {
    return $db->table($this->mapTable)
    ->where('id',$id)
    ->get()
    ->getRow();
  }

  public function EkleHarita($data,$db)
  {
    return $db->table($this->mapTable)->insert($data);
  }

  public function GuncelleHarita($data,$where,$db)
  {
    return $db->table($this->mapTable)
    ->where('id',$where)
    ->update($data);
  }

  public function SilHarita($where,$db)
  {
    return $db->table($this->mapTable)
    ->where('id',$where)
    ->delete();
  }
}
