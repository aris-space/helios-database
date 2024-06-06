-- MySQL dump 10.13  Distrib 8.0.29, for Linux (x86_64)
--
-- Host: localhost    Database: dacs
-- ------------------------------------------------------
-- Server version	8.0.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `actuator_values`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `actuator_values` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'primary key',
  `actuator_id` int NOT NULL COMMENT 'which actuator and config',
  `value` float NOT NULL COMMENT 'actuator value',
  `timestamp` double NOT NULL COMMENT 'timestamp',
  PRIMARY KEY (`id`),
  KEY `actuator_id` (`actuator_id`),
  CONSTRAINT `actuator_values_ibfk_1` FOREIGN KEY (`actuator_id`) REFERENCES `actuators` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actuator_values`
--

LOCK TABLES `actuator_values` WRITE;
/*!40000 ALTER TABLE `actuator_values` DISABLE KEYS */;
/*!40000 ALTER TABLE `actuator_values` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `actuators`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `actuators` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'primary key',
  `name` varchar(255) NOT NULL COMMENT 'actuator name',
  `config_id` int NOT NULL COMMENT 'config used',
  PRIMARY KEY (`id`),
  KEY `config_id` (`config_id`),
  CONSTRAINT `actuators_ibfk_1` FOREIGN KEY (`config_id`) REFERENCES `configurations` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actuators`
--

