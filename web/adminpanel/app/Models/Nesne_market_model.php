<?php
namespace App\Models;
class Nesne_market_model
{
  protected $kategoriTable  = 'player.itemshop_category';
  protected $itemTable      = 'player.itemshop_item';
  protected $iconTable      = 'item_icon';
  protected $attrIDTable    = 'item_attr_id';
  protected $itemProtoTable = 'player.item_proto';

  public function KategoriAjaxAra($search,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->kategoriTable)
    ->groupStart()
    ->orLike($this->kategoriTable.".cat_name",mb_convert_encoding(addslashes(addcslashes($search,'%')), 'ISO-8859-9' ,"UTF-8"))
    ->groupEnd()
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function KategoriAjax($start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->kategoriTable)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function KategoriKontrolCache($cat_id)
  {
    if (GetFileCache('KategoriKontrol-'.permalink($cat_id))) {
      return GetFileCache('KategoriKontrol-'.permalink($cat_id));
    }else {
      $db   = \Config\Database::connect('metin2');
      $data = $db->table($this->kategoriTable)
      ->where($this->kategoriTable.'.cat_id',$cat_id)
      ->get()
      ->getRow();
      CreateFileCache('KategoriKontrol-'.permalink($cat_id),$data,600);
      return $data;
    }
  }

  public function KategoriKontrol($cat_id,$db)
  {
    return $db->table($this->kategoriTable)
    ->where($this->kategoriTable.'.cat_id',$cat_id)
    ->get()
    ->getRow();
  }

  public function KategoriEkle($data,$db)
  {
    return $db->table($this->kategoriTable)->insert($data);
  }

  public function KategoriGuncelle($data,$cat_id,$db)
  {
    return $db->table($this->kategoriTable)
    ->where('cat_id',$cat_id)
    ->update($data);
  }

  public function KategoriSil($cat_id,$db)
  {
    return $db->table($this->kategoriTable)
    ->where('cat_id',$cat_id)
    ->delete();
  }

  public function KategoriAra($search)
  {
    header('Content-Type: text/html; charset=latin5');
    $db = \Config\Database::connect('metin2');
    return $db->query("SELECT * FROM player.itemshop_category
    WHERE cat_name LIKE '%".addslashes(addcslashes(mb_convert_encoding($search, 'ISO-8859-9' ,"UTF-8"),'%'))."%'
    COLLATE latin5_turkish_ci
    ORDER BY cat_id asc
    ")
    ->getResult();
  }

  public function AjaxAra($search,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->itemTable)
    ->groupStart()
    ->orLike($this->itemTable.".item_name",mb_convert_encoding(addslashes(addcslashes($search,'%')), 'ISO-8859-9' ,"UTF-8"))
    ->groupEnd()
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function Ajax($start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->itemTable)
    ->join($this->kategoriTable,$this->kategoriTable.'.cat_id='.$this->itemTable.'.category_id','left')
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
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

  public function Kontrol($id,$db)
  {
    return $db->table($this->itemTable)
    ->select($this->kategoriTable.'.cat_name')
    ->select($this->itemTable.'.*')
    ->join($this->kategoriTable,$this->kategoriTable.'.cat_id='.$this->itemTable.'.category_id','left')
    ->where('id',$id)
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
    return $db->table($this->itemTable)->insert($data);
  }

  public function Guncelle($data,$id,$db)
  {
    return $db->table($this->itemTable)
    ->where('id',$id)
    ->update($data);
  }

  public function Sil($id,$db)
  {
    return $db->table($this->itemTable)
    ->where('id',$id)
    ->delete();
  }
}
