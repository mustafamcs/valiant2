<?php
namespace App\Models;
class Giris_yap_model
{
  protected $userTable = 'users';

  /**
   * Oyun hesabini account.account tablosundan kontrol eder.
   */
  public function KontrolAccount($user_name,$db)
  {
    return $db->table('account.account')
    ->where('login',$user_name)
    ->get()
    ->getRow();
  }

  /**
   * MySQL PASSWORD() ile sifre dogrulama.
   */
  public function SifreDogrula($user_name,$password,$db)
  {
    $result = $db->query(
      "SELECT (password = PASSWORD(?)) AS pass_ok FROM account.account WHERE login = ?",
      [$password, $user_name]
    )->getRow();
    return $result && $result->pass_ok == 1;
  }

  /**
   * GM seviyesini common.gmlist tablosundan kontrol eder.
   */
  public function GMKontrol($account_login,$db)
  {
    return $db->table('common.gmlist')
    ->where('mAccount',$account_login)
    ->where('mAuthority','IMPLEMENTOR')
    ->get()
    ->getRow();
  }

  /**
   * Panel users tablosundan kullanici kontrol/getir (session ve token icin).
   */
  public function Kontrol($user_name,$db)
  {
    return $db->table($this->userTable)
    ->where('user_name',$user_name)
    ->get()
    ->getRow();
  }

  /**
   * Oyun hesabini panel users tablosuna otomatik ekler (yoksa).
   */
  public function OtoKayit($account_login,$db)
  {
    $existing = $this->Kontrol($account_login,$db);
    if ($existing) return $existing;
    $db->table($this->userTable)->insert([
      'user_name'        => $account_login,
      'user_password'    => '',
      'user_rank'        => '9',
      'user_status'      => '1',
      'user_role'        => '{}',
      'user_token'       => '',
      'user_create_date' => date('Y-m-d H:i:s'),
      'user_login_date'  => date('Y-m-d H:i:s'),
      'user_end_session' => '0',
    ]);
    return $this->Kontrol($account_login,$db);
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
