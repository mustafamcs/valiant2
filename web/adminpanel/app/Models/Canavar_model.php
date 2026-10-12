<?php
namespace App\Models;
class Canavar_model
{
  protected $mobProtoTable    = 'player.mob_proto';
  protected $itemProtoTable   = 'player.item_proto';
  protected $dropDefaultTable = 'player.drop_default';
  protected $iconTable        = 'item_icon';
  protected $levelGroupTable  = 'player.drop_mob_group_level';
  protected $levelItemTable   = 'player.drop_mob_item_level';
  protected $killGroupTable   = 'player.drop_mob_group_kill';
  protected $killItemTable    = 'player.drop_mob_item_kill';

  public function AjaxAra($query,$db)
  {
    header('Content-Type: text/html; charset=latin5');
    return $db->query($query)->getResult();
  }

  public function MobProtoKontrol($vnum,$db)
  {
    return $db->table($this->mobProtoTable)
    ->where('vnum',$vnum)
    ->get()
    ->getRow();
  }

  public function Guncelle($data,$where,$db)
  {
    return $db->table($this->mobProtoTable)
    ->where('vnum',$where)
    ->update($data);
  }

  public function ItemProtoKontrol($vnum,$db)
  {
    return $db->table($this->itemProtoTable)
    ->where('vnum',$vnum)
    ->get()
    ->getRow();
  }

  public function DropEkle($data,$db)
  {
    return $db->table($this->dropDefaultTable)
    ->insert($data);
  }

  public function DropKontrol($mob_vnum,$item_vnum,$count,$prob,$db)
  {
    return $db->table($this->dropDefaultTable)
    ->where('mob_vnum',$mob_vnum)
    ->where('item_vnum',$item_vnum)
    ->where('count',$count)
    ->like('prob',$prob)
    ->get()
    ->getRow();
  }

  public function DropGuncelle($data,$mob_vnum,$item_vnum,$count,$prob,$db)
  {
    return $db->table($this->dropDefaultTable)
    ->where('mob_vnum',$mob_vnum)
    ->where('item_vnum',$item_vnum)
    ->where('count',$count)
    ->like('prob',$prob)
    ->update($data);
  }

