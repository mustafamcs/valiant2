<?php
namespace App\Models;
class Kayit_model
{

  public function AjaxAra($query,$db)
  {
    header('Content-Type: text/html; charset=latin5');
    return $db->query($query)->getResult();
  }
}
