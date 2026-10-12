<?php
namespace App\Models;
class Islem_kayit_model
{
  protected $logTable   = 'logs';
  protected $userTable  = 'users';

  public function GorulmemisIslemKayitiSayisi()
  {
    $db = \Config\Database::connect();
    return $db->table($this->logTable)
    ->where('log_user_id',session('user_id'))
    ->where('log_status',"0")
    ->countAllResults();
  }

  public function SonIslemKayitlari()
  {
    $db = \Config\Database::connect();
    return $db->table($this->logTable)
    ->where('log_user_id',session('user_id'))
    ->orderBy('log_id desc')
    ->limit(10)
    ->get()
    ->getResult();
  }

  public function Ekle($data)
  {
    $db = \Config\Database::connect();
    return $db->table($this->logTable)
    ->insert($data);
  }

  public function HepsiniOku()
  {
    $db = \Config\Database::connect();
    return $db->table($this->logTable)
    ->set('log_status',"1")
    ->where('log_user_id',session('user_id'))
    ->where('log_status',"0")
    ->update();
  }

  public function Kullanicilar($search)
  {
    $db = \Config\Database::connect();
    return $db->table($this->userTable)
    ->groupStart()
    ->orLike("user_name",$search)
    ->groupEnd()
    ->orderBy('user_id asc')
    ->get()
    ->getResult();
  }

  public function AjaxAra($search,$start,$length,$orderColumn,$orderType,$db)
  {
    if (IsAllowedViewModule('tumBildirimleriGorebilsin')) {
      return $db->table($this->logTable)
      ->join($this->userTable,$this->userTable.'.user_id='.$this->logTable.'.log_user_id','left')
      ->groupStart()
      ->orLike($this->userTable.".user_name",$search)
      ->orLike($this->logTable.".log_content",$search)
      ->orLike($this->logTable.".log_link",$search)
      ->orLike($this->logTable.".log_ip",$search)
      ->groupEnd()
      ->where('log_user_id',session('user_id'))
      ->orderBy($orderColumn,$orderType)
      ->limit($length,$start)
      ->get()
      ->getResult();
    }else {
      return $db->table($this->logTable)
      ->groupStart()
      ->orLike($this->logTable.".log_content",$search)
      ->orLike($this->logTable.".log_link",$search)
      ->orLike($this->logTable.".log_ip",$search)
      ->groupEnd()
      ->where('log_user_id',session('user_id'))
      ->orderBy($orderColumn,$orderType)
      ->limit($length,$start)
      ->get()
      ->getResult();
    }
  }

  public function AjaxAraFiltreleDurumKullanici($log_status,$log_user_id,$search,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->logTable)
    ->join($this->userTable,$this->userTable.'.user_id='.$this->logTable.'.log_user_id','left')
    ->groupStart()
    ->orLike($this->userTable.".user_name",$search)
    ->orLike($this->logTable.".log_content",$search)
    ->orLike($this->logTable.".log_link",$search)
    ->orLike($this->logTable.".log_ip",$search)
    ->groupEnd()
    ->where('log_user_id',$log_user_id)
    ->where('log_status',$log_status)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function AjaxAraFiltreleDurumHepsi($log_status,$search,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->logTable)
    ->join($this->userTable,$this->userTable.'.user_id='.$this->logTable.'.log_user_id','left')
    ->groupStart()
    ->orLike($this->userTable.".user_name",$search)
    ->orLike($this->logTable.".log_content",$search)
    ->orLike($this->logTable.".log_link",$search)
    ->orLike($this->logTable.".log_ip",$search)
    ->groupEnd()
    ->where('log_status',$log_status)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function AjaxAraFiltreleKullanici($log_user_id,$search,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->logTable)
    ->join($this->userTable,$this->userTable.'.user_id='.$this->logTable.'.log_user_id','left')
    ->groupStart()
    ->orLike($this->userTable.".user_name",$search)
    ->orLike($this->logTable.".log_content",$search)
    ->orLike($this->logTable.".log_link",$search)
    ->orLike($this->logTable.".log_ip",$search)
    ->groupEnd()
    ->where('log_user_id',$log_user_id)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function AjaxAraFiltreleDurum($log_status,$search,$start,$length,$orderColumn,$orderType,$db)
  {
    if (IsAllowedViewModule('tumBildirimleriGorebilsin')) {
      return $db->table($this->logTable)
      ->join($this->userTable,$this->userTable.'.user_id='.$this->logTable.'.log_user_id','left')
      ->groupStart()
      ->orLike($this->userTable.".user_name",$search)
      ->orLike($this->logTable.".log_content",$search)
      ->orLike($this->logTable.".log_link",$search)
      ->orLike($this->logTable.".log_ip",$search)
      ->groupEnd()
      ->where('log_user_id',session('user_id'))
      ->where('log_status',$log_status)
      ->orderBy($orderColumn,$orderType)
      ->limit($length,$start)
      ->get()
      ->getResult();
    }else {
      return $db->table($this->logTable)
      ->groupStart()
      ->orLike($this->logTable.".log_content",$search)
      ->orLike($this->logTable.".log_link",$search)
      ->orLike($this->logTable.".log_ip",$search)
      ->groupEnd()
      ->where('log_user_id',session('user_id'))
      ->where('log_status',$log_status)
      ->orderBy($orderColumn,$orderType)
      ->limit($length,$start)
      ->get()
      ->getResult();
    }
  }

