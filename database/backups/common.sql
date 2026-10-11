/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.4.8-MariaDB, for Win64 (AMD64)
--
-- Host: 127.0.0.1    Database: common
-- ------------------------------------------------------
-- Server version	11.4.8-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `exp_table`
--

DROP TABLE IF EXISTS `exp_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `exp_table` (
  `level` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `exp` int(10) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`level`) USING BTREE
) ENGINE=Aria AUTO_INCREMENT=121 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci PAGE_CHECKSUM=1 ROW_FORMAT=FIXED;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exp_table`
--

LOCK TABLES `exp_table` WRITE;
/*!40000 ALTER TABLE `exp_table` DISABLE KEYS */;
INSERT INTO `exp_table` VALUES
(1,300),
(2,800),
(3,1500),
(4,2500),
(5,4300),
(6,7200),
(7,11000),
(8,17000),
(9,24000),
(10,33000),
(11,43000),
(12,58000),
(13,76000),
(14,100000),
(15,130000),
(16,169000),
(17,219000),
(18,283000),
(19,365000),
(20,472000),
(21,610000),
(22,705000),
(23,813000),
(24,937000),
(25,1077000),
(26,1237000),
(27,1418000),
(28,1624000),
(29,1857000),
(30,2122000),
(31,2421000),
(32,2761000),
(33,3145000),
(34,3580000),
(35,4073000),
(36,4632000),
(37,5194000),
(38,5717000),
(39,6264000),
(40,6837000),
(41,7600000),
(42,8274000),
(43,8990000),
(44,9753000),
(45,10560000),
(46,11410000),
(47,12320000),
(48,13270000),
(49,14280000),
(50,15340000),
(51,16870000),
(52,18960000),
(53,19980000),
(54,21420000),
(55,22930000),
(56,24530000),
(57,26200000),
(58,27960000),
(59,29800000),
(60,32780000),
(61,36060000),
(62,39670000),
(63,43640000),
(64,48000000),
(65,52800000),
(66,58080000),
(67,63890000),
(68,70280000),
(69,77310000),
(70,85040000),
(71,93540000),
(72,102900000),
(73,113200000),
(74,124500000),
(75,137000000),
(76,150700000),
(77,165700000),
(78,236990000),
(79,260650000),
(80,286780000),
(81,315380000),
(82,346970000),
(83,381680000),
(84,419770000),
(85,461760000),
(86,508040000),
(87,558740000),
(88,614640000),
(89,676130000),
(90,743730000),
(91,1041222000),
(92,1145344200),
(93,1259878620),
(94,1385866482),
(95,1524453130),
(96,1676898443),
(97,1844588288),
(98,2029047116),
(99,2050000000),
(100,2150000000),
(101,2210000000),
(102,2250000000),
(103,2280000000),
(104,2310000000),
(105,2330000000),
(106,2350000000),
(107,2370000000),
(108,2390000000),
(109,2400000000),
(110,2410000000),
(111,2420000000),
(112,2430000000),
(113,2440000000),
(114,2450000000),
(115,2460000000),
(116,2470000000),
(117,2480000000),
(118,2490000000),
(119,2490000000),
(120,2500000000);
/*!40000 ALTER TABLE `exp_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game_settings`
--

DROP TABLE IF EXISTS `game_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `game_settings` (
  `version` int(11) NOT NULL,
  `player_mode` varchar(64) NOT NULL DEFAULT '',
  `maintenance_active` tinyint(3) DEFAULT NULL,
  `maintenance_start_time` datetime DEFAULT NULL,
  `maintenance_time` int(8) DEFAULT NULL,
  `maintenance_reason` varchar(64) DEFAULT NULL
) ENGINE=Aria DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci PAGE_CHECKSUM=1 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_settings`
--

LOCK TABLES `game_settings` WRITE;
/*!40000 ALTER TABLE `game_settings` DISABLE KEYS */;
INSERT INTO `game_settings` VALUES
(1000138963,'0',0,'2023-09-15 12:20:00',0,'Check discord for details!');
/*!40000 ALTER TABLE `game_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gmhost`
--

DROP TABLE IF EXISTS `gmhost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `gmhost` (
  `mIP` varchar(16) NOT NULL DEFAULT '',
  PRIMARY KEY (`mIP`) USING BTREE
) ENGINE=Aria DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci PAGE_CHECKSUM=1 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gmhost`
--

LOCK TABLES `gmhost` WRITE;
/*!40000 ALTER TABLE `gmhost` DISABLE KEYS */;
INSERT INTO `gmhost` VALUES
('127.0.0.1');
/*!40000 ALTER TABLE `gmhost` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gmlist`
--

DROP TABLE IF EXISTS `gmlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `gmlist` (
  `mID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `mAccount` varchar(16) NOT NULL DEFAULT '',
  `mName` varchar(16) NOT NULL DEFAULT '',
  `mContactIP` varchar(16) NOT NULL DEFAULT '',
  `mServerIP` varchar(16) NOT NULL DEFAULT 'ALL',
  `mAuthority` enum('IMPLEMENTOR','HIGH_WIZARD','GOD','LOW_WIZARD','PLAYER') NOT NULL DEFAULT 'PLAYER',
  `mMessengerShow` tinyint(2) NOT NULL DEFAULT 0,
  PRIMARY KEY (`mID`) USING BTREE
) ENGINE=Aria AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci PAGE_CHECKSUM=1 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gmlist`
--

LOCK TABLES `gmlist` WRITE;
/*!40000 ALTER TABLE `gmlist` DISABLE KEYS */;
INSERT INTO `gmlist` VALUES
(1,'md','MD','','ALL','IMPLEMENTOR',0),
(2,'mcs','MCS','127.0.0.1','ALL','IMPLEMENTOR',1);
/*!40000 ALTER TABLE `gmlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `goc`
--

DROP TABLE IF EXISTS `goc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `goc` (
  `dosya` varchar(255) NOT NULL,
  `uygulandi` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`dosya`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goc`
--

LOCK TABLES `goc` WRITE;
/*!40000 ALTER TABLE `goc` DISABLE KEYS */;
INSERT INTO `goc` VALUES
('0001_log_innodb.sql','2026-10-06 02:26:55'),
('0002_world_artik_tablolar.sql','2026-10-06 02:26:55'),
('0003_veri_durum.sql','2026-10-06 02:32:57'),
('0004_log_giris.sql','2026-10-08 20:01:24'),
('0005_log_quest.sql','2026-10-08 20:01:24'),
('0100_exp_tablosu.sql','2026-10-08 20:01:24'),
('0101_item_attr_exp_yang.sql','2026-10-08 20:01:24'),
('0110_otomatik_iksir_tarifleri.sql','2026-10-08 20:01:24'),
('0120_labirent_dukkani.sql','2026-10-08 20:01:25'),
('0130_ip_beyaz_liste.sql','2026-10-08 20:01:25'),
('0140_log_bot_guard.sql','2026-10-08 20:01:25'),
('0170_world_valentine_ozel_dukkan.sql','2026-10-08 20:01:25'),
('0171_log_money_log.sql','2026-10-08 20:01:25'),
('0180_item_kilit.sql','2026-10-08 20:01:25'),
('0200_player_achievement.sql','2026-10-08 20:01:25'),
('0210_guild_safebox.sql','2026-10-08 20:01:25'),
('0220_player_delete_pending.sql','2026-10-08 20:01:25'),
('0221_change_name_history.sql','2026-10-08 20:01:26'),
('0230_log_chat_log.sql','2026-10-08 20:01:26'),
('0231_world_banword_sohbet.sql','2026-10-08 20:01:26'),
('0240_argon2_sifre.sql','2026-10-08 20:01:26'),
('0250_hesap_kayit.sql','2026-10-08 20:01:26'),
('0260_hukumdar_secim.sql','2026-10-08 20:01:26'),
('0270_log_cash_reward.sql','2026-10-08 20:01:27'),
('0280_gorunum_binek_itemshop.sql','2026-10-08 20:01:27'),
('0290_log_bug_report.sql','2026-10-08 20:01:27'),
('0300_xmas_sil.sql','2026-10-08 20:01:27'),
('0301_xmas_fisek_sil.sql','2026-10-08 20:01:27'),
('0310_log_ekonomi.sql','2026-10-08 20:01:27'),
('0311_log_money_log.sql','2026-10-08 20:01:27'),
('0320_log_satir_kimligi.sql','2026-10-08 20:01:27'),
('0321_item_iade.sql','2026-10-08 20:01:27'),
('0322_davet_kodu.sql','2026-10-08 20:01:27'),
('0340_lisan_sil.sql','2026-10-08 20:01:28'),
('0360_etkinlik_skor.sql','2026-10-08 20:01:28'),
('0420_evlilik_yuzukleri_sil.sql','2026-10-08 20:01:28'),
('0421_zamanli_satis_908_sil.sql','2026-10-08 20:01:28'),
('0422_crafting_30341.sql','2026-10-08 20:01:28'),
('0423_object_proto_ad_satir_sonu.sql','2026-10-08 20:01:28'),
('0430_itemshop_guc_sil.sql','2026-10-08 20:01:28'),
('0440_kalici_dunya.sql','2026-10-08 20:01:28'),
('0460_special_flag_aid_indeks.sql','2026-10-08 20:01:28'),
('0480_ajan_test_hesaplari.sql','2026-10-08 20:01:29'),
('0490_log_item_pazar_olcum.sql','2026-10-08 20:01:29'),
('0510_log_eksik_tablolar.sql','2026-10-08 20:01:29'),
('0520_ajan_test_hesabi_karaktersiz.sql','2026-10-08 20:01:29'),
('0530_eski_binek_sil.sql','2026-10-08 20:01:29'),
('0540_etkinlik_sonuc.sql','2026-10-08 20:01:29'),
('0570_log_saklama_indeks.sql','2026-10-08 20:01:30'),
('0580_itemshop_onerilenler.sql','2026-10-08 20:01:30'),
('0600_cadilar_bayrami_sil.sql','2026-10-08 20:01:30'),
('0610_drop_gecersiz_mob_temizle.sql','2026-10-08 20:01:30'),
('0610_ikarusshop_log.sql','2026-10-08 20:01:30'),
('0620_log_chat_log_duyuru.sql','2026-10-08 20:01:30'),
('0630_itemshop_sayac.sql','2026-10-08 20:01:30');
/*!40000 ALTER TABLE `goc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ip_izin`
--

DROP TABLE IF EXISTS `ip_izin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ip_izin` (
  `ip` varchar(15) NOT NULL,
  `aciklama` varchar(128) NOT NULL DEFAULT '',
  `aktif` tinyint(1) NOT NULL DEFAULT 1,
  `ekleyen` varchar(32) NOT NULL DEFAULT '',
  `eklendi` datetime NOT NULL DEFAULT current_timestamp(),
  `guncellendi` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ip_izin`
--

LOCK TABLES `ip_izin` WRITE;
/*!40000 ALTER TABLE `ip_izin` DISABLE KEYS */;
/*!40000 ALTER TABLE `ip_izin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ip_izin_ayar`
--

DROP TABLE IF EXISTS `ip_izin_ayar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ip_izin_ayar` (
  `anahtar` varchar(32) NOT NULL,
  `deger` varchar(64) NOT NULL DEFAULT '',
  `degistiren` varchar(32) NOT NULL DEFAULT '',
  `guncellendi` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`anahtar`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ip_izin_ayar`
--

LOCK TABLES `ip_izin_ayar` WRITE;
/*!40000 ALTER TABLE `ip_izin_ayar` DISABLE KEYS */;
INSERT INTO `ip_izin_ayar` VALUES
('mod','izleme','goc','2026-10-08 20:01:25');
/*!40000 ALTER TABLE `ip_izin_ayar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ip_izin_log`
--

DROP TABLE IF EXISTS `ip_izin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ip_izin_log` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `zaman` datetime NOT NULL DEFAULT current_timestamp(),
  `islem` varchar(16) NOT NULL,
  `ip` varchar(15) NOT NULL DEFAULT '',
  `kim` varchar(32) NOT NULL DEFAULT '',
  `surec` varchar(32) NOT NULL DEFAULT '',
  `aciklama` varchar(128) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `zaman` (`zaman`),
  KEY `ip_zaman` (`ip`,`zaman`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ip_izin_log`
--

LOCK TABLES `ip_izin_log` WRITE;
/*!40000 ALTER TABLE `ip_izin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `ip_izin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `itemshop_items`
--

DROP TABLE IF EXISTS `itemshop_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `itemshop_items` (
  `index` int(10) NOT NULL,
  `vnum` int(10) NOT NULL,
  `count` smallint(4) NOT NULL,
  `price` int(10) NOT NULL,
  `currency` enum('DRAGON_COIN','DRAGON_MARK') NOT NULL DEFAULT 'DRAGON_COIN',
  `minLevel` int(10) NOT NULL DEFAULT 0,
  `socket0` int(10) NOT NULL DEFAULT 0,
  `socket1` int(10) NOT NULL DEFAULT 0,
  `socket2` int(10) NOT NULL DEFAULT 0,
  PRIMARY KEY (`index`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `itemshop_items`
--

LOCK TABLES `itemshop_items` WRITE;
/*!40000 ALTER TABLE `itemshop_items` DISABLE KEYS */;
INSERT INTO `itemshop_items` VALUES
(1,72701,1,49,'DRAGON_COIN',0,0,0,0),
(3,70138,50,49,'DRAGON_COIN',50,0,0,0),
(4,71099,1,95,'DRAGON_COIN',0,0,0,0),
(5,72702,1,59,'DRAGON_COIN',0,0,0,0),
(107,72131,1,19,'DRAGON_COIN',0,0,0,0),
(108,72132,1,39,'DRAGON_COIN',0,0,0,0),
(111,72151,1,79,'DRAGON_COIN',0,0,0,0),
(112,72161,1,19,'DRAGON_COIN',0,0,0,0),
(301,73001,1,39,'DRAGON_COIN',0,0,0,0),
(302,73002,1,39,'DRAGON_COIN',0,0,0,0),
(303,73003,1,39,'DRAGON_COIN',0,0,0,0),
(304,73004,1,39,'DRAGON_COIN',0,0,0,0),
(305,73005,1,39,'DRAGON_COIN',0,0,0,0),
(306,73006,1,39,'DRAGON_COIN',0,0,0,0),
(307,73007,1,39,'DRAGON_COIN',0,0,0,0),
(308,73008,1,39,'DRAGON_COIN',0,0,0,0),
(309,73009,1,39,'DRAGON_COIN',0,0,0,0),
(310,73010,1,39,'DRAGON_COIN',0,0,0,0),
(311,73011,1,39,'DRAGON_COIN',0,0,0,0),
(312,73012,1,39,'DRAGON_COIN',0,0,0,0),
(313,73051,1,39,'DRAGON_COIN',0,0,0,0),
(314,73052,1,39,'DRAGON_COIN',0,0,0,0),
(315,73053,1,39,'DRAGON_COIN',0,0,0,0),
(316,73054,1,39,'DRAGON_COIN',0,0,0,0),
(317,73055,1,39,'DRAGON_COIN',0,0,0,0),
(318,73056,1,39,'DRAGON_COIN',0,0,0,0),
(319,73057,1,39,'DRAGON_COIN',0,0,0,0),
(320,73058,1,39,'DRAGON_COIN',0,0,0,0),
(321,73059,1,39,'DRAGON_COIN',0,0,0,0),
(322,73060,1,39,'DRAGON_COIN',0,0,0,0),
(323,73061,1,39,'DRAGON_COIN',0,0,0,0),
(324,73062,1,39,'DRAGON_COIN',0,0,0,0),
(325,73251,1,39,'DRAGON_COIN',0,0,0,0),
(326,73252,1,39,'DRAGON_COIN',0,0,0,0),
(327,73253,1,39,'DRAGON_COIN',0,0,0,0),
(328,73254,1,39,'DRAGON_COIN',0,0,0,0),
(329,73255,1,39,'DRAGON_COIN',0,0,0,0),
(330,73256,1,39,'DRAGON_COIN',0,0,0,0),
(331,73257,1,39,'DRAGON_COIN',0,0,0,0),
(332,73258,1,39,'DRAGON_COIN',0,0,0,0),
(333,73259,1,39,'DRAGON_COIN',0,0,0,0),
(334,73260,1,39,'DRAGON_COIN',0,0,0,0),
(335,73261,1,39,'DRAGON_COIN',0,0,0,0),
(336,73262,1,39,'DRAGON_COIN',0,0,0,0),
(337,73301,1,39,'DRAGON_COIN',0,0,0,0),
(338,73302,1,39,'DRAGON_COIN',0,0,0,0),
(339,73303,1,39,'DRAGON_COIN',0,0,0,0),
(340,73304,1,39,'DRAGON_COIN',0,0,0,0),
(341,73305,1,39,'DRAGON_COIN',0,0,0,0),
(342,73306,1,39,'DRAGON_COIN',0,0,0,0),
(343,73307,1,39,'DRAGON_COIN',0,0,0,0),
(344,73308,1,39,'DRAGON_COIN',0,0,0,0),
(345,73309,1,39,'DRAGON_COIN',0,0,0,0),
(346,73310,1,39,'DRAGON_COIN',0,0,0,0),
(347,73311,1,39,'DRAGON_COIN',0,0,0,0),
(348,73312,1,39,'DRAGON_COIN',0,0,0,0),
(349,73501,1,39,'DRAGON_COIN',0,0,0,0),
(350,73502,1,39,'DRAGON_COIN',0,0,0,0),
(351,73503,1,39,'DRAGON_COIN',0,0,0,0),
(352,73504,1,39,'DRAGON_COIN',0,0,0,0),
(353,73505,1,39,'DRAGON_COIN',0,0,0,0),
(354,73506,1,39,'DRAGON_COIN',0,0,0,0),
(355,73507,1,39,'DRAGON_COIN',0,0,0,0),
(356,73508,1,39,'DRAGON_COIN',0,0,0,0),
(357,73509,1,39,'DRAGON_COIN',0,0,0,0),
(358,73510,1,39,'DRAGON_COIN',0,0,0,0),
(359,73511,1,39,'DRAGON_COIN',0,0,0,0),
(360,73512,1,39,'DRAGON_COIN',0,0,0,0),
(361,73601,1,39,'DRAGON_COIN',0,0,0,0),
(362,73602,1,39,'DRAGON_COIN',0,0,0,0),
(363,73603,1,39,'DRAGON_COIN',0,0,0,0),
(364,73604,1,39,'DRAGON_COIN',0,0,0,0),
(365,73605,1,39,'DRAGON_COIN',0,0,0,0),
(366,73606,1,39,'DRAGON_COIN',0,0,0,0),
(367,73607,1,39,'DRAGON_COIN',0,0,0,0),
(368,73608,1,39,'DRAGON_COIN',0,0,0,0),
(369,73609,1,39,'DRAGON_COIN',0,0,0,0),
(370,73610,1,39,'DRAGON_COIN',0,0,0,0),
(371,73611,1,39,'DRAGON_COIN',0,0,0,0),
(372,73612,1,39,'DRAGON_COIN',0,0,0,0),
(373,73751,1,39,'DRAGON_COIN',0,0,0,0),
(374,73752,1,39,'DRAGON_COIN',0,0,0,0),
(375,73753,1,39,'DRAGON_COIN',0,0,0,0),
(376,73754,1,39,'DRAGON_COIN',0,0,0,0),
(377,73755,1,39,'DRAGON_COIN',0,0,0,0),
(378,73756,1,39,'DRAGON_COIN',0,0,0,0),
(379,73757,1,39,'DRAGON_COIN',0,0,0,0),
(380,73758,1,39,'DRAGON_COIN',0,0,0,0),
(381,73759,1,39,'DRAGON_COIN',0,0,0,0),
(382,73760,1,39,'DRAGON_COIN',0,0,0,0),
(383,73761,1,39,'DRAGON_COIN',0,0,0,0),
(384,73762,1,39,'DRAGON_COIN',0,0,0,0),
(385,73801,1,39,'DRAGON_COIN',0,0,0,0),
(386,73802,1,39,'DRAGON_COIN',0,0,0,0),
(387,73803,1,39,'DRAGON_COIN',0,0,0,0),
(388,73804,1,39,'DRAGON_COIN',0,0,0,0),
(389,73805,1,39,'DRAGON_COIN',0,0,0,0),
(390,73806,1,39,'DRAGON_COIN',0,0,0,0),
(391,73807,1,39,'DRAGON_COIN',0,0,0,0),
(392,73808,1,39,'DRAGON_COIN',0,0,0,0),
(393,73809,1,39,'DRAGON_COIN',0,0,0,0),
(394,73810,1,39,'DRAGON_COIN',0,0,0,0),
(395,73811,1,39,'DRAGON_COIN',0,0,0,0),
(396,73812,1,39,'DRAGON_COIN',0,0,0,0),
(601,71048,1,199,'DRAGON_COIN',0,0,0,0),
(602,71002,1,79,'DRAGON_COIN',0,0,0,0),
(603,71003,1,49,'DRAGON_COIN',0,0,0,0),
(605,22010,10,39,'DRAGON_COIN',0,0,0,0),
(609,71095,1,7,'DRAGON_COIN',0,0,0,0),
(610,71095,25,49,'DRAGON_COIN',0,0,0,0),
(611,71054,1,149,'DRAGON_COIN',0,0,0,0),
(613,71103,1,39,'DRAGON_COIN',0,0,0,0),
(614,71104,1,39,'DRAGON_COIN',0,0,0,0),
(615,71105,1,39,'DRAGON_COIN',0,0,0,0),
(616,71106,1,39,'DRAGON_COIN',0,0,0,0),
(690,71055,1,149,'DRAGON_COIN',0,0,0,0),
(711,22000,1,69,'DRAGON_MARK',0,0,0,0),
(713,30177,1,1,'DRAGON_MARK',0,0,0,0),
(901,80017,1,58,'DRAGON_COIN',0,0,0,0),
(902,80014,1,112,'DRAGON_COIN',0,0,0,0),
(903,80018,1,275,'DRAGON_COIN',0,0,0,0),
(904,80015,1,540,'DRAGON_COIN',0,0,0,0),
(905,80016,1,1060,'DRAGON_COIN',0,0,0,0),
(906,27989,1,99,'DRAGON_COIN',0,0,0,0),
(2800,71137,1,129,'DRAGON_COIN',0,0,0,0),
(2801,71138,1,129,'DRAGON_COIN',0,0,0,0),
(2802,71139,1,129,'DRAGON_COIN',0,0,0,0),
(2803,71140,1,129,'DRAGON_COIN',0,0,0,0),
(2804,71141,1,129,'DRAGON_COIN',0,0,0,0),
(2805,71142,1,129,'DRAGON_COIN',0,0,0,0);
/*!40000 ALTER TABLE `itemshop_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `itemshop_promotions`
--

DROP TABLE IF EXISTS `itemshop_promotions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `itemshop_promotions` (
  `item_index` int(10) NOT NULL,
  `price` int(11) NOT NULL,
  `start_time` datetime NOT NULL DEFAULT current_timestamp(),
  `end_time` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`item_index`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `itemshop_promotions`
--

LOCK TABLES `itemshop_promotions` WRITE;
/*!40000 ALTER TABLE `itemshop_promotions` DISABLE KEYS */;
INSERT INTO `itemshop_promotions` VALUES
(4,95,'2026-10-07 00:00:00','2037-12-31 23:59:59'),
(111,79,'2026-10-07 00:00:00','2037-12-31 23:59:59'),
(112,19,'2026-10-07 00:00:00','2037-12-31 23:59:59'),
(301,39,'2026-10-07 00:00:00','2037-12-31 23:59:59'),
(313,39,'2026-10-07 00:00:00','2037-12-31 23:59:59'),
(329,39,'2026-10-07 00:00:00','2037-12-31 23:59:59'),
(345,39,'2026-10-07 00:00:00','2037-12-31 23:59:59'),
(353,39,'2026-10-07 00:00:00','2037-12-31 23:59:59'),
(365,39,'2026-10-07 00:00:00','2037-12-31 23:59:59'),
(373,39,'2026-10-07 00:00:00','2037-12-31 23:59:59'),
(385,39,'2026-10-07 00:00:00','2037-12-31 23:59:59'),
(605,39,'2026-10-07 00:00:00','2037-12-31 23:59:59'),
(2800,129,'2026-10-07 00:00:00','2037-12-31 23:59:59'),
(2802,129,'2026-10-07 00:00:00','2037-12-31 23:59:59'),
(2805,129,'2026-10-07 00:00:00','2037-12-31 23:59:59');
/*!40000 ALTER TABLE `itemshop_promotions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `itemshop_time_auctions`
--

DROP TABLE IF EXISTS `itemshop_time_auctions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `itemshop_time_auctions` (
  `item_index` int(10) NOT NULL,
  `max_amount` int(10) NOT NULL DEFAULT 0,
  `account_limit` int(10) unsigned NOT NULL DEFAULT 0,
  `start_time` datetime NOT NULL DEFAULT current_timestamp(),
  `end_time` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`item_index`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `itemshop_time_auctions`
--

LOCK TABLES `itemshop_time_auctions` WRITE;
/*!40000 ALTER TABLE `itemshop_time_auctions` DISABLE KEYS */;
INSERT INTO `itemshop_time_auctions` VALUES
(906,1,0,'2024-12-28 05:14:27','2024-12-28 05:14:27');
/*!40000 ALTER TABLE `itemshop_time_auctions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kalici_dunya`
--

DROP TABLE IF EXISTS `kalici_dunya`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `kalici_dunya` (
  `id` tinyint(3) unsigned NOT NULL DEFAULT 1,
  `acik` tinyint(1) NOT NULL DEFAULT 0,
  `baslangic` datetime DEFAULT NULL,
  `baslatan` varchar(32) NOT NULL DEFAULT '',
  `yedek` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kalici_dunya`
--

LOCK TABLES `kalici_dunya` WRITE;
/*!40000 ALTER TABLE `kalici_dunya` DISABLE KEYS */;
INSERT INTO `kalici_dunya` VALUES
(1,0,NULL,'','');
/*!40000 ALTER TABLE `kalici_dunya` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `locale`
--

DROP TABLE IF EXISTS `locale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `locale` (
  `mKey` varchar(255) NOT NULL DEFAULT '',
  `mValue` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`mKey`) USING BTREE
) ENGINE=Aria DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci PAGE_CHECKSUM=1 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `locale`
--

LOCK TABLES `locale` WRITE;
/*!40000 ALTER TABLE `locale` DISABLE KEYS */;
INSERT INTO `locale` VALUES
('SKILL_POWER_BY_LEVEL_TYPE0','0 5 6 8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40 50 52 54 56 58 60 63 66 69 72 82 85 88 91 94 98 102 106 110 115 130 140 150 160 170 180 190 200 210 220 230 240 255 270 285 300 315 330 345 360 375 390 405 410'),
('SKILL_POWER_BY_LEVEL_TYPE1','0 5 6 8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40 50 52 54 56 58 60 63 66 69 72 82 85 88 91 94 98 102 106 110 115 130 140 150 160 170 180 190 200 210 220 230 240 255 270 285 300 315 330 345 360 375 390 405 410'),
('SKILL_POWER_BY_LEVEL_TYPE2','0 5 6 8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40 50 52 54 56 58 60 63 66 69 72 82 85 88 91 94 98 102 106 110 115 130 140 150 160 170 180 190 200 210 220 230 240 255 270 285 300 315 330 345 360 375 390 405 410'),
('SKILL_POWER_BY_LEVEL_TYPE3','0 5 6 8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40 50 52 54 56 58 60 63 66 69 72 82 85 88 91 94 98 102 106 110 115 130 140 150 160 170 180 190 200 210 220 230 240 255 270 285 300 315 330 345 360 375 390 405 410'),
('SKILL_POWER_BY_LEVEL_TYPE4','0 5 6 8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40 50 52 54 56 58 60 63 66 69 72 82 85 88 91 94 98 102 106 110 115 130 140 150 160 170 180 190 200 210 220 230 240 255 270 285 300 315 330 345 360 375 390 405 410'),
('SKILL_POWER_BY_LEVEL_TYPE5','0 5 6 8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40 50 52 54 56 58 60 63 66 69 72 82 85 88 91 94 98 102 106 110 115 130 140 150 160 170 180 190 200 210 220 230 240 255 270 285 300 315 330 345 360 375 390 405 410'),
('SKILL_POWER_BY_LEVEL_TYPE6','0 5 6 8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40 50 52 54 56 58 60 63 66 69 72 82 85 88 91 94 98 102 106 110 115 130 140 150 160 170 180 190 200 210 220 230 240 255 270 285 300 315 330 345 360 375 390 405 410'),
('SKILL_POWER_BY_LEVEL_TYPE7','0 5 6 8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40 50 52 54 56 58 60 63 66 69 72 82 85 88 91 94 98 102 106 110 115 130 140 150 160 170 180 190 200 210 220 230 240 255 270 285 300 315 330 345 360 375 390 405 410'),
('LOCALE','europe'),
('DB_NAME_COLUMN','locale_name'),
('SKILL_DAMAGE_BY_LEVEL_UNDER_90','92 94 96 98 100 102 104 106 108 110 112 114 116 118 120'),
('SKILL_DAMAGE_BY_LEVEL_UNDER_45','2 4 6 8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40 42 44 46 48 50 52 54 56 58 60 62 64 66 68 70 72 74 76 78 80 82 84 86 88 90'),
('SKILL_POWER_BY_LEVEL','0 5 6 8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40 50 52 54 56 58 60 63 66 69 72 82 85 88 91 94 98 102 106 110 115 130 140 150 160 170 180 190 200 210 220 230 240 255 270 285 300 315 330 345 360 375 390 405 410');
/*!40000 ALTER TABLE `locale` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `priv_settings`
--

DROP TABLE IF EXISTS `priv_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `priv_settings` (
  `priv_type` enum('PLAYER','GUILD','EMPIRE') NOT NULL DEFAULT 'EMPIRE' COMMENT 'GUILD and PLAYER are untested.',
  `id` int(10) unsigned NOT NULL DEFAULT 0 COMMENT 'this is for empire_id, player_id or guild_id',
  `type` int(10) unsigned NOT NULL DEFAULT 4 COMMENT '1:item_drop, 2:gold_drop, 3:gold10_drop, 4:exp (1~4)',
  `value` int(11) NOT NULL DEFAULT 0 COMMENT '0~1000%',
  `duration` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`priv_type`,`id`,`type`) USING BTREE
) ENGINE=Aria DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci PAGE_CHECKSUM=1 ROW_FORMAT=FIXED;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `priv_settings`
--

LOCK TABLES `priv_settings` WRITE;
/*!40000 ALTER TABLE `priv_settings` DISABLE KEYS */;
/*!40000 ALTER TABLE `priv_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spam_db`
--

DROP TABLE IF EXISTS `spam_db`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `spam_db` (
  `word` varchar(255) NOT NULL,
  `score` int(11) NOT NULL DEFAULT 1,
  `type` enum('SPAM','MAPS') NOT NULL DEFAULT 'SPAM',
  PRIMARY KEY (`word`) USING BTREE
) ENGINE=Aria DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci PAGE_CHECKSUM=1 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spam_db`
--

LOCK TABLES `spam_db` WRITE;
/*!40000 ALTER TABLE `spam_db` DISABLE KEYS */;
/*!40000 ALTER TABLE `spam_db` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `veri_durum`
--

DROP TABLE IF EXISTS `veri_durum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `veri_durum` (
  `tablo` varchar(64) NOT NULL,
  `ozet` char(64) NOT NULL,
  `guncellendi` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`tablo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `veri_durum`
--

LOCK TABLES `veri_durum` WRITE;
/*!40000 ALTER TABLE `veri_durum` DISABLE KEYS */;
INSERT INTO `veri_durum` VALUES
('item_proto','f80ec5f6eede12fd8f50ca0543fca7b6b1cdaae70a25767764254da247567be9','2026-10-08 20:01:31'),
('mob_proto','f60f1c2aa3e45e2a200c95fb105ec193f8cf2615e399b63d887a5eae2bd5e26e','2026-10-08 20:01:31'),
('refine_proto','28c9a0906e6be72c2a655df9b5aebb0cb3948c0147d30a4fcaa8f8e5b9a0fc79','2026-10-08 20:01:31'),
('shop','843d8f894acc6a592a75c1c451bddf32abd2b3fc5da1b31cf6b94d23edf84937','2026-10-08 20:01:31'),
('shop_item','fe000c6699af393fb64d4f935de8e0e03de772dd21b4b5f40c6c1c7db5992da0','2026-10-08 20:01:32');
/*!40000 ALTER TABLE `veri_durum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vouchers`
--

DROP TABLE IF EXISTS `vouchers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `vouchers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(20) NOT NULL,
  `max_use_count` int(11) unsigned NOT NULL DEFAULT 1,
  `use_count` int(11) unsigned NOT NULL DEFAULT 0,
  `cash` int(11) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vouchers`
--

LOCK TABLES `vouchers` WRITE;
/*!40000 ALTER TABLE `vouchers` DISABLE KEYS */;
/*!40000 ALTER TABLE `vouchers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'common'
--

--
-- Dumping routines for database 'common'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-10-11 22:43:19
