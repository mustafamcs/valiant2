<?php
namespace App\Models;
class Anasayfa_model
{
  protected $settingTable = 'settings';

  public function AyarCek($setting_name)
  {
    if (GetFileCache('AyarCek-'.$setting_name)) {
      return GetFileCache('AyarCek-'.$setting_name);
    }else {
      $db   = \Config\Database::connect();
      $data = $db->table($this->settingTable)
      ->where('setting_name',$setting_name)
      ->get()
      ->getRow();
      CreateFileCache('AyarCek-'.$setting_name,$data,86400);
      return $data;
    }
  }
}
