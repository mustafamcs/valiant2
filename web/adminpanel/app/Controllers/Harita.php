<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class Harita extends BaseController
{
  public $viewFolder = "";
  private $mapBaseDir;
  private $atlasFile;

  public function __construct()
  {
    $this->viewFolder = "Harita";
    $root = dirname(FCPATH, 2);
    $this->mapBaseDir = $root . "/runtime/server/main/srv1/share/locale/europe/map";
    $this->atlasFile  = $root . "/assets/unpacked/data/config/general/atlasinfo.txt";
    if (!session('user_id')) {
      header('Location: '.base_url('GirisYap'));
      exit;
    }
  }

  public function Index()
  {
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData['maps']       = $this->ListMaps();
    $viewData['atlas']      = $this->ParseAtlasInfo();
    $viewData = array_merge(ConstantHeader(), $viewData);
    return view("{$this->viewFolder}/Index", $viewData);
  }

  private function ListMaps()
  {
    $maps = [];
    if (is_dir($this->mapBaseDir)) {
      foreach (scandir($this->mapBaseDir) as $d) {
        if ($d === '.' || $d === '..') continue;
        $full = $this->mapBaseDir . '/' . $d;
        if (is_dir($full) && is_file($full . '/Setting.txt')) {
          $setting = $this->ParseSetting($full . '/Setting.txt');
          $maps[] = [
            'name'    => $d,
            'width'   => $setting['width'],
            'height'  => $setting['height'],
            'base_x'  => $setting['base_x'],
            'base_y'  => $setting['base_y'],
            'has_regen' => is_file($full . '/regen.txt'),
            'has_stone' => is_file($full . '/stone.txt'),
            'has_boss'  => is_file($full . '/boss.txt'),
            'has_npc'   => is_file($full . '/npc.txt'),
          ];
        }
      }
    }
    return $maps;
  }

  private function ParseSetting($file)
  {
    $res = ['width' => 4, 'height' => 4, 'base_x' => 0, 'base_y' => 0];
    if (!is_file($file)) return $res;
    foreach (file($file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $line) {
      $parts = preg_split('/\s+/', trim($line));
      if (count($parts) >= 3 && strcasecmp($parts[0], 'MapSize') === 0) {
        $res['width']  = max(1, (int)$parts[1]);
        $res['height'] = max(1, (int)$parts[2]);
      } elseif (count($parts) >= 3 && strcasecmp($parts[0], 'BasePosition') === 0) {
        $res['base_x'] = (int)$parts[1];
        $res['base_y'] = (int)$parts[2];
      }
    }
    return $res;
  }

  private function ParseAtlasInfo()
  {
    $sectors = [];
    if (!is_file($this->atlasFile)) return $sectors;
    foreach (file($this->atlasFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $line) {
      $t = trim($line);
      if ($t === '' || $t[0] === '#' || strpos($t, '//') === 0) continue;
      $p = preg_split('/\s+/', $t);
      if (count($p) >= 5) {
        $bx = (int)$p[1];
        $by = (int)$p[2];
        $wx = (int)$p[3];
        $wy = (int)$p[4];
        $sectors[] = [
          'name' => $p[0],
          'bx'   => $bx,
          'by'   => $by,
          'wx'   => $wx,
          'wy'   => $wy,
          'aligned' => (($bx % 25600) === 0 && ($by % 25600) === 0)
        ];
      }
    }
    return $sectors;
  }

  private function SafeMapName($name)
  {
    $name = preg_replace('/[^a-zA-Z0-9_\-]/', '', (string)$name);
    if ($name === '' || !is_dir($this->mapBaseDir . '/' . $name)) return false;
    return $name;
  }

  private function SafeFileType($type)
  {
    $allowed = ['regen.txt', 'stone.txt', 'boss.txt', 'npc.txt'];
    return in_array($type, $allowed, true) ? $type : 'regen.txt';
  }

  private function ParseSeconds($timeStr)
  {
    $timeStr = strtolower(trim((string)$timeStr));
    if (preg_match('/^(\d+)s$/', $timeStr, $m)) return max(1, (int)$m[1]);
    if (preg_match('/^(\d+)m$/', $timeStr, $m)) return max(1, (int)$m[1] * 60);
    if (preg_match('/^(\d+)h$/', $timeStr, $m)) return max(1, (int)$m[1] * 3600);
    return max(15, (int)$timeStr ?: 60);
  }

  public function DetayAjax()
  {
    $request = \Config\Services::request();
    $mapName = $this->SafeMapName($request->getPost('map'));
    $fileType = $this->SafeFileType($request->getPost('type') ?: 'regen.txt');
    if (!$mapName) {
      echo json_encode(['status' => 'error', 'message' => 'Geçersiz harita!']);
      exit;
    }

    $mapDir = $this->mapBaseDir . '/' . $mapName;
    $setting = $this->ParseSetting($mapDir . '/Setting.txt');
    $targetFile = $mapDir . '/' . $fileType;
    $rawContent = is_file($targetFile) ? file_get_contents($targetFile) : '';

    $db = \Config\Database::connect('metin2');
    $mobGrades = [];
    try {
      $q = $db->query("SELECT vnum, locale_name, gold_min, gold_max, exp FROM player.mob_proto");
      foreach ($q->getResult() as $r) {
        $mobGrades[(int)$r->vnum] = [
          'name' => mb_convert_encoding($r->locale_name, 'UTF-8', 'ISO-8859-9'),
          'gold' => (($r->gold_min + $r->gold_max) / 2.0),
          'exp'  => (int)$r->exp
        ];
      }
    } catch (\Throwable $e) {}

    $spawns = [];
    $allFiles = ['regen.txt', 'stone.txt', 'boss.txt', 'npc.txt'];
    foreach ($allFiles as $fName) {
      $fPath = $mapDir . '/' . $fName;
      if (!is_file($fPath)) continue;
      foreach (file($fPath, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $idx => $line) {
        $t = trim($line);
        if ($t === '' || $t[0] === '#' || strpos($t, '//') === 0) continue;
        $p = preg_split('/\s+/', $t);
        if (count($p) >= 11) {
          $kind = $p[0];
          $x    = (int)$p[1];
          $y    = (int)$p[2];
          $sx   = (int)$p[3];
          $sy   = (int)$p[4];
          $resp = $p[7];
          $cnt  = max(1, (int)$p[9]);
          $vnum = (int)$p[10];
          $sec  = $this->ParseSeconds($resp);
          $mobInfo = $mobGrades[$vnum] ?? ['name' => 'Grup/Mob #'.$vnum, 'gold' => 2500, 'exp' => 5000];
          $hourlyYang = (int)((3600.0 / $sec) * $cnt * max(500, $mobInfo['gold']));
          $spawns[] = [
            'file'  => $fName,
            'kind'  => $kind,
            'x'     => $x,
            'y'     => $y,
            'sx'    => $sx,
            'sy'    => $sy,
            'time'  => $resp,
            'count' => $cnt,
            'vnum'  => $vnum,
            'name'  => $mobInfo['name'],
            'yang_h'=> $hourlyYang
          ];
        }
      }
    }

    echo json_encode([
      'status'  => 'ok',
      'map'     => $mapName,
      'type'    => $fileType,
      'setting' => $setting,
      'raw'     => $rawContent,
      'spawns'  => $spawns
    ], JSON_INVALID_UTF8_SUBSTITUTE);
    exit;
  }

  public function KaydetAjax()
  {
    $request  = \Config\Services::request();
    $mapName  = $this->SafeMapName($request->getPost('map'));
    $fileType = $this->SafeFileType($request->getPost('type') ?: 'regen.txt');
    $content  = (string)$request->getPost('content');
    if (!$mapName) {
      echo json_encode(['status' => 'error', 'message' => 'Geçersiz harita!']);
      exit;
    }
    $targetFile = $this->mapBaseDir . '/' . $mapName . '/' . $fileType;
    file_put_contents($targetFile, str_replace("\r\n", "\n", $content));
    LogAdd("$mapName / $fileType harita spawn dosyası güncellendi.", 'Harita/Index', session('user_id'));

    $reloadSent = false;
    if (function_exists('SendServer')) {
      @SendServer('regen', 'RELOAD', 30004);
      $reloadSent = true;
    }
    echo json_encode([
      'status'  => 'ok',
      'message' => "$mapName/$fileType kaydedildi" . ($reloadSent ? ' ve canlı sunucuya RELOAD gönderildi!' : '!')
    ]);
    exit;
  }

  public function IzgaraDagitAjax()
  {
    $request  = \Config\Services::request();
    $mapName  = $this->SafeMapName($request->getPost('map'));
    $fileType = $this->SafeFileType($request->getPost('type') ?: 'stone.txt');
    $vnum     = (int)$request->getPost('vnum');
    $count    = min(200, max(1, (int)$request->getPost('adet')));
    $respTime = preg_replace('/[^0-9smh]/i', '', (string)$request->getPost('sure')) ?: '60s';
    $kind     = ($fileType === 'regen.txt') ? 'r' : 'm';

    if (!$mapName || $vnum <= 0) {
      echo json_encode(['status' => 'error', 'message' => 'Geçersiz harita veya VNUM!']);
      exit;
    }

    $mapDir  = $this->mapBaseDir . '/' . $mapName;
    $setting = $this->ParseSetting($mapDir . '/Setting.txt');
    $maxW    = $setting['width'] * 256;
    $maxH    = $setting['height'] * 256;

    $lines = [];
    $cols  = max(1, (int)ceil(sqrt($count)));
    $rows  = max(1, (int)ceil($count / $cols));
    $padX  = (int)($maxW * 0.12);
    $padY  = (int)($maxH * 0.12);
    $useW  = max(100, $maxW - 2 * $padX);
    $useH  = max(100, $maxH - 2 * $padY);

    $generated = 0;
    for ($r = 0; $r < $rows && $generated < $count; $r++) {
      for ($c = 0; $c < $cols && $generated < $count; $c++) {
        $cx = $padX + (int)(($c + 0.5) * ($useW / $cols)) + rand(-12, 12);
        $cy = $padY + (int)(($r + 0.5) * ($useH / $rows)) + rand(-12, 12);
        $lines[] = sprintf("%s\t%d\t%d\t10\t10\t0\t0\t%s\t100\t1\t%d", $kind, max(10, $cx), max(10, $cy), $respTime, $vnum);
        $generated++;
      }
    }

    $targetFile = $mapDir . '/' . $fileType;
    $existing = is_file($targetFile) ? rtrim(file_get_contents($targetFile)) . "\n" : "";
    $newContent = $existing . implode("\n", $lines) . "\n";
    file_put_contents($targetFile, $newContent);
    LogAdd("$mapName / $fileType içine $generated adet VNUM #$vnum ızgara modunda dağıtıldı.", 'Harita/Index', session('user_id'));

    echo json_encode([
      'status'  => 'ok',
      'message' => "$generated adet VNUM #$vnum haritaya ızgara olarak eklendi!",
      'raw'     => $newContent
    ]);
    exit;
  }
}
