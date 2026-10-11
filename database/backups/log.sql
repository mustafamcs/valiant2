/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.4.8-MariaDB, for Win64 (AMD64)
--
-- Host: 127.0.0.1    Database: log
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
-- Table structure for table `bootlog`
--

DROP TABLE IF EXISTS `bootlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `bootlog` (
  `time` datetime NOT NULL,
  `hostname` varchar(128) NOT NULL DEFAULT '',
  `channel` tinyint(3) unsigned NOT NULL DEFAULT 0,
  KEY `time` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bootlog`
--

LOCK TABLES `bootlog` WRITE;
/*!40000 ALTER TABLE `bootlog` DISABLE KEYS */;
INSERT INTO `bootlog` VALUES
('2026-10-08 20:01:41','channel1',1),
('2026-10-08 20:01:41','channel99',99),
('2026-10-08 21:39:13','channel1',1),
('2026-10-08 21:39:13','channel99',99),
('2026-10-08 21:41:02','channel1',1),
('2026-10-08 21:41:03','channel99',99),
('2026-10-08 21:42:53','channel1',1),
('2026-10-08 21:42:53','channel99',99),
('2026-10-08 22:56:37','channel1',1),
('2026-10-08 22:56:37','channel99',99),
('2026-10-08 23:05:22','channel1',1),
('2026-10-08 23:05:22','channel99',99),
('2026-10-08 23:10:06','channel1',1),
('2026-10-08 23:10:06','channel99',99),
('2026-10-08 23:16:17','channel1',1),
('2026-10-08 23:16:17','channel99',99),
('2026-10-08 23:22:03','channel1',1),
('2026-10-08 23:22:03','channel99',99),
('2026-10-08 23:26:16','channel1',1),
('2026-10-08 23:26:16','channel99',99),
('2026-10-08 23:33:00','channel1',1),
('2026-10-08 23:33:00','channel99',99),
('2026-10-08 23:42:34','channel1',1),
('2026-10-08 23:42:34','channel99',99),
('2026-10-08 23:43:14','channel1',1),
('2026-10-08 23:43:14','channel99',99),
('2026-10-08 23:48:01','channel1',1),
('2026-10-08 23:48:01','channel99',99),
('2026-10-08 23:54:50','channel1',1),
('2026-10-08 23:54:50','channel99',99),
('2026-10-09 00:03:11','channel1',1),
('2026-10-09 00:03:11','channel99',99),
('2026-10-09 00:10:18','channel1',1),
('2026-10-09 00:10:18','channel99',99),
('2026-10-09 00:15:26','channel1',1),
('2026-10-09 00:15:26','channel99',99),
('2026-10-09 00:18:41','channel1',1),
('2026-10-09 00:18:41','channel99',99),
('2026-10-09 00:25:01','channel1',1),
('2026-10-09 00:25:01','channel99',99),
('2026-10-09 00:26:36','channel1',1),
('2026-10-09 00:26:36','channel99',99),
('2026-10-09 00:32:23','channel1',1),
('2026-10-09 00:32:23','channel99',99),
('2026-10-09 00:36:59','channel1',1),
('2026-10-09 00:36:59','channel99',99),
('2026-10-09 00:40:25','channel1',1),
('2026-10-09 00:40:25','channel99',99),
('2026-10-09 00:43:45','channel1',1),
('2026-10-09 00:43:45','channel99',99),
('2026-10-09 01:32:55','channel1',1),
('2026-10-09 01:32:55','channel99',99),
('2026-10-09 01:36:32','channel1',1),
('2026-10-09 01:36:32','channel99',99),
('2026-10-09 01:42:44','channel1',1),
('2026-10-09 01:42:44','channel99',99),
('2026-10-09 01:47:34','channel1',1),
('2026-10-09 01:47:34','channel99',99),
('2026-10-09 01:56:20','channel1',1),
('2026-10-09 01:56:20','channel99',99),
('2026-10-09 07:34:12','channel1',1),
('2026-10-09 07:34:12','channel99',99),
('2026-10-09 07:38:53','channel1',1),
('2026-10-09 07:38:53','channel99',99),
('2026-10-09 07:41:25','channel1',1),
('2026-10-09 07:41:25','channel99',99),
('2026-10-09 07:44:45','channel1',1),
('2026-10-09 07:44:45','channel99',99),
('2026-10-09 07:49:34','channel1',1),
('2026-10-09 07:49:34','channel99',99),
('2026-10-09 08:23:08','channel1',1),
('2026-10-09 08:23:08','channel99',99),
('2026-10-09 08:42:31','channel1',1),
('2026-10-09 08:42:31','channel99',99),
('2026-10-09 08:52:42','channel1',1),
('2026-10-09 08:52:42','channel99',99),
('2026-10-09 08:57:10','channel1',1),
('2026-10-09 08:57:10','channel99',99),
('2026-10-09 09:14:16','channel1',1),
('2026-10-09 09:14:16','channel99',99),
('2026-10-09 10:26:26','channel1',1),
('2026-10-09 10:26:26','channel99',99),
('2026-10-09 10:27:36','channel1',1),
('2026-10-09 10:27:36','channel99',99),
('2026-10-09 11:06:42','channel1',1),
('2026-10-09 11:06:42','channel99',99),
('2026-10-09 11:08:55','channel1',1),
('2026-10-09 11:08:55','channel99',99),
('2026-10-09 11:13:08','channel1',1),
('2026-10-09 11:13:08','channel99',99);
/*!40000 ALTER TABLE `bootlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bot_guard_log`
--

DROP TABLE IF EXISTS `bot_guard_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `bot_guard_log` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `zaman` datetime NOT NULL,
  `kanal` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `hesap_id` int(10) unsigned NOT NULL DEFAULT 0,
  `hesap` varchar(30) NOT NULL DEFAULT '',
  `pid` int(10) unsigned NOT NULL DEFAULT 0,
  `isim` varchar(64) NOT NULL DEFAULT '',
  `olay` varchar(24) NOT NULL DEFAULT '',
  `kip` varchar(8) NOT NULL DEFAULT '',
  `puan` int(11) NOT NULL DEFAULT 0,
  `dongu` int(11) NOT NULL DEFAULT 0,
  `zamanlama` int(11) NOT NULL DEFAULT 0,
  `oturum` int(11) NOT NULL DEFAULT 0,
  `hiz` int(11) NOT NULL DEFAULT 0,
  `ayrinti` varchar(128) NOT NULL DEFAULT '',
  `incelendi` tinyint(3) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `zaman` (`zaman`),
  KEY `pid` (`pid`),
  KEY `olay` (`olay`)
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bot_guard_log`
--

LOCK TABLES `bot_guard_log` WRITE;
/*!40000 ALTER TABLE `bot_guard_log` DISABLE KEYS */;
INSERT INTO `bot_guard_log` VALUES
(1,'2026-10-08 20:11:41',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(2,'2026-10-08 20:11:41',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(3,'2026-10-08 20:21:41',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(4,'2026-10-08 20:21:41',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(5,'2026-10-08 20:31:42',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(6,'2026-10-08 20:31:42',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(7,'2026-10-08 20:41:42',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(8,'2026-10-08 20:41:43',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(9,'2026-10-08 21:52:53',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(10,'2026-10-08 21:52:54',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(11,'2026-10-08 22:02:54',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(12,'2026-10-08 22:02:54',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(13,'2026-10-08 22:12:54',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(14,'2026-10-08 22:12:55',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(15,'2026-10-08 22:22:54',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(16,'2026-10-08 22:22:55',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(17,'2026-10-08 22:32:55',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(18,'2026-10-08 22:32:56',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(19,'2026-10-08 22:42:55',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(20,'2026-10-08 22:42:56',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(21,'2026-10-08 22:52:55',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(22,'2026-10-08 22:52:57',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(23,'2026-10-09 00:53:45',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(24,'2026-10-09 00:53:45',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(25,'2026-10-09 01:03:46',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(26,'2026-10-09 01:03:46',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(27,'2026-10-09 01:13:46',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(28,'2026-10-09 01:13:47',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(29,'2026-10-09 01:23:47',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(30,'2026-10-09 01:23:47',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(31,'2026-10-09 07:59:33',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(32,'2026-10-09 07:59:34',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(33,'2026-10-09 08:09:34',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(34,'2026-10-09 08:09:34',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(35,'2026-10-09 08:19:34',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(36,'2026-10-09 08:19:35',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(37,'2026-10-09 08:33:08',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(38,'2026-10-09 08:33:08',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(39,'2026-10-09 09:07:09',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(40,'2026-10-09 09:07:10',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(41,'2026-10-09 09:24:16',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(42,'2026-10-09 09:24:17',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(43,'2026-10-09 09:34:17',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(44,'2026-10-09 09:34:17',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(45,'2026-10-09 09:44:18',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(46,'2026-10-09 09:44:18',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(47,'2026-10-09 09:54:18',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(48,'2026-10-09 09:54:19',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(49,'2026-10-09 10:04:19',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(50,'2026-10-09 10:04:19',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(51,'2026-10-09 10:14:19',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(52,'2026-10-09 10:14:20',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(53,'2026-10-09 10:24:20',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(54,'2026-10-09 10:24:21',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(55,'2026-10-09 10:37:36',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(56,'2026-10-09 10:37:36',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(57,'2026-10-09 10:47:36',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(58,'2026-10-09 10:47:37',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(59,'2026-10-09 10:57:36',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(60,'2026-10-09 10:57:38',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(61,'2026-10-09 11:23:08',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(62,'2026-10-09 11:23:09',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(63,'2026-10-09 11:33:09',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(64,'2026-10-09 11:33:09',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(65,'2026-10-09 11:43:09',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(66,'2026-10-09 11:43:09',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(67,'2026-10-09 11:53:10',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(68,'2026-10-09 11:53:10',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(69,'2026-10-09 12:03:11',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(70,'2026-10-09 12:03:11',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(71,'2026-10-09 12:13:11',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(72,'2026-10-09 12:13:11',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(73,'2026-10-09 12:23:12',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(74,'2026-10-09 12:23:12',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(75,'2026-10-09 12:33:12',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(76,'2026-10-09 12:33:13',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(77,'2026-10-09 12:43:13',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(78,'2026-10-09 12:43:13',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(79,'2026-10-09 12:53:13',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(80,'2026-10-09 12:53:14',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(81,'2026-10-09 13:03:14',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(82,'2026-10-09 13:03:15',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(83,'2026-10-09 13:13:14',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(84,'2026-10-09 13:13:16',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(85,'2026-10-09 13:23:15',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(86,'2026-10-09 13:23:16',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(87,'2026-10-09 13:33:15',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(88,'2026-10-09 13:33:17',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(89,'2026-10-09 13:43:16',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(90,'2026-10-09 13:43:18',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(91,'2026-10-09 13:53:16',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(92,'2026-10-09 13:53:18',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(93,'2026-10-09 14:03:17',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(94,'2026-10-09 14:03:19',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(95,'2026-10-09 14:13:17',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(96,'2026-10-09 14:13:20',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(97,'2026-10-09 14:23:18',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(98,'2026-10-09 14:23:20',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(99,'2026-10-09 14:33:18',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(100,'2026-10-09 14:33:21',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(101,'2026-10-09 14:43:19',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(102,'2026-10-09 14:43:22',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(103,'2026-10-09 14:53:19',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(104,'2026-10-09 14:53:23',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(105,'2026-10-09 15:03:20',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(106,'2026-10-09 15:03:23',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(107,'2026-10-09 15:13:20',99,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0),
(108,'2026-10-09 15:13:24',1,0,'',0,'','OZET','izleme',0,0,0,0,0,'oyuncu=0 yari_esik=0 esikte=0 esik=100 muaf=0',0);
/*!40000 ALTER TABLE `bot_guard_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bright_protect_log`
--

DROP TABLE IF EXISTS `bright_protect_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `bright_protect_log` (
  `date` datetime DEFAULT NULL,
  `login` varchar(32) DEFAULT NULL,
  `name` varchar(32) DEFAULT NULL,
  `IP` mediumtext DEFAULT NULL,
  `cheat` varchar(22) DEFAULT NULL,
  `value` int(9) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bright_protect_log`
--

LOCK TABLES `bright_protect_log` WRITE;
/*!40000 ALTER TABLE `bright_protect_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `bright_protect_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bug_report`
--

DROP TABLE IF EXISTS `bug_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `bug_report` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL DEFAULT current_timestamp(),
  `source` enum('OYUN','KARARGAH') NOT NULL DEFAULT 'OYUN',
  `category` varchar(16) NOT NULL DEFAULT 'DIGER',
  `status` enum('YENI','INCELENIYOR','COZULDU','GECERSIZ') NOT NULL DEFAULT 'YENI',
  `account_id` int(10) unsigned NOT NULL DEFAULT 0,
  `login` varchar(30) NOT NULL DEFAULT '',
  `pid` int(10) unsigned NOT NULL DEFAULT 0,
  `player_name` varchar(24) NOT NULL DEFAULT '',
  `level` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `channel` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `map_index` int(11) NOT NULL DEFAULT 0,
  `x` int(11) NOT NULL DEFAULT 0,
  `y` int(11) NOT NULL DEFAULT 0,
  `client_version` varchar(32) NOT NULL DEFAULT '',
  `description` varchar(512) NOT NULL DEFAULT '',
  `note` varchar(255) NOT NULL DEFAULT '',
  `updated` datetime DEFAULT NULL,
  `reward_type` enum('','CASH','ITEM') NOT NULL DEFAULT '',
  `reward_value` int(10) unsigned NOT NULL DEFAULT 0,
  `reward_count` int(10) unsigned NOT NULL DEFAULT 0,
  `reward_time` datetime DEFAULT NULL,
  `reward_by` varchar(32) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `status` (`status`),
  KEY `account_id` (`account_id`),
  KEY `created` (`created`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bug_report`
--

LOCK TABLES `bug_report` WRITE;
/*!40000 ALTER TABLE `bug_report` DISABLE KEYS */;
/*!40000 ALTER TABLE `bug_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cash_reward_log`
--

DROP TABLE IF EXISTS `cash_reward_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `cash_reward_log` (
  `time` datetime DEFAULT NULL,
  `account_id` int(10) unsigned NOT NULL DEFAULT 0,
  `pid` int(10) unsigned NOT NULL DEFAULT 0,
  `source` varchar(16) NOT NULL DEFAULT '',
  `requested` int(11) NOT NULL DEFAULT 0,
  `granted` int(11) NOT NULL DEFAULT 0,
  `detail` varchar(64) NOT NULL DEFAULT '',
  KEY `account_id` (`account_id`),
  KEY `pid` (`pid`),
  KEY `time` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cash_reward_log`
--

LOCK TABLES `cash_reward_log` WRITE;
/*!40000 ALTER TABLE `cash_reward_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `cash_reward_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `change_name`
--

DROP TABLE IF EXISTS `change_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `change_name` (
  `pid` int(20) NOT NULL DEFAULT 0,
  `old_name` varchar(30) DEFAULT NULL,
  `new_name` varchar(30) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `ip` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`pid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `change_name`
--

LOCK TABLES `change_name` WRITE;
/*!40000 ALTER TABLE `change_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `change_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `change_name_history`
--

DROP TABLE IF EXISTS `change_name_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `change_name_history` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `pid` int(10) unsigned NOT NULL DEFAULT 0,
  `old_name` varchar(24) NOT NULL DEFAULT '',
  `new_name` varchar(24) NOT NULL DEFAULT '',
  `time` datetime NOT NULL,
  `ip` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `pid` (`pid`),
  KEY `time` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `change_name_history`
--

LOCK TABLES `change_name_history` WRITE;
/*!40000 ALTER TABLE `change_name_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `change_name_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_log`
--

DROP TABLE IF EXISTS `chat_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_log` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `when` datetime NOT NULL,
  `channel` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `where` int(10) unsigned NOT NULL DEFAULT 0,
  `type` enum('NORMAL','WHISPER','PARTY','GUILD','SHOUT','TRADE','KARARGAH','DUYURU') NOT NULL,
  `who_id` int(10) unsigned NOT NULL DEFAULT 0,
  `who_name` varbinary(24) NOT NULL DEFAULT '',
  `whom_id` int(10) unsigned NOT NULL DEFAULT 0,
  `whom_name` varbinary(24) NOT NULL DEFAULT '',
  `msg` varbinary(512) NOT NULL DEFAULT '',
  `ip` varchar(45) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`,`when`),
  KEY `who_when` (`who_id`,`when`),
  KEY `whom_name_when` (`whom_name`,`when`),
  KEY `when_type` (`when`,`type`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
 PARTITION BY RANGE (to_days(`when`))
(PARTITION `p_eski` VALUES LESS THAN (740260) ENGINE = InnoDB,
 PARTITION `p20261008` VALUES LESS THAN (740263) ENGINE = InnoDB,
 PARTITION `p20261009` VALUES LESS THAN (740264) ENGINE = InnoDB,
 PARTITION `p20261010` VALUES LESS THAN (740265) ENGINE = InnoDB,
 PARTITION `p20261011` VALUES LESS THAN (740266) ENGINE = InnoDB,
 PARTITION `p20261012` VALUES LESS THAN (740267) ENGINE = InnoDB,
 PARTITION `p20261013` VALUES LESS THAN (740268) ENGINE = InnoDB,
 PARTITION `p20261014` VALUES LESS THAN (740269) ENGINE = InnoDB,
 PARTITION `p20261015` VALUES LESS THAN (740270) ENGINE = InnoDB,
 PARTITION `p20261016` VALUES LESS THAN (740271) ENGINE = InnoDB,
 PARTITION `pmax` VALUES LESS THAN MAXVALUE ENGINE = InnoDB);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_log`
--

LOCK TABLES `chat_log` WRITE;
/*!40000 ALTER TABLE `chat_log` DISABLE KEYS */;
INSERT INTO `chat_log` VALUES
(1,'2026-10-09 00:37:52',1,41,'NORMAL',5,'MCS',0,'','s','127.0.0.1');
/*!40000 ALTER TABLE `chat_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `command_log`
--

DROP TABLE IF EXISTS `command_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `command_log` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `userid` int(11) unsigned NOT NULL DEFAULT 0,
  `server` int(11) NOT NULL DEFAULT 0,
  `ip` varchar(15) NOT NULL DEFAULT '',
  `port` int(11) NOT NULL DEFAULT 0,
  `username` varbinary(64) NOT NULL DEFAULT '',
  `command` varbinary(1024) NOT NULL DEFAULT '',
  `date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  KEY `userid` (`userid`),
  KEY `date` (`date`)
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `command_log`
--

LOCK TABLES `command_log` WRITE;
/*!40000 ALTER TABLE `command_log` DISABLE KEYS */;
INSERT INTO `command_log` VALUES
(1,5,999,'127.0.0.1',1,'MCS','m 8001','2026-10-08 23:16:51'),
(2,5,999,'127.0.0.1',1,'MCS','i 19','2026-10-08 23:17:07'),
(3,5,999,'127.0.0.1',1,'MCS','mk 8001','2026-10-08 23:18:48'),
(4,5,999,'127.0.0.1',1,'MCS','mk 8001 12','2026-10-08 23:19:00'),
(5,5,999,'127.0.0.1',1,'MCS','mk 8001 122','2026-10-08 23:19:05'),
(6,5,999,'127.0.0.1',1,'MCS','mk 8001 122','2026-10-08 23:19:19'),
(7,5,999,'127.0.0.1',1,'MCS','mk 8001 122','2026-10-08 23:19:28'),
(8,5,999,'127.0.0.1',1,'MCS','mk 8001 122','2026-10-08 23:19:29'),
(9,5,999,'127.0.0.1',1,'MCS','mk 8001 122','2026-10-08 23:19:39'),
(10,5,999,'127.0.0.1',1,'MCS','i 19','2026-10-08 23:33:18'),
(11,5,999,'127.0.0.1',1,'MCS','m 8001 200','2026-10-08 23:44:29'),
(12,5,999,'127.0.0.1',1,'MCS','m 8001 200','2026-10-08 23:49:03'),
(13,5,999,'127.0.0.1',1,'MCS','m 8001 200','2026-10-08 23:55:08'),
(14,5,999,'127.0.0.1',1,'MCS','m 8001 200','2026-10-08 23:56:23'),
(15,5,999,'127.0.0.1',1,'MCS','m 8001 200','2026-10-08 23:56:27'),
(16,5,999,'127.0.0.1',1,'MCS','m 8001 200','2026-10-08 23:56:29'),
(17,5,999,'127.0.0.1',1,'MCS','m 8001 200','2026-10-08 23:56:30'),
(18,5,999,'127.0.0.1',1,'MCS','m 8001 200','2026-10-08 23:56:31'),
(19,5,999,'127.0.0.1',1,'MCS','m 8001 200','2026-10-08 23:56:31'),
(20,5,999,'127.0.0.1',1,'MCS','m 8001 200','2026-10-08 23:56:32'),
(21,5,999,'127.0.0.1',1,'MCS','m 8001 200','2026-10-08 23:56:33'),
(22,5,999,'127.0.0.1',1,'MCS','p','2026-10-08 23:57:08'),
(23,5,999,'127.0.0.1',1,'MCS','mk 8001 200','2026-10-08 23:57:26'),
(24,5,999,'127.0.0.1',1,'MCS','mk 8001 200','2026-10-08 23:57:29'),
(25,5,999,'127.0.0.1',1,'MCS','mk 8001 200','2026-10-08 23:57:30'),
(26,5,999,'127.0.0.1',1,'MCS','mk 8001 200','2026-10-08 23:57:31'),
(27,5,999,'127.0.0.1',1,'MCS','m 8001 200','2026-10-08 23:57:33'),
(28,5,999,'127.0.0.1',1,'MCS','p','2026-10-08 23:57:37'),
(29,5,999,'127.0.0.1',1,'MCS','m 8001 200','2026-10-09 00:03:36'),
(30,5,999,'127.0.0.1',1,'MCS','m 8001 200','2026-10-09 00:03:54'),
(31,5,999,'127.0.0.1',1,'MCS','m 8001 200','2026-10-09 00:04:01'),
(32,5,999,'127.0.0.1',1,'MCS','m 8001 200','2026-10-09 00:04:06'),
(33,5,999,'127.0.0.1',1,'MCS','p','2026-10-09 00:04:12'),
(34,5,999,'127.0.0.1',1,'MCS','m 8001 600','2026-10-09 00:04:24'),
(35,5,999,'127.0.0.1',1,'MCS','p','2026-10-09 00:05:39'),
(36,5,999,'127.0.0.1',1,'MCS','set mcs exp 123123123','2026-10-09 00:05:55'),
(37,5,999,'127.0.0.1',1,'MCS','setjob 1','2026-10-09 00:06:10'),
(38,5,999,'127.0.0.1',1,'MCS','all','2026-10-09 00:06:12'),
(39,5,999,'127.0.0.1',1,'MCS','r','2026-10-09 00:06:25'),
(40,5,999,'127.0.0.1',1,'MCS','m 8001 600','2026-10-09 00:10:47'),
(41,5,999,'127.0.0.1',1,'MCS','m 8001 600','2026-10-09 00:12:10'),
(42,5,999,'127.0.0.1',1,'MCS','m 8001 600','2026-10-09 00:12:13'),
(43,5,999,'127.0.0.1',1,'MCS','go 424 386','2026-10-09 00:12:21'),
(44,5,999,'127.0.0.1',1,'MCS','we','2026-10-09 00:13:09'),
(45,5,999,'127.0.0.1',1,'MCS','we','2026-10-09 00:13:17'),
(46,5,999,'127.0.0.1',1,'MCS','we','2026-10-09 00:13:21'),
(47,5,999,'127.0.0.1',1,'MCS','p','2026-10-09 00:13:29'),
(48,5,999,'127.0.0.1',1,'MCS','r','2026-10-09 00:13:43'),
(49,5,999,'127.0.0.1',1,'MCS','cannot_dead','2026-10-09 00:13:48'),
(50,5,999,'127.0.0.1',1,'MCS','we','2026-10-09 00:13:52'),
(51,5,999,'127.0.0.1',1,'MCS','M 8001 600','2026-10-09 00:15:37'),
(52,5,999,'127.0.0.1',1,'MCS','m 8001 600','2026-10-09 00:18:55'),
(53,5,999,'127.0.0.1',1,'MCS','m 8001 600','2026-10-09 00:26:53'),
(54,5,999,'127.0.0.1',1,'MCS','p','2026-10-09 00:28:53'),
(55,5,999,'127.0.0.1',1,'MCS','p','2026-10-09 00:28:56'),
(56,5,999,'127.0.0.1',1,'MCS','p','2026-10-09 00:28:59'),
(57,5,999,'127.0.0.1',1,'MCS','m 8001 600','2026-10-09 00:37:33'),
(58,5,999,'127.0.0.1',1,'MCS','m 8001 600','2026-10-09 00:37:50'),
(59,5,999,'127.0.0.1',1,'MCS','m','2026-10-09 00:38:09'),
(60,5,999,'127.0.0.1',1,'MCS','m 8001','2026-10-09 00:38:14'),
(61,5,999,'127.0.0.1',1,'MCS','m 8001 12','2026-10-09 00:38:24'),
(62,5,999,'127.0.0.1',1,'MCS','m 101','2026-10-09 00:38:30'),
(63,5,999,'127.0.0.1',1,'MCS','m 8001 9000','2026-10-09 00:39:03'),
(64,5,999,'127.0.0.1',1,'MCS','p all','2026-10-09 00:39:34'),
(65,5,999,'127.0.0.1',1,'MCS','m 8001 200','2026-10-09 00:40:36'),
(66,5,999,'127.0.0.1',1,'MCS','go 440 239','2026-10-09 00:41:04'),
(67,5,999,'127.0.0.1',1,'MCS','p all','2026-10-09 00:41:55'),
(68,5,999,'127.0.0.1',1,'MCS','m 8001 200','2026-10-09 00:42:03'),
(69,5,999,'127.0.0.1',1,'MCS','p','2026-10-09 00:42:17'),
(70,5,999,'127.0.0.1',1,'MCS','we','2026-10-09 00:42:40'),
(71,5,999,'127.0.0.1',1,'MCS','m 8001 600','2026-10-09 00:44:01'),
(72,5,999,'127.0.0.1',1,'MCS','cannot_dead','2026-10-09 01:37:16'),
(73,5,999,'127.0.0.1',1,'MCS','m 8001 200','2026-10-09 01:38:27'),
(74,5,999,'127.0.0.1',1,'MCS','go 492 350','2026-10-09 01:38:43'),
(75,5,999,'127.0.0.1',1,'MCS','go 428 342','2026-10-09 01:38:45'),
(76,5,999,'127.0.0.1',1,'MCS','m 8001 600','2026-10-09 01:44:48'),
(77,5,999,'127.0.0.1',1,'MCS','go 388 366','2026-10-09 01:45:02'),
(78,5,999,'127.0.0.1',1,'MCS','go 572 968','2026-10-09 01:48:23'),
(79,5,999,'127.0.0.1',1,'MCS','go 656 1064','2026-10-09 01:48:24'),
(80,5,999,'127.0.0.1',1,'MCS','go 708 1204','2026-10-09 01:48:25'),
(81,5,999,'127.0.0.1',1,'MCS','go 752 1168','2026-10-09 01:48:25'),
(82,5,999,'127.0.0.1',1,'MCS','go 392 653','2026-10-09 01:48:36'),
(83,5,999,'127.0.0.1',1,'MCS','go 764 805','2026-10-09 01:48:45'),
(84,5,999,'127.0.0.1',1,'MCS','m 8001 600','2026-10-09 01:50:09'),
(85,5,999,'127.0.0.1',1,'MCS','p all','2026-10-09 01:50:40'),
(86,5,999,'127.0.0.1',1,'MCS','m 8001 600','2026-10-09 01:57:02'),
(87,5,999,'127.0.0.1',1,'MCS','go 592 881','2026-10-09 01:57:27'),
(88,5,999,'127.0.0.1',1,'MCS','go 752 941','2026-10-09 01:57:33'),
(89,5,999,'127.0.0.1',1,'MCS','go 720 901','2026-10-09 01:57:38'),
(90,5,999,'127.0.0.1',1,'MCS','go 716 877','2026-10-09 01:58:02'),
(91,5,999,'127.0.0.1',1,'MCS','go 692 825','2026-10-09 01:58:03'),
(92,5,999,'127.0.0.1',1,'MCS','we','2026-10-09 01:58:16'),
(93,5,999,'127.0.0.1',1,'MCS','go 676 905','2026-10-09 01:58:40'),
(94,5,999,'127.0.0.1',1,'MCS','n 8001 ','2026-10-09 07:35:13'),
(95,5,999,'127.0.0.1',1,'MCS','m 8001','2026-10-09 07:35:18'),
(96,5,999,'127.0.0.1',1,'MCS','m 8001 600','2026-10-09 08:15:16'),
(97,5,999,'127.0.0.1',1,'MCS','m 8001 600','2026-10-09 08:35:32'),
(98,5,999,'127.0.0.1',1,'MCS','m 8001 600','2026-10-09 08:46:38'),
(99,5,999,'127.0.0.1',1,'MCS','m 8001 600','2026-10-09 09:09:13'),
(100,5,999,'127.0.0.1',1,'MCS','m 8001 600','2026-10-09 10:11:57'),
(101,5,999,'127.0.0.1',1,'MCS','m 8001 600','2026-10-09 11:00:36'),
(102,5,999,'127.0.0.1',1,'MCS','p','2026-10-09 11:02:03'),
(103,5,999,'127.0.0.1',1,'MCS','m 8001 600','2026-10-09 11:06:57'),
(104,5,999,'127.0.0.1',1,'MCS','m 8001 600','2026-10-09 11:10:26');
/*!40000 ALTER TABLE `command_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cube`
--

DROP TABLE IF EXISTS `cube`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `cube` (
  `pid` int(10) unsigned NOT NULL DEFAULT 0,
  `time` datetime NOT NULL,
  `x` int(10) unsigned NOT NULL DEFAULT 0,
  `y` int(10) unsigned NOT NULL DEFAULT 0,
  `item_vnum` int(10) unsigned NOT NULL DEFAULT 0,
  `item_uid` int(10) unsigned NOT NULL DEFAULT 0,
  `item_count` int(11) NOT NULL DEFAULT 0,
  `success` tinyint(1) NOT NULL DEFAULT 0,
  KEY `time` (`time`),
  KEY `pid` (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cube`
--

LOCK TABLES `cube` WRITE;
/*!40000 ALTER TABLE `cube` DISABLE KEYS */;
/*!40000 ALTER TABLE `cube` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dragon_slay_log`
--

DROP TABLE IF EXISTS `dragon_slay_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `dragon_slay_log` (
  `guild_id` int(11) NOT NULL DEFAULT 0,
  `vnum` int(11) NOT NULL DEFAULT 0,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  KEY `start_time` (`start_time`),
  KEY `guild_id` (`guild_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dragon_slay_log`
--

LOCK TABLES `dragon_slay_log` WRITE;
/*!40000 ALTER TABLE `dragon_slay_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `dragon_slay_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `economy_metric`
--

DROP TABLE IF EXISTS `economy_metric`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `economy_metric` (
  `time` datetime NOT NULL,
  `channel` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `port` smallint(5) unsigned NOT NULL DEFAULT 0,
  `kind` varchar(24) NOT NULL DEFAULT '',
  `direction` enum('IN','OUT','TRANSFER') NOT NULL DEFAULT 'IN',
  `count` int(10) unsigned NOT NULL DEFAULT 0,
  `amount` bigint(20) NOT NULL DEFAULT 0,
  KEY `time` (`time`),
  KEY `kind_time` (`kind`,`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `economy_metric`
--

LOCK TABLES `economy_metric` WRITE;
/*!40000 ALTER TABLE `economy_metric` DISABLE KEYS */;
INSERT INTO `economy_metric` VALUES
('2026-10-08 23:19:39',1,28000,'canavar','IN',1879,65417),
('2026-10-08 23:34:25',1,28000,'canavar','IN',1,26),
('2026-10-08 23:48:29',1,28000,'canavar','IN',1,21),
('2026-10-08 23:58:10',1,28000,'canavar','IN',2399,83903);
/*!40000 ALTER TABLE `economy_metric` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchange_log`
--

DROP TABLE IF EXISTS `exchange_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `exchange_log` (
  `type` varchar(20) NOT NULL DEFAULT '',
  `time` datetime NOT NULL,
  `pid` int(11) NOT NULL DEFAULT 0,
  `target_pid` int(11) NOT NULL DEFAULT 0,
  `item_id` int(11) NOT NULL DEFAULT 0,
  `vnum` int(11) NOT NULL DEFAULT 0,
  `count` bigint(20) NOT NULL DEFAULT 0,
  `hint` varchar(32) NOT NULL DEFAULT '',
  KEY `time` (`time`),
  KEY `pid` (`pid`),
  KEY `target_pid` (`target_pid`),
  KEY `item_id` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchange_log`
--

LOCK TABLES `exchange_log` WRITE;
/*!40000 ALTER TABLE `exchange_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `exchange_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fish_log`
--

DROP TABLE IF EXISTS `fish_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `fish_log` (
  `time` datetime NOT NULL,
  `pid` int(11) NOT NULL DEFAULT 0,
  `item_vnum` int(11) NOT NULL DEFAULT 0,
  `count` int(11) NOT NULL DEFAULT 0,
  `rod_level` int(11) NOT NULL DEFAULT 0,
  `bait_vnum` int(11) NOT NULL DEFAULT 0,
  KEY `time` (`time`),
  KEY `pid` (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fish_log`
--

LOCK TABLES `fish_log` WRITE;
/*!40000 ALTER TABLE `fish_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `fish_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gold_session_log`
--

DROP TABLE IF EXISTS `gold_session_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `gold_session_log` (
  `pid` int(11) NOT NULL DEFAULT 0,
  `gold` bigint(20) NOT NULL DEFAULT 0,
  `time` datetime NOT NULL,
  `duration` int(11) NOT NULL DEFAULT 0,
  KEY `time` (`time`),
  KEY `pid` (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gold_session_log`
--

LOCK TABLES `gold_session_log` WRITE;
/*!40000 ALTER TABLE `gold_session_log` DISABLE KEYS */;
INSERT INTO `gold_session_log` VALUES
(5,65417,'2026-10-08 23:20:48',264),
(5,83903,'2026-10-09 00:01:07',372);
/*!40000 ALTER TABLE `gold_session_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `goldlog`
--

DROP TABLE IF EXISTS `goldlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `goldlog` (
  `date` date NOT NULL,
  `time` time NOT NULL,
  `pid` int(10) unsigned NOT NULL DEFAULT 0,
  `what` int(10) unsigned NOT NULL DEFAULT 0,
  `how` varchar(16) NOT NULL DEFAULT '',
  `hint` varchar(255) NOT NULL DEFAULT '',
  KEY `date` (`date`),
  KEY `pid` (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goldlog`
--

LOCK TABLES `goldlog` WRITE;
/*!40000 ALTER TABLE `goldlog` DISABLE KEYS */;
/*!40000 ALTER TABLE `goldlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `guild_safebox_log`
--

DROP TABLE IF EXISTS `guild_safebox_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `guild_safebox_log` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  `guild_id` int(10) unsigned NOT NULL DEFAULT 0,
  `pid` int(10) unsigned NOT NULL DEFAULT 0,
  `name` varchar(24) NOT NULL DEFAULT '',
  `action` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `item_id` int(10) unsigned NOT NULL DEFAULT 0,
  `vnum` int(10) unsigned NOT NULL DEFAULT 0,
  `count` int(10) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `guild_id` (`guild_id`,`id`),
  KEY `item_id` (`item_id`),
  KEY `pid` (`pid`),
  KEY `time` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guild_safebox_log`
--

LOCK TABLES `guild_safebox_log` WRITE;
/*!40000 ALTER TABLE `guild_safebox_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `guild_safebox_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hack_log`
--

DROP TABLE IF EXISTS `hack_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `hack_log` (
  `time` datetime DEFAULT NULL,
  `name` varbinary(16) DEFAULT NULL,
  `server` varbinary(56) DEFAULT NULL,
  `why` varbinary(300) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hack_log`
--

LOCK TABLES `hack_log` WRITE;
/*!40000 ALTER TABLE `hack_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `hack_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hesap_olay`
--

DROP TABLE IF EXISTS `hesap_olay`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `hesap_olay` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `zaman` datetime NOT NULL DEFAULT current_timestamp(),
  `islem` varchar(16) NOT NULL,
  `sonuc` varchar(24) NOT NULL DEFAULT '',
  `login` varchar(16) NOT NULL DEFAULT '',
  `hesap_id` int(11) unsigned DEFAULT NULL,
  `ip` varchar(15) NOT NULL DEFAULT '',
  `kim` varchar(32) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `zaman` (`zaman`),
  KEY `ip_zaman` (`ip`,`zaman`),
  KEY `login` (`login`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hesap_olay`
--

LOCK TABLES `hesap_olay` WRITE;
/*!40000 ALTER TABLE `hesap_olay` DISABLE KEYS */;
/*!40000 ALTER TABLE `hesap_olay` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ikarusshop_log`
--

DROP TABLE IF EXISTS `ikarusshop_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ikarusshop_log` (
  `who` int(10) unsigned NOT NULL DEFAULT 0,
  `itemid` int(10) unsigned NOT NULL DEFAULT 0,
  `what` varchar(64) NOT NULL DEFAULT '',
  `shop_owner` int(10) unsigned NOT NULL DEFAULT 0,
  `extra` varchar(255) NOT NULL DEFAULT '',
  `vnum` int(10) unsigned NOT NULL DEFAULT 0,
  `count` int(10) unsigned NOT NULL DEFAULT 0,
  `yang` bigint(20) NOT NULL DEFAULT 0,
  `date` datetime NOT NULL DEFAULT current_timestamp(),
  KEY `date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ikarusshop_log`
--

LOCK TABLES `ikarusshop_log` WRITE;
/*!40000 ALTER TABLE `ikarusshop_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `ikarusshop_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item_iade`
--

DROP TABLE IF EXISTS `item_iade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `item_iade` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `zaman` datetime NOT NULL DEFAULT current_timestamp(),
  `log_id` bigint(20) unsigned NOT NULL,
  `log_zaman` datetime DEFAULT NULL,
  `log_islem` varchar(50) NOT NULL DEFAULT '',
  `pid` int(11) unsigned NOT NULL DEFAULT 0,
  `oyuncu` varchar(24) NOT NULL DEFAULT '',
  `hesap` varchar(16) NOT NULL DEFAULT '',
  `item_id` bigint(20) unsigned NOT NULL DEFAULT 0,
  `vnum` int(11) unsigned NOT NULL DEFAULT 0,
  `adet` int(11) unsigned NOT NULL DEFAULT 1,
  `soketler` varchar(64) NOT NULL DEFAULT '',
  `efsunlar` varchar(128) NOT NULL DEFAULT '',
  `award_id` int(11) unsigned DEFAULT NULL,
  `kim` varchar(32) NOT NULL DEFAULT '',
  `neden` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `log_id` (`log_id`),
  KEY `pid` (`pid`),
  KEY `hesap` (`hesap`),
  KEY `zaman` (`zaman`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item_iade`
--

LOCK TABLES `item_iade` WRITE;
/*!40000 ALTER TABLE `item_iade` DISABLE KEYS */;
/*!40000 ALTER TABLE `item_iade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item_meta_log`
--

DROP TABLE IF EXISTS `item_meta_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `item_meta_log` (
  `itemid` int(11) NOT NULL DEFAULT 0,
  `time` datetime NOT NULL,
  `who` int(11) NOT NULL DEFAULT 0,
  `what` varchar(32) NOT NULL DEFAULT '',
  `value` varchar(80) NOT NULL DEFAULT '',
  `vnum` int(11) NOT NULL DEFAULT 0,
  KEY `time` (`time`),
  KEY `itemid` (`itemid`),
  KEY `who` (`who`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item_meta_log`
--

LOCK TABLES `item_meta_log` WRITE;
/*!40000 ALTER TABLE `item_meta_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `item_meta_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item_metric`
--

DROP TABLE IF EXISTS `item_metric`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `item_metric` (
  `time` datetime NOT NULL,
  `channel` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `port` smallint(5) unsigned NOT NULL DEFAULT 0,
  `item_class` varchar(16) NOT NULL DEFAULT '',
  `direction` enum('IN','OUT') NOT NULL DEFAULT 'IN',
  `source` varchar(16) NOT NULL DEFAULT '',
  `events` int(10) unsigned NOT NULL DEFAULT 0,
  `quantity` bigint(20) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`time`,`channel`,`port`,`item_class`,`source`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item_metric`
--

LOCK TABLES `item_metric` WRITE;
/*!40000 ALTER TABLE `item_metric` DISABLE KEYS */;
INSERT INTO `item_metric` VALUES
('2026-10-08 23:00:00',1,28000,'kitap','IN','drop',353,353),
('2026-10-08 23:00:00',1,28000,'malzeme','IN','drop',71,355);
/*!40000 ALTER TABLE `item_metric` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item_sell_log`
--

DROP TABLE IF EXISTS `item_sell_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `item_sell_log` (
  `pid` int(10) NOT NULL DEFAULT 0,
  `sell_date` datetime NOT NULL,
  `log_type` varchar(64) NOT NULL DEFAULT '0',
  `vnum` int(11) NOT NULL DEFAULT 0,
  `count` int(11) NOT NULL DEFAULT 0,
  `socket0` int(11) NOT NULL DEFAULT 0,
  `socket1` int(11) NOT NULL DEFAULT 0,
  `socket2` int(11) NOT NULL DEFAULT 0,
  `socket3` int(11) NOT NULL DEFAULT 0,
  `socket4` int(11) NOT NULL DEFAULT 0,
  `socket5` int(11) NOT NULL DEFAULT 0,
  `attr0` int(11) NOT NULL DEFAULT 0,
  `attrval0` int(11) NOT NULL DEFAULT 0,
  `attr1` int(11) NOT NULL DEFAULT 0,
  `attrval1` int(11) NOT NULL DEFAULT 0,
  `attr2` int(11) NOT NULL DEFAULT 0,
  `attrval2` int(11) NOT NULL DEFAULT 0,
  `attr3` int(11) NOT NULL DEFAULT 0,
  `attrval3` int(11) NOT NULL DEFAULT 0,
  `attr4` int(11) NOT NULL DEFAULT 0,
  `attrval4` int(11) NOT NULL DEFAULT 0,
  `attr5` int(11) NOT NULL DEFAULT 0,
  `attrval5` int(11) NOT NULL DEFAULT 0,
  `attr6` int(11) NOT NULL DEFAULT 0,
  `attrval6` int(11) NOT NULL DEFAULT 0,
  `attr7` int(11) NOT NULL DEFAULT 0,
  `attrval7` int(11) NOT NULL DEFAULT 0,
  `attr8` int(11) NOT NULL DEFAULT 0,
  `attrval8` int(11) NOT NULL DEFAULT 0,
  `attr9` int(11) NOT NULL DEFAULT 0,
  `attrval9` int(11) NOT NULL DEFAULT 0
) ENGINE=Aria DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci PAGE_CHECKSUM=1 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item_sell_log`
--

LOCK TABLES `item_sell_log` WRITE;
/*!40000 ALTER TABLE `item_sell_log` DISABLE KEYS */;
INSERT INTO `item_sell_log` VALUES
(2,'2026-10-11 14:25:20','ITEM_DELETE',13049,1,0,0,0,0,0,0,3,12,27,15,39,10,48,1,49,1,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',11299,1,1,1,1,0,0,0,1,2000,9,20,23,10,39,10,53,50,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',13049,1,0,0,0,0,0,0,3,12,27,15,39,10,48,1,49,1,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',15189,1,0,0,0,0,0,0,1,2000,2,80,8,8,7,8,15,10,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',16109,1,0,0,0,0,0,0,1,2000,2,80,15,10,16,10,24,10,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',14109,1,0,0,0,0,0,0,1,2000,2,80,16,10,23,10,25,10,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',12249,1,0,0,0,0,0,0,7,8,10,30,11,30,28,15,24,10,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',16109,1,0,0,0,0,0,0,1,2000,2,80,15,10,16,10,24,10,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',12249,1,0,0,0,0,0,0,7,8,10,30,11,30,28,15,24,10,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',3009,1,0,0,0,0,0,0,5,12,15,10,16,10,18,20,6,12,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',16109,1,0,0,0,0,0,0,1,2000,2,80,15,10,16,10,24,10,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',15189,1,0,0,0,0,0,0,1,2000,2,80,8,8,7,8,15,10,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',16009,1,0,0,0,0,0,0,1,2000,16,10,15,10,44,20,43,20,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',15189,1,0,0,0,0,0,0,1,2000,2,80,8,8,7,8,15,10,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',13049,1,0,0,0,0,0,0,3,12,27,15,39,10,48,1,49,1,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',13009,1,0,0,0,0,0,0,48,1,5,12,27,15,18,20,6,12,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',3159,1,1,1,1,0,0,0,9,20,15,10,16,10,22,20,5,12,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',12249,1,0,0,0,0,0,0,7,8,10,30,11,30,28,15,24,10,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',11299,1,1,1,1,0,0,0,1,2000,9,20,23,10,39,10,53,50,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',14109,1,0,0,0,0,0,0,1,2000,2,80,16,10,23,10,25,10,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',11299,1,1,1,1,0,0,0,1,2000,9,20,23,10,39,10,53,50,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',11209,1,0,0,0,0,0,0,1,2000,23,10,39,15,53,50,9,20,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',14109,1,0,0,0,0,0,0,1,2000,2,80,16,10,23,10,25,10,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',12209,1,0,0,0,0,0,0,7,8,10,30,12,8,18,20,19,20,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',14009,1,0,0,0,0,0,0,1,2000,16,10,23,10,45,20,18,20,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',15009,1,0,0,0,0,0,0,1,2000,7,8,15,10,44,20,43,20,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',19,1,0,0,0,0,0,0,5,12,15,10,16,10,18,20,6,12,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',3159,1,1,1,1,0,0,0,9,20,15,10,16,10,22,20,5,12,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:20','ITEM_DELETE',3159,1,1,1,1,0,0,0,9,20,15,10,16,10,22,20,5,12,0,0,0,0,0,0,0,0,0,0),
(2,'2026-10-11 14:25:30','ITEM_SELL',80008,89,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
/*!40000 ALTER TABLE `item_sell_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `itemshop`
--

DROP TABLE IF EXISTS `itemshop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `itemshop` (
  `pid` int(11) NOT NULL DEFAULT 0,
  `account_id` int(11) NOT NULL DEFAULT 0,
  `item_index` int(11) NOT NULL DEFAULT 0,
  `vnum` int(11) NOT NULL DEFAULT 0,
  `count` int(11) NOT NULL DEFAULT 0,
  `price` bigint(20) NOT NULL DEFAULT 0,
  `charge_type` int(11) NOT NULL DEFAULT 0,
  `item_id` bigint(20) unsigned DEFAULT NULL,
  `time` datetime NOT NULL,
  `money_before` int(11) NOT NULL DEFAULT 0,
  KEY `time` (`time`),
  KEY `pid` (`pid`),
  KEY `account_id` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `itemshop`
--

LOCK TABLES `itemshop` WRITE;
/*!40000 ALTER TABLE `itemshop` DISABLE KEYS */;
/*!40000 ALTER TABLE `itemshop` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `itemshop_log`
--

DROP TABLE IF EXISTS `itemshop_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `itemshop_log` (
  `account_id` int(11) DEFAULT NULL,
  `vnum` int(11) DEFAULT NULL,
  `count` int(11) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `id` int(11) DEFAULT NULL,
  `category` int(11) DEFAULT NULL,
  `channel` smallint(6) DEFAULT NULL,
  `date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `itemshop_log`
--

LOCK TABLES `itemshop_log` WRITE;
/*!40000 ALTER TABLE `itemshop_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `itemshop_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `itemshop_logs`
--

DROP TABLE IF EXISTS `itemshop_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `itemshop_logs` (
  `accountID` int(11) NOT NULL DEFAULT 0,
  `playerName` varchar(50) DEFAULT '',
  `buyDate` datetime DEFAULT '0000-00-00 00:00:00' ON UPDATE current_timestamp(),
  `buyTime` int(11) DEFAULT 0,
  `ipAdress` varchar(16) DEFAULT NULL,
  `itemID` int(11) DEFAULT 0,
  `itemVnum` int(11) DEFAULT 0,
  `itemCount` int(11) DEFAULT 0,
  `itemPrice` bigint(55) DEFAULT 0
) ENGINE=Aria DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci PAGE_CHECKSUM=1 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `itemshop_logs`
--

LOCK TABLES `itemshop_logs` WRITE;
/*!40000 ALTER TABLE `itemshop_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `itemshop_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `levellog`
--

DROP TABLE IF EXISTS `levellog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `levellog` (
  `level` smallint(5) unsigned NOT NULL DEFAULT 0,
  `time` datetime NOT NULL,
  `account_id` int(11) NOT NULL DEFAULT 0,
  `pid` int(11) NOT NULL DEFAULT 0,
  `playtime` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`pid`,`level`),
  KEY `time` (`time`),
  KEY `account_id` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `levellog`
--

LOCK TABLES `levellog` WRITE;
/*!40000 ALTER TABLE `levellog` DISABLE KEYS */;
INSERT INTO `levellog` VALUES
(2,'2026-10-08 23:19:29',6,5,10),
(3,'2026-10-09 00:05:55',6,5,40),
(4,'2026-10-09 00:05:55',6,5,40),
(5,'2026-10-09 00:05:55',6,5,40),
(6,'2026-10-09 00:05:55',6,5,40),
(7,'2026-10-09 00:05:55',6,5,40),
(8,'2026-10-09 00:05:55',6,5,40),
(9,'2026-10-09 00:05:55',6,5,40),
(10,'2026-10-09 00:05:55',6,5,40),
(11,'2026-10-09 00:05:55',6,5,40),
(12,'2026-10-09 00:05:55',6,5,40),
(13,'2026-10-09 00:05:55',6,5,40),
(14,'2026-10-09 00:05:55',6,5,40),
(15,'2026-10-09 00:05:55',6,5,40),
(16,'2026-10-09 00:05:55',6,5,40),
(17,'2026-10-09 00:05:55',6,5,40),
(18,'2026-10-09 00:05:55',6,5,40),
(19,'2026-10-09 00:05:55',6,5,40),
(20,'2026-10-09 00:05:55',6,5,40),
(21,'2026-10-09 00:05:55',6,5,40),
(22,'2026-10-09 00:05:55',6,5,40),
(23,'2026-10-09 00:05:55',6,5,40),
(24,'2026-10-09 00:05:55',6,5,40),
(25,'2026-10-09 00:05:55',6,5,40),
(26,'2026-10-09 00:05:55',6,5,40),
(27,'2026-10-09 00:05:55',6,5,40),
(28,'2026-10-09 00:05:55',6,5,40),
(29,'2026-10-09 00:05:55',6,5,40),
(30,'2026-10-09 00:05:55',6,5,40),
(31,'2026-10-09 00:05:55',6,5,40),
(32,'2026-10-09 00:05:55',6,5,40),
(33,'2026-10-09 00:05:55',6,5,40),
(34,'2026-10-09 00:05:55',6,5,40),
(35,'2026-10-09 00:05:55',6,5,40),
(36,'2026-10-09 00:05:55',6,5,40),
(37,'2026-10-09 00:05:55',6,5,40),
(38,'2026-10-09 00:05:55',6,5,40),
(39,'2026-10-09 00:05:55',6,5,40),
(40,'2026-10-09 00:05:55',6,5,40),
(41,'2026-10-09 00:05:55',6,5,40),
(42,'2026-10-09 00:05:55',6,5,40),
(43,'2026-10-09 00:05:55',6,5,40),
(44,'2026-10-09 00:05:55',6,5,40),
(45,'2026-10-09 00:05:55',6,5,40),
(46,'2026-10-09 00:05:55',6,5,40),
(47,'2026-10-09 00:05:55',6,5,40),
(48,'2026-10-09 00:05:55',6,5,40),
(49,'2026-10-09 00:05:55',6,5,40),
(50,'2026-10-09 00:05:55',6,5,40),
(51,'2026-10-09 00:05:55',6,5,40),
(52,'2026-10-09 00:05:55',6,5,40),
(53,'2026-10-09 00:05:55',6,5,40),
(54,'2026-10-09 00:05:55',6,5,40),
(55,'2026-10-09 00:05:55',6,5,40);
/*!40000 ALTER TABLE `levellog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log`
--

DROP TABLE IF EXISTS `log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `log` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `type` varbinary(20) DEFAULT NULL COMMENT 'contains: CHARACTER, ITEM',
  `time` datetime DEFAULT NULL,
  `who` int(11) unsigned DEFAULT NULL,
  `x` int(11) unsigned DEFAULT NULL,
  `y` int(11) unsigned DEFAULT NULL,
  `what` bigint(11) unsigned DEFAULT NULL,
  `how` varbinary(50) DEFAULT NULL,
  `hint` varbinary(500) DEFAULT NULL,
  `vnum` int(11) unsigned DEFAULT NULL,
  `ip` varchar(15) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `who_time` (`who`,`time`),
  KEY `time` (`time`)
) ENGINE=InnoDB AUTO_INCREMENT=1487 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log`
--

LOCK TABLES `log` WRITE;
/*!40000 ALTER TABLE `log` DISABLE KEYS */;
INSERT INTO `log` VALUES
(1,'CHARACTER','2026-10-08 23:01:29',5,0,0,0,'CREATE PLAYER','',NULL,'127.0.0.1'),
(2,'CHARACTER','2026-10-08 23:01:30',5,957328,255311,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(3,'CHARACTER','2026-10-08 23:05:43',6,0,0,0,'CREATE PLAYER','',NULL,'127.0.0.1'),
(4,'CHARACTER','2026-10-08 23:10:13',5,955382,249581,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(5,'CHARACTER','2026-10-08 23:16:24',5,955829,250331,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(6,'ITEM','2026-10-08 23:17:07',5,954476,249526,10000001,'GM','Kılıç+9',19,'127.0.0.1'),
(7,'CHARACTER','2026-10-08 23:18:48',5,954666,249571,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(8,'ITEM','2026-10-08 23:18:52',5,954777,249300,10000002,'GET','Beceri Kitabı 1 50300 81,0,0 0,0|0,0|0,0|0,0|0,0|0,0|0,0',50300,'127.0.0.1'),
(9,'ITEM','2026-10-08 23:18:52',5,954777,249300,10000003,'GET','Mavi İksir(O) 30 27005 0,0,0 0,0|0,0|0,0|0,0|0,0|0,0|0,0',27005,'127.0.0.1'),
(10,'ITEM','2026-10-08 23:18:53',5,954777,249300,10000004,'GET','Kırmızı İksir(O) 50 27002 0,0,0 0,0|0,0|0,0|0,0|0,0|0,0|0,0',27002,'127.0.0.1'),
(11,'CHARACTER','2026-10-08 23:18:59',5,956105,247773,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(12,'CHARACTER','2026-10-08 23:18:59',5,956105,247773,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(13,'CHARACTER','2026-10-08 23:18:59',5,956105,247773,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(14,'CHARACTER','2026-10-08 23:19:00',5,956105,247773,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(15,'CHARACTER','2026-10-08 23:19:00',5,956105,247773,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(16,'CHARACTER','2026-10-08 23:19:00',5,956105,247773,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(17,'CHARACTER','2026-10-08 23:19:00',5,956105,247773,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(18,'CHARACTER','2026-10-08 23:19:00',5,956105,247773,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(19,'CHARACTER','2026-10-08 23:19:00',5,956105,247773,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(20,'CHARACTER','2026-10-08 23:19:00',5,956105,247773,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(21,'CHARACTER','2026-10-08 23:19:00',5,956105,247773,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(22,'CHARACTER','2026-10-08 23:19:00',5,956105,247773,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(23,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(24,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(25,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(26,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(27,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(28,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(29,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(30,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(31,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(32,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(33,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(34,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(35,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(36,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(37,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(38,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(39,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(40,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(41,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(42,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(43,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(44,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(45,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(46,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(47,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(48,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(49,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(50,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(51,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(52,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(53,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(54,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(55,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(56,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(57,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(58,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(59,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(60,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(61,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(62,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(63,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(64,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(65,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(66,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(67,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(68,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(69,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(70,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(71,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(72,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(73,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(74,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(75,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(76,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(77,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(78,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(79,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(80,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(81,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(82,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(83,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(84,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(85,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(86,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(87,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(88,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(89,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(90,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(91,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(92,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(93,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(94,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(95,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(96,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(97,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(98,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(99,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(100,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(101,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(102,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(103,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(104,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(105,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(106,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(107,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(108,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(109,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(110,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(111,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(112,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(113,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(114,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(115,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(116,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(117,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(118,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(119,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(120,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(121,'ITEM','2026-10-08 23:19:05',5,956162,248050,10000005,'SYSTEM','Kırmızı İksir(K)',27001,'127.0.0.1'),
(122,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(123,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(124,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(125,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(126,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(127,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(128,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(129,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(130,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(131,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(132,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(133,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(134,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(135,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(136,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(137,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(138,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(139,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(140,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(141,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(142,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(143,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(144,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(145,'CHARACTER','2026-10-08 23:19:05',5,956162,248050,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(146,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(147,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(148,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(149,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(150,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(151,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(152,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(153,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(154,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(155,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(156,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(157,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(158,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(159,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(160,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(161,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(162,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(163,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(164,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(165,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(166,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(167,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(168,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(169,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(170,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(171,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(172,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(173,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(174,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(175,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(176,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(177,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(178,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(179,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(180,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(181,'CHARACTER','2026-10-08 23:19:18',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(182,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(183,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(184,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(185,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(186,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(187,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(188,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(189,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(190,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(191,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(192,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(193,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(194,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(195,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(196,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(197,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(198,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(199,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(200,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(201,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(202,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(203,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(204,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(205,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(206,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(207,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(208,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(209,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(210,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(211,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(212,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(213,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(214,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(215,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(216,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(217,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(218,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(219,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(220,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(221,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(222,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(223,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(224,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(225,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(226,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(227,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(228,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(229,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(230,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(231,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(232,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(233,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(234,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(235,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(236,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(237,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(238,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(239,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(240,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(241,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(242,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(243,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(244,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(245,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(246,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(247,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(248,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(249,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(250,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(251,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(252,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(253,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(254,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(255,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(256,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(257,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(258,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(259,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(260,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(261,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(262,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(263,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(264,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(265,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(266,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(267,'CHARACTER','2026-10-08 23:19:19',5,956953,247721,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(268,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(269,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(270,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(271,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(272,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(273,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(274,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(275,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(276,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(277,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(278,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(279,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(280,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(281,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(282,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(283,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(284,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(285,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(286,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(287,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(288,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(289,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(290,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(291,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(292,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(293,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(294,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(295,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(296,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(297,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(298,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(299,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(300,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(301,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(302,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(303,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(304,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(305,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(306,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(307,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(308,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(309,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(310,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(311,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(312,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(313,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(314,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(315,'CHARACTER','2026-10-08 23:19:27',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(316,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(317,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(318,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(319,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(320,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(321,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(322,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(323,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(324,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(325,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(326,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(327,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(328,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(329,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(330,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(331,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(332,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(333,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(334,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(335,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(336,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(337,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(338,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(339,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(340,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(341,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(342,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(343,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(344,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(345,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(346,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(347,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(348,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(349,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(350,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(351,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(352,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(353,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(354,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(355,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(356,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(357,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(358,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(359,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(360,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(361,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(362,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(363,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(364,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(365,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(366,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(367,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(368,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(369,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(370,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(371,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(372,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(373,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(374,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(375,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(376,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(377,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(378,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(379,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(380,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(381,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(382,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(383,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(384,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(385,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(386,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(387,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(388,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(389,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(390,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(391,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(392,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(393,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(394,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(395,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(396,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(397,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(398,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(399,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(400,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(401,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(402,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(403,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(404,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(405,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(406,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(407,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(408,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(409,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(410,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(411,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(412,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(413,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(414,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(415,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(416,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(417,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(418,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(419,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(420,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(421,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(422,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(423,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(424,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(425,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(426,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(427,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(428,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(429,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(430,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(431,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(432,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(433,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(434,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(435,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(436,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(437,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(438,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(439,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(440,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(441,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(442,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(443,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(444,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(445,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(446,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(447,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(448,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(449,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(450,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(451,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(452,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(453,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(454,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(455,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(456,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(457,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(458,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(459,'CHARACTER','2026-10-08 23:19:28',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(460,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(461,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(462,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(463,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(464,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(465,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(466,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(467,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(468,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(469,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(470,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(471,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(472,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(473,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(474,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(475,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(476,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(477,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(478,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(479,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(480,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(481,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(482,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(483,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(484,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(485,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(486,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(487,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(488,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(489,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(490,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(491,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(492,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(493,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(494,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(495,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(496,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(497,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(498,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(499,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(500,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(501,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(502,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(503,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(504,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(505,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(506,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(507,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(508,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(509,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(510,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(511,'CHARACTER','2026-10-08 23:19:29',5,956559,248580,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(512,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(513,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(514,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(515,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(516,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(517,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(518,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(519,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(520,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(521,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(522,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(523,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(524,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(525,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(526,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(527,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(528,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(529,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(530,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(531,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(532,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(533,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(534,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(535,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(536,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(537,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(538,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(539,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(540,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(541,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(542,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(543,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(544,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(545,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(546,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(547,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(548,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(549,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(550,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(551,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(552,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(553,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(554,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(555,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(556,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(557,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(558,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(559,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(560,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(561,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(562,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(563,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(564,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(565,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(566,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(567,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(568,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(569,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(570,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(571,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(572,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(573,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(574,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(575,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(576,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(577,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(578,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(579,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(580,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(581,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(582,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(583,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(584,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(585,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(586,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(587,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(588,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(589,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(590,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(591,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(592,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(593,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(594,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(595,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(596,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(597,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(598,'CHARACTER','2026-10-08 23:19:38',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(599,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(600,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(601,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(602,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(603,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(604,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(605,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(606,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(607,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(608,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(609,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(610,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(611,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(612,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(613,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(614,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(615,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(616,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(617,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(618,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(619,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(620,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(621,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(622,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(623,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(624,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(625,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(626,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(627,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(628,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(629,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(630,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(631,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(632,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(633,'CHARACTER','2026-10-08 23:19:39',5,956370,248067,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(634,'CHARACTER','2026-10-08 23:22:11',5,958269,247786,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(635,'CHARACTER','2026-10-08 23:22:35',5,958269,247786,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(636,'CHARACTER','2026-10-08 23:26:26',5,957049,247446,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(637,'CHARACTER','2026-10-08 23:33:06',5,956636,247583,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(638,'ITEM','2026-10-08 23:33:18',5,956636,247464,10000006,'GM','Kılıç+9',19,'127.0.0.1'),
(639,'CHARACTER','2026-10-08 23:42:42',5,958443,249368,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(640,'CHARACTER','2026-10-08 23:43:22',5,958443,249368,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(641,'CHARACTER','2026-10-08 23:48:05',5,957166,247665,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(642,'ITEM','2026-10-08 23:48:21',5,957650,246759,10000006,'DROP','Kılıç+9 1 19',19,'127.0.0.1'),
(643,'ITEM','2026-10-08 23:48:22',5,957650,246759,10000006,'GET','Kılıç+9 1 19 1,0,0 0,0|0,0|0,0|0,0|0,0|0,0|0,0',19,'127.0.0.1'),
(644,'CHARACTER','2026-10-08 23:54:55',5,957677,245733,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(645,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(646,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(647,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(648,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(649,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(650,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(651,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(652,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(653,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(654,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(655,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(656,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(657,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(658,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(659,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(660,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(661,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(662,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(663,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(664,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(665,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(666,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(667,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(668,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(669,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(670,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(671,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(672,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(673,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(674,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(675,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(676,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(677,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(678,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(679,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(680,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(681,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(682,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(683,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(684,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(685,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(686,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(687,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(688,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(689,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(690,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(691,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(692,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(693,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(694,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(695,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(696,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(697,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(698,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(699,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(700,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(701,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(702,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(703,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(704,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(705,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(706,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(707,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(708,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(709,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(710,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(711,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(712,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(713,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(714,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(715,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(716,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(717,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(718,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(719,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(720,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(721,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(722,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(723,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(724,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(725,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(726,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(727,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(728,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(729,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(730,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(731,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(732,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(733,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(734,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(735,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(736,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(737,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(738,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(739,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(740,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(741,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(742,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(743,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(744,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(745,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(746,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(747,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(748,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(749,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(750,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(751,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(752,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(753,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(754,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(755,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(756,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(757,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(758,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(759,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(760,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(761,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(762,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(763,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(764,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(765,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(766,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(767,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(768,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(769,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(770,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(771,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(772,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(773,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(774,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(775,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(776,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(777,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(778,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(779,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(780,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(781,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(782,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(783,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(784,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(785,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(786,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(787,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(788,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(789,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(790,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(791,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(792,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(793,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(794,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(795,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(796,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(797,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(798,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(799,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(800,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(801,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(802,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(803,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(804,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(805,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(806,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(807,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(808,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(809,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(810,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(811,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(812,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(813,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(814,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(815,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(816,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(817,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(818,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(819,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(820,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(821,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(822,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(823,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(824,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(825,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(826,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(827,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(828,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(829,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(830,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(831,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(832,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(833,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(834,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(835,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(836,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(837,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(838,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(839,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(840,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(841,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(842,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(843,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(844,'CHARACTER','2026-10-08 23:57:26',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(845,'CHARACTER','2026-10-08 23:57:28',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(846,'CHARACTER','2026-10-08 23:57:28',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(847,'CHARACTER','2026-10-08 23:57:28',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(848,'CHARACTER','2026-10-08 23:57:28',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(849,'CHARACTER','2026-10-08 23:57:28',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(850,'CHARACTER','2026-10-08 23:57:28',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(851,'CHARACTER','2026-10-08 23:57:28',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(852,'CHARACTER','2026-10-08 23:57:28',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(853,'CHARACTER','2026-10-08 23:57:28',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(854,'CHARACTER','2026-10-08 23:57:28',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(855,'CHARACTER','2026-10-08 23:57:28',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(856,'CHARACTER','2026-10-08 23:57:28',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(857,'CHARACTER','2026-10-08 23:57:28',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(858,'CHARACTER','2026-10-08 23:57:28',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(859,'CHARACTER','2026-10-08 23:57:28',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(860,'CHARACTER','2026-10-08 23:57:28',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(861,'CHARACTER','2026-10-08 23:57:28',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(862,'CHARACTER','2026-10-08 23:57:28',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(863,'CHARACTER','2026-10-08 23:57:28',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(864,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(865,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(866,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(867,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(868,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(869,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(870,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(871,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(872,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(873,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(874,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(875,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(876,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(877,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(878,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(879,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(880,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(881,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(882,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(883,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(884,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(885,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(886,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(887,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(888,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(889,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(890,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(891,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(892,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(893,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(894,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(895,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(896,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(897,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(898,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(899,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(900,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(901,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(902,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(903,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(904,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(905,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(906,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(907,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(908,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(909,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(910,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(911,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(912,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(913,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(914,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(915,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(916,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(917,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(918,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(919,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(920,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(921,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(922,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(923,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(924,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(925,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(926,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(927,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(928,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(929,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(930,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(931,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(932,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(933,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(934,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(935,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(936,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(937,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(938,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(939,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(940,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(941,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(942,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(943,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(944,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(945,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(946,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(947,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(948,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(949,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(950,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(951,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(952,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(953,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(954,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(955,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(956,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(957,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(958,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(959,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(960,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(961,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(962,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(963,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(964,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(965,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(966,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(967,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(968,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(969,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(970,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(971,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(972,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(973,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(974,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(975,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(976,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(977,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(978,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(979,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(980,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(981,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(982,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(983,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(984,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(985,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(986,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(987,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(988,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(989,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(990,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(991,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(992,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(993,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(994,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(995,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(996,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(997,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(998,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(999,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1000,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1001,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1002,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1003,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1004,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1005,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1006,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1007,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1008,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1009,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1010,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1011,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1012,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1013,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1014,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1015,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1016,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1017,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1018,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1019,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1020,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1021,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1022,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1023,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1024,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1025,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1026,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1027,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1028,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1029,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1030,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1031,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1032,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1033,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1034,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1035,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1036,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1037,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1038,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1039,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1040,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1041,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1042,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1043,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1044,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1045,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1046,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1047,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1048,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1049,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1050,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1051,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1052,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1053,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1054,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1055,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1056,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1057,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1058,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1059,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1060,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1061,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1062,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1063,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1064,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1065,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1066,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1067,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1068,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1069,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1070,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1071,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1072,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1073,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1074,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1075,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1076,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1077,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1078,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1079,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1080,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1081,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1082,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1083,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1084,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1085,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1086,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1087,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1088,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1089,'CHARACTER','2026-10-08 23:57:29',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1090,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1091,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1092,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1093,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1094,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1095,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1096,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1097,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1098,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1099,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1100,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1101,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1102,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1103,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1104,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1105,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1106,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1107,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1108,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1109,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1110,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1111,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1112,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1113,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1114,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1115,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1116,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1117,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1118,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1119,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1120,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1121,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1122,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1123,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1124,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1125,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1126,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1127,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1128,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1129,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1130,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1131,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1132,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1133,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1134,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1135,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1136,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1137,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1138,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1139,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1140,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1141,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1142,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1143,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1144,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1145,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1146,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1147,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1148,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1149,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1150,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1151,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1152,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1153,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1154,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1155,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1156,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1157,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1158,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1159,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1160,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1161,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1162,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1163,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1164,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1165,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1166,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1167,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1168,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1169,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1170,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1171,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1172,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1173,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1174,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1175,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1176,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1177,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1178,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1179,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1180,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1181,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1182,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1183,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1184,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1185,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1186,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1187,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1188,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1189,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1190,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1191,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1192,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1193,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1194,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1195,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1196,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1197,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1198,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1199,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1200,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1201,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1202,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1203,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1204,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1205,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1206,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1207,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1208,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1209,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1210,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1211,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1212,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1213,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1214,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1215,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1216,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1217,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1218,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1219,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1220,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1221,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1222,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1223,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1224,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1225,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1226,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1227,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1228,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1229,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1230,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1231,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1232,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1233,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1234,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1235,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1236,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1237,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1238,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1239,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1240,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1241,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1242,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1243,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1244,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1245,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1246,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1247,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1248,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1249,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1250,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1251,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1252,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1253,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1254,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1255,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1256,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1257,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1258,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1259,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1260,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1261,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1262,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1263,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1264,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1265,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1266,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1267,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1268,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1269,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1270,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1271,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1272,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1273,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1274,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1275,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1276,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1277,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1278,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1279,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1280,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1281,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1282,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1283,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1284,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1285,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1286,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1287,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1288,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1289,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1290,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1291,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1292,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1293,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1294,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1295,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1296,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1297,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1298,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1299,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1300,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1301,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1302,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1303,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1304,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1305,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1306,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1307,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1308,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1309,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1310,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1311,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1312,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1313,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1314,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1315,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1316,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1317,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1318,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1319,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1320,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1321,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1322,'CHARACTER','2026-10-08 23:57:30',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1323,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1324,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1325,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1326,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1327,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1328,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1329,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1330,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1331,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1332,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1333,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1334,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1335,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1336,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1337,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1338,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1339,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1340,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1341,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1342,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1343,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1344,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1345,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1346,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1347,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1348,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1349,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1350,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1351,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1352,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1353,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1354,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1355,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1356,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1357,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1358,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1359,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1360,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1361,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1362,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1363,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1364,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1365,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1366,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1367,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1368,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1369,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1370,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1371,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1372,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1373,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1374,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1375,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1376,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1377,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1378,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1379,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1380,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1381,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1382,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1383,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1384,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1385,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1386,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1387,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1388,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1389,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1390,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1391,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1392,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1393,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1394,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1395,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1396,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1397,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1398,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1399,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1400,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1401,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1402,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1403,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1404,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1405,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1406,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1407,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1408,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1409,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1410,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1411,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1412,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1413,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1414,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1415,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1416,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1417,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1418,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1419,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1420,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1421,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1422,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1423,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1424,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1425,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1426,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1427,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1428,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1429,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1430,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1431,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1432,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1433,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1434,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1435,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1436,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1437,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1438,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1439,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1440,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1441,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1442,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1443,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1444,'CHARACTER','2026-10-08 23:57:31',5,957664,245867,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1445,'CHARACTER','2026-10-09 00:03:15',5,959830,242828,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1446,'ITEM','2026-10-09 00:05:55',5,959664,242081,10000007,'SYSTEM','Kırmızı İksir(O)',27002,'127.0.0.1'),
(1447,'ITEM','2026-10-09 00:05:55',5,959664,242081,10000008,'SYSTEM','Kırmızı İksir(O)',27002,'127.0.0.1'),
(1448,'ITEM','2026-10-09 00:06:12',5,958456,241903,10000009,'SYSTEM','Siyah at',71134,'127.0.0.1'),
(1449,'CHARACTER','2026-10-09 00:06:12',5,958456,241903,71134,'COSMETIC_MOUNT_REWARD','basarim_17',NULL,'127.0.0.1'),
(1450,'CHARACTER','2026-10-09 00:10:25',5,957439,241990,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1451,'CHARACTER','2026-10-09 00:13:28',5,958886,240989,104,'DEAD_BY_NPC','Mavi Kurt',NULL,'127.0.0.1'),
(1452,'CHARACTER','2026-10-09 00:15:29',5,958366,241254,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1453,'CHARACTER','2026-10-09 00:18:47',5,958366,241254,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1454,'CHARACTER','2026-10-09 00:26:40',5,958366,241254,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1455,'CHARACTER','2026-10-09 00:37:23',5,957572,241258,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1456,'CHARACTER','2026-10-09 00:40:28',5,957863,240882,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1457,'CHARACTER','2026-10-09 00:42:09',5,957438,243314,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1458,'CHARACTER','2026-10-09 00:42:21',5,957656,243094,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1459,'CHARACTER','2026-10-09 00:42:41',5,957334,243900,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1460,'CHARACTER','2026-10-09 00:43:50',5,956989,243833,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1461,'CHARACTER','2026-10-09 01:33:01',5,959144,242071,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1462,'CHARACTER','2026-10-09 01:36:37',5,959144,242071,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1463,'CHARACTER','2026-10-09 01:37:32',5,959259,241836,8001,'STONE_KILL','1 41',NULL,'127.0.0.1'),
(1464,'CHARACTER','2026-10-09 01:42:49',5,960221,241418,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1465,'CHARACTER','2026-10-09 01:47:39',5,959316,241365,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1466,'CHARACTER','2026-10-09 01:56:28',5,992149,286765,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1467,'CHARACTER','2026-10-09 01:58:18',5,991202,286956,105,'DEAD_BY_NPC','Alfa Mavi Kurt',NULL,'127.0.0.1'),
(1468,'CHARACTER','2026-10-09 01:58:32',5,991202,286956,108,'DEAD_BY_NPC','Yaban Domuzu',NULL,'127.0.0.1'),
(1469,'CHARACTER','2026-10-09 07:34:27',5,993248,287220,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1470,'CHARACTER','2026-10-09 07:34:51',5,993248,287220,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1471,'CHARACTER','2026-10-09 07:39:38',5,993206,286323,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1472,'CHARACTER','2026-10-09 07:40:23',5,992555,286358,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1473,'CHARACTER','2026-10-09 07:44:53',5,992555,286358,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1474,'CHARACTER','2026-10-09 08:14:55',5,992555,286358,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1475,'CHARACTER','2026-10-09 08:15:07',5,992562,285981,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1476,'CHARACTER','2026-10-09 08:35:22',5,992562,285981,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1477,'CHARACTER','2026-10-09 08:46:29',5,992468,286048,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1478,'CHARACTER','2026-10-09 09:09:01',5,992468,286048,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1479,'CHARACTER','2026-10-09 09:09:26',5,992468,286048,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1480,'CHARACTER','2026-10-09 10:11:46',5,992468,286048,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1481,'CHARACTER','2026-10-09 10:12:07',5,992468,286048,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1482,'CHARACTER','2026-10-09 11:00:24',5,991709,286322,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1483,'CHARACTER','2026-10-09 11:00:58',5,991709,286322,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1484,'CHARACTER','2026-10-09 11:06:48',5,991634,285390,5,'GM_LOGIN','',NULL,'127.0.0.1'),
(1485,'CHARACTER','2026-10-09 11:07:18',5,991634,285311,155,'DEAD_BY_NPC','Li-An',NULL,'127.0.0.1'),
(1486,'CHARACTER','2026-10-09 11:10:10',5,990944,285845,5,'GM_LOGIN','',NULL,'127.0.0.1');
/*!40000 ALTER TABLE `log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log_chat`
--

DROP TABLE IF EXISTS `log_chat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `log_chat` (
  `where` int(10) unsigned NOT NULL,
  `who_id` int(10) unsigned NOT NULL,
  `type` enum('NORMAL','WHISPER','PARTY','GUILD','SHOUT','OFFLINE_WHISPER') NOT NULL,
  `msg` varbinary(512) NOT NULL,
  `when` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_chat`
--

LOCK TABLES `log_chat` WRITE;
/*!40000 ALTER TABLE `log_chat` DISABLE KEYS */;
/*!40000 ALTER TABLE `log_chat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log_chat_priv`
--

DROP TABLE IF EXISTS `log_chat_priv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `log_chat_priv` (
  `where` int(10) unsigned NOT NULL,
  `who_id` int(10) unsigned NOT NULL,
  `who_name` varchar(25) NOT NULL,
  `whom_id` int(10) unsigned DEFAULT NULL,
  `whom_name` varchar(25) NOT NULL,
  `type` enum('NORMAL','WHISPER','PARTY','GUILD','SHOUT','OFFLINE_WHISPER') NOT NULL,
  `msg` varbinary(512) NOT NULL,
  `when` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_chat_priv`
--

LOCK TABLES `log_chat_priv` WRITE;
/*!40000 ALTER TABLE `log_chat_priv` DISABLE KEYS */;
/*!40000 ALTER TABLE `log_chat_priv` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log_commands`
--

DROP TABLE IF EXISTS `log_commands`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `log_commands` (
  `userid` int(11) DEFAULT NULL,
  `port` int(11) DEFAULT NULL,
  `command` varbinary(1024) DEFAULT NULL,
  `date` datetime DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_commands`
--

LOCK TABLES `log_commands` WRITE;
/*!40000 ALTER TABLE `log_commands` DISABLE KEYS */;
/*!40000 ALTER TABLE `log_commands` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log_dungeon`
--

DROP TABLE IF EXISTS `log_dungeon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `log_dungeon` (
  `name` varbinary(20) DEFAULT NULL COMMENT 'contains: CHARACTER, ITEM',
  `time` datetime DEFAULT NULL,
  `mob` bigint(11) unsigned DEFAULT NULL,
  `map` varbinary(80) DEFAULT NULL COMMENT 'snprintf with 80u size',
  `x` int(11) unsigned DEFAULT NULL,
  `y` int(11) unsigned DEFAULT NULL,
  `how` varbinary(50) DEFAULT NULL,
  `id` int(11) unsigned DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_dungeon`
--

LOCK TABLES `log_dungeon` WRITE;
/*!40000 ALTER TABLE `log_dungeon` DISABLE KEYS */;
/*!40000 ALTER TABLE `log_dungeon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log_level`
--

DROP TABLE IF EXISTS `log_level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `log_level` (
  `name` varchar(50) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `time` time DEFAULT NULL,
  `playtime` int(11) DEFAULT NULL,
  `account_id` int(11) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_level`
--

LOCK TABLES `log_level` WRITE;
/*!40000 ALTER TABLE `log_level` DISABLE KEYS */;
/*!40000 ALTER TABLE `log_level` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log_quest`
--

DROP TABLE IF EXISTS `log_quest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `log_quest` (
  `1` varchar(50) DEFAULT NULL,
  `2` int(11) DEFAULT NULL,
  `3` int(11) DEFAULT NULL,
  `4` int(11) DEFAULT NULL,
  `5` int(11) DEFAULT NULL,
  `6` int(11) DEFAULT NULL,
  `7` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_quest`
--

LOCK TABLES `log_quest` WRITE;
/*!40000 ALTER TABLE `log_quest` DISABLE KEYS */;
/*!40000 ALTER TABLE `log_quest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loginlog`
--

DROP TABLE IF EXISTS `loginlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `loginlog` (
  `type` enum('LOGIN','LOGOUT') DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `channel` tinyint(4) DEFAULT NULL,
  `account_id` int(11) unsigned DEFAULT NULL,
  `pid` int(11) unsigned DEFAULT NULL,
  `mapIndex` int(11) DEFAULT NULL,
  `x` int(11) DEFAULT NULL,
  `y` int(11) DEFAULT NULL,
  `playtime` int(11) DEFAULT NULL,
  `ip` varchar(15) NOT NULL DEFAULT '',
  `hwid` varchar(255) NOT NULL DEFAULT '',
  `info` varchar(64) DEFAULT NULL,
  KEY `account_id` (`account_id`),
  KEY `pid` (`pid`),
  KEY `time` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loginlog`
--

LOCK TABLES `loginlog` WRITE;
/*!40000 ALTER TABLE `loginlog` DISABLE KEYS */;
INSERT INTO `loginlog` VALUES
('LOGIN','2026-10-08 23:01:30',1,6,5,41,957328,255311,0,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 0 alignment: 0'),
('LOGOUT','2026-10-08 23:03:58',1,6,5,41,955382,249581,0,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 0 alignment: 0'),
('LOGIN','2026-10-08 23:05:46',1,6,6,41,957547,255356,0,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 0 alignment: 0'),
('LOGOUT','2026-10-08 23:07:31',1,6,6,41,956089,247485,1,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 0 alignment: 5'),
('LOGIN','2026-10-08 23:10:13',1,6,5,41,955382,249581,2,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 0 alignment: 10'),
('LOGOUT','2026-10-08 23:15:32',1,6,5,41,955829,250331,4,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 0 alignment: 20'),
('LOGIN','2026-10-08 23:16:24',1,6,5,41,955829,250331,7,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 0 alignment: 35'),
('LOGOUT','2026-10-08 23:20:48',1,6,5,41,958269,247786,10,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 65417 alignment: 1296'),
('LOGIN','2026-10-08 23:22:11',1,6,5,41,958269,247786,11,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 65417 alignment: 1301'),
('LOGOUT','2026-10-08 23:22:19',1,6,5,41,958269,247786,11,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 65417 alignment: 1301'),
('LOGIN','2026-10-08 23:22:35',1,6,5,41,958269,247786,11,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 65417 alignment: 1301'),
('LOGOUT','2026-10-08 23:25:24',1,6,5,41,957049,247446,11,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 65417 alignment: 1307'),
('LOGIN','2026-10-08 23:26:26',1,6,5,41,957049,247446,13,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 65417 alignment: 1317'),
('LOGOUT','2026-10-08 23:32:11',1,6,5,41,956636,247583,18,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 65417 alignment: 1342'),
('LOGIN','2026-10-08 23:33:06',1,6,5,41,956636,247583,18,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 65417 alignment: 1342'),
('LOGOUT','2026-10-08 23:40:34',1,6,5,41,958443,249368,23,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 65443 alignment: 1373'),
('LOGIN','2026-10-08 23:42:42',1,6,5,41,958443,249368,25,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 65443 alignment: 1383'),
('LOGOUT','2026-10-08 23:42:44',1,6,5,41,958443,249368,25,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 65443 alignment: 1383'),
('LOGIN','2026-10-08 23:43:22',1,6,5,41,958443,249368,25,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 65443 alignment: 1383'),
('LOGOUT','2026-10-08 23:46:19',1,6,5,41,957166,247665,27,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 65443 alignment: 1393'),
('LOGIN','2026-10-08 23:48:05',1,6,5,41,957166,247665,27,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 65443 alignment: 1393'),
('LOGOUT','2026-10-08 23:53:48',1,6,5,41,957677,245733,29,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 65464 alignment: 1409'),
('LOGIN','2026-10-08 23:54:55',1,6,5,41,957677,245733,32,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 65464 alignment: 1424'),
('LOGOUT','2026-10-09 00:01:07',1,6,5,41,959830,242828,37,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3049'),
('LOGIN','2026-10-09 00:03:15',1,6,5,41,959830,242828,38,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3054'),
('LOGOUT','2026-10-09 00:09:13',1,6,5,41,957439,241990,43,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3079'),
('LOGIN','2026-10-09 00:10:25',1,6,5,41,957439,241990,43,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3079'),
('LOGOUT','2026-10-09 00:14:15',1,6,5,41,958366,241254,46,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3094'),
('LOGIN','2026-10-09 00:15:29',1,6,5,41,958366,241254,46,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3094'),
('LOGOUT','2026-10-09 00:17:34',1,6,5,41,958366,241254,46,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3094'),
('LOGIN','2026-10-09 00:18:47',1,6,5,41,958366,241254,48,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3104'),
('LOGOUT','2026-10-09 00:23:47',1,6,5,41,958366,241254,50,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3114'),
('LOGIN','2026-10-09 00:26:40',1,6,5,41,958366,241254,52,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3124'),
('LOGOUT','2026-10-09 00:31:34',1,6,5,41,957572,241258,54,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3134'),
('LOGIN','2026-10-09 00:37:23',1,6,5,41,957572,241258,56,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3144'),
('LOGOUT','2026-10-09 00:39:40',1,6,5,41,957863,240882,56,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3144'),
('LOGIN','2026-10-09 00:40:28',1,6,5,41,957863,240882,58,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3154'),
('LOGOUT','2026-10-09 00:42:06',1,6,5,41,957438,243314,59,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3159'),
('LOGIN','2026-10-09 00:42:09',1,6,5,41,957438,243314,59,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3159'),
('LOGOUT','2026-10-09 00:42:18',1,6,5,41,957656,243094,59,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3159'),
('LOGIN','2026-10-09 00:42:21',1,6,5,41,957656,243094,59,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3159'),
('LOGOUT','2026-10-09 00:42:46',1,6,5,41,956989,243833,59,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3159'),
('LOGIN','2026-10-09 00:43:50',1,6,5,41,956989,243833,59,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3159'),
('LOGOUT','2026-10-09 01:31:42',1,6,5,41,959144,242071,104,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3384'),
('LOGIN','2026-10-09 01:33:01',1,6,5,41,959144,242071,106,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3394'),
('LOGOUT','2026-10-09 01:33:02',1,6,5,41,959144,242071,106,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3394'),
('LOGIN','2026-10-09 01:36:37',1,6,5,41,959144,242071,106,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3394'),
('LOGOUT','2026-10-09 01:40:40',1,6,5,41,960221,241418,110,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3414'),
('LOGIN','2026-10-09 01:42:49',1,6,5,41,960221,241418,110,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3414'),
('LOGOUT','2026-10-09 01:46:42',1,6,5,41,959316,241365,112,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3424'),
('LOGIN','2026-10-09 01:47:39',1,6,5,41,959316,241365,113,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3429'),
('LOGOUT','2026-10-09 01:55:08',1,6,5,41,992149,286765,118,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3454'),
('LOGIN','2026-10-09 01:56:28',1,6,5,41,992149,286765,120,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3464'),
('LOGOUT','2026-10-09 01:59:04',1,6,5,41,993248,287220,122,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3474'),
('LOGIN','2026-10-09 07:34:27',1,6,5,41,993248,287220,122,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3474'),
('LOGOUT','2026-10-09 07:34:34',1,6,5,41,993248,287220,122,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3474'),
('LOGIN','2026-10-09 07:34:51',1,6,5,41,993248,287220,122,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3474'),
('LOGOUT','2026-10-09 07:36:20',1,6,5,41,993206,286323,123,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3479'),
('LOGIN','2026-10-09 07:39:38',1,6,5,41,993206,286323,123,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3479'),
('LOGOUT','2026-10-09 07:40:01',1,6,5,41,992555,286358,123,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3479'),
('LOGIN','2026-10-09 07:40:23',1,6,5,41,992555,286358,123,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3479'),
('LOGOUT','2026-10-09 07:40:42',1,6,5,41,992555,286358,123,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3479'),
('LOGIN','2026-10-09 07:44:53',1,6,5,41,992555,286358,123,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3479'),
('LOGOUT','2026-10-09 07:48:19',1,6,5,41,992555,286358,125,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3489'),
('LOGIN','2026-10-09 08:14:55',1,6,5,41,992555,286358,126,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3494'),
('LOGOUT','2026-10-09 08:15:01',1,6,5,41,992562,285981,126,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3494'),
('LOGIN','2026-10-09 08:15:07',1,6,5,41,992562,285981,126,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3494'),
('LOGOUT','2026-10-09 08:16:33',1,6,5,41,992562,285981,127,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3499'),
('LOGIN','2026-10-09 08:35:22',1,6,5,41,992562,285981,127,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3499'),
('LOGOUT','2026-10-09 08:36:11',1,6,5,41,992468,286048,127,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3499'),
('LOGIN','2026-10-09 08:46:29',1,6,5,41,992468,286048,127,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3499'),
('LOGOUT','2026-10-09 08:46:45',1,6,5,41,992468,286048,127,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3499'),
('LOGIN','2026-10-09 09:09:01',1,6,5,41,992468,286048,127,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3499'),
('LOGOUT','2026-10-09 09:09:19',1,6,5,41,992468,286048,127,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3499'),
('LOGIN','2026-10-09 09:09:26',1,6,5,41,992468,286048,127,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3499'),
('LOGOUT','2026-10-09 09:09:42',1,6,5,41,992468,286048,127,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3499'),
('LOGIN','2026-10-09 10:11:46',1,6,5,41,992468,286048,127,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3499'),
('LOGOUT','2026-10-09 10:12:01',1,6,5,41,992468,286048,127,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3499'),
('LOGIN','2026-10-09 10:12:08',1,6,5,41,992468,286048,127,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3499'),
('LOGOUT','2026-10-09 10:13:01',1,6,5,41,991709,286322,127,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3499'),
('LOGIN','2026-10-09 11:00:24',1,6,5,41,991709,286322,127,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3499'),
('LOGOUT','2026-10-09 11:00:41',1,6,5,41,991709,286322,127,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3499'),
('LOGIN','2026-10-09 11:00:58',1,6,5,41,991709,286322,127,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3499'),
('LOGOUT','2026-10-09 11:02:15',1,6,5,41,991634,285390,127,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3499'),
('LOGIN','2026-10-09 11:06:48',1,6,5,41,991634,285390,128,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3504'),
('LOGOUT','2026-10-09 11:07:29',1,6,5,41,990944,285845,128,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3504'),
('LOGIN','2026-10-09 11:10:10',1,6,5,41,990944,285845,128,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3504'),
('LOGOUT','2026-10-09 11:10:30',1,6,5,41,990944,285845,128,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461','gold: 149367 alignment: 3504');
/*!40000 ALTER TABLE `loginlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loginlog2`
--

DROP TABLE IF EXISTS `loginlog2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `loginlog2` (
  `id` int(11) unsigned NOT NULL,
  `type` enum('INVALID','VALID') NOT NULL DEFAULT 'INVALID',
  `login_time` datetime DEFAULT NULL,
  `logout_time` datetime DEFAULT NULL,
  `playtime` time NOT NULL DEFAULT '00:00:00',
  `channel` tinyint(4) DEFAULT NULL,
  `account_id` int(11) unsigned NOT NULL,
  `pid` int(11) unsigned NOT NULL,
  `ip` varchar(15) NOT NULL DEFAULT '',
  `hwid` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`account_id`,`pid`,`id`),
  KEY `pid_id` (`pid`,`id`),
  KEY `login_time` (`login_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loginlog2`
--

LOCK TABLES `loginlog2` WRITE;
/*!40000 ALTER TABLE `loginlog2` DISABLE KEYS */;
INSERT INTO `loginlog2` VALUES
(1,'INVALID','2026-10-08 23:01:30',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(2,'INVALID','2026-10-08 23:10:13',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(3,'INVALID','2026-10-08 23:16:24',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(4,'VALID','2026-10-08 23:22:11','2026-10-08 23:22:19','00:00:08',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(5,'INVALID','2026-10-08 23:22:35',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(6,'INVALID','2026-10-08 23:26:26',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(7,'INVALID','2026-10-08 23:33:06',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(8,'INVALID','2026-10-08 23:42:42',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(9,'INVALID','2026-10-08 23:43:22',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(10,'INVALID','2026-10-08 23:48:05',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(11,'INVALID','2026-10-08 23:54:55',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(12,'INVALID','2026-10-09 00:03:15',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(13,'INVALID','2026-10-09 00:10:25',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(14,'INVALID','2026-10-09 00:15:29',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(15,'INVALID','2026-10-09 00:18:47',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(16,'INVALID','2026-10-09 00:26:40',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(17,'INVALID','2026-10-09 00:37:23',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(18,'VALID','2026-10-09 00:40:28','2026-10-09 00:42:06','00:01:38',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(19,'INVALID','2026-10-09 00:42:09',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(20,'INVALID','2026-10-09 00:42:21',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(21,'INVALID','2026-10-09 00:43:50',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(22,'INVALID','2026-10-09 01:33:01',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(23,'INVALID','2026-10-09 01:36:37',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(24,'INVALID','2026-10-09 01:42:49',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(25,'INVALID','2026-10-09 01:47:39',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(26,'INVALID','2026-10-09 01:56:28',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(27,'VALID','2026-10-09 07:34:27','2026-10-09 07:34:34','00:00:07',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(28,'VALID','2026-10-09 07:34:51','2026-10-09 07:36:20','00:01:29',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(29,'INVALID','2026-10-09 07:39:38',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(30,'INVALID','2026-10-09 07:40:23',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(31,'INVALID','2026-10-09 07:44:53',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(32,'INVALID','2026-10-09 08:14:55',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(33,'INVALID','2026-10-09 08:15:07',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(34,'INVALID','2026-10-09 08:35:22',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(35,'INVALID','2026-10-09 08:46:29',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(36,'INVALID','2026-10-09 09:09:01',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(37,'INVALID','2026-10-09 09:09:26',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(38,'INVALID','2026-10-09 10:11:46',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(39,'INVALID','2026-10-09 10:12:08',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(40,'INVALID','2026-10-09 11:00:24',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(41,'INVALID','2026-10-09 11:00:58',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(42,'VALID','2026-10-09 11:06:48','2026-10-09 11:07:29','00:00:41',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(43,'INVALID','2026-10-09 11:10:10',NULL,'00:00:00',1,6,5,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461'),
(1,'VALID','2026-10-08 23:05:46','2026-10-08 23:07:31','00:01:45',1,6,6,'127.0.0.1','69746E650000000D178BFBFFFED8320B85394401607C3722_K91C50680103060905-0A00-4D00-6963-726F2D537461');
/*!40000 ALTER TABLE `loginlog2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `market_metric`
--

DROP TABLE IF EXISTS `market_metric`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `market_metric` (
  `time` datetime NOT NULL,
  `channel` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `port` smallint(5) unsigned NOT NULL DEFAULT 0,
  `kind` varchar(16) NOT NULL DEFAULT '',
  `trades` int(10) unsigned NOT NULL DEFAULT 0,
  `items` bigint(20) unsigned NOT NULL DEFAULT 0,
  `amount` bigint(20) NOT NULL DEFAULT 0,
  PRIMARY KEY (`time`,`channel`,`port`,`kind`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `market_metric`
--

LOCK TABLES `market_metric` WRITE;
/*!40000 ALTER TABLE `market_metric` DISABLE KEYS */;
/*!40000 ALTER TABLE `market_metric` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `money_log`
--

DROP TABLE IF EXISTS `money_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `money_log` (
  `time` datetime DEFAULT NULL,
  `type` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `vnum` int(10) unsigned NOT NULL DEFAULT 0,
  `gold` bigint(20) NOT NULL DEFAULT 0,
  KEY `time` (`time`),
  KEY `type_vnum` (`type`,`vnum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `money_log`
--

LOCK TABLES `money_log` WRITE;
/*!40000 ALTER TABLE `money_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `money_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `new_money_log`
--

DROP TABLE IF EXISTS `new_money_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `new_money_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `char_id` int(11) DEFAULT NULL,
  `player_name` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `add_info` varchar(255) DEFAULT NULL,
  `vnum` int(11) DEFAULT NULL,
  `with_id` int(11) DEFAULT NULL,
  `with_name` varchar(255) DEFAULT NULL,
  `transaction_gold` varchar(255) DEFAULT NULL,
  `pgold_before_transaction` varchar(255) DEFAULT NULL,
  `pgold_after_transaction` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `time` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `new_money_log`
--

LOCK TABLES `new_money_log` WRITE;
/*!40000 ALTER TABLE `new_money_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `new_money_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offline_shop`
--

DROP TABLE IF EXISTS `offline_shop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `offline_shop` (
  `owner_pid` int(11) DEFAULT NULL,
  `shop_id` int(11) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `buyer_pid` int(11) DEFAULT NULL,
  `item_id` int(11) DEFAULT NULL,
  `vnum` int(11) DEFAULT NULL,
  `count` int(11) DEFAULT NULL,
  `gold` bigint(20) DEFAULT NULL,
  `cheque` bigint(20) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  KEY `time` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offline_shop`
--

LOCK TABLES `offline_shop` WRITE;
/*!40000 ALTER TABLE `offline_shop` DISABLE KEYS */;
/*!40000 ALTER TABLE `offline_shop` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offlineshop_logs`
--

DROP TABLE IF EXISTS `offlineshop_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `offlineshop_logs` (
  `owner_id` bigint(20) unsigned NOT NULL DEFAULT 0,
  `log_type` varchar(64) NOT NULL DEFAULT '0',
  `log` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `event_date` datetime NOT NULL
) ENGINE=Aria DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci PAGE_CHECKSUM=1 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offlineshop_logs`
--

LOCK TABLES `offlineshop_logs` WRITE;
/*!40000 ALTER TABLE `offlineshop_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `offlineshop_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offlineshop_sold`
--

DROP TABLE IF EXISTS `offlineshop_sold`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `offlineshop_sold` (
  `owner_id` int(10) NOT NULL DEFAULT 0,
  `buyer_name` varchar(24) NOT NULL DEFAULT 'NONAME',
  `sell_price` bigint(20) NOT NULL DEFAULT 0,
  `sell_date` datetime NOT NULL,
  `vnum` int(11) NOT NULL DEFAULT 0,
  `count` int(11) NOT NULL DEFAULT 0,
  `socket0` int(11) NOT NULL DEFAULT 0,
  `socket1` int(11) NOT NULL DEFAULT 0,
  `socket2` int(11) NOT NULL DEFAULT 0,
  `socket3` int(11) NOT NULL DEFAULT 0,
  `socket4` int(11) NOT NULL DEFAULT 0,
  `socket5` int(11) NOT NULL DEFAULT 0,
  `attr0` int(11) NOT NULL DEFAULT 0,
  `attrval0` int(11) NOT NULL DEFAULT 0,
  `attr1` int(11) NOT NULL DEFAULT 0,
  `attrval1` int(11) NOT NULL DEFAULT 0,
  `attr2` int(11) NOT NULL DEFAULT 0,
  `attrval2` int(11) NOT NULL DEFAULT 0,
  `attr3` int(11) NOT NULL DEFAULT 0,
  `attrval3` int(11) NOT NULL DEFAULT 0,
  `attr4` int(11) NOT NULL DEFAULT 0,
  `attrval4` int(11) NOT NULL DEFAULT 0,
  `attr5` int(11) NOT NULL DEFAULT 0,
  `attrval5` int(11) NOT NULL DEFAULT 0,
  `attr6` int(11) NOT NULL DEFAULT 0,
  `attrval6` int(11) NOT NULL DEFAULT 0,
  `attr7` int(11) NOT NULL DEFAULT 0,
  `attrval7` int(11) NOT NULL DEFAULT 0,
  `attr8` int(11) NOT NULL DEFAULT 0,
  `attrval8` int(11) NOT NULL DEFAULT 0,
  `attr9` int(11) NOT NULL DEFAULT 0,
  `attrval9` int(11) NOT NULL DEFAULT 0
) ENGINE=Aria DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci PAGE_CHECKSUM=1 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offlineshop_sold`
--

LOCK TABLES `offlineshop_sold` WRITE;
/*!40000 ALTER TABLE `offlineshop_sold` DISABLE KEYS */;
/*!40000 ALTER TABLE `offlineshop_sold` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `okay_event`
--

DROP TABLE IF EXISTS `okay_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `okay_event` (
  `pid` int(11) DEFAULT NULL,
  `name` varchar(11) DEFAULT NULL,
  `points` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `okay_event`
--

LOCK TABLES `okay_event` WRITE;
/*!40000 ALTER TABLE `okay_event` DISABLE KEYS */;
/*!40000 ALTER TABLE `okay_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `player_hack`
--

DROP TABLE IF EXISTS `player_hack`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_hack` (
  `pid` int(10) NOT NULL,
  `name` varchar(24) NOT NULL,
  `hack_count` int(4) NOT NULL,
  `bot_count` int(4) NOT NULL
) ENGINE=Aria DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci PAGE_CHECKSUM=1 ROW_FORMAT=PAGE TRANSACTIONAL=1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `player_hack`
--

LOCK TABLES `player_hack` WRITE;
/*!40000 ALTER TABLE `player_hack` DISABLE KEYS */;
INSERT INTO `player_hack` VALUES
(1,'MD',0,0),
(2,'MCS',1,0);
/*!40000 ALTER TABLE `player_hack` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quest_reward_log`
--

DROP TABLE IF EXISTS `quest_reward_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `quest_reward_log` (
  `quest_name` varchar(32) NOT NULL DEFAULT '',
  `player_id` int(10) unsigned NOT NULL DEFAULT 0,
  `player_level` int(10) unsigned NOT NULL DEFAULT 0,
  `reward_type` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `reward_value1` bigint(20) NOT NULL DEFAULT 0,
  `reward_value2` int(11) NOT NULL DEFAULT 0,
  `time` datetime DEFAULT NULL,
  KEY `player_id` (`player_id`),
  KEY `time` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quest_reward_log`
--

LOCK TABLES `quest_reward_log` WRITE;
/*!40000 ALTER TABLE `quest_reward_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `quest_reward_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quest_state_log`
--

DROP TABLE IF EXISTS `quest_state_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `quest_state_log` (
  `quest_name` varchar(32) NOT NULL DEFAULT '',
  `quest_state` varchar(64) NOT NULL DEFAULT '',
  `time` datetime DEFAULT NULL,
  `pid` int(10) unsigned NOT NULL DEFAULT 0,
  KEY `pid` (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quest_state_log`
--

LOCK TABLES `quest_state_log` WRITE;
/*!40000 ALTER TABLE `quest_state_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `quest_state_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `refine_metric`
--

DROP TABLE IF EXISTS `refine_metric`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `refine_metric` (
  `time` datetime NOT NULL,
  `channel` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `port` smallint(5) unsigned NOT NULL DEFAULT 0,
  `refine_id` int(10) unsigned NOT NULL DEFAULT 0,
  `how` varchar(32) NOT NULL DEFAULT '',
  `prob` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `attempt` int(10) unsigned NOT NULL DEFAULT 0,
  `success` int(10) unsigned NOT NULL DEFAULT 0,
  `destroyed` int(10) unsigned NOT NULL DEFAULT 0,
  KEY `time` (`time`),
  KEY `refine_id` (`refine_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `refine_metric`
--

LOCK TABLES `refine_metric` WRITE;
/*!40000 ALTER TABLE `refine_metric` DISABLE KEYS */;
/*!40000 ALTER TABLE `refine_metric` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `refinelog`
--

DROP TABLE IF EXISTS `refinelog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `refinelog` (
  `pid` int(10) unsigned NOT NULL DEFAULT 0,
  `item_name` varchar(64) NOT NULL DEFAULT '',
  `item_id` int(10) unsigned NOT NULL DEFAULT 0,
  `step` int(11) NOT NULL DEFAULT 0,
  `time` datetime NOT NULL,
  `is_success` tinyint(1) NOT NULL DEFAULT 0,
  `setType` varchar(32) NOT NULL DEFAULT '',
  KEY `time` (`time`),
  KEY `pid` (`pid`),
  KEY `item_id` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `refinelog`
--

LOCK TABLES `refinelog` WRITE;
/*!40000 ALTER TABLE `refinelog` DISABLE KEYS */;
/*!40000 ALTER TABLE `refinelog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report_player_log`
--

DROP TABLE IF EXISTS `report_player_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `report_player_log` (
  `pid` int(11) NOT NULL DEFAULT 0,
  `target_pid` int(11) NOT NULL DEFAULT 0,
  `target_name` varchar(64) NOT NULL DEFAULT '',
  `reason` varchar(16) NOT NULL DEFAULT '',
  `time` datetime NOT NULL,
  KEY `time` (`time`),
  KEY `target_pid` (`target_pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report_player_log`
--

LOCK TABLES `report_player_log` WRITE;
/*!40000 ALTER TABLE `report_player_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `report_player_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `request_info_log`
--

DROP TABLE IF EXISTS `request_info_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `request_info_log` (
  `pid` int(11) NOT NULL DEFAULT 0,
  `time` datetime NOT NULL,
  `type` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `arg1` varchar(255) NOT NULL DEFAULT '',
  `arg2` varchar(255) NOT NULL DEFAULT '',
  KEY `time` (`time`),
  KEY `pid` (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `request_info_log`
--

LOCK TABLES `request_info_log` WRITE;
/*!40000 ALTER TABLE `request_info_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `request_info_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `speed_hack`
--

DROP TABLE IF EXISTS `speed_hack`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `speed_hack` (
  `pid` int(10) unsigned NOT NULL DEFAULT 0,
  `time` datetime NOT NULL,
  `x` int(10) unsigned NOT NULL DEFAULT 0,
  `y` int(10) unsigned NOT NULL DEFAULT 0,
  `hack_count` int(11) NOT NULL DEFAULT 0,
  KEY `time` (`time`),
  KEY `pid` (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `speed_hack`
--

LOCK TABLES `speed_hack` WRITE;
/*!40000 ALTER TABLE `speed_hack` DISABLE KEYS */;
/*!40000 ALTER TABLE `speed_hack` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trade_info_log`
--

DROP TABLE IF EXISTS `trade_info_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `trade_info_log` (
  `log_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `trade_date` datetime NOT NULL,
  `owner_id` int(10) NOT NULL,
  `owner_name` varchar(24) NOT NULL DEFAULT 'NONAME',
  `owner_gold` bigint(20) NOT NULL,
  `victim_id` int(10) NOT NULL,
  `victim_name` varchar(24) NOT NULL DEFAULT 'NONAME',
  `victim_gold` bigint(20) NOT NULL,
  PRIMARY KEY (`log_id`) USING BTREE
) ENGINE=Aria DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci PAGE_CHECKSUM=1 ROW_FORMAT=PAGE TRANSACTIONAL=1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trade_info_log`
--

LOCK TABLES `trade_info_log` WRITE;
/*!40000 ALTER TABLE `trade_info_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `trade_info_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trade_item_log`
--

DROP TABLE IF EXISTS `trade_item_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `trade_item_log` (
  `log_id` int(10) NOT NULL DEFAULT 0,
  `owner_id` int(10) NOT NULL DEFAULT 0,
  `pos` smallint(2) NOT NULL DEFAULT 0,
  `vnum` int(11) NOT NULL DEFAULT 0,
  `count` int(11) NOT NULL DEFAULT 0,
  `socket0` int(11) NOT NULL DEFAULT 0,
  `socket1` int(11) NOT NULL DEFAULT 0,
  `socket2` int(11) NOT NULL DEFAULT 0,
  `socket3` int(11) NOT NULL DEFAULT 0,
  `socket4` int(11) NOT NULL DEFAULT 0,
  `socket5` int(11) NOT NULL DEFAULT 0,
  `attr0` int(11) NOT NULL DEFAULT 0,
  `attrval0` int(11) NOT NULL DEFAULT 0,
  `attr1` int(11) NOT NULL DEFAULT 0,
  `attrval1` int(11) NOT NULL DEFAULT 0,
  `attr2` int(11) NOT NULL DEFAULT 0,
  `attrval2` int(11) NOT NULL DEFAULT 0,
  `attr3` int(11) NOT NULL DEFAULT 0,
  `attrval3` int(11) NOT NULL DEFAULT 0,
  `attr4` int(11) NOT NULL DEFAULT 0,
  `attrval4` int(11) NOT NULL DEFAULT 0,
  `attr5` int(11) NOT NULL DEFAULT 0,
  `attrval5` int(11) NOT NULL DEFAULT 0,
  `attr6` int(11) NOT NULL DEFAULT 0,
  `attrval6` int(11) NOT NULL DEFAULT 0,
  `attr7` int(11) NOT NULL DEFAULT 0,
  `attrval7` int(11) NOT NULL DEFAULT 0,
  `attr8` int(11) NOT NULL DEFAULT 0,
  `attrval8` int(11) NOT NULL DEFAULT 0,
  `attr9` int(11) NOT NULL DEFAULT 0,
  `attrval9` int(11) NOT NULL DEFAULT 0
) ENGINE=Aria DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci PAGE_CHECKSUM=1 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trade_item_log`
--

LOCK TABLES `trade_item_log` WRITE;
/*!40000 ALTER TABLE `trade_item_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `trade_item_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `voucher_code_log`
--

DROP TABLE IF EXISTS `voucher_code_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `voucher_code_log` (
  `code` varchar(32) NOT NULL DEFAULT '',
  `pid` int(11) NOT NULL DEFAULT 0,
  `account_id` int(11) NOT NULL DEFAULT 0,
  `time` datetime NOT NULL,
  KEY `time` (`time`),
  KEY `code` (`code`),
  KEY `account_id` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `voucher_code_log`
--

LOCK TABLES `voucher_code_log` WRITE;
/*!40000 ALTER TABLE `voucher_code_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `voucher_code_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'log'
--

--
-- Dumping routines for database 'log'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-10-11 22:43:20