  public function AjaxAraHepsi($search,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->logTable)
    ->join($this->userTable,$this->userTable.'.user_id='.$this->logTable.'.log_user_id','left')
    ->groupStart()
    ->orLike($this->userTable.".user_name",$search)
    ->orLike($this->logTable.".log_content",$search)
    ->orLike($this->logTable.".log_link",$search)
    ->orLike($this->logTable.".log_ip",$search)
    ->groupEnd()
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function Ajax($start,$length,$orderColumn,$orderType,$db)
  {
    if (IsAllowedViewModule('tumBildirimleriGorebilsin')) {
      return $db->table($this->logTable)
      ->join($this->userTable,$this->userTable.'.user_id='.$this->logTable.'.log_user_id','left')
      ->where('log_user_id',session('user_id'))
      ->orderBy($orderColumn,$orderType)
      ->limit($length,$start)
      ->get()
      ->getResult();
    }else {
      return $db->table($this->logTable)
      ->where('log_user_id',session('user_id'))
      ->orderBy($orderColumn,$orderType)
      ->limit($length,$start)
      ->get()
      ->getResult();
    }
  }

  public function AjaxFiltreleDurumKullanici($log_status,$log_user_id,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->logTable)
    ->join($this->userTable,$this->userTable.'.user_id='.$this->logTable.'.log_user_id','left')
    ->where('log_user_id',$log_user_id)
    ->where('log_status',$log_status)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function AjaxFiltreleDurumHepsi($log_status,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->logTable)
    ->join($this->userTable,$this->userTable.'.user_id='.$this->logTable.'.log_user_id','left')
    ->where('log_status',$log_status)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function AjaxFiltreleKullanici($log_user_id,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->logTable)
    ->join($this->userTable,$this->userTable.'.user_id='.$this->logTable.'.log_user_id','left')
    ->where('log_user_id',$log_user_id)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function AjaxFiltreleDurum($log_status,$start,$length,$orderColumn,$orderType,$db)
  {
    if (IsAllowedViewModule('tumBildirimleriGorebilsin')) {
      return $db->table($this->logTable)
      ->join($this->userTable,$this->userTable.'.user_id='.$this->logTable.'.log_user_id','left')
      ->where('log_user_id',session('user_id'))
      ->where('log_status',$log_status)
      ->orderBy($orderColumn,$orderType)
      ->limit($length,$start)
      ->get()
      ->getResult();
    }else {
      return $db->table($this->logTable)
      ->where('log_user_id',session('user_id'))
      ->where('log_status',$log_status)
      ->orderBy($orderColumn,$orderType)
      ->limit($length,$start)
      ->get()
      ->getResult();
    }
  }

  public function AjaxHepsi($start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->logTable)
    ->join($this->userTable,$this->userTable.'.user_id='.$this->logTable.'.log_user_id','left')
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }
}
