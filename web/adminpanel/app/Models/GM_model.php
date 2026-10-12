<?php
namespace App\Models;
class GM_model
{
  protected $gmTable      = 'common.gmlist';
  protected $accountTable = 'account.account';
  protected $playerTable  = 'player.player';

  public function AjaxAra($search,$start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->gmTable)
    ->groupStart()
    ->orLike($this->gmTable.".mAccount",$search)
    ->orLike($this->gmTable.".mName",$search)
    ->groupEnd()
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function Ajax($start,$length,$orderColumn,$orderType,$db)
  {
    return $db->table($this->gmTable)
    ->orderBy($orderColumn,$orderType)
    ->limit($length,$start)
    ->get()
    ->getResult();
  }

  public function OyuncuKontrol($login,$name,$db)
  {
    return $db->table($this->accountTable)
    ->join($this->playerTable,$this->playerTable.'.account_id='.$this->accountTable.'.id','left')
    ->where('login',$login)
    ->where('name',$name)
    ->get()
    ->getRow();
  }

  public function Kontrol($mAccount,$mName,$db)
  {
    return $db->table($this->gmTable)
    ->where('mAccount',$mAccount)
    ->where('mName',$mName)
    ->get()
    ->getRow();
  }

  public function KontrolID($mID,$db)
  {
    return $db->table($this->gmTable)
    ->where('mID',$mID)
    ->get()
    ->getRow();
  }

  public function Ekle($data,$db)
  {
    return $db->table($this->gmTable)->insert($data);
  }

  public function Guncelle($data,$where,$db)
  {
    return $db->table($this->gmTable)
    ->where('mID',$where)
    ->update($data);
  }

  public function Sil($where,$db)
  {
    return $db->table($this->gmTable)
    ->where('mID',$where)
    ->delete();
  }
}