LOCK TABLES `actuators` WRITE;
/*!40000 ALTER TABLE `actuators` DISABLE KEYS */;
/*!40000 ALTER TABLE `actuators` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `actuators_meta`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `actuators_meta` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'primary key',
  `actuator_id` int NOT NULL COMMENT 'which actuator and config',
  `model` varchar(255) DEFAULT NULL COMMENT 'actuator model',
  `number` varchar(255) DEFAULT NULL COMMENT 'actuator serial number',
  `location` varchar(255) DEFAULT NULL COMMENT 'location',
  `ain` varchar(255) DEFAULT NULL COMMENT 'AIN channel',
  `normal_state` varchar(255) DEFAULT NULL COMMENT 'normal state',
  PRIMARY KEY (`id`),
  KEY `actuator_id` (`actuator_id`),
  CONSTRAINT `actuators_meta_ibfk_1` FOREIGN KEY (`actuator_id`) REFERENCES `actuators` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actuators_meta`
--

LOCK TABLES `actuators_meta` WRITE;
/*!40000 ALTER TABLE `actuators_meta` DISABLE KEYS */;
/*!40000 ALTER TABLE `actuators_meta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `configurations`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `configurations` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'primary key',
  `name` varchar(255) NOT NULL COMMENT 'file name of config',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configurations`
--

LOCK TABLES `configurations` WRITE;
/*!40000 ALTER TABLE `configurations` DISABLE KEYS */;
/*!40000 ALTER TABLE `configurations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `phases`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `phases` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'primary key',
  `name` varchar(255) NOT NULL COMMENT 'phase name',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phases`
--

LOCK TABLES `phases` WRITE;
/*!40000 ALTER TABLE `phases` DISABLE KEYS */;
/*!40000 ALTER TABLE `phases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `safety`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `safety` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'primary key',
  `is_warning` tinyint NOT NULL COMMENT 'warning?',
  `is_abort` tinyint NOT NULL COMMENT 'abort?',
  `timestamp` double NOT NULL COMMENT 'timestamp',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `safety`
--

LOCK TABLES `safety` WRITE;
/*!40000 ALTER TABLE `safety` DISABLE KEYS */;
/*!40000 ALTER TABLE `safety` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor_thresholds`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `sensor_thresholds` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'primary key',
  `sensor_id` int NOT NULL COMMENT 'which sensor and config',
  `phase_id` int NOT NULL COMMENT 'which phase',
  `warning_min` float DEFAULT NULL COMMENT 'warning min. threshold',
  `warning_max` float DEFAULT NULL COMMENT 'warning max. threshold',
  `abort_min` float DEFAULT NULL COMMENT 'abort min. threshold',
  `abort_max` float DEFAULT NULL COMMENT 'abort max. threshold',
  PRIMARY KEY (`id`),
  KEY `sensor_id` (`sensor_id`),
  KEY `phase_id` (`phase_id`),
  CONSTRAINT `sensor_thresholds_ibfk_1` FOREIGN KEY (`sensor_id`) REFERENCES `sensors` (`id`),
  CONSTRAINT `sensor_thresholds_ibfk_2` FOREIGN KEY (`phase_id`) REFERENCES `phases` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor_thresholds`
--

LOCK TABLES `sensor_thresholds` WRITE;
/*!40000 ALTER TABLE `sensor_thresholds` DISABLE KEYS */;
/*!40000 ALTER TABLE `sensor_thresholds` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor_values`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `sensor_values` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'primary key',
  `sensor_id` int NOT NULL COMMENT 'which sensor and config',
  `value` float NOT NULL COMMENT 'sensor value',
  `timestamp` double NOT NULL COMMENT 'timestamp',
  PRIMARY KEY (`id`),
  KEY `sensor_id` (`sensor_id`),
  CONSTRAINT `sensor_values_ibfk_1` FOREIGN KEY (`sensor_id`) REFERENCES `sensors` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor_values`
--

LOCK TABLES `sensor_values` WRITE;
/*!40000 ALTER TABLE `sensor_values` DISABLE KEYS */;
/*!40000 ALTER TABLE `sensor_values` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensors`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `sensors` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'primary key',
  `name` varchar(255) NOT NULL COMMENT 'sensor name',
  `config_id` int NOT NULL COMMENT 'config used',
  PRIMARY KEY (`id`),
  KEY `config_id` (`config_id`),
  CONSTRAINT `sensors_ibfk_1` FOREIGN KEY (`config_id`) REFERENCES `configurations` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensors`
--

LOCK TABLES `sensors` WRITE;
/*!40000 ALTER TABLE `sensors` DISABLE KEYS */;
/*!40000 ALTER TABLE `sensors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensors_meta`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `sensors_meta` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'primary key',
  `sensor_id` int NOT NULL COMMENT 'which sensor and config',
  `model` varchar(255) DEFAULT NULL COMMENT 'sensor model',
  `number` varchar(255) DEFAULT NULL COMMENT 'sensor serial number',
  `location` varchar(255) DEFAULT NULL COMMENT 'location',
  `ain` varchar(255) DEFAULT NULL COMMENT 'AIN channel',
  `unit` varchar(255) DEFAULT NULL COMMENT 'unit of measurement',
  PRIMARY KEY (`id`),
  KEY `sensor_id` (`sensor_id`),
  CONSTRAINT `sensors_meta_ibfk_1` FOREIGN KEY (`sensor_id`) REFERENCES `sensors` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensors_meta`
--

LOCK TABLES `sensors_meta` WRITE;
/*!40000 ALTER TABLE `sensors_meta` DISABLE KEYS */;
/*!40000 ALTER TABLE `sensors_meta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `states`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `states` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'primary key',
  `state` varchar(255) NOT NULL COMMENT 'state',
  `timestamp` double NOT NULL COMMENT 'timestamp',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `states`
--

LOCK TABLES `states` WRITE;
/*!40000 ALTER TABLE `states` DISABLE KEYS */;
/*!40000 ALTER TABLE `states` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tests`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `tests` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'primary key',
  `name` varchar(255) NOT NULL COMMENT 'test name',
  `date` date NOT NULL COMMENT 'format: YYYY-MM-DD',
  `starttime` time NOT NULL COMMENT 'format: hh:mm:ss',
  `config_id` int NOT NULL COMMENT 'config used',
  `description` varchar(255) DEFAULT NULL COMMENT 'optional',
  PRIMARY KEY (`id`),
  KEY `config_id` (`config_id`),
  CONSTRAINT `tests_ibfk_1` FOREIGN KEY (`config_id`) REFERENCES `configurations` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tests`
--

LOCK TABLES `tests` WRITE;
/*!40000 ALTER TABLE `tests` DISABLE KEYS */;
/*!40000 ALTER TABLE `tests` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-06-01 13:05:00
