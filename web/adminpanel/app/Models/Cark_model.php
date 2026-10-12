<?php
namespace App\Models;
class Cark_model
{
  protected $faterouletteTable = 'player.fateroulette';
  protected $itemProtoTable = 'player.item_proto';

  public function AjaxAra($search,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->faterouletteTable)
    ->select($this->itemProtoTable.'.locale_name')
    ->select($this->faterouletteTable.'.vnum')
    ->select($this->faterouletteTable.'.count')
    ->join($this->itemProtoTable,$this->itemProtoTable.".vnum=".$this->faterouletteTable.'.vnum','left')
    ->groupStart()
    ->orLike($this->itemProtoTable.".locale_name",mb_convert_encoding(addslashes(addcslashes($search,'%')), 'ISO-8859-9' ,"UTF-8"))
    ->orLike($this->faterouletteTable.".vnum",$search)
    ->groupEnd()
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function Ajax($start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->faterouletteTable)
    ->select($this->itemProtoTable.'.locale_name')
    ->select($this->faterouletteTable.'.vnum')
    ->select($this->faterouletteTable.'.count')
    ->join($this->itemProtoTable,$this->itemProtoTable.".vnum=".$this->faterouletteTable.'.vnum','left')
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function Kontrol($vnum,$count,$db)
  {
    return $db->table($this->faterouletteTable)
    ->select($this->itemProtoTable.'.locale_name')
    ->select($this->faterouletteTable.'.vnum')
    ->select($this->faterouletteTable.'.count')
    ->join($this->itemProtoTable,$this->itemProtoTable.".vnum=".$this->faterouletteTable.'.vnum','left')
    ->where($this->faterouletteTable.'.vnum',$vnum)
    ->where($this->faterouletteTable.'.count',$count)
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
    return $db->table($this->faterouletteTable)->insert($data);
  }

  public function Guncelle($data,$vnum,$count,$db)
  {
    return $db->table($this->faterouletteTable)
    ->where('vnum',$vnum)
    ->where('count',$count)
    ->update($data);
  }

  public function Sil($vnum,$count,$db)
  {
    return $db->table($this->faterouletteTable)
    ->where('vnum',$vnum)
    ->where('count',$count)
    ->delete();
  }
}
