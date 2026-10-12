<?php
namespace App\Models;
class Ayar_model
{
  protected $settingTable = 'settings';

  public function AyarCek($setting_name,$db)
  {
    return $db->table($this->settingTable)
    ->where('setting_name',$setting_name)
    ->get()
    ->getRow();
  }

  public function Ekle($data,$db)
  {
    return $db->table($this->settingTable)
    ->insert($data);
  }

  public function Guncelle($data,$where,$db)
  {
    return $db->table($this->settingTable)
    ->where('setting_name',$where)
    ->update($data);
  }

  public function TabloyuBosalt($tableName,$db)
  {
    return $db->table($tableName)->truncate();
  }

  public function VeriEkle($tableName,$data,$db)
  {
    return $db->table($tableName)
    ->insert($data);
  }

  public function ItemProtoCek(){
    $db = \Config\Database::connect('metin2');
    return $db->table('player.item_proto')
    ->select('vnum')
    ->get()
    ->getResult();
  }
}
