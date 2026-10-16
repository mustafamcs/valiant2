<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class Arindirma extends BaseController
{
  public $viewFolder = "";
  private $serverCubeFile;
  private $clientWikiCubeFile;

  public function __construct()
  {
    $this->viewFolder = "Arindirma";
    $root = dirname(FCPATH, 2);
    $this->serverCubeFile     = $root . "/runtime/server/main/srv1/share/locale/europe/common/cube.txt";
    $this->clientWikiCubeFile = $root . "/assets/unpacked/data/config/general/wikipedia/cube.txt";
    if (!session('user_id')) {
      header('Location: '.base_url('GirisYap'));
      exit;
    }
  }

  public function Index()
  {
    $viewData['viewFolder'] = $this->viewFolder;
    $parsed                 = $this->ParseCubeRecipes();
    $viewData['recipes']    = $parsed['recipes'];
    $viewData['conflicts']  = $parsed['conflicts'];
    $viewData = array_merge(ConstantHeader(), $viewData);
    return view("{$this->viewFolder}/Index", $viewData);
  }

  private function GetItemAndNpcMaps()
  {
    $db = \Config\Database::connect('metin2');
    $items = [];
    $npcs  = [];
    try {
      $q = $db->query("SELECT vnum, locale_name FROM player.item_proto");
      foreach ($q->getResult() as $r) {
        $items[(int)$r->vnum] = mb_convert_encoding($r->locale_name, 'UTF-8', 'ISO-8859-9');
      }
      $qm = $db->query("SELECT vnum, locale_name FROM player.mob_proto");
      foreach ($qm->getResult() as $r) {
        $npcs[(int)$r->vnum] = mb_convert_encoding($r->locale_name, 'UTF-8', 'ISO-8859-9');
      }
    } catch (\Throwable $e) {}
    return ['items' => $items, 'npcs' => $npcs];
  }

  private function ParseCubeRecipes()
  {
    $recipes   = [];
    $conflicts = [];
    if (!is_file($this->serverCubeFile)) {
      return ['recipes' => $recipes, 'conflicts' => $conflicts];
    }

    $maps = $this->GetItemAndNpcMaps();
    $itemNames = $maps['items'];
    $npcNames  = $maps['npcs'];

    $current = null;
    $idx = 0;
    foreach (file($this->serverCubeFile, FILE_IGNORE_NEW_LINES) as $line) {
      $t = trim($line);
      if ($t === '' || $t[0] === '#' || strpos($t, '//') === 0) continue;
      if (strcasecmp($t, 'section') === 0) {
        $current = [
          'idx'       => $idx++,
          'npc'       => 0,
          'npc_name'  => '',
          'items'     => [],
          'reward'    => ['vnum' => 0, 'count' => 1, 'name' => ''],
          'gold'      => 0,
          'percent'   => 100,
          'category'  => 'UPGRADE',
          'allow_copy'=> 0,
        ];
        continue;
      }
      if (strcasecmp($t, 'end') === 0) {
        if ($current !== null) {
          $recipes[] = $current;
          $current = null;
        }
        continue;
      }
      if ($current === null) continue;

      $p = preg_split('/\s+/', $t);
      $key = strtolower($p[0]);
      if ($key === 'npc' && isset($p[1])) {
        $v = (int)$p[1];
        $current['npc']      = $v;
        $current['npc_name'] = $npcNames[$v] ?? ('NPC #'.$v);
      } elseif ($key === 'item' && isset($p[1], $p[2])) {
        $v = (int)$p[1];
        $c = (int)$p[2];
        $current['items'][] = [
          'vnum'  => $v,
          'count' => $c,
          'name'  => $itemNames[$v] ?? ('Eşya #'.$v)
        ];
      } elseif ($key === 'reward' && isset($p[1], $p[2])) {
        $v = (int)$p[1];
        $c = (int)$p[2];
        $current['reward'] = [
          'vnum'  => $v,
          'count' => $c,
          'name'  => $itemNames[$v] ?? ('Eşya #'.$v)
        ];
      } elseif ($key === 'gold' && isset($p[1])) {
        $current['gold'] = (int)$p[1];
      } elseif ($key === 'percent' && isset($p[1])) {
        $current['percent'] = (int)$p[1];
      } elseif ($key === 'category' && isset($p[1])) {
        $current['category'] = $p[1];
      } elseif ($key === 'allow_copy' && isset($p[1])) {
        $current['allow_copy'] = (int)$p[1];
      }
    }

    // Conflict detection: same NPC + identical sorted material set + same reward
    $seen = [];
    foreach ($recipes as $r) {
      $matKeyParts = [];
      foreach ($r['items'] as $m) {
        $matKeyParts[] = $m['vnum'] . 'x' . $m['count'];
      }
      sort($matKeyParts);
      $sig = $r['npc'] . '|' . implode('+', $matKeyParts) . '|' . $r['reward']['vnum'];
      if (isset($seen[$sig])) {
        $conflicts[] = "Tarif #" . ($seen[$sig] + 1) . " ve #" . ($r['idx'] + 1) . " çakışıyor (NPC: {$r['npc']}, Ödül: {$r['reward']['vnum']})";
      } else {
        $seen[$sig] = $r['idx'];
      }
    }

    return ['recipes' => $recipes, 'conflicts' => $conflicts];
  }

  private function SaveCubeRecipesArray(array $recipes)
  {
    $lines = [];
    foreach ($recipes as $r) {
      $lines[] = "section";
      $lines[] = "npc\t" . (int)$r['npc'];
      foreach ($r['items'] as $m) {
        if ((int)$m['vnum'] > 0 && (int)$m['count'] > 0) {
          $lines[] = "item\t" . (int)$m['vnum'] . "\t" . (int)$m['count'];
        }
      }
      $lines[] = "reward\t" . (int)$r['reward']['vnum'] . "\t" . max(1, (int)$r['reward']['count']);
      $lines[] = "gold\t" . max(0, (int)$r['gold']);
      $lines[] = "percent\t" . min(100, max(1, (int)$r['percent']));
      if (!empty($r['allow_copy'])) {
        $lines[] = "allow_copy\t" . (int)$r['allow_copy'];
      }
      $lines[] = "category " . preg_replace('/[^A-Za-z0-9_]/', '', (string)($r['category'] ?: 'UPGRADE'));
      $lines[] = "end";
    }
    $content = implode("\n", $lines) . "\n";
    file_put_contents($this->serverCubeFile, $content);
    if (is_dir(dirname($this->clientWikiCubeFile))) {
      file_put_contents($this->clientWikiCubeFile, $content);
    }
    if (function_exists('SendServer')) {
      @SendServer('c', 'RELOAD', 30004);
    }
  }

  public function EkleAjax()
  {
    $request = \Config\Services::request();
    $npc     = (int)$request->getPost('npc');
    $rewVnum = (int)$request->getPost('reward_vnum');
    $rewCnt  = max(1, (int)$request->getPost('reward_count'));
    $gold    = max(0, (int)$request->getPost('gold'));
    $pct     = min(100, max(1, (int)$request->getPost('percent')));
    $cat     = preg_replace('/[^A-Za-z0-9_]/', '', (string)$request->getPost('category')) ?: 'UPGRADE';

    $mats = [];
    for ($i = 1; $i <= 5; $i++) {
      $mv = (int)$request->getPost("mat_vnum_$i");
      $mc = (int)$request->getPost("mat_count_$i");
      if ($mv > 0 && $mc > 0) {
        $mats[] = ['vnum' => $mv, 'count' => $mc];
      }
    }

    if ($npc <= 0 || $rewVnum <= 0 || empty($mats)) {
      echo json_encode(['status' => 'error', 'message' => 'NPC, ödül VNUM ve en az 1 malzeme zorunludur!']);
      exit;
    }

    $parsed = $this->ParseCubeRecipes();
    $recipes = $parsed['recipes'];
    $recipes[] = [
      'npc'        => $npc,
      'items'      => $mats,
      'reward'     => ['vnum' => $rewVnum, 'count' => $rewCnt],
      'gold'       => $gold,
      'percent'    => $pct,
      'category'   => $cat,
      'allow_copy' => (int)$request->getPost('allow_copy')
    ];

    $this->SaveCubeRecipesArray($recipes);
    LogAdd("Cube tarifi eklendi (NPC: $npc -> Ödül: $rewVnum x$rewCnt).", 'Arindirma/Index', session('user_id'));

    echo json_encode(['status' => 'ok', 'message' => 'Yeni arındırma (Cube) tarifi eklendi ve hem sunucuya hem Wikipedia\'ya senkronize edildi!']);
    exit;
  }

  public function SilAjax()
  {
    $request = \Config\Services::request();
    $idx     = (int)$request->getPost('idx');
    $parsed  = $this->ParseCubeRecipes();
    $recipes = $parsed['recipes'];

    if (!isset($recipes[$idx])) {
      echo json_encode(['status' => 'error', 'message' => 'Tarif bulunamadı!']);
      exit;
    }
    unset($recipes[$idx]);
    $this->SaveCubeRecipesArray(array_values($recipes));
    LogAdd("Cube tarifi #$idx silindi.", 'Arindirma/Index', session('user_id'));

    echo json_encode(['status' => 'ok', 'message' => 'Tarif silindi ve sunucuya RELOAD gönderildi!']);
    exit;
  }
}
