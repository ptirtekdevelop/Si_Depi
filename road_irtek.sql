-- MySQL dump 10.13  Distrib 8.0.35, for Linux (x86_64)
--
-- Host: localhost    Database: IRTEK_ROAD
-- ------------------------------------------------------
-- Server version	8.0.35-0ubuntu0.22.04.1

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
-- Current Database: `IRTEK_ROAD`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `IRTEK_ROAD` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `IRTEK_ROAD`;

--
-- Table structure for table `road_damage`
--

DROP TABLE IF EXISTS `road_damage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `road_damage` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sum_damage` int NOT NULL,
  `type_damage` varchar(100) NOT NULL,
  `road_data_id` varchar(36) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `road_data_id` (`road_data_id`),
  CONSTRAINT `road_damage_ibfk_1` FOREIGN KEY (`road_data_id`) REFERENCES `road_data` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `road_damage`
--

LOCK TABLES `road_damage` WRITE;
/*!40000 ALTER TABLE `road_damage` DISABLE KEYS */;
INSERT INTO `road_damage` VALUES (17,11,'pathole','4b9bd83d-579d-4d6c-8abe-cb4912eda497'),(18,5,'crocodile','4b9bd83d-579d-4d6c-8abe-cb4912eda497'),(19,17,'longitudinal','4b9bd83d-579d-4d6c-8abe-cb4912eda497'),(20,0,'transversal','4b9bd83d-579d-4d6c-8abe-cb4912eda497'),(21,23,'pathole','734c8491-1b8d-4235-94a3-9aa90616f75b'),(22,19,'crocodile','734c8491-1b8d-4235-94a3-9aa90616f75b'),(23,12,'transversal','734c8491-1b8d-4235-94a3-9aa90616f75b'),(24,25,'longitudinal','734c8491-1b8d-4235-94a3-9aa90616f75b'),(25,4,'longitudinal','730b61a7-b7d2-41d9-9c1d-97e223e6b022'),(26,0,'transversal','730b61a7-b7d2-41d9-9c1d-97e223e6b022'),(27,1,'crocodile','730b61a7-b7d2-41d9-9c1d-97e223e6b022'),(28,2,'pathole','730b61a7-b7d2-41d9-9c1d-97e223e6b022'),(29,2,'pathole','7b67df66-cbf2-4e61-8a26-857dd56aa6c1'),(30,0,'crocodile','7b67df66-cbf2-4e61-8a26-857dd56aa6c1'),(31,0,'transversal','7b67df66-cbf2-4e61-8a26-857dd56aa6c1'),(32,16,'longitudinal','7b67df66-cbf2-4e61-8a26-857dd56aa6c1'),(33,0,'pathole','89b40ea9-4e45-4780-8903-872043dce39f'),(34,1,'crocodile','89b40ea9-4e45-4780-8903-872043dce39f'),(35,0,'longitudinal','89b40ea9-4e45-4780-8903-872043dce39f'),(36,3,'transversal','89b40ea9-4e45-4780-8903-872043dce39f');
/*!40000 ALTER TABLE `road_damage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `road_data`
--

DROP TABLE IF EXISTS `road_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `road_data` (
  `id` varchar(36) NOT NULL,
  `province` varchar(64) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `street_name` varchar(200) DEFAULT NULL,
  `video_path` varchar(254) DEFAULT NULL,
  `user_id` int NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `road_data_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `road_data`
--

LOCK TABLES `road_data` WRITE;
/*!40000 ALTER TABLE `road_data` DISABLE KEYS */;
INSERT INTO `road_data` VALUES ('245ccf02-7989-4b50-a69a-375c0e769add','4','Padang','Jl.Andalas',NULL,2,'2023-11-03 05:16:58',NULL),('4b9bd83d-579d-4d6c-8abe-cb4912eda497','4','Padang','Jl.Andalas','video1_anduriang.webm',2,'2023-11-03 05:19:04','2023-11-03 05:31:35'),('730b61a7-b7d2-41d9-9c1d-97e223e6b022','4','Padang','Jl.Dr.Moh.Hatta','video1_bawah.webm',2,'2023-11-03 04:06:41',NULL),('734c8491-1b8d-4235-94a3-9aa90616f75b','4','Padang','Jl.Dr.Moh.Hatta',NULL,2,'2023-11-03 03:22:40',NULL),('7b67df66-cbf2-4e61-8a26-857dd56aa6c1','4','Padang','Jl.Raya Indarung','video1_gadut.webm',2,'2023-11-03 04:47:19',NULL),('89b40ea9-4e45-4780-8903-872043dce39f','2','Test','Test','video0.webm',2,'2023-11-03 07:35:51','2023-11-03 07:37:49');
/*!40000 ALTER TABLE `road_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `email` varchar(128) NOT NULL,
  `password` varchar(128) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  `suspended` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','admin@gmail.com','$2b$12$hpk09w52xMURS9P1u5W4iumMV/IRPB6w4IxLKT/LVzf7YnXcVoRE6','2023-11-03 02:29:13',NULL,0),(2,'irtek','irtek@gmail.com','$2b$12$UFA5cSV//YBBEjWibv0v7OJr/LZGqV2xNSLWWAKbdu4Tx1by9nE86','2023-11-03 02:29:50',NULL,0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-03 14:46:20
