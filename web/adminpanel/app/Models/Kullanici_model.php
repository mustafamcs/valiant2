<?php
namespace App\Models;
class Kullanici_model
{
  protected $userTable  = 'users';
  protected $logTable   = 'logs';

  public function AjaxAra($search,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->userTable)
    ->groupStart()
    ->orLike($this->userTable.".user_name",$search)
    ->groupEnd()
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function AjaxAraFiltreleDurum($user_status,$search,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->userTable)
    ->groupStart()
    ->orLike($this->userTable.".user_name",$search)
    ->groupEnd()
    ->where('user_status',$user_status)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function Ajax($start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->userTable)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function AjaxFiltreleDurum($user_status,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->userTable)
    ->where('user_status',$user_status)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function Kontrol($id,$db)
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

  public function Ekle($data,$db)
  {
    return $db->table($this->userTable)->insert($data);
  }

  public function Sil($where,$db)
  {
    return $db->table($this->userTable)
    ->where('user_id',$where)
    ->delete();
  }

  public function IslemKayitlariAjaxAra($id,$search,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->logTable)
    ->groupStart()
    ->orLike($this->logTable.".log_content",$search)
    ->orLike($this->logTable.".log_link",$search)
    ->orLike($this->logTable.".log_ip",$search)
    ->groupEnd()
    ->where('log_user_id',$id)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function IslemKayitlariAjaxAraFiltreleDurum($id,$log_status,$search,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->logTable)
    ->groupStart()
    ->orLike($this->logTable.".log_content",$search)
    ->orLike($this->logTable.".log_link",$search)
    ->orLike($this->logTable.".log_ip",$search)
    ->groupEnd()
    ->where('log_user_id',$id)
    ->where('log_status',$log_status)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function IslemKayitlariAjax($id,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->logTable)
    ->where('log_user_id',$id)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function IslemKayitlariAjaxFiltreleDurum($id,$log_status,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->logTable)
    ->where('log_user_id',$id)
    ->where('log_status',$log_status)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }
}
