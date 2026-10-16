<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class Sistemler extends BaseController
{
  public $viewFolder = "";
  private $clientControlsFile;
  private $serverControlsFile;
  private $basicWeaponQuestFile;

  public function __construct()
  {
    $this->viewFolder = "Sistemler";
    $root = dirname(FCPATH, 2);
    $this->clientControlsFile   = $root . "/source/client/source/Controls.h";
    $this->serverControlsFile   = $root . "/source/server/source/common/Controls.h";
    $this->basicWeaponQuestFile = $root . "/runtime/server/main/srv1/share/locale/europe/quest/collection/special/give_basic_weapon.lua";
    if (!session('user_id')) {
      header('Location: '.base_url('GirisYap'));
      exit;
    }
  }

  public function Index()
  {
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData['flags']      = $this->ReadFeatureFlags();
    $viewData['startQuest'] = is_file($this->basicWeaponQuestFile) ? file_get_contents($this->basicWeaponQuestFile) : '';
    $viewData = array_merge(ConstantHeader(), $viewData);
    return view("{$this->viewFolder}/Index", $viewData);
  }

  private function ParseControlsFile($path)
  {
    $map = [];
    if (!is_file($path)) return $map;
    foreach (file($path, FILE_IGNORE_NEW_LINES) as $line) {
      $t = trim($line);
      if (preg_match('/^#define\s+([A-Za-z0-9_]+)/', $t, $m)) {
        $map[$m[1]] = true;
      } elseif (preg_match('/^\/\/\s*#define\s+([A-Za-z0-9_]+)/', $t, $m)) {
        if (!isset($map[$m[1]])) $map[$m[1]] = false;
      }
    }
    return $map;
  }

  private function ReadFeatureFlags()
  {
    $cMap = $this->ParseControlsFile($this->clientControlsFile);
    $sMap = $this->ParseControlsFile($this->serverControlsFile);
    $allKeys = array_unique(array_merge(array_keys($cMap), array_keys($sMap)));
    sort($allKeys);

    $rows = [];
    foreach ($allKeys as $k) {
      if (strpos($k, 'ENABLE_') !== 0 && strpos($k, 'WJ_') !== 0) continue;
      $inClient = array_key_exists($k, $cMap);
      $inServer = array_key_exists($k, $sMap);
      $cVal = $inClient ? $cMap[$k] : null;
      $sVal = $inServer ? $sMap[$k] : null;
      $rows[] = [
        'name'      => $k,
        'in_client' => $inClient,
        'in_server' => $inServer,
        'client_on' => $cVal,
        'server_on' => $sVal,
        'active'    => ($cVal === true || $sVal === true),
        'synced'    => (!$inClient || !$inServer || $cVal === $sVal)
      ];
    }
    return $rows;
  }

  private function ToggleFlagInFile($filePath, $flagName, $enable)
  {
    if (!is_file($filePath)) return false;
    $lines = file($filePath, FILE_IGNORE_NEW_LINES);
    $changed = false;
    foreach ($lines as $i => $line) {
      if ($enable) {
        if (preg_match('/^(\s*)\/\/\s*(#define\s+' . preg_quote($flagName, '/') . '\b.*)$/', $line, $m)) {
          $lines[$i] = $m[1] . $m[2];
          $changed = true;
        }
      } else {
        if (preg_match('/^(\s*)(#define\s+' . preg_quote($flagName, '/') . '\b.*)$/', $line, $m)) {
          $lines[$i] = $m[1] . '// ' . $m[2];
          $changed = true;
        }
      }
    }
    if ($changed) {
      file_put_contents($filePath, implode("\n", $lines) . "\n");
    }
    return $changed;
  }

  public function BayrakDegistirAjax()
  {
    $request  = \Config\Services::request();
    $flagName = preg_replace('/[^A-Za-z0-9_]/', '', (string)$request->getPost('flag'));
    $enable   = ((int)$request->getPost('enable')) === 1;

    if ($flagName === '') {
      echo json_encode(['status' => 'error', 'message' => 'Geçersiz bayrak adı!']);
      exit;
    }

    $cChanged = $this->ToggleFlagInFile($this->clientControlsFile, $flagName, $enable);
    $sChanged = $this->ToggleFlagInFile($this->serverControlsFile, $flagName, $enable);

    $stateText = $enable ? 'AKTİF (#define)' : 'PASİF (//#define)';
    LogAdd("Controls.h bayrağı güncellendi: $flagName -> $stateText", 'Sistemler/Index', session('user_id'));

    echo json_encode([
      'status'  => 'ok',
      'message' => "$flagName bayrağı hem Client hem Server Controls.h içinde $stateText yapıldı! (Geçerli olması için Control Center'dan derleyin)"
    ]);
    exit;
  }

  public function ProfilUygulaAjax()
  {
    $request = \Config\Services::request();
    $profile = (string)$request->getPost('profile');
    $db      = \Config\Database::connect('metin2');

    try {
      if ($profile === '1_99_emek') {
        $db->query("UPDATE player.mob_proto SET gold_min = GREATEST(100, ROUND(gold_min * 0.7)), gold_max = GREATEST(250, ROUND(gold_max * 0.7))");
        $msg = "1-99 Hard Emek profili uygulandı (Mob Yang oranları dengelendi).";
      } elseif ($profile === '1_105_orta') {
        $db->query("UPDATE player.mob_proto SET gold_min = GREATEST(250, ROUND(gold_min * 1.1)), gold_max = GREATEST(500, ROUND(gold_max * 1.1))");
        $msg = "1-105 Orta Emek profili uygulandı.";
      } elseif ($profile === '65_250_pvm') {
        $db->query("UPDATE player.mob_proto SET gold_min = GREATEST(500, ROUND(gold_min * 1.5)), gold_max = GREATEST(1000, ROUND(gold_max * 1.5))");
        $msg = "65-250 PvM/Farm profili uygulandı.";
      } elseif ($profile === '98_99_wslik') {
        $msg = "98-99 WS'lik Düello profili seçildi.";
      } else {
        echo json_encode(['status' => 'error', 'message' => 'Bilinmeyen profil!']);
        exit;
      }

      if (function_exists('SendServer')) {
        @SendServer('p', 'RELOAD', 30004);
      }
      LogAdd("Sunucu profili uygulandı: $profile", 'Sistemler/Index', session('user_id'));
      echo json_encode(['status' => 'ok', 'message' => $msg]);
    } catch (\Throwable $e) {
      echo json_encode(['status' => 'error', 'message' => $e->getMessage()]);
    }
    exit;
  }

  public function BaslangicKaydetAjax()
  {
    $request = \Config\Services::request();
    $content = (string)$request->getPost('content');
    if ($content === '' || strpos($content, 'quest ') === false) {
      echo json_encode(['status' => 'error', 'message' => 'Geçersiz Lua quest içeriği!']);
      exit;
    }

    file_put_contents($this->basicWeaponQuestFile, str_replace("\r\n", "\n", $content));
    LogAdd("Başlangıç paketi (give_basic_weapon.lua) güncellendi.", 'Sistemler/Index', session('user_id'));

    echo json_encode([
      'status'  => 'ok',
      'message' => 'Başlangıç quest dosyası kaydedildi! Derlemek için Control Center veya build-quests.cmd kullanabilirsiniz.'
    ]);
    exit;
  }
}
