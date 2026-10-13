<?php
namespace App\Models;
class Kayit_model
{

  public function AjaxAra($query,$db)
  {
    header('Content-Type: text/html; charset=utf-8');
    return $db->query($query)->getResult();
  }
}
