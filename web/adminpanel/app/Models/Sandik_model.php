<?php
namespace App\Models;
class Sandik_model
{
  protected $groupTable     = 'player.drop_special_group';
  protected $itemTable      = 'player.drop_special_item';
  protected $itemProtoTable = 'player.item_proto';
  protected $iconTable      = 'valiant_panel.item_icon';

  public function AjaxAra($search,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->groupTable)
    ->select($this->groupTable.'.vnum,'.$this->groupTable.'.type, COUNT('.$this->itemTable.'.id) AS item_count,'.$this->itemProtoTable.'.locale_name')
    ->join($this->itemTable,$this->itemTable.'.group_vnum = '.$this->groupTable.'.vnum','left')
    ->join($this->itemProtoTable,$this->itemProtoTable.'.vnum = '.$this->groupTable.'.vnum','left')
    ->groupStart()
      ->orLike($this->groupTable.".vnum",$search)
      ->orLike($this->itemProtoTable.".locale_name",$search)
    ->groupEnd()
    ->groupBy($this->groupTable.'.vnum')
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function Ajax($start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->groupTable)
    ->select($this->groupTable.'.vnum,'.$this->groupTable.'.type, COUNT('.$this->itemTable.'.id) AS item_count,'.$this->itemProtoTable.'.locale_name')
    ->join($this->itemTable,$this->itemTable.'.group_vnum = '.$this->groupTable.'.vnum','left')
    ->join($this->itemProtoTable,$this->itemProtoTable.'.vnum = '.$this->groupTable.'.vnum','left')
    ->groupBy($this->groupTable.'.vnum')
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function Sayi($db)
  {
    return $db->table($this->groupTable)->countAllResults();
  }

  public function GrupKontrol($vnum,$db)
  {
    return $db->table($this->groupTable)
    ->where('vnum',$vnum)
    ->get()
    ->getRow();
  }

  public function Icerikler($groupVnum,$db)
  {
    return $db->table($this->itemTable)
    ->select($this->itemTable.'.*,'.$this->itemProtoTable.'.locale_name,'.$this->iconTable.'.icon')
    ->join($this->itemProtoTable,$this->itemProtoTable.'.vnum = '.$this->itemTable.'.item_vnum','left')
    ->join($this->iconTable,$this->iconTable.'.vnum = '.$this->itemTable.'.item_vnum','left')
    ->where($this->itemTable.'.group_vnum',$groupVnum)
    ->orderBy($this->itemTable.'.idx','asc')
    ->get()
    ->getResult();
  }

  public function ItemKontrol($id,$db)
  {
    return $db->table($this->itemTable)
    ->where('id',$id)
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

  public function Ikon($vnum,$db)
  {
    $row = $db->table($this->iconTable)->where('vnum',$vnum)->get()->getRow();
    return ($row && $row->icon) ? $row->icon : 'noicon.png';
  }

  public function GrupEkle($data,$db)
  {
    return $db->table($this->groupTable)->insert($data);
  }

  public function GrupGuncelle($data,$vnum,$db)
  {
    return $db->table($this->groupTable)
    ->where('vnum',$vnum)
    ->update($data);
  }

  public function GrupSil($vnum,$db)
  {
    $db->table($this->itemTable)->where('group_vnum',$vnum)->delete();
    return $db->table($this->groupTable)->where('vnum',$vnum)->delete();
  }

  public function ItemEkle($data,$db)
  {
    return $db->table($this->itemTable)->insert($data);
  }

  public function ItemGuncelle($data,$id,$db)
  {
    return $db->table($this->itemTable)
    ->where('id',$id)
    ->update($data);
  }

  public function ItemSil($id,$db)
  {
    return $db->table($this->itemTable)
    ->where('id',$id)
    ->delete();
  }
}
