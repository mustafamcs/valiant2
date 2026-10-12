<?php
namespace App\Models;
class Esya_model
{
  protected $itemProtoTable   = 'player.item_proto';
  protected $attrIDTable      = 'item_attr_id';
  protected $iconTable        = 'item_icon';
  protected $mobProtoTable    = 'player.mob_proto';
  protected $dropDefaultTable = 'player.drop_default';

  public function AjaxAra($query,$db)
  {
    header('Content-Type: text/html; charset=latin5');
    return $db->query($query)->getResult();
  }

  public function EsyaAra($search)
  {
    header('Content-Type: text/html; charset=latin5');
    $db = \Config\Database::connect('metin2');
    return $db->query("SELECT * FROM player.item_proto
    WHERE vnum LIKE '%".addslashes(addcslashes(mb_convert_encoding($search, 'ISO-8859-9' ,"UTF-8"),'%'))."%'
    OR locale_name LIKE '%".addslashes(addcslashes(mb_convert_encoding($search, 'ISO-8859-9' ,"UTF-8"),'%'))."%'
    COLLATE latin5_turkish_ci
    ORDER BY vnum asc
    LIMIT 10
    ")
    ->getResult();
  }

  public function Efsunlar()
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

  public function ItemProtoKontrol($vnum,$db)
  {
    return $db->table($this->itemProtoTable)
    ->where('vnum',$vnum)
    ->get()
    ->getRow();
  }

  public function Guncelle($data,$where,$db)
  {
    return $db->table($this->itemProtoTable)
    ->where('vnum',$where)
    ->update($data);
  }

  public function MobProtoKontrol($vnum,$db)
  {
    return $db->table($this->mobProtoTable)
    ->where('vnum',$vnum)
    ->get()
    ->getRow();
  }

  public function DropEkle($data,$db)
  {
    return $db->table($this->dropDefaultTable)
    ->insert($data);
  }

  public function DropKontrol($mob_vnum,$item_vnum,$count,$prob,$db)
  {
    return $db->table($this->dropDefaultTable)
    ->where('mob_vnum',$mob_vnum)
    ->where('item_vnum',$item_vnum)
    ->where('count',$count)
    ->like('prob',$prob)
    ->get()
    ->getRow();
  }

  public function DropGuncelle($data,$mob_vnum,$item_vnum,$count,$prob,$db)
  {
    return $db->table($this->dropDefaultTable)
    ->where('mob_vnum',$mob_vnum)
    ->where('item_vnum',$item_vnum)
    ->where('count',$count)
    ->like('prob',$prob)
    ->update($data);
  }

  public function DropSil($mob_vnum,$item_vnum,$count,$prob,$db)
  {
    return $db->table($this->dropDefaultTable)
    ->where('mob_vnum',$mob_vnum)
    ->where('item_vnum',$item_vnum)
    ->where('count',$count)
    ->like('prob',$prob)
    ->delete();
  }
}
