/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.4.8-MariaDB, for Win64 (AMD64)
--
-- Host: 127.0.0.1    Database: account
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
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `account` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `login` varchar(16) NOT NULL DEFAULT '' COMMENT 'LOGIN_MAX_LEN=30',
  `password` varchar(42) NOT NULL DEFAULT '' COMMENT 'PASSWD_MAX_LEN=16; default 45 size',
  `social_id` varchar(7) NOT NULL DEFAULT '',
  `email` varchar(100) NOT NULL DEFAULT '',
  `status` varchar(8) NOT NULL DEFAULT 'OK',
  `availDt` datetime NOT NULL DEFAULT current_timestamp(),
  `create_time` datetime NOT NULL DEFAULT current_timestamp(),
  `last_play` datetime NOT NULL DEFAULT current_timestamp(),
  `gold_expire` datetime NOT NULL DEFAULT current_timestamp(),
  `silver_expire` datetime NOT NULL DEFAULT current_timestamp(),
  `safebox_expire` datetime NOT NULL DEFAULT current_timestamp(),
  `autoloot_expire` datetime NOT NULL DEFAULT current_timestamp(),
  `fish_mind_expire` datetime NOT NULL DEFAULT current_timestamp(),
  `marriage_fast_expire` datetime NOT NULL DEFAULT current_timestamp(),
  `money_drop_rate_expire` datetime NOT NULL DEFAULT current_timestamp(),
  `real_name` varchar(16) DEFAULT '',
  `question1` varchar(56) DEFAULT NULL,
  `answer1` varchar(56) DEFAULT NULL,
  `question2` varchar(56) DEFAULT NULL,
  `answer2` varchar(56) DEFAULT NULL,
  `cash` int(11) DEFAULT 0,
  `hwidID` int(10) DEFAULT 0,
  `hwidID2` int(10) DEFAULT 0,
  `language` tinyint(4) unsigned NOT NULL DEFAULT 1,
  `votecoins` tinyint(4) NOT NULL DEFAULT 0,
  `vote4date` datetime NOT NULL DEFAULT current_timestamp(),
  `phone1` varchar(20) DEFAULT NULL,
  `referans` varchar(255) DEFAULT NULL,
  `passwordToken` varchar(255) DEFAULT NULL,
  `passwordTokenTime` datetime DEFAULT NULL,
  `pinToken` varchar(255) DEFAULT NULL,
  `pinTokenTime` datetime DEFAULT NULL,
  `emailToken` varchar(255) DEFAULT NULL,
  `emailTokenTime` datetime DEFAULT NULL,
  `newEposta` varchar(255) DEFAULT NULL,
  `deleteCodeTime` datetime DEFAULT NULL,
  `safeBoxCodeTime` datetime DEFAULT NULL,
  `securityPasswordCodeTime` datetime DEFAULT NULL,
  `sozlesme` int(11) DEFAULT NULL,
  `oldPassword` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `login` (`login`) USING BTREE,
  KEY `social_id` (`social_id`) USING BTREE
) ENGINE=Aria AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci PAGE_CHECKSUM=1 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
INSERT INTO `account` VALUES
(1,'md','*27AEDA0D3A56422C3F1D20DAFF0C8109058134F3','','','OK','2024-09-10 22:31:07','2024-09-10 22:31:07','2024-09-10 22:33:18','2024-09-10 22:31:07','2024-09-10 22:31:07','2024-09-10 22:31:07','2024-09-10 22:31:07','2024-09-10 22:31:07','2024-09-10 22:31:07','2024-09-10 22:31:07','',NULL,NULL,NULL,NULL,0,1,0,11,0,'2024-09-10 22:31:07',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
(2,'mcs','*23AE809DDACAF96AF0FD78ED04B6A265E05AA257','1234567','','OK','2026-10-11 00:02:18','2026-10-11 00:02:18','2026-10-11 14:47:32','2026-10-11 00:02:18','2026-10-11 00:02:18','2026-10-11 00:02:18','2026-10-11 00:02:18','2026-10-11 00:02:18','2026-10-11 00:02:18','2026-10-11 00:02:18','',NULL,NULL,NULL,NULL,0,2,0,11,0,'2026-10-11 00:02:18',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_block`
--

DROP TABLE IF EXISTS `account_block`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_block` (
  `account_id` int(11) NOT NULL,
  `ban_duration` int(11) NOT NULL DEFAULT 0,
  `pid` int(11) NOT NULL DEFAULT 0,
  `who` int(11) NOT NULL DEFAULT 0,
  `reason` varchar(255) NOT NULL DEFAULT '',
  `status` tinyint(1) NOT NULL DEFAULT 0,
  `flush_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_block`
--

LOCK TABLES `account_block` WRITE;
/*!40000 ALTER TABLE `account_block` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_block` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `block_exception`
--

DROP TABLE IF EXISTS `block_exception`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `block_exception` (
  `login` varchar(16) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `block_exception`
--

LOCK TABLES `block_exception` WRITE;
/*!40000 ALTER TABLE `block_exception` DISABLE KEYS */;
/*!40000 ALTER TABLE `block_exception` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `davet_kodu`
--

DROP TABLE IF EXISTS `davet_kodu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `davet_kodu` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `kod` varchar(16) NOT NULL,
  `aciklama` varchar(128) NOT NULL DEFAULT '',
  `olusturan` varchar(32) NOT NULL DEFAULT '',
  `olusturuldu` datetime NOT NULL DEFAULT current_timestamp(),
  `son_kullanma` datetime NOT NULL,
  `iptal` tinyint(1) NOT NULL DEFAULT 0,
  `kullanildi` datetime DEFAULT NULL,
  `kullanan_hesap_id` int(11) unsigned DEFAULT NULL,
  `kullanan_login` varchar(16) NOT NULL DEFAULT '',
  `kullanan_ip` varchar(15) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `kod` (`kod`),
  KEY `kullanan_ip` (`kullanan_ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `davet_kodu`
--

LOCK TABLES `davet_kodu` WRITE;
/*!40000 ALTER TABLE `davet_kodu` DISABLE KEYS */;
/*!40000 ALTER TABLE `davet_kodu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dungeon_hwid_time`
--

DROP TABLE IF EXISTS `dungeon_hwid_time`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `dungeon_hwid_time` (
  `hwidID` int(11) NOT NULL,
  `d0` int(11) DEFAULT 0,
  `d1` int(11) DEFAULT 0,
  `d2` int(11) DEFAULT 0
) ENGINE=Aria DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci PAGE_CHECKSUM=1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dungeon_hwid_time`
--

LOCK TABLES `dungeon_hwid_time` WRITE;
/*!40000 ALTER TABLE `dungeon_hwid_time` DISABLE KEYS */;
/*!40000 ALTER TABLE `dungeon_hwid_time` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gametime`
--

DROP TABLE IF EXISTS `gametime`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `gametime` (
  `UserID` varchar(16) NOT NULL DEFAULT '',
  `paymenttype` tinyint(2) NOT NULL DEFAULT 1,
  `LimitTime` int(11) unsigned DEFAULT 0,
  `LimitDt` datetime DEFAULT current_timestamp(),
  `Scores` int(11) DEFAULT 0,
  PRIMARY KEY (`UserID`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gametime`
--

LOCK TABLES `gametime` WRITE;
/*!40000 ALTER TABLE `gametime` DISABLE KEYS */;
/*!40000 ALTER TABLE `gametime` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gametimeip`
--

DROP TABLE IF EXISTS `gametimeip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `gametimeip` (
  `ipid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) DEFAULT NULL,
  `ip` varchar(15) NOT NULL DEFAULT '000.000.000.000',
  `startIP` int(11) NOT NULL DEFAULT 0,
  `endIP` int(11) NOT NULL DEFAULT 255,
  `paymenttype` tinyint(2) NOT NULL DEFAULT 1,
  `LimitTime` int(11) NOT NULL DEFAULT 0,
  `LimitDt` datetime NOT NULL DEFAULT current_timestamp(),
  `readme` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`ipid`) USING BTREE,
  UNIQUE KEY `ip_uniq` (`ip`,`startIP`,`endIP`) USING BTREE,
  KEY `ip_idx` (`ip`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gametimeip`
--

LOCK TABLES `gametimeip` WRITE;
/*!40000 ALTER TABLE `gametimeip` DISABLE KEYS */;
/*!40000 ALTER TABLE `gametimeip` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gametimelog`
--

DROP TABLE IF EXISTS `gametimelog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `gametimelog` (
  `login` varchar(16) DEFAULT NULL,
  `type` enum('IP_FREE','FREE','IP_TIME','IP_DAY','TIME','DAY') DEFAULT NULL,
  `logon_time` datetime NOT NULL DEFAULT current_timestamp(),
  `logout_time` datetime NOT NULL DEFAULT current_timestamp(),
  `use_time` int(11) unsigned DEFAULT NULL,
  `ip` varchar(15) NOT NULL DEFAULT '000.000.000.000',
  `server` varchar(56) NOT NULL DEFAULT '',
  KEY `login_key` (`login`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gametimelog`
--

LOCK TABLES `gametimelog` WRITE;
/*!40000 ALTER TABLE `gametimelog` DISABLE KEYS */;
/*!40000 ALTER TABLE `gametimelog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hardware_status`
--

DROP TABLE IF EXISTS `hardware_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `hardware_status` (
  `hwid` varchar(255) NOT NULL,
  `status` varchar(8) NOT NULL DEFAULT 'OK',
  PRIMARY KEY (`hwid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hardware_status`
--

LOCK TABLES `hardware_status` WRITE;
/*!40000 ALTER TABLE `hardware_status` DISABLE KEYS */;
/*!40000 ALTER TABLE `hardware_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hwid_ban_list`
--

DROP TABLE IF EXISTS `hwid_ban_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `hwid_ban_list` (
  `hwid` varchar(64) DEFAULT NULL
) ENGINE=Aria DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci PAGE_CHECKSUM=1 ROW_FORMAT=PAGE TRANSACTIONAL=1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hwid_ban_list`
--

LOCK TABLES `hwid_ban_list` WRITE;
/*!40000 ALTER TABLE `hwid_ban_list` DISABLE KEYS */;
/*!40000 ALTER TABLE `hwid_ban_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hwid_list`
--

DROP TABLE IF EXISTS `hwid_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `hwid_list` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `hwid` varchar(64) DEFAULT NULL,
  `vote_buff_type` int(1) DEFAULT 0,
  `vote_buff_time` bigint(20) DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=Aria AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci PAGE_CHECKSUM=1 ROW_FORMAT=PAGE TRANSACTIONAL=1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hwid_list`
--

LOCK TABLES `hwid_list` WRITE;
/*!40000 ALTER TABLE `hwid_list` DISABLE KEYS */;
INSERT INTO `hwid_list` VALUES
(1,'TbGNUSiegA18PzB6Swh2hAoNnbd97Sj8hzZzeY7gmqc=',0,0),
(2,'UpTMR/hsbhA2zFrzzkG+E7o9RFhjAoewHwgQOLiTGBo=',0,0);
/*!40000 ALTER TABLE `hwid_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `iptocountry`
--

DROP TABLE IF EXISTS `iptocountry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `iptocountry` (
  `IP_FROM` varchar(16) DEFAULT NULL,
  `IP_TO` varchar(16) DEFAULT NULL,
  `COUNTRY_NAME` varchar(56) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iptocountry`
--

LOCK TABLES `iptocountry` WRITE;
/*!40000 ALTER TABLE `iptocountry` DISABLE KEYS */;
/*!40000 ALTER TABLE `iptocountry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `string`
--

DROP TABLE IF EXISTS `string`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `string` (
  `name` varchar(64) NOT NULL DEFAULT '',
  `text` mediumtext DEFAULT NULL,
  PRIMARY KEY (`name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `string`
--

LOCK TABLES `string` WRITE;
/*!40000 ALTER TABLE `string` DISABLE KEYS */;
/*!40000 ALTER TABLE `string` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'account'
--

--
-- Dumping routines for database 'account'
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
