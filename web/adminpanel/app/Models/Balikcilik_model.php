<?php
namespace App\Models;
class Balikcilik_model
{
  protected $fisheventTable = 'player.fishevent_items';
  protected $itemProtoTable = 'player.item_proto';

  public function AjaxAra($search,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->fisheventTable)
    ->select($this->itemProtoTable.'.locale_name')
    ->select($this->fisheventTable.'.vnum')
    ->select($this->fisheventTable.'.chance')
    ->join($this->itemProtoTable,$this->itemProtoTable.".vnum=".$this->fisheventTable.'.vnum','left')
    ->groupStart()
    ->orLike($this->itemProtoTable.".locale_name",mb_convert_encoding(addslashes(addcslashes($search,'%')), 'ISO-8859-9' ,"UTF-8"))
    ->orLike($this->fisheventTable.".vnum",$search)
    ->groupEnd()
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function Ajax($start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->fisheventTable)
    ->select($this->itemProtoTable.'.locale_name')
    ->select($this->fisheventTable.'.vnum')
    ->select($this->fisheventTable.'.chance')
    ->join($this->itemProtoTable,$this->itemProtoTable.".vnum=".$this->fisheventTable.'.vnum','left')
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function Kontrol($vnum,$chance,$db)
  {
    return $db->table($this->fisheventTable)
    ->select($this->itemProtoTable.'.locale_name')
    ->select($this->fisheventTable.'.vnum')
    ->select($this->fisheventTable.'.chance')
    ->join($this->itemProtoTable,$this->itemProtoTable.".vnum=".$this->fisheventTable.'.vnum','left')
    ->where($this->fisheventTable.'.vnum',$vnum)
    ->where($this->fisheventTable.'.chance',$chance)
    ->get()
    ->getRow();
  }

  public function ItemProtoKontrol($vnum,$db)
  {
    return $db->table($this->itemProtoTable)
    ->where('vnum',$vnum)
    ->get()
    ->getRow();
  }

  public function Ekle($data,$db)
  {
    return $db->table($this->fisheventTable)->insert($data);
  }

  public function Guncelle($data,$vnum,$chance,$db)
  {
    return $db->table($this->fisheventTable)
    ->where('vnum',$vnum)
    ->where('chance',$chance)
    ->update($data);
  }

  public function Sil($vnum,$chance,$db)
  {
    return $db->table($this->fisheventTable)
    ->where('vnum',$vnum)
    ->where('chance',$chance)
    ->delete();
  }
}
