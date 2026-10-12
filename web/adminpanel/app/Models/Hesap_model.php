<?php
namespace App\Models;
class Hesap_model
{
  protected $userTable = 'users';

  public function KullaniciBilgileri($id,$db)
  {
    return $db->table($this->userTable)
    ->where('user_id',$id)
    ->get()
    ->getRow();
  }

  public function Guncelle($data,$where,$db)
  {
    return $db->table($this->userTable)
    ->where('user_id',$where)
    ->update($data);
  }

  public function KullaniciAdiKontrol($user_name,$db)
  {
    return $db->table($this->userTable)
    ->where('user_name',$user_name)
    ->get()
    ->getRow();
  }
}