  public function DropSil($mob_vnum,$item_vnum,$count,$prob,$db)
  {
    return $db->table($this->dropDefaultTable)
    ->where('mob_vnum',$mob_vnum)
    ->where('item_vnum',$item_vnum)
    ->where('count',$count)
    ->like('prob',$prob)
    ->delete();
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

  public function CanavarAra($search)
  {
    header('Content-Type: text/html; charset=latin5');
    $db = \Config\Database::connect('metin2');
    return $db->query("SELECT * FROM player.mob_proto
    WHERE vnum LIKE '%".addslashes(addcslashes(mb_convert_encoding($search, 'ISO-8859-9' ,"UTF-8"),'%'))."%'
    OR locale_name LIKE '%".addslashes(addcslashes(mb_convert_encoding($search, 'ISO-8859-9' ,"UTF-8"),'%'))."%'
    COLLATE latin5_turkish_ci
    ORDER BY vnum asc
    LIMIT 10
    ")
    ->getResult();
  }

  public function DropLevelGrupGenelKontrol($group_id,$mob_vnum,$db)
  {
    return $db->table($this->levelGroupTable)
    ->where('group_id',$group_id)
    ->where('mob_vnum !=',$mob_vnum)
    ->get()
    ->getRow();
  }

  public function DropLevelGrupKontrol($group_id,$mob_vnum,$level_start,$level_end,$db)
  {
    return $db->table($this->levelGroupTable)
    ->where('group_id',$group_id)
    ->where('mob_vnum',$mob_vnum)
    ->where('level_start',$level_start)
    ->where('level_end',$level_end)
    ->get()
    ->getRow();
  }

  public function DropLevelGrupEkle($data,$db)
  {
    return $db->table($this->levelGroupTable)
    ->insert($data);
  }

  public function DropLevelGrupSil($group_id,$mob_vnum,$level_start,$level_end,$db)
  {
    return $db->table($this->levelGroupTable)
    ->where('group_id',$group_id)
    ->where('mob_vnum',$mob_vnum)
    ->where('level_start',$level_start)
    ->where('level_end',$level_end)
    ->delete();
  }

  public function DropLevelEkle($data,$db)
  {
    return $db->table($this->levelItemTable)
    ->insert($data);
  }

  public function DropLevelKontrol($group_id,$item_vnum,$count,$prob,$db)
  {
    return $db->table($this->levelItemTable)
    ->select($this->levelGroupTable.'.mob_vnum')
    ->select($this->levelGroupTable.'.level_start')
    ->select($this->levelGroupTable.'.level_end')
    ->select($this->levelItemTable.'.*')
    ->join($this->levelGroupTable,$this->levelGroupTable.'.group_id='.$this->levelItemTable.'.group_id','left')
    ->where($this->levelItemTable.'.group_id',$group_id)
    ->where('item_vnum',$item_vnum)
    ->where('count',$count)
    ->like('prob',$prob)
    ->get()
    ->getRow();
  }

  public function DropLevelGuncelle($data,$group_id,$item_vnum,$count,$prob,$db)
  {
    return $db->table($this->levelItemTable)
    ->where('group_id',$group_id)
    ->where('item_vnum',$item_vnum)
    ->where('count',$count)
    ->like('prob',$prob)
    ->update($data);
  }

  public function DropLevelEsyalar($group_id,$db)
  {
    return $db->table($this->levelItemTable)
    ->where('group_id',$group_id)
    ->countAllResults();
  }

  public function DropLevelSil($group_id,$item_vnum,$count,$prob,$db)
  {
    return $db->table($this->levelItemTable)
    ->where('group_id',$group_id)
    ->where('item_vnum',$item_vnum)
    ->where('count',$count)
    ->like('prob',$prob)
    ->delete();
  }

  public function DropKillGrupGenelKontrol($group_id,$mob_vnum,$db)
  {
    return $db->table($this->killGroupTable)
    ->where('group_id',$group_id)
    ->where('mob_vnum !=',$mob_vnum)
    ->get()
    ->getRow();
  }

  public function DropKillGrupKontrol($group_id,$mob_vnum,$kill_per_drop,$db)
  {
    return $db->table($this->killGroupTable)
    ->where('group_id',$group_id)
    ->where('mob_vnum',$mob_vnum)
    ->where('kill_per_drop',$kill_per_drop)
    ->get()
    ->getRow();
  }

  public function DropKillGrupEkle($data,$db)
  {
    return $db->table($this->killGroupTable)
    ->insert($data);
  }

  public function DropKillGrupSil($group_id,$mob_vnum,$kill_per_drop,$db)
  {
    return $db->table($this->killGroupTable)
    ->where('group_id',$group_id)
    ->where('mob_vnum',$mob_vnum)
    ->where('kill_per_drop',$kill_per_drop)
    ->delete();
  }

  public function DropKillEkle($data,$db)
  {
    return $db->table($this->killItemTable)
    ->insert($data);
  }

  public function DropKillKontrol($group_id,$item_vnum,$count,$part_prob,$db)
  {
    return $db->table($this->killItemTable)
    ->select($this->killGroupTable.'.mob_vnum')
    ->select($this->killGroupTable.'.kill_per_drop')
    ->select($this->killItemTable.'.*')
    ->join($this->killGroupTable,$this->killGroupTable.'.group_id='.$this->killItemTable.'.group_id','left')
    ->where($this->killItemTable.'.group_id',$group_id)
    ->where('item_vnum',$item_vnum)
    ->where('count',$count)
    ->like('part_prob',$part_prob)
    ->get()
    ->getRow();
  }

  public function DropKillGuncelle($data,$group_id,$item_vnum,$count,$part_prob,$db)
  {
    return $db->table($this->killItemTable)
    ->where('group_id',$group_id)
    ->where('item_vnum',$item_vnum)
    ->where('count',$count)
    ->like('part_prob',$part_prob)
    ->update($data);
  }

  public function DropKillEsyalar($group_id,$db)
  {
    return $db->table($this->killItemTable)
    ->where('group_id',$group_id)
    ->countAllResults();
  }

  public function DropKillSil($group_id,$item_vnum,$count,$part_prob,$db)
  {
    return $db->table($this->killItemTable)
    ->where('group_id',$group_id)
    ->where('item_vnum',$item_vnum)
    ->where('count',$count)
    ->like('part_prob',$part_prob)
    ->delete();
  }
}
