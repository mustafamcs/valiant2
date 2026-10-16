<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class Ekonomi extends BaseController
{
  public $viewFolder = "";

  public function __construct()
  {
    $this->viewFolder = "Ekonomi";
    if (!session('user_id')) {
      header('Location: '.base_url('GirisYap'));
      exit;
    }
  }

  public function Index()
  {
    $db = \Config\Database::connect('metin2');
    $panelDb = \Config\Database::connect();

    $stats = [
      'total_gold'      => 0,
      'total_chars'     => 0,
      'total_accounts'  => 0,
      'avg_level'       => 1,
      'top_rich'        => [],
      'guild_stats'     => [],
      'hack_logs'       => [],
      'webhook_url'     => '',
    ];

    try {
      $r = $db->query("SELECT COALESCE(SUM(gold),0) AS t_gold, COUNT(*) AS t_chars, COALESCE(AVG(level),1) AS avg_lv FROM player.player")->getRow();
      if ($r) {
        $stats['total_gold']  = (int)$r->t_gold;
        $stats['total_chars'] = (int)$r->t_chars;
        $stats['avg_level']   = round((float)$r->avg_lv, 1);
      }

      $ra = $db->query("SELECT COUNT(*) AS cnt FROM account.account")->getRow();
      if ($ra) $stats['total_accounts'] = (int)$ra->cnt;

      $stats['top_rich'] = $db->query("SELECT id, name, level, gold, playtime, last_play FROM player.player ORDER BY gold DESC LIMIT 15")->getResultArray();

      $stats['guild_stats'] = $db->query("
        SELECT g.id, g.name, g.level, g.win, g.draw, g.loss,
               COUNT(gm.pid) AS member_count,
               COUNT(DISTINCT p.ip) AS unique_ips
        FROM player.guild g
        LEFT JOIN player.guild_member gm ON gm.guild_id = g.id
        LEFT JOIN player.player p ON p.id = gm.pid
        GROUP BY g.id
        ORDER BY g.level DESC, member_count DESC
        LIMIT 20
      ")->getResultArray();

      $stats['hack_logs'] = $db->query("SELECT * FROM log.hack_log ORDER BY id DESC LIMIT 50")->getResultArray();
    } catch (\Throwable $e) {}

    try {
      $wRow = $panelDb->query("SELECT setting_content FROM settings WHERE setting_name = 'discordWebhookUrl' LIMIT 1")->getRow();
      if ($wRow) $stats['webhook_url'] = $wRow->setting_content;
    } catch (\Throwable $e) {}

    $viewData['viewFolder'] = $this->viewFolder;
    $viewData['stats']      = $stats;
    $viewData = array_merge(ConstantHeader(), $viewData);
    return view("{$this->viewFolder}/Index", $viewData);
  }

  public function KaynakAnalizAjax()
  {
    $request = \Config\Services::request();
    $vnum    = (int)$request->getPost('vnum');
    if ($vnum <= 0) {
      echo json_encode(['status' => 'error', 'message' => 'Geçerli bir eşya VNUM girin!']);
      exit;
    }

    $db = \Config\Database::connect('metin2');
    $result = [
      'item'       => null,
      'mobs'       => [],
      'chests'     => [],
      'shops'      => [],
      'cubes'      => [],
      'inv_count'  => 0,
    ];

    try {
      $it = $db->query("SELECT vnum, locale_name, gold, shop_buy_price, limitvalue0, refine_set, refined_vnum FROM player.item_proto WHERE vnum = ?", [$vnum])->getRow();
      if ($it) {
        $result['item'] = [
          'vnum'        => (int)$it->vnum,
          'name'        => mb_convert_encoding($it->locale_name, 'UTF-8', 'ISO-8859-9'),
          'gold'        => (int)$it->gold,
          'sell_price'  => (int)$it->shop_buy_price,
          'level'       => (int)$it->limitvalue0,
          'refine_set'  => (int)$it->refine_set,
          'refined_vnum'=> (int)$it->refined_vnum
        ];
      }

      // 1. Mob Drops
      $mobs = $db->query("
        SELECT d.mob_vnum, d.count, d.prob, m.locale_name, m.level
        FROM player.drop_default d
        LEFT JOIN player.mob_proto m ON m.vnum = d.mob_vnum
        WHERE d.item_vnum = ?
        ORDER BY d.prob DESC
        LIMIT 50
      ", [$vnum])->getResultArray();
      foreach ($mobs as $m) {
        $result['mobs'][] = [
          'mob_vnum' => (int)$m['mob_vnum'],
          'mob_name' => isset($m['locale_name']) ? mb_convert_encoding($m['locale_name'], 'UTF-8', 'ISO-8859-9') : ('Mob #'.$m['mob_vnum']),
          'level'    => (int)($m['level'] ?? 1),
          'count'    => (int)$m['count'],
          'prob_pct' => round(((int)$m['prob']) / 100.0, 2)
        ];
      }

      // 2. Special Item Groups (Chests)
      $chests = $db->query("
        SELECT i.group_vnum, i.count, i.prob, p.locale_name
        FROM player.drop_special_items i
        LEFT JOIN player.item_proto p ON p.vnum = i.group_vnum
        WHERE i.item_vnum = ?
        LIMIT 40
      ", [$vnum])->getResultArray();
      foreach ($chests as $c) {
        $result['chests'][] = [
          'chest_vnum' => (int)$c['group_vnum'],
          'chest_name' => isset($c['locale_name']) ? mb_convert_encoding($c['locale_name'], 'UTF-8', 'ISO-8859-9') : ('Sandık #'.$c['group_vnum']),
          'count'      => (int)$c['count'],
          'prob'       => (int)$c['prob']
        ];
      }

      // 3. NPC Shops
      $shops = $db->query("
        SELECT s.vnum AS shop_id, s.npc_vnum, si.count, m.locale_name
        FROM player.shop_item si
        JOIN player.shop s ON s.vnum = si.shop_vnum
        LEFT JOIN player.mob_proto m ON m.vnum = s.npc_vnum
        WHERE si.item_vnum = ?
      ", [$vnum])->getResultArray();
      foreach ($shops as $sh) {
        $result['shops'][] = [
          'shop_id'  => (int)$sh['shop_id'],
          'npc_vnum' => (int)$sh['npc_vnum'],
          'npc_name' => isset($sh['locale_name']) ? mb_convert_encoding($sh['locale_name'], 'UTF-8', 'ISO-8859-9') : ('NPC #'.$sh['npc_vnum']),
          'count'    => (int)$sh['count']
        ];
      }

      // 4. Total Existing in Player Inventories
      $inv = $db->query("SELECT COALESCE(SUM(count),0) AS total_cnt FROM player.item WHERE vnum = ?", [$vnum])->getRow();
      if ($inv) $result['inv_count'] = (int)$inv->total_cnt;
    } catch (\Throwable $e) {}

    // 5. Cube Recipes
    $cubeFile = dirname(FCPATH, 2) . "/runtime/server/main/srv1/share/locale/europe/common/cube.txt";
    if (is_file($cubeFile)) {
      $curNpc = 0; $curRew = 0; $curMats = [];
      foreach (file($cubeFile, FILE_IGNORE_NEW_LINES) as $line) {
        $t = trim($line);
        if (strcasecmp($t, 'section') === 0) { $curNpc = 0; $curRew = 0; $curMats = []; }
        elseif (strcasecmp($t, 'end') === 0) {
          $usedAsMat = false;
          foreach ($curMats as $cm) { if ($cm['vnum'] === $vnum) $usedAsMat = true; }
          if ($curRew === $vnum || $usedAsMat) {
            $result['cubes'][] = [
              'npc'    => $curNpc,
              'role'   => ($curRew === $vnum) ? 'Üretilen Ödül' : 'Gerekli Malzeme',
              'reward' => $curRew
            ];
          }
        } else {
          $p = preg_split('/\s+/', $t);
          if (strtolower($p[0]) === 'npc' && isset($p[1])) $curNpc = (int)$p[1];
          elseif (strtolower($p[0]) === 'reward' && isset($p[1])) $curRew = (int)$p[1];
          elseif (strtolower($p[0]) === 'item' && isset($p[1], $p[2])) $curMats[] = ['vnum'=>(int)$p[1], 'count'=>(int)$p[2]];
        }
      }
    }

    echo json_encode(['status' => 'ok', 'data' => $result], JSON_INVALID_UTF8_SUBSTITUTE);
    exit;
  }

  public function DiscordWebhookAjax()
  {
    $request = \Config\Services::request();
    $url     = trim((string)$request->getPost('webhook_url'));
    $testMsg = trim((string)$request->getPost('test_message')) ?: 'VALIANT2 Ekonomi & Güvenlik Merkezi Discord bağlantısı aktif!';

    $panelDb = \Config\Database::connect();
    try {
      $exists = $panelDb->query("SELECT setting_name FROM settings WHERE setting_name = 'discordWebhookUrl'")->getRow();
      if ($exists) {
        $panelDb->query("UPDATE settings SET setting_content = ? WHERE setting_name = 'discordWebhookUrl'", [$url]);
      } else {
        $panelDb->query("INSERT INTO settings (setting_name, setting_content) VALUES ('discordWebhookUrl', ?)", [$url]);
      }
    } catch (\Throwable $e) {}

    if ($url !== '' && filter_var($url, FILTER_VALIDATE_URL)) {
      $payload = json_encode([
        'username' => 'VALIANT2 Sistem Gözcüsü',
        'embeds'   => [[
          'title'       => '🛡️ VALIANT2 Bildirim Sistemi',
          'description' => $testMsg,
          'color'       => 13938487,
          'timestamp'   => date('c')
        ]]
      ]);
      $ctx = stream_context_create([
        'http' => [
          'method'  => 'POST',
          'header'  => "Content-Type: application/json\r\n",
          'content' => $payload,
          'timeout' => 4
        ]
      ]);
      @file_get_contents($url, false, $ctx);
    }

    LogAdd("Discord Webhook ayarları güncellendi.", 'Ekonomi/Index', session('user_id'));
    echo json_encode(['status' => 'ok', 'message' => 'Discord Webhook kaydedildi ve test bildirimi gönderildi!']);
    exit;
  }
}
