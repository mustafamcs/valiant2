<?php
namespace App\Models;
class Giris_yap_model
{
  protected $userTable = 'users';

  public function Kontrol($user_name,$db)
  {
    return $db->table($this->userTable)
    ->where('user_name',$user_name)
    ->get()
    ->getRow();
  }

  public function BeniHatirlaTokenKontrol($user_token,$db)
  {
    return $db->table($this->userTable)
    ->where('user_token',$user_token)
    ->get()
    ->getRow();
  }

  public function Guncelle($data,$where,$db)
  {
    return $db->table($this->userTable)
    ->where('user_id',$where)
    ->update($data);
  }
}
