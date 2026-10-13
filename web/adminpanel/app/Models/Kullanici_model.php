<?php
namespace App\Models;
class Kullanici_model
{
  protected $userTable  = 'users';
  protected $logTable   = 'logs';

  /**
   * Oyun hesabı DB bağlantısı (account.account + common.gmlist)
   */
  private function gameDb()
  {
    return \Config\Database::connect('metin2');
  }

  // ---------- Kullanıcı listeleme (account.account + gmlist) ----------

  public function AjaxAra($search,$start,$length,$orderColumn,$orderType,$db)
  {
    $gameDb = $this->gameDb();
    $query = "SELECT a.id AS user_id, a.login AS user_name,
              COALESCE(u.user_status,'1') AS user_status,
              COALESCE(u.user_login_date, a.create_time) AS user_login_date,
              COALESCE(u.user_role,'{}') AS user_role,
              COALESCE(u.user_rank,'1') AS user_rank,
              g.mAuthority
              FROM account.account a
              INNER JOIN common.gmlist g ON g.mAccount = a.login AND g.mAuthority = 'IMPLEMENTOR'
              LEFT JOIN {$db->getDatabase()}.{$this->userTable} u ON u.user_name = a.login
              WHERE a.login LIKE ?
              ORDER BY {$orderColumn} {$orderType}
              LIMIT {$length} OFFSET {$start}";
    return $gameDb->query($query, ['%'.$search.'%'])->getResult();
  }

  public function AjaxAraFiltreleDurum($user_status,$search,$start,$length,$orderColumn,$orderType,$db)
  {
    $gameDb = $this->gameDb();
    $query = "SELECT a.id AS user_id, a.login AS user_name,
              COALESCE(u.user_status,'1') AS user_status,
              COALESCE(u.user_login_date, a.create_time) AS user_login_date,
              COALESCE(u.user_role,'{}') AS user_role,
              COALESCE(u.user_rank,'1') AS user_rank,
              g.mAuthority
              FROM account.account a
              INNER JOIN common.gmlist g ON g.mAccount = a.login AND g.mAuthority = 'IMPLEMENTOR'
              LEFT JOIN {$db->getDatabase()}.{$this->userTable} u ON u.user_name = a.login
              WHERE a.login LIKE ? AND COALESCE(u.user_status,'1') = ?
              ORDER BY {$orderColumn} {$orderType}
              LIMIT {$length} OFFSET {$start}";
    return $gameDb->query($query, ['%'.$search.'%', $user_status])->getResult();
  }

  public function Ajax($start,$length,$orderColumn,$orderType,$db)
  {
    $gameDb = $this->gameDb();
    $query = "SELECT a.id AS user_id, a.login AS user_name,
              COALESCE(u.user_status,'1') AS user_status,
              COALESCE(u.user_login_date, a.create_time) AS user_login_date,
              COALESCE(u.user_role,'{}') AS user_role,
              COALESCE(u.user_rank,'1') AS user_rank,
              g.mAuthority
              FROM account.account a
              INNER JOIN common.gmlist g ON g.mAccount = a.login AND g.mAuthority = 'IMPLEMENTOR'
              LEFT JOIN {$db->getDatabase()}.{$this->userTable} u ON u.user_name = a.login
              ORDER BY {$orderColumn} {$orderType}
              LIMIT {$length} OFFSET {$start}";
    return $gameDb->query($query)->getResult();
  }

  public function AjaxFiltreleDurum($user_status,$start,$length,$orderColumn,$orderType,$db)
  {
    $gameDb = $this->gameDb();
    $query = "SELECT a.id AS user_id, a.login AS user_name,
              COALESCE(u.user_status,'1') AS user_status,
              COALESCE(u.user_login_date, a.create_time) AS user_login_date,
              COALESCE(u.user_role,'{}') AS user_role,
              COALESCE(u.user_rank,'1') AS user_rank,
              g.mAuthority
              FROM account.account a
              INNER JOIN common.gmlist g ON g.mAccount = a.login AND g.mAuthority = 'IMPLEMENTOR'
              LEFT JOIN {$db->getDatabase()}.{$this->userTable} u ON u.user_name = a.login
              WHERE COALESCE(u.user_status,'1') = ?
              ORDER BY {$orderColumn} {$orderType}
              LIMIT {$length} OFFSET {$start}";
    return $gameDb->query($query, [$user_status])->getResult();
  }

  // ---------- Tekli kontrol ----------

  public function Kontrol($id,$db)
  {
    // Önce account tablosundan ara (id veya user_id olarak)
    $gameDb = $this->gameDb();
    $query = "SELECT a.id AS user_id, a.login AS user_name,
              COALESCE(u.user_status,'1') AS user_status,
              COALESCE(u.user_login_date, a.create_time) AS user_login_date,
              COALESCE(u.user_role,'{}') AS user_role,
              COALESCE(u.user_rank,'1') AS user_rank,
              COALESCE(u.user_id, 0) AS panel_user_id,
              g.mAuthority
              FROM account.account a
              INNER JOIN common.gmlist g ON g.mAccount = a.login AND g.mAuthority = 'IMPLEMENTOR'
              LEFT JOIN {$db->getDatabase()}.{$this->userTable} u ON u.user_name = a.login
              WHERE a.id = ?
              LIMIT 1";
    $row = $gameDb->query($query, [$id])->getRow();
    if (!$row) {
      // Fallback: users tablosundan dene (eski panel user_id ile çağrılmış olabilir)
      return $db->table($this->userTable)->where('user_id',$id)->get()->getRow();
    }
    return $row;
  }

  public function Guncelle($data,$where,$db)
  {
    // Panel users tablosundaki kaydı güncelle (user_name ile eşleş)
    // Önce users'ta kayıt var mı kontrol et
    $gameDb = $this->gameDb();
    $acc = $gameDb->query("SELECT login FROM account.account WHERE id = ? LIMIT 1", [$where])->getRow();
    if ($acc) {
      $existing = $db->table($this->userTable)->where('user_name', $acc->login)->get()->getRow();
      if ($existing) {
        return $db->table($this->userTable)->where('user_name', $acc->login)->update($data);
      } else {
        // Yoksa oluştur
        $data['user_name'] = $acc->login;
        $data['user_rank'] = '1';
        $data['user_create_date'] = date('Y-m-d H:i:s');
        return $db->table($this->userTable)->insert($data);
      }
    }
    // Fallback: eski user_id ile
    return $db->table($this->userTable)->where('user_id',$where)->update($data);
  }

  public function KullaniciAdiKontrol($user_name,$db)
  {
    $gameDb = $this->gameDb();
    return $gameDb->query("SELECT id, login FROM account.account WHERE login = ? LIMIT 1", [$user_name])->getRow();
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

  // ---------- İşlem kayıtları ----------

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
