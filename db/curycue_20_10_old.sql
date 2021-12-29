-- MariaDB dump 10.18  Distrib 10.4.17-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: curycue
-- ------------------------------------------------------
-- Server version	10.4.17-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cue`
--

DROP TABLE IF EXISTS `cue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cue` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `order` float DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `memo` text NOT NULL DEFAULT ' ',
  `type` enum('Regular') NOT NULL DEFAULT 'Regular',
  `update_mode` enum('Stored','All') NOT NULL DEFAULT 'Stored',
  `osc_bind` varchar(255) DEFAULT NULL,
  `dmx_bind` int(11) DEFAULT NULL,
  `is_enabled` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id`),
  KEY `order` (`order`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cue`
--

LOCK TABLES `cue` WRITE;
/*!40000 ALTER TABLE `cue` DISABLE KEYS */;
INSERT INTO `cue` VALUES (5,10,'АААААААА','','Regular','Stored',NULL,NULL,1),(6,20,'Ключик 1','','Regular','Stored',NULL,NULL,1),(7,30,'Ключик 3','','Regular','Stored',NULL,NULL,1);
/*!40000 ALTER TABLE `cue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cue_float_data`
--

DROP TABLE IF EXISTS `cue_float_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cue_float_data` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `id_cue` bigint(20) unsigned NOT NULL,
  `id_fixture` bigint(20) unsigned NOT NULL,
  `par_name` varchar(255) NOT NULL,
  `par_value` float DEFAULT 0,
  `fade_in` float DEFAULT 0,
  `fade_out` float DEFAULT 0,
  `delay_in` float DEFAULT 0,
  `delay_out` float DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `Unique_index` (`id_cue`,`id_fixture`,`par_name`),
  KEY `id_fixture` (`id_fixture`) USING BTREE,
  KEY `par_name` (`par_name`) USING BTREE,
  KEY `id_cue` (`id_cue`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=131 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cue_float_data`
--

LOCK TABLES `cue_float_data` WRITE;
/*!40000 ALTER TABLE `cue_float_data` DISABLE KEYS */;
INSERT INTO `cue_float_data` VALUES (5,5,2,'Index',0,1,1,0,0),(100,5,2,'Level',0,1,0,0,0),(114,6,1,'Index',1,1,0,0,0),(115,6,1,'Subindex',1,1,0,0,0),(116,6,1,'Level',0.1,1,0,0,0),(117,6,1,'Level2',0.7,1,0,0,0),(120,7,1,'Index',2,2,0,0,0),(121,7,1,'Subindex',2,1,0,0,0),(122,7,1,'Level',0.4,1,0,0,0),(123,7,1,'Level2',1,1,0,0,0),(124,6,2,'Index',1,1,0,0,0),(125,6,2,'Level',0.536,1,0,0,0),(126,5,1,'Index',0,2,0,0,0),(127,5,1,'Subindex',0,1,0,0,0),(128,5,1,'Level',0,1,0,0,0),(129,5,1,'Level2',0,1,0,0,0);
/*!40000 ALTER TABLE `cue_float_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fixture`
--

DROP TABLE IF EXISTS `fixture`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fixture` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `order` float DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `global_object_location` varchar(255) NOT NULL,
  `type` int(11) DEFAULT 0,
  `is_enabled` int(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_path` (`global_object_location`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fixture`
--

LOCK TABLES `fixture` WRITE;
/*!40000 ALTER TABLE `fixture` DISABLE KEYS */;
INSERT INTO `fixture` VALUES (1,4,'Общий недосвет','op.globlights',0,1),(2,1,'Локальный светик 3','op.locallights',0,1);
/*!40000 ALTER TABLE `fixture` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fixture_float_data`
--

DROP TABLE IF EXISTS `fixture_float_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fixture_float_data` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `id_fixture` bigint(20) unsigned NOT NULL,
  `par_name` varchar(255) NOT NULL,
  `default_value` float DEFAULT 0,
  `is_enabled` int(1) DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `id_fixture` (`id_fixture`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fixture_float_data`
--

LOCK TABLES `fixture_float_data` WRITE;
/*!40000 ALTER TABLE `fixture_float_data` DISABLE KEYS */;
INSERT INTO `fixture_float_data` VALUES (1,1,'Index',0,1),(2,1,'Subindex',0,1),(5,2,'Index',0,1),(9,1,'Level',0.4,1),(17,1,'Level2',0.1,1),(20,2,'Level',1,1);
/*!40000 ALTER TABLE `fixture_float_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `все приборы и их поля`
--

DROP TABLE IF EXISTS `все приборы и их поля`;
/*!50001 DROP VIEW IF EXISTS `все приборы и их поля`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `все приборы и их поля` (
  `name` tinyint NOT NULL,
  `global_object_location` tinyint NOT NULL,
  `par_name` tinyint NOT NULL,
  `type` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `ключи`
--

DROP TABLE IF EXISTS `ключи`;
/*!50001 DROP VIEW IF EXISTS `ключи`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `ключи` (
  `Номер` tinyint NOT NULL,
  `Название` tinyint NOT NULL,
  `Кол-во полей` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `поля внутри ключей`
--

DROP TABLE IF EXISTS `поля внутри ключей`;
/*!50001 DROP VIEW IF EXISTS `поля внутри ключей`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `поля внутри ключей` (
  `Номер` tinyint NOT NULL,
  `Название` tinyint NOT NULL,
  `Девайс` tinyint NOT NULL,
  `Путь к объекту` tinyint NOT NULL,
  `Поле` tinyint NOT NULL,
  `Значение` tinyint NOT NULL,
  `fade_in` tinyint NOT NULL,
  `fade_out` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `все приборы и их поля`
--

/*!50001 DROP TABLE IF EXISTS `все приборы и их поля`*/;
/*!50001 DROP VIEW IF EXISTS `все приборы и их поля`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `все приборы и их поля` AS select `fixture`.`name` AS `name`,`fixture`.`global_object_location` AS `global_object_location`,`fixture_float_data`.`par_name` AS `par_name`,`fixture`.`type` AS `type` from (`fixture` join `fixture_float_data`) where `fixture`.`id` = `fixture_float_data`.`id_fixture` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `ключи`
--

/*!50001 DROP TABLE IF EXISTS `ключи`*/;
/*!50001 DROP VIEW IF EXISTS `ключи`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `ключи` AS select `cue`.`order` AS `Номер`,`cue`.`name` AS `Название`,(select count(0) from `cue_float_data` where `cue_float_data`.`id_cue` = `cue`.`id`) AS `Кол-во полей` from `cue` order by `cue`.`order` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `поля внутри ключей`
--

/*!50001 DROP TABLE IF EXISTS `поля внутри ключей`*/;
/*!50001 DROP VIEW IF EXISTS `поля внутри ключей`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `поля внутри ключей` AS select `cue`.`order` AS `Номер`,`cue`.`name` AS `Название`,`fixture`.`name` AS `Девайс`,`fixture`.`global_object_location` AS `Путь к объекту`,`cue_float_data`.`par_name` AS `Поле`,`cue_float_data`.`par_value` AS `Значение`,`cue_float_data`.`fade_in` AS `fade_in`,`cue_float_data`.`fade_out` AS `fade_out` from ((`cue` join `cue_float_data`) join `fixture`) where `cue`.`id` = `cue_float_data`.`id_cue` and `cue_float_data`.`id_fixture` = `fixture`.`id` order by `cue`.`order` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-10-21 18:56:16
