<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class Anasayfa extends BaseController
{
  public $viewFolder = "";

  public function __construct()
  {
    $this->viewFolder     = "Anasayfa";
    $this->anasayfaModel  = model('Anasayfa_model');
    if (!session('user_id')) {
      header('Location: '.base_url('GirisYap'));
      exit;
    }
  }

  public function Index()
  {
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Index",$viewData);
  }

  public function Istatistikler()
  {
    $db = \Config\Database::connect('metin2');
    $data = [
      'hesap'    => $db->table('account.account')->countAllResults(),
      'karakter' => $db->table('player.player')->countAllResults(),
      'lonca'    => $db->table('player.guild')->countAllResults(),
      'esya'     => $db->table('player.item')->countAllResults(),
      'nesne'    => $db->table('player.itemshop_item')->countAllResults(),
    ];
    echo json_encode($data, JSON_INVALID_UTF8_SUBSTITUTE);
    exit;
  }

  public function OnBellekleriTemizle()
  {
    if (!IsAllowedViewModule('onBellekTemizleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    helper('filesystem');
    delete_files(FCPATH.'writable/cache/',TRUE,TRUE);
    LogAdd(lang('Genel.onBelleklerTemizlendi'),'#',session('user_id'));
    $alert = [
      'type' => "success",
      'text' => lang('Genel.onBelleklerTemizlendi')
    ];
    session()->setFlashdata('alert',$alert);
    return redirect()->to($this->request->getUserAgent()->getReferrer());
  }

  public function KaranlikTema($type="")
  {
    if ($type=="Ac") {
      setcookie("karanlik_tema","acik",time()+YEAR,'/','');
    }else {
      if (get_cookie("karanlik_tema")){
        setcookie("karanlik_tema","kapat",-1,'/','');
      }
    }
    return redirect()->to($this->request->getUserAgent()->getReferrer());
  }

  public function OnlineCount(){
    if (!IsAllowedViewModule('anasayfaOnlineGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    if (p2pStatus==1 && p2pStatistics==1) {
      $count            = [];
      $count['red']     = 0;
      $count['yellow']  = 0;
      $count['blue']    = 0;
      $count['total']   = 0;
      foreach (p2pChannel as $key => $value) {
        if ($key==(count(p2pChannel)-1)) {
          $key = 98;
        }
        $count[$key] = SendServer("","USER_COUNT",$value);
        if (!isset($count[$key][1]) || !is_numeric($count[$key][1])) {
          $count[$key][1] = 0;
        }
        $count['red'] += $count[$key][1];
        if (!isset($count[$key][2]) || !is_numeric($count[$key][2])) {
          $count[$key][2] = 0;
        }
        $count['yellow'] += $count[$key][2];
        if (!isset($count[$key][3]) || !is_numeric($count[$key][3])) {
          $count[$key][3] = 0;
        }
        $count['blue'] += $count[$key][3];
        $count['total'] += $count[$key][1];
        $count['total'] += $count[$key][2];
        $count['total'] += $count[$key][3];
        $count['ch'.($key+1)] = $count[$key][1]+$count[$key][2]+$count[$key][3];
        $count['chTR'][($key+1)] = "<tr><td>CH".($key+1)."</td><td>".($count[$key][1]>0?'<strong>'.$count[$key][1].'</strong>':0)."</td><td>".($count[$key][2]>0?'<strong>'.$count[$key][2].'</strong>':0)."</td><td>".($count[$key][3]>0?'<strong>'.$count[$key][3].'</strong>':0)."</td><td>".($count['ch'.($key+1)]>0?'<strong>'.$count['ch'.($key+1)].'</strong>':0)."</td></tr>";
      }
      $count['totalTr'] = "<tr><td>Toplam</td><td>".($count['red']>0?'<strong>'.$count['red'].'</strong>':0)."</td><td>".($count['yellow']>0?'<strong>'.$count['yellow'].'</strong>':0)."</td><td>".($count['blue']>0?'<strong>'.$count['blue'].'</strong>':0)."</td><td>".($count['total']>0?'<strong>'.$count['total'].'</strong>':0)."</td></tr>";
      $count['total'] = '<h4>'.lang('Anasayfa.sayfa.toplamOyuncuSayisi').' : '.$count['total'].'</h4>';
      echo json_encode($count, JSON_INVALID_UTF8_SUBSTITUTE);
      exit;
    }else {
      return redirect()->to(base_url('Hata'));
    }
  }
}
