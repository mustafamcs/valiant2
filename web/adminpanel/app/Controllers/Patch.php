<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class Patch extends BaseController
{
  public $viewFolder   = "";
  private $patchDir    = "C:/patchserver/patch";
  private $filesDir    = "C:/patchserver/patch/files";
  private $listFile    = "C:/patchserver/patch/patchlist.json";
  private $hashCache   = "C:/patchserver/patch/hashcache.json";

  public function __construct()
  {
    $this->viewFolder   = "Patch";
    if (!session('user_id')) {
      header('Location: '.base_url('GirisYap'));
      exit;
    }
  }

  public function Index()
  {
    if (!IsAllowedViewModule('patchGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData['surum']      = $this->SurumOku();
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Index",$viewData);
  }

  private function SurumOku()
  {
    if (is_file($this->listFile)) {
      $j = json_decode(file_get_contents($this->listFile),true);
      return isset($j['version'])?(int)$j['version']:0;
    }
    return 0;
  }

  private function DosyaListele()
  {
    $list  = [];
    $cache = [];
    if (is_file($this->hashCache)) {
      $cache = json_decode(file_get_contents($this->hashCache),true) ?: [];
    }
    $yeniCache = [];
    if (is_dir($this->filesDir)) {
      $it = new \RecursiveIteratorIterator(new \RecursiveDirectoryIterator($this->filesDir, \FilesystemIterator::SKIP_DOTS));
      foreach ($it as $f) {
        if ($f->isFile()) {
          $rel  = str_replace('\\','/',substr($f->getPathname(),strlen($this->filesDir)+1));
          $size = $f->getSize();
          $mt   = $f->getMTime();
          if (isset($cache[$rel]) && $cache[$rel]['size']===$size && $cache[$rel]['mtime']===$mt) {
            $sha = $cache[$rel]['sha256'];
          } else {
            $sha = hash_file('sha256',$f->getPathname());
          }
          $yeniCache[$rel] = ['size'=>$size,'mtime'=>$mt,'sha256'=>$sha];
          $list[] = ['path'=>$rel,'size'=>$size,'sha256'=>$sha];
        }
      }
      usort($list,function($a,$b){return strcmp($a['path'],$b['path']);});
    }
    if (!is_dir($this->patchDir)) mkdir($this->patchDir,0755,true);
    file_put_contents($this->hashCache,json_encode($yeniCache));
    return $list;
  }

  public function Ajax()
  {
    if (!IsAllowedViewModule('patchGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request = \Config\Services::request();
    $all     = $this->DosyaListele();
    $search  = $request->getPost('search[value]');
    if ($search) {
      $all = array_values(array_filter($all,function($r)use($search){return stripos($r['path'],$search)!==false;}));
    }
    $start = (int)$request->getPost('start');
    $len   = (int)$request->getPost('length');
    $page  = array_slice($all,$start,$len>0?$len:count($all));
    $data  = [];
    foreach ($page as $row) {
      $sub   = [];
      $sub[] = htmlspecialchars($row['path']);
      $sub[] = number_format($row['size']/1024,1).' KB';
      $sub[] = '<code>'.substr($row['sha256'],0,12).'…</code>';
      if (IsAllowedViewModule('patchSilebilsin')) {
        $sub[] = '<a class="btn btn-danger pt-1 pb-1 ps-2 pe-2 patchSil" href="javascript:void(0)" data-id="'.htmlspecialchars($row['path']).'" data-header="'.lang('Genel.silBaslik').'" data-message="'.lang('Genel.buIslemGeriAlinamaz').'" data-yes="'.lang('Genel.evet').'" data-no="'.lang('Genel.hayir').'">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" style="width:25px;height:25px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><line x1="4" y1="7" x2="20" y2="7" /><line x1="10" y1="11" x2="10" y2="17" /><line x1="14" y1="11" x2="14" y2="17" /><path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12" /><path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3" /></svg>
        </a>';
      }
      $data[] = $sub;
    }
    echo json_encode([
      "draw"            => intval($_POST["draw"]),
      "recordsTotal"    => count($all),
      "recordsFiltered" => count($all),
      "data"            => $data,
    ], JSON_INVALID_UTF8_SUBSTITUTE);
    exit;
  }

  private function GuvenliYol($rel)
  {
    $rel = str_replace('\\','/',trim((string)$rel));
    if ($rel==='' || strpos($rel,'..')!==false || $rel[0]==='/' ) return false;
    return $rel;
  }

  public function Yukle()
  {
    if (!IsAllowedViewModule('patchEkleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request = \Config\Services::request();
    $file    = $request->getFile('dosya');
    $hedef   = $this->GuvenliYol($request->getPost('hedef'));
    if (!$file || !$file->isValid()) {
      responseResult('error',lang('Patch.cikti.dosyaYok'));
    }
    if (!$hedef) {
      $hedef = $file->getName();
    }
    if (!preg_match('/^[\w\-\.\/]+$/',$hedef) || strpos($hedef,'..')!==false) {
      responseResult('error',lang('Patch.cikti.gecersizYol'));
    }
    $dest = $this->filesDir.'/'.$hedef;
    if (!is_dir(dirname($dest))) {
      mkdir(dirname($dest),0755,true);
    }
    if ($file->move(dirname($dest),basename($dest),true)) {
      LogAdd(lang('Patch.kayit.dosyaYuklendi',['yol'=>$hedef]),'Patch/Index',session('user_id'));
      responseResult('success',lang('Patch.cikti.dosyaYuklendi'));
    }
    responseResult('error',lang('Genel.bilinmeyenHata'));
  }

  public function Sil()
  {
    if (!IsAllowedViewModule('patchSilebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request = \Config\Services::request();
    $yol     = $this->GuvenliYol($request->getPost('yol'));
    $tam     = $yol ? $this->filesDir.'/'.$yol : '';
    if ($tam && is_file($tam)) {
      unlink($tam);
      LogAdd(lang('Patch.kayit.dosyaSilindi',['yol'=>$yol]),'Patch/Index',session('user_id'));
      responseResult('success',lang('Patch.cikti.dosyaSilindi'));
    }
    responseResult('error',lang('Patch.cikti.dosyaBulunamadi'));
  }

  public function ManifestOlustur()
  {
    if (!IsAllowedViewModule('patchEkleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $files = $this->DosyaListele();
    $manifest = [
      'version' => $this->SurumOku()+1,
      'base'    => rtrim(base_url('update/files/'),'/').'/',
      'files'   => $files,
    ];
    if (!is_dir($this->patchDir)) mkdir($this->patchDir,0755,true);
    file_put_contents($this->listFile,json_encode($manifest,JSON_UNESCAPED_SLASHES|JSON_PRETTY_PRINT));
    LogAdd(lang('Patch.kayit.manifestOlusturuldu',['surum'=>$manifest['version'],'adet'=>count($files)]),'Patch/Index',session('user_id'));
    responseResult('success',lang('Patch.cikti.manifestOlusturuldu',['version'=>$manifest['version'],'adet'=>count($files)]));
  }

  public function PatcherIndir()
  {
    if (!IsAllowedViewModule('patchGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $p = 'C:/patchserver/patcher/VALIANT2.exe';
    if (is_file($p)) {
      return $this->response->download($p,null)->setFileName('VALIANT2.exe');
    }
    responseResult('error',lang('Patch.cikti.patcherYok'));
  }
}
