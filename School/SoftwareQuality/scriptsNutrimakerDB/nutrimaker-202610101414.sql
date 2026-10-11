-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: nutrimaker
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

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
-- Table structure for table `comida`
--

DROP TABLE IF EXISTS `comida`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comida` (
  `ID_COMIDA` int(11) NOT NULL,
  `ID_DIETA` int(11) DEFAULT NULL,
  `DIA_SEMANA` tinyint(3) unsigned DEFAULT NULL,
  `HORA` time DEFAULT NULL,
  `TIPO_COMIDA` varchar(10) DEFAULT NULL,
  `GRUPO_COMIDA` varchar(15) DEFAULT NULL,
  `CALORIAS` decimal(9,4) DEFAULT NULL,
  `GRASAS` decimal(9,4) DEFAULT NULL,
  `COLESTEROL` decimal(9,4) DEFAULT NULL,
  `SODIO` decimal(9,4) DEFAULT NULL,
  `CARBOHIDRATOS` decimal(9,4) DEFAULT NULL,
  `PROTEINA` decimal(9,4) DEFAULT NULL,
  `CALCIO` decimal(9,4) DEFAULT NULL,
  `HIERRO` decimal(9,4) DEFAULT NULL,
  `NOMBRE_COMIDA` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID_COMIDA`),
  KEY `FK_COMIDA_DIETA` (`ID_DIETA`),
  CONSTRAINT `FK_COMIDA_DIETA` FOREIGN KEY (`ID_DIETA`) REFERENCES `dieta` (`ID_DIETA`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comida`
--

LOCK TABLES `comida` WRITE;
/*!40000 ALTER TABLE `comida` DISABLE KEYS */;
INSERT INTO `comida` VALUES (1,1,NULL,'08:00:00','Desayuno','Avena',508.7221,4.8682,0.0000,328.6004,94.9290,29.2089,65.7201,2.4341,'Egg White Oatmeal with Blueberries - Plan 01'),(2,1,NULL,'14:00:00','Cena','Ensalada',691.2779,38.9452,109.5335,408.9249,46.2475,46.2475,331.0345,4.8682,'Veggie & Chicken Salad - Plan 01'),(3,2,NULL,'08:00:00','Desayuno','Yogur',627.4563,13.1898,20.7268,173.3513,82.9071,52.7591,NULL,NULL,'Breakfast Parfait - Plan 02'),(4,2,NULL,'14:00:00','Cena','Ensalada',772.5437,58.4118,184.6568,446.5680,7.5370,56.5276,92.3284,1.8843,'Basic Chicken Salad - Plan 02'),(5,3,NULL,'08:00:00','Desayuno','Huevo y avena',994.5946,32.4324,467.0270,1234.5946,131.8919,54.0541,521.0811,6.4865,'Eggs and Oatmeal - Plan 03'),(6,3,NULL,'14:00:00','Cena','Ensalada',605.4054,30.2703,192.4324,614.0541,19.4595,60.5405,38.9189,2.1622,'Bistro Chicken Salad - Plan 03'),(7,4,NULL,'08:00:00','Desayuno','Avena',422.6966,4.0449,0.0000,273.0337,78.8764,24.2697,54.6067,2.0225,'Egg White Oatmeal with Blueberries - Plan 04'),(8,4,NULL,'13:00:00','Comida','Ensalada',829.2135,62.6966,198.2022,479.3258,8.0899,60.6742,99.1011,2.0225,'Basic Chicken Salad - Plan 04'),(9,4,NULL,'19:00:00','Cena','Ensalada',548.0899,30.3371,182.0225,768.5393,14.1573,60.6742,204.2697,2.0225,'Balsamic Parmesan Chicken Salad - Plan 04'),(10,5,NULL,'08:00:00','Desayuno','Yogur',742.4749,15.6076,24.5262,205.1282,98.1048,62.4303,NULL,NULL,'Breakfast Parfait - Plan 05'),(11,5,NULL,'13:00:00','Comida','Ensalada',633.2218,35.6745,100.3344,374.5819,42.3634,42.3634,303.2330,4.4593,'Veggie & Chicken Salad - Plan 05'),(12,5,NULL,'19:00:00','Cena','Ensalada',624.3032,31.2152,198.4392,633.2218,20.0669,62.4303,40.1338,2.2297,'Bistro Chicken Salad - Plan 05'),(13,6,NULL,'08:00:00','Desayuno','Huevo y avena',876.9497,28.5962,411.7851,1088.5615,116.2912,47.6603,459.4454,5.7192,'Eggs and Oatmeal - Plan 06'),(14,6,NULL,'13:00:00','Comida','Ensalada',781.6291,59.0988,186.8284,451.8198,7.6256,57.1924,93.4142,1.9064,'Basic Chicken Salad - Plan 06'),(15,6,NULL,'19:00:00','Cena','Ensalada',541.4211,30.5026,85.7886,320.2773,36.2218,36.2218,259.2721,3.8128,'Veggie & Chicken Salad - Plan 06'),(16,7,NULL,'08:00:00','Desayuno','Avena',430.1131,15.4162,6.1665,55.4985,55.4985,26.2076,178.8284,3.0832,'Peanut Butter Yogurt Oatmeal - Plan 07'),(17,7,NULL,'13:00:00','Comida','Ensalada',632.0658,47.7903,151.0791,365.3649,6.1665,46.2487,75.5396,1.5416,'Basic Chicken Salad - Plan 07'),(18,7,NULL,'19:00:00','Cena','Ensalada',437.8212,24.6660,69.3731,258.9928,29.2909,29.2909,209.6608,3.0832,'Veggie & Chicken Salad - Plan 07'),(19,8,NULL,'08:00:00','Desayuno','Yogur',394.6217,8.2954,13.0356,109.0246,52.1422,33.1814,NULL,NULL,'Breakfast Parfait - Plan 08'),(20,8,NULL,'10:30:00','Colacion','Avena',247.6755,2.3701,0.0000,159.9818,46.2170,14.2206,31.9964,1.1851,'Egg White Oatmeal with Blueberries - Plan 08'),(21,8,NULL,'14:00:00','Comida','Ensalada',336.5542,18.9608,53.3273,199.0884,22.5160,22.5160,161.1668,2.3701,'Veggie & Chicken Salad - Plan 08'),(22,8,NULL,'19:00:00','Cena','Ensalada',321.1486,17.7758,106.6545,450.3191,8.2954,35.5515,119.6901,1.1851,'Balsamic Parmesan Chicken Salad - Plan 08'),(23,9,NULL,'08:00:00','Desayuno','Huevo y avena',545.3278,17.7824,256.0669,676.9177,72.3152,29.6374,285.7043,3.5565,'Eggs and Oatmeal - Plan 09'),(24,9,NULL,'10:30:00','Colacion','Ensalada',331.9386,16.5969,105.5091,336.6806,10.6695,33.1939,21.3389,1.1855,'Bistro Chicken Salad - Plan 09'),(25,9,NULL,'14:00:00','Comida','Ensalada',336.6806,18.9679,53.3473,199.1632,22.5244,22.5244,161.2273,2.3710,'Veggie & Chicken Salad - Plan 09'),(26,9,NULL,'19:00:00','Cena','Ensalada',486.0530,36.7503,116.1785,280.9623,4.7420,35.5649,58.0893,1.1855,'Basic Chicken Salad - Plan 09'),(27,10,NULL,'08:00:00','Desayuno','Huevo y avena',648.3680,21.1424,304.4510,804.8220,85.9792,35.2374,339.6884,4.2285,'Eggs and Oatmeal - Plan 10'),(28,10,NULL,'10:30:00','Colacion','Yogur',469.3620,9.8665,15.5045,129.6736,62.0178,39.4659,NULL,NULL,'Breakfast Parfait - Plan 10'),(29,10,NULL,'14:00:00','Comida','Ensalada',381.9733,21.1424,126.8546,535.6083,9.8665,42.2849,142.3591,1.4095,'Balsamic Parmesan Chicken Salad - Plan 10'),(30,10,NULL,'19:00:00','Cena','Ensalada',400.2967,22.5519,63.4273,236.7953,26.7804,26.7804,191.6914,2.8190,'Veggie & Chicken Salad - Plan 10'),(31,11,NULL,'08:00:00','Desayuno','Huevo y avena',550.7412,17.9590,258.6089,683.6374,73.0331,29.9316,288.5405,3.5918,'Eggs and Oatmeal - Plan 11'),(32,11,NULL,'10:30:00','Colacion','Yogur',398.6887,8.3808,13.1699,110.1482,52.6796,33.5234,NULL,NULL,'Breakfast Parfait - Plan 11'),(33,11,NULL,'13:00:00','Comida','Ensalada',490.8780,37.1152,117.3318,283.7514,4.7891,35.9179,58.6659,1.1973,'Basic Chicken Salad - Plan 11'),(34,11,NULL,'16:30:00','Colacion','Ensalada',335.2338,16.7617,106.5564,340.0228,10.7754,33.5234,21.5507,1.1973,'Bistro Chicken Salad - Plan 11'),(35,11,NULL,'19:00:00','Cena','Ensalada',324.4584,17.9590,107.7537,454.9601,8.3808,35.9179,120.9236,1.1973,'Balsamic Parmesan Chicken Salad - Plan 11'),(36,12,NULL,'08:00:00','Desayuno','Huevo y avena',617.6299,20.1401,290.0175,766.6667,81.9031,33.5668,323.5844,4.0280,'Eggs and Oatmeal - Plan 12'),(37,12,NULL,'10:30:00','Colacion','Avena',374.6060,13.4267,5.3707,48.3363,48.3363,22.8255,155.7501,2.6853,'Peanut Butter Yogurt Oatmeal - Plan 12'),(38,12,NULL,'13:00:00','Comida','Ensalada',550.4962,41.6229,131.5820,318.2137,5.3707,40.2802,65.7910,1.3427,'Basic Chicken Salad - Plan 12'),(39,12,NULL,'16:30:00','Colacion','Ensalada',381.3193,21.4828,60.4203,225.5692,25.5108,25.5108,182.6036,2.6853,'Veggie & Chicken Salad - Plan 12'),(40,12,NULL,'19:00:00','Cena','Ensalada',375.9486,18.7974,119.4980,381.3193,12.0841,37.5949,24.1681,1.3427,'Bistro Chicken Salad - Plan 12'),(41,13,NULL,'08:00:00','Desayuno','Yogur',310.1796,6.5203,10.2462,85.6953,40.9847,26.0812,NULL,NULL,'Breakfast Parfait - Plan 13'),(42,13,NULL,'10:30:00','Colacion','Avena',194.6773,1.8629,0.0000,125.7485,36.3273,11.1776,25.1497,0.9315,'Egg White Oatmeal with Blueberries - Plan 13'),(43,13,NULL,'13:00:00','Comida','Ensalada',381.9029,28.8756,91.2841,220.7585,3.7259,27.9441,45.6420,0.9315,'Basic Chicken Salad - Plan 13'),(44,13,NULL,'16:30:00','Colacion','Ensalada',260.8117,13.0406,82.9009,264.5376,8.3832,26.0812,16.7665,0.9315,'Bistro Chicken Salad - Plan 13'),(45,13,NULL,'19:00:00','Cena','Ensalada',252.4285,13.9721,83.8323,353.9587,6.5203,27.9441,94.0785,0.9315,'Balsamic Parmesan Chicken Salad - Plan 13'),(46,14,NULL,'08:00:00','Desayuno','Huevo y avena',584.6467,19.0646,274.5297,725.7245,77.5292,31.7743,306.3040,3.8129,'Eggs and Oatmeal - Plan 14'),(47,14,NULL,'10:00:00','Colacion','Yogur',423.2333,8.8968,13.9807,116.9293,55.9227,35.5872,NULL,NULL,'Breakfast Parfait - Plan 14'),(48,14,NULL,'13:00:00','Comida','Avena',265.6329,2.5419,0.0000,171.5811,49.5679,15.2517,34.3162,1.2710,'Egg White Oatmeal with Blueberries - Plan 14'),(49,14,NULL,'16:00:00','Colacion','Ensalada',521.0981,39.4001,124.5552,301.2201,5.0839,38.1291,62.2776,1.2710,'Basic Chicken Salad - Plan 14'),(50,14,NULL,'19:00:00','Cena','Ensalada',360.9558,20.3355,57.1937,213.5231,24.1484,24.1484,172.8521,2.5419,'Veggie & Chicken Salad - Plan 14'),(51,14,NULL,'21:00:00','Colacion','Ensalada',344.4331,19.0646,114.3874,482.9690,8.8968,38.1291,128.3681,1.2710,'Balsamic Parmesan Chicken Salad - Plan 14'),(52,15,NULL,'08:00:00','Desayuno','Huevo y avena',434.1898,14.1584,203.8804,538.9617,57.5773,23.5973,227.4777,2.8317,'Eggs and Oatmeal - Plan 15'),(53,15,NULL,'10:00:00','Colacion','Avena',263.3456,9.4389,3.7756,33.9801,33.9801,16.0461,109.4913,1.8878,'Peanut Butter Yogurt Oatmeal - Plan 15'),(54,15,NULL,'13:00:00','Comida','Yogur',314.3157,6.6072,10.3828,86.8380,41.5312,26.4289,NULL,NULL,'Breakfast Parfait - Plan 15'),(55,15,NULL,'16:00:00','Colacion','Ensalada',264.2895,13.2145,84.0063,268.0650,8.4950,26.4289,16.9900,0.9439,'Bistro Chicken Salad - Plan 15'),(56,15,NULL,'19:00:00','Cena','Ensalada',268.0650,15.1023,42.4751,158.5737,17.9339,17.9339,128.3692,1.8878,'Veggie & Chicken Salad - Plan 15'),(57,15,NULL,'21:00:00','Colacion','Ensalada',255.7944,14.1584,84.9502,358.6786,6.6072,28.3167,95.3330,0.9439,'Balsamic Parmesan Chicken Salad - Plan 15'),(58,16,NULL,'08:00:00','Desayuno','Huevo y avena',550.7412,17.9590,258.6089,683.6374,73.0331,29.9316,288.5405,3.5918,'Eggs and Oatmeal - Plan 11'),(59,16,NULL,'11:00:00','Colacion','Ensalada',264.2895,13.2145,84.0063,268.0650,8.4950,26.4289,16.9900,0.9439,'Bistro Chicken Salad - Plan 15'),(60,16,NULL,'14:00:00','Comida','Ensalada',490.8780,37.1152,117.3318,283.7514,4.7891,35.9179,58.6659,1.1973,'Basic Chicken Salad - Plan 11'),(61,16,NULL,'17:00:00','Colacion','Avena',263.3456,9.4389,3.7756,33.9801,33.9801,16.0461,109.4913,1.8878,'Peanut Butter Yogurt Oatmeal - Plan 15'),(62,16,NULL,'20:00:00','Cena','Ensalada',375.9486,18.7974,119.4980,381.3193,12.0841,37.5949,24.1681,1.3427,'Bistro Chicken Salad - Plan 12'),(63,17,1,'08:00:00','Desayuno','Huevo y avena',434.1898,14.1584,203.8804,538.9617,57.5773,23.5973,227.4777,2.8317,'Eggs and Oatmeal - Plan 15'),(64,17,1,'14:00:00','Comida','Ensalada',550.4962,41.6229,131.5820,318.2137,5.3707,40.2802,65.7910,1.3427,'Basic Chicken Salad - Plan 12'),(65,17,1,'20:00:00','Cena','Ensalada',437.8212,24.6660,69.3731,258.9928,29.2909,29.2909,209.6608,3.0832,'Veggie & Chicken Salad - Plan 07'),(66,17,2,'08:00:00','Desayuno','Huevo y avena',434.1898,14.1584,203.8804,538.9617,57.5773,23.5973,227.4777,2.8317,'Eggs and Oatmeal - Plan 15'),(67,17,2,'14:00:00','Comida','Ensalada',550.4962,41.6229,131.5820,318.2137,5.3707,40.2802,65.7910,1.3427,'Basic Chicken Salad - Plan 12'),(68,17,2,'20:00:00','Cena','Ensalada',437.8212,24.6660,69.3731,258.9928,29.2909,29.2909,209.6608,3.0832,'Veggie & Chicken Salad - Plan 07'),(69,17,3,'08:00:00','Desayuno','Huevo y avena',434.1898,14.1584,203.8804,538.9617,57.5773,23.5973,227.4777,2.8317,'Eggs and Oatmeal - Plan 15'),(70,17,3,'14:00:00','Comida','Ensalada',550.4962,41.6229,131.5820,318.2137,5.3707,40.2802,65.7910,1.3427,'Basic Chicken Salad - Plan 12'),(71,17,3,'20:00:00','Cena','Ensalada',437.8212,24.6660,69.3731,258.9928,29.2909,29.2909,209.6608,3.0832,'Veggie & Chicken Salad - Plan 07'),(72,17,4,'08:00:00','Desayuno','Huevo y avena',434.1898,14.1584,203.8804,538.9617,57.5773,23.5973,227.4777,2.8317,'Eggs and Oatmeal - Plan 15'),(73,17,4,'14:00:00','Comida','Ensalada',550.4962,41.6229,131.5820,318.2137,5.3707,40.2802,65.7910,1.3427,'Basic Chicken Salad - Plan 12'),(74,17,4,'20:00:00','Cena','Ensalada',437.8212,24.6660,69.3731,258.9928,29.2909,29.2909,209.6608,3.0832,'Veggie & Chicken Salad - Plan 07'),(75,17,5,'08:00:00','Desayuno','Huevo y avena',434.1898,14.1584,203.8804,538.9617,57.5773,23.5973,227.4777,2.8317,'Eggs and Oatmeal - Plan 15'),(76,17,5,'14:00:00','Comida','Ensalada',550.4962,41.6229,131.5820,318.2137,5.3707,40.2802,65.7910,1.3427,'Basic Chicken Salad - Plan 12'),(77,17,5,'20:00:00','Cena','Ensalada',437.8212,24.6660,69.3731,258.9928,29.2909,29.2909,209.6608,3.0832,'Veggie & Chicken Salad - Plan 07'),(78,17,6,'08:00:00','Desayuno','Huevo y avena',434.1898,14.1584,203.8804,538.9617,57.5773,23.5973,227.4777,2.8317,'Eggs and Oatmeal - Plan 15'),(79,17,6,'14:00:00','Comida','Ensalada',550.4962,41.6229,131.5820,318.2137,5.3707,40.2802,65.7910,1.3427,'Basic Chicken Salad - Plan 12'),(80,17,6,'20:00:00','Cena','Ensalada',437.8212,24.6660,69.3731,258.9928,29.2909,29.2909,209.6608,3.0832,'Veggie & Chicken Salad - Plan 07'),(81,17,7,'08:00:00','Desayuno','Huevo y avena',434.1898,14.1584,203.8804,538.9617,57.5773,23.5973,227.4777,2.8317,'Eggs and Oatmeal - Plan 15'),(82,17,7,'14:00:00','Comida','Ensalada',550.4962,41.6229,131.5820,318.2137,5.3707,40.2802,65.7910,1.3427,'Basic Chicken Salad - Plan 12'),(83,17,7,'20:00:00','Cena','Ensalada',437.8212,24.6660,69.3731,258.9928,29.2909,29.2909,209.6608,3.0832,'Veggie & Chicken Salad - Plan 07'),(84,18,1,'08:00:00','Desayuno','Avena',422.6966,4.0449,0.0000,273.0337,78.8764,24.2697,54.6067,2.0225,'Egg White Oatmeal with Blueberries - Plan 04'),(85,18,1,'14:00:00','Comida','Ensalada',336.5542,18.9608,53.3273,199.0884,22.5160,22.5160,161.1668,2.3701,'Veggie & Chicken Salad - Plan 08'),(86,18,1,'20:00:00','Cena','Ensalada',437.8212,24.6660,69.3731,258.9928,29.2909,29.2909,209.6608,3.0832,'Veggie & Chicken Salad - Plan 07'),(87,18,2,'08:00:00','Desayuno','Avena',430.1131,15.4162,6.1665,55.4985,55.4985,26.2076,178.8284,3.0832,'Peanut Butter Yogurt Oatmeal - Plan 07'),(88,18,2,'14:00:00','Comida','Ensalada',336.6806,18.9679,53.3473,199.1632,22.5244,22.5244,161.2273,2.3710,'Veggie & Chicken Salad - Plan 09'),(89,18,2,'20:00:00','Cena','Ensalada',321.1486,17.7758,106.6545,450.3191,8.2954,35.5515,119.6901,1.1851,'Balsamic Parmesan Chicken Salad - Plan 08'),(90,18,3,'08:00:00','Desayuno','Yogur',394.6217,8.2954,13.0356,109.0246,52.1422,33.1814,NULL,NULL,'Breakfast Parfait - Plan 08'),(91,18,3,'14:00:00','Comida','Ensalada',381.9733,21.1424,126.8546,535.6083,9.8665,42.2849,142.3591,1.4095,'Balsamic Parmesan Chicken Salad - Plan 10'),(92,18,3,'20:00:00','Cena','Ensalada',400.2967,22.5519,63.4273,236.7953,26.7804,26.7804,191.6914,2.8190,'Veggie & Chicken Salad - Plan 10'),(93,18,4,'08:00:00','Desayuno','Yogur',310.1796,6.5203,10.2462,85.6953,40.9847,26.0812,NULL,NULL,'Breakfast Parfait - Plan 13'),(94,18,4,'14:00:00','Comida','Ensalada',490.8780,37.1152,117.3318,283.7514,4.7891,35.9179,58.6659,1.1973,'Basic Chicken Salad - Plan 11'),(95,18,4,'20:00:00','Cena','Ensalada',324.4584,17.9590,107.7537,454.9601,8.3808,35.9179,120.9236,1.1973,'Balsamic Parmesan Chicken Salad - Plan 11'),(96,18,5,'08:00:00','Desayuno','Huevo y avena',434.1898,14.1584,203.8804,538.9617,57.5773,23.5973,227.4777,2.8317,'Eggs and Oatmeal - Plan 15'),(97,18,5,'14:00:00','Comida','Ensalada',550.4962,41.6229,131.5820,318.2137,5.3707,40.2802,65.7910,1.3427,'Basic Chicken Salad - Plan 12'),(98,18,5,'20:00:00','Cena','Ensalada',375.9486,18.7974,119.4980,381.3193,12.0841,37.5949,24.1681,1.3427,'Bistro Chicken Salad - Plan 12'),(99,18,6,'08:00:00','Desayuno','Huevo y avena',434.1898,14.1584,203.8804,538.9617,57.5773,23.5973,227.4777,2.8317,'Eggs and Oatmeal - Plan 15'),(100,18,6,'14:00:00','Comida','Ensalada',381.9029,28.8756,91.2841,220.7585,3.7259,27.9441,45.6420,0.9315,'Basic Chicken Salad - Plan 13'),(101,18,6,'20:00:00','Cena','Ensalada',252.4285,13.9721,83.8323,353.9587,6.5203,27.9441,94.0785,0.9315,'Balsamic Parmesan Chicken Salad - Plan 13');
/*!40000 ALTER TABLE `comida` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dieta`
--

DROP TABLE IF EXISTS `dieta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dieta` (
  `ID_DIETA` int(11) NOT NULL,
  `ID_USUARIO` int(11) DEFAULT NULL,
  `ID_PACIENTE` int(11) DEFAULT NULL,
  `CALORIAS` decimal(9,4) DEFAULT NULL,
  `GRASAS` decimal(9,4) DEFAULT NULL,
  `COLESTEROL` decimal(9,4) DEFAULT NULL,
  `SODIO` decimal(9,4) DEFAULT NULL,
  `CARBOHIDRATOS` decimal(9,4) DEFAULT NULL,
  `PROTEINA` decimal(9,4) DEFAULT NULL,
  `CALCIO` decimal(9,4) DEFAULT NULL,
  `HIERRO` decimal(9,4) DEFAULT NULL,
  `COMENTARIO` varchar(300) DEFAULT NULL,
  `FECHA_CREACION` datetime DEFAULT NULL,
  `DIA_DESCANSO` varchar(10) DEFAULT NULL,
  `GENERO_DESTINATARIO` varchar(8) DEFAULT NULL,
  `CANTIDAD_COMIDAS` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`ID_DIETA`),
  KEY `FK_DIETA_USUARIO` (`ID_USUARIO`),
  KEY `FK_DIETA_PACIENTE` (`ID_PACIENTE`),
  CONSTRAINT `FK_DIETA_PACIENTE` FOREIGN KEY (`ID_PACIENTE`) REFERENCES `paciente` (`ID_PACIENTE`),
  CONSTRAINT `FK_DIETA_USUARIO` FOREIGN KEY (`ID_USUARIO`) REFERENCES `usuario` (`ID_USUARIO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dieta`
--

LOCK TABLES `dieta` WRITE;
/*!40000 ALTER TABLE `dieta` DISABLE KEYS */;
INSERT INTO `dieta` VALUES (1,NULL,NULL,1200.0000,43.8134,109.5335,737.5254,141.1765,75.4564,396.7546,7.3022,'Datos de prueba basados en recetas de Eat This Much. Objetivo: 1200.0000 kcal. Cantidades escaladas proporcionalmente.','2026-10-09 19:44:21','No','Todos',2),(2,NULL,NULL,1400.0000,71.6016,205.3836,619.9192,90.4441,109.2867,NULL,NULL,'Datos de prueba basados en recetas de Eat This Much. Objetivo: 1400.0000 kcal. Cantidades escaladas proporcionalmente.','2026-10-09 19:44:21','No','Todos',2),(3,NULL,NULL,1600.0000,62.7027,659.4595,1848.6486,151.3514,114.5946,560.0000,8.6486,'Datos de prueba basados en recetas de Eat This Much. Objetivo: 1600.0000 kcal. Cantidades escaladas proporcionalmente.','2026-10-09 19:44:21','No','Todos',2),(4,NULL,NULL,1800.0000,97.0787,380.2247,1520.8989,101.1236,145.6180,357.9775,6.0674,'Datos de prueba basados en recetas de Eat This Much. Objetivo: 1800.0000 kcal. Cantidades escaladas proporcionalmente.','2026-10-09 19:44:21','No','Todos',3),(5,NULL,NULL,2000.0000,82.4972,323.2999,1212.9320,160.5351,167.2241,NULL,NULL,'Datos de prueba basados en recetas de Eat This Much. Objetivo: 2000.0000 kcal. Cantidades escaladas proporcionalmente.','2026-10-09 19:44:21','No','Todos',3),(6,NULL,NULL,2200.0000,118.1976,684.4021,1860.6586,160.1386,141.0745,812.1317,11.4385,'Datos de prueba basados en recetas de Eat This Much. Objetivo: 2200.0000 kcal. Cantidades escaladas proporcionalmente.','2026-10-09 19:44:21','No','Todos',3),(7,NULL,NULL,1500.0000,87.8726,226.6187,679.8561,90.9558,101.7472,464.0288,7.7081,'Datos de prueba basados en recetas de Eat This Much. Objetivo: 1500.0000 kcal. Cantidades escaladas proporcionalmente.','2026-10-09 19:44:21','No','Todos',3),(8,NULL,NULL,1300.0000,47.4020,173.0173,918.4139,129.1705,105.4695,NULL,NULL,'Datos de prueba basados en recetas de Eat This Much. Objetivo: 1300.0000 kcal. Cantidades escaladas proporcionalmente.','2026-10-09 19:44:21','No','Todos',4),(9,NULL,NULL,1700.0000,90.0976,531.1018,1493.7239,110.2510,120.9205,526.3598,8.2985,'Datos de prueba basados en recetas de Eat This Much. Objetivo: 1700.0000 kcal. Cantidades escaladas proporcionalmente.','2026-10-09 19:44:21','No','Todos',4),(10,NULL,NULL,1900.0000,74.7033,510.2374,1706.8991,184.6439,143.7685,NULL,NULL,'Datos de prueba basados en recetas de Eat This Much. Objetivo: 1900.0000 kcal. Cantidades escaladas proporcionalmente.','2026-10-09 19:44:21','No','Todos',4),(11,NULL,NULL,2100.0000,98.1756,603.4208,1872.5200,149.6579,168.8141,NULL,NULL,'Datos de prueba basados en recetas de Eat This Much. Objetivo: 2100.0000 kcal. Cantidades escaladas proporcionalmente.','2026-10-09 19:44:21','No','Todos',5),(12,NULL,NULL,2300.0000,115.4699,606.8885,1740.1051,173.2049,159.7782,751.8973,12.0841,'Datos de prueba basados en recetas de Eat This Much. Objetivo: 2300.0000 kcal. Cantidades escaladas proporcionalmente.','2026-10-09 19:44:21','No','Todos',5),(13,NULL,NULL,1400.0000,64.2715,268.2635,1050.6986,95.9415,119.2282,NULL,NULL,'Datos de prueba basados en recetas de Eat This Much. Objetivo: 1400.0000 kcal. Cantidades escaladas proporcionalmente.','2026-10-09 19:44:21','No','Todos',5),(14,NULL,NULL,2500.0000,109.3035,584.6467,2011.9471,221.1490,183.0198,NULL,NULL,'Datos de prueba basados en recetas de Eat This Much. Objetivo: 2500.0000 kcal. Cantidades escaladas proporcionalmente.','2026-10-09 19:44:21','No','Todos',6),(15,NULL,NULL,1800.0000,72.6796,429.4704,1445.0970,166.1248,138.7520,NULL,NULL,'Datos de prueba basados en recetas de Eat This Much. Objetivo: 1800.0000 kcal. Cantidades escaladas proporcionalmente.','2026-10-09 19:44:21','No','Todos',6),(16,1,1,1945.2029,96.5250,583.2206,1650.7532,132.3814,145.9194,497.8558,8.9635,'X','2026-10-10 03:51:18','SUNDAY',NULL,5),(17,1,2,1422.5072,80.4473,404.8355,1116.1682,92.2389,93.1684,502.9295,7.2576,'X','2026-10-10 17:55:11','FRIDAY',NULL,3),(18,1,3,1169.4296,57.5001,260.2459,915.6841,83.8002,90.2470,347.2425,5.1583,'X','2026-10-10 18:05:50','SUNDAY',NULL,3);
/*!40000 ALTER TABLE `dieta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingrediente`
--

DROP TABLE IF EXISTS `ingrediente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingrediente` (
  `ID_INGREDIENTE` int(11) NOT NULL,
  `NOMBRE` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID_INGREDIENTE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingrediente`
--

LOCK TABLES `ingrediente` WRITE;
/*!40000 ALTER TABLE `ingrediente` DISABLE KEYS */;
INSERT INTO `ingrediente` VALUES (1,'Almonds'),(2,'American cheese, low fat'),(3,'Apple'),(4,'Balsamic vinaigrette, low fat'),(5,'Bay leaf'),(6,'Black pepper'),(7,'Blueberries'),(8,'Carrots'),(9,'Celery'),(10,'Chicken breast, raw skinless'),(11,'Chicken stock'),(12,'Cinnamon'),(13,'Dijon mustard'),(14,'Dried cranberries, sweetened'),(15,'Egg'),(16,'Egg white'),(17,'Flaxseed'),(18,'Granola with almonds'),(19,'Greek yogurt, plain nonfat'),(20,'Lemon juice'),(21,'Maple syrup'),(22,'Mayonnaise, regular salted'),(23,'Olive oil'),(24,'Parmesan cheese'),(25,'Peanut butter, unsalted'),(26,'Pecans'),(27,'Red bell pepper'),(28,'Rolled oats'),(29,'Romaine lettuce'),(30,'Shallots'),(31,'Strawberries'),(32,'Tarragon, dried'),(33,'Tomatoes'),(34,'Water');
/*!40000 ALTER TABLE `ingrediente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingrediente_comida`
--

DROP TABLE IF EXISTS `ingrediente_comida`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingrediente_comida` (
  `ID_INGREDIENTE` int(11) NOT NULL,
  `ID_COMIDA` int(11) NOT NULL,
  `CANTIDAD` decimal(6,2) DEFAULT NULL,
  PRIMARY KEY (`ID_INGREDIENTE`,`ID_COMIDA`),
  KEY `FK_INGREDIENTE_COMIDA_COM` (`ID_COMIDA`),
  CONSTRAINT `FK_INGREDIENTE_COMIDA_COM` FOREIGN KEY (`ID_COMIDA`) REFERENCES `comida` (`ID_COMIDA`),
  CONSTRAINT `FK_INGREDIENTE_COMIDA_ING` FOREIGN KEY (`ID_INGREDIENTE`) REFERENCES `ingrediente` (`ID_INGREDIENTE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingrediente_comida`
--

LOCK TABLES `ingrediente_comida` WRITE;
/*!40000 ALTER TABLE `ingrediente_comida` DISABLE KEYS */;
INSERT INTO `ingrediente_comida` VALUES (1,4,25.44),(1,8,27.30),(1,14,25.74),(1,17,20.81),(1,26,16.00),(1,33,16.16),(1,38,18.13),(1,43,12.57),(1,49,17.16),(1,60,16.16),(1,64,18.13),(1,67,18.13),(1,70,18.13),(1,73,18.13),(1,76,18.13),(1,79,18.13),(1,82,18.13),(1,94,16.16),(1,97,18.13),(1,100,12.57),(2,5,45.41),(2,13,40.03),(2,23,24.90),(2,27,29.60),(2,31,25.14),(2,36,28.20),(2,46,26.69),(2,52,19.82),(2,58,25.14),(2,63,19.82),(2,66,19.82),(2,69,19.82),(2,72,19.82),(2,75,19.82),(2,78,19.82),(2,81,19.82),(2,96,19.82),(2,99,19.82),(3,5,240.00),(3,13,211.61),(3,23,131.59),(3,27,156.45),(3,31,132.90),(3,36,149.04),(3,46,141.08),(3,52,104.77),(3,58,132.90),(3,63,104.77),(3,66,104.77),(3,69,104.77),(3,72,104.77),(3,75,104.77),(3,78,104.77),(3,81,104.77),(3,96,104.77),(3,99,104.77),(4,9,30.34),(4,22,17.78),(4,29,21.14),(4,35,17.96),(4,45,13.97),(4,51,19.06),(4,57,14.16),(4,89,17.78),(4,91,21.14),(4,95,17.96),(4,101,13.97),(5,6,0.07),(5,12,0.07),(5,24,0.04),(5,34,0.04),(5,40,0.04),(5,44,0.03),(5,55,0.03),(5,59,0.03),(5,62,0.04),(5,98,0.04),(6,4,0.24),(6,8,0.25),(6,14,0.24),(6,17,0.19),(6,26,0.15),(6,33,0.15),(6,38,0.17),(6,43,0.12),(6,49,0.16),(6,60,0.15),(6,64,0.17),(6,67,0.17),(6,70,0.17),(6,73,0.17),(6,76,0.17),(6,79,0.17),(6,82,0.17),(6,94,0.15),(6,97,0.17),(6,100,0.12),(7,1,377.28),(7,3,139.43),(7,7,313.48),(7,10,164.99),(7,19,87.69),(7,20,183.68),(7,28,104.30),(7,32,88.60),(7,41,68.93),(7,42,144.38),(7,47,94.05),(7,48,197.00),(7,54,69.85),(7,84,313.48),(7,90,87.69),(7,93,68.93),(8,2,148.48),(8,11,136.01),(8,15,116.29),(8,18,94.04),(8,21,72.29),(8,25,72.32),(8,30,85.98),(8,39,81.90),(8,50,77.53),(8,56,57.58),(8,65,94.04),(8,68,94.04),(8,71,94.04),(8,74,94.04),(8,77,94.04),(8,80,94.04),(8,83,94.04),(8,85,72.29),(8,86,94.04),(8,88,72.32),(8,92,85.98),(9,4,18.84),(9,8,20.22),(9,14,19.06),(9,17,15.42),(9,26,11.85),(9,33,11.97),(9,38,13.43),(9,43,9.31),(9,49,12.71),(9,60,11.97),(9,64,13.43),(9,67,13.43),(9,70,13.43),(9,73,13.43),(9,76,13.43),(9,79,13.43),(9,82,13.43),(9,94,11.97),(9,97,13.43),(9,100,9.31),(10,2,138.74),(10,4,222.34),(10,6,245.04),(10,8,238.65),(10,9,238.65),(10,11,127.09),(10,12,252.69),(10,14,224.96),(10,15,108.67),(10,17,181.91),(10,18,87.87),(10,21,67.55),(10,22,139.84),(10,24,134.36),(10,25,67.57),(10,26,139.89),(10,29,166.32),(10,30,80.34),(10,33,141.28),(10,34,135.69),(10,35,141.28),(10,38,158.44),(10,39,76.53),(10,40,152.17),(10,43,109.91),(10,44,105.57),(10,45,109.91),(10,49,149.97),(10,50,72.45),(10,51,149.97),(10,55,106.97),(10,56,53.80),(10,57,111.38),(10,59,106.97),(10,60,141.28),(10,62,152.17),(10,64,158.44),(10,65,87.87),(10,67,158.44),(10,68,87.87),(10,70,158.44),(10,71,87.87),(10,73,158.44),(10,74,87.87),(10,76,158.44),(10,77,87.87),(10,79,158.44),(10,80,87.87),(10,82,158.44),(10,83,87.87),(10,85,67.55),(10,86,87.87),(10,88,67.57),(10,89,139.84),(10,91,166.32),(10,92,80.34),(10,94,141.28),(10,95,141.28),(10,97,158.44),(10,98,152.17),(10,100,109.91),(10,101,109.91),(11,6,172.97),(11,12,178.37),(11,24,94.84),(11,34,95.78),(11,40,107.41),(11,44,74.52),(11,55,75.51),(11,59,75.51),(11,62,107.41),(11,98,107.41),(12,5,4.32),(12,13,3.81),(12,23,2.37),(12,27,2.82),(12,31,2.39),(12,36,2.69),(12,46,2.54),(12,52,1.89),(12,58,2.39),(12,63,1.89),(12,66,1.89),(12,69,1.89),(12,72,1.89),(12,75,1.89),(12,78,1.89),(12,81,1.89),(12,96,1.89),(12,99,1.89),(13,6,5.41),(13,12,5.57),(13,24,2.96),(13,34,2.99),(13,40,3.36),(13,44,2.33),(13,55,2.36),(13,59,2.36),(13,62,3.36),(13,98,3.36),(14,6,10.81),(14,12,11.15),(14,24,5.93),(14,34,5.99),(14,40,6.71),(14,44,4.66),(14,55,4.72),(14,59,4.72),(14,62,6.71),(14,98,6.71),(15,5,121.08),(15,13,106.76),(15,23,66.39),(15,27,78.93),(15,31,67.05),(15,36,75.19),(15,46,71.17),(15,52,52.86),(15,58,67.05),(15,63,52.86),(15,66,52.86),(15,69,52.86),(15,72,52.86),(15,75,52.86),(15,78,52.86),(15,81,52.86),(15,96,52.86),(15,99,52.86),(16,1,194.73),(16,5,142.70),(16,7,161.80),(16,13,125.82),(16,20,94.80),(16,23,78.24),(16,27,93.03),(16,31,79.02),(16,36,88.62),(16,42,74.52),(16,46,83.88),(16,48,101.68),(16,52,62.30),(16,58,79.02),(16,63,62.30),(16,66,62.30),(16,69,62.30),(16,72,62.30),(16,75,62.30),(16,78,62.30),(16,81,62.30),(16,84,161.80),(16,96,62.30),(16,99,62.30),(17,2,17.04),(17,11,15.61),(17,15,13.34),(17,18,10.79),(17,21,8.30),(17,25,8.30),(17,30,9.87),(17,39,9.40),(17,50,8.90),(17,56,6.61),(17,65,10.79),(17,68,10.79),(17,71,10.79),(17,74,10.79),(17,77,10.79),(17,80,10.79),(17,83,10.79),(17,85,8.30),(17,86,10.79),(17,88,8.30),(17,92,9.87),(18,3,54.64),(18,10,64.66),(18,19,34.37),(18,28,40.88),(18,32,34.72),(18,41,27.01),(18,47,36.86),(18,54,27.37),(18,90,34.37),(18,93,27.01),(19,3,427.73),(19,10,506.13),(19,16,131.04),(19,19,269.01),(19,28,319.96),(19,32,271.78),(19,37,114.13),(19,41,211.44),(19,47,288.51),(19,53,80.23),(19,54,214.26),(19,61,80.23),(19,87,131.04),(19,90,269.01),(19,93,211.44),(20,4,7.07),(20,6,5.41),(20,8,7.58),(20,12,5.57),(20,14,7.15),(20,17,5.78),(20,24,2.96),(20,26,4.45),(20,33,4.49),(20,34,2.99),(20,38,5.04),(20,40,3.36),(20,43,3.49),(20,44,2.33),(20,49,4.77),(20,55,2.36),(20,59,2.36),(20,60,4.49),(20,62,3.36),(20,64,5.04),(20,67,5.04),(20,70,5.04),(20,73,5.04),(20,76,5.04),(20,79,5.04),(20,82,5.04),(20,94,4.49),(20,97,5.04),(20,98,3.36),(20,100,3.49),(21,5,43.24),(21,13,38.13),(21,23,23.71),(21,27,28.19),(21,31,23.95),(21,36,26.85),(21,46,25.42),(21,52,18.88),(21,58,23.95),(21,63,18.88),(21,66,18.88),(21,69,18.88),(21,72,18.88),(21,75,18.88),(21,78,18.88),(21,81,18.88),(21,96,18.88),(21,99,18.88),(22,4,51.82),(22,6,19.82),(22,8,55.62),(22,12,20.44),(22,14,52.43),(22,17,42.39),(22,24,10.87),(22,26,32.60),(22,33,32.92),(22,34,10.98),(22,38,36.92),(22,40,12.31),(22,43,25.62),(22,44,8.54),(22,49,34.95),(22,55,8.65),(22,59,8.65),(22,60,32.92),(22,62,12.31),(22,64,36.92),(22,67,36.92),(22,70,36.92),(22,73,36.92),(22,76,36.92),(22,79,36.92),(22,82,36.92),(22,94,32.92),(22,97,36.92),(22,98,12.31),(22,100,25.62),(23,2,21.91),(23,5,15.14),(23,9,18.20),(23,11,20.07),(23,13,13.34),(23,15,17.16),(23,18,13.87),(23,21,10.67),(23,22,10.67),(23,23,8.30),(23,25,10.67),(23,27,9.87),(23,29,12.69),(23,30,12.69),(23,31,8.38),(23,35,10.78),(23,36,9.40),(23,39,12.08),(23,45,8.38),(23,46,8.90),(23,50,11.44),(23,51,11.44),(23,52,6.61),(23,56,8.50),(23,57,8.50),(23,58,8.38),(23,63,6.61),(23,65,13.87),(23,66,6.61),(23,68,13.87),(23,69,6.61),(23,71,13.87),(23,72,6.61),(23,74,13.87),(23,75,6.61),(23,77,13.87),(23,78,6.61),(23,80,13.87),(23,81,6.61),(23,83,13.87),(23,85,10.67),(23,86,13.87),(23,88,10.67),(23,89,10.67),(23,91,12.69),(23,92,12.69),(23,95,10.78),(23,96,6.61),(23,99,6.61),(23,101,8.38),(24,2,12.17),(24,9,10.11),(24,11,11.15),(24,15,9.53),(24,18,7.71),(24,21,5.93),(24,22,5.93),(24,25,5.93),(24,29,7.05),(24,30,7.05),(24,35,5.99),(24,39,6.71),(24,45,4.66),(24,50,6.35),(24,51,6.35),(24,56,4.72),(24,57,4.72),(24,65,7.71),(24,68,7.71),(24,71,7.71),(24,74,7.71),(24,77,7.71),(24,80,7.71),(24,83,7.71),(24,85,5.93),(24,86,7.71),(24,88,5.93),(24,89,5.93),(24,91,7.05),(24,92,7.05),(24,95,5.99),(24,101,4.66),(25,16,24.67),(25,37,21.48),(25,53,15.10),(25,61,15.10),(25,87,24.67),(26,6,9.73),(26,12,10.03),(26,24,5.33),(26,34,5.39),(26,40,6.04),(26,44,4.19),(26,55,4.25),(26,59,4.25),(26,62,6.04),(26,98,6.04),(27,2,180.12),(27,11,164.99),(27,15,141.07),(27,18,114.08),(27,21,87.69),(27,25,87.73),(27,30,104.30),(27,39,99.36),(27,50,94.05),(27,56,69.85),(27,65,114.08),(27,68,114.08),(27,71,114.08),(27,74,114.08),(27,77,114.08),(27,80,114.08),(27,83,114.08),(27,85,87.69),(27,86,114.08),(27,88,87.73),(27,92,104.30),(28,1,63.29),(28,5,86.49),(28,7,52.58),(28,13,76.26),(28,16,61.66),(28,20,30.81),(28,23,47.42),(28,27,56.38),(28,31,47.89),(28,36,53.71),(28,37,53.71),(28,42,24.22),(28,46,50.84),(28,48,33.05),(28,52,37.76),(28,53,37.76),(28,58,47.89),(28,61,37.76),(28,63,37.76),(28,66,37.76),(28,69,37.76),(28,72,37.76),(28,75,37.76),(28,78,37.76),(28,81,37.76),(28,84,52.58),(28,87,61.66),(28,96,37.76),(28,99,37.76),(29,2,114.40),(29,9,190.11),(29,11,104.79),(29,15,89.60),(29,18,72.46),(29,21,55.70),(29,22,111.39),(29,25,55.72),(29,29,132.49),(29,30,66.25),(29,35,112.54),(29,39,63.11),(29,45,87.56),(29,50,59.74),(29,51,119.47),(29,56,44.36),(29,57,88.73),(29,65,72.46),(29,68,72.46),(29,71,72.46),(29,74,72.46),(29,77,72.46),(29,80,72.46),(29,83,72.46),(29,85,55.70),(29,86,72.46),(29,88,55.72),(29,89,111.39),(29,91,132.49),(29,92,66.25),(29,95,112.54),(29,101,87.56),(30,6,3.60),(30,12,3.72),(30,24,1.98),(30,34,2.00),(30,40,2.24),(30,44,1.55),(30,55,1.57),(30,59,1.57),(30,62,2.24),(30,98,2.24),(31,3,143.20),(31,10,169.45),(31,19,90.06),(31,28,107.12),(31,32,90.99),(31,41,70.79),(31,47,96.59),(31,54,71.74),(31,90,90.06),(31,93,70.79),(32,6,0.72),(32,12,0.74),(32,24,0.39),(32,34,0.40),(32,40,0.45),(32,44,0.31),(32,55,0.31),(32,59,0.31),(32,62,0.45),(32,98,0.45),(33,2,299.39),(33,11,274.25),(33,15,234.49),(33,18,189.62),(33,21,145.76),(33,25,145.82),(33,30,173.37),(33,39,165.15),(33,50,156.33),(33,56,116.10),(33,65,189.62),(33,68,189.62),(33,71,189.62),(33,74,189.62),(33,77,189.62),(33,80,189.62),(33,83,189.62),(33,85,145.76),(33,86,189.62),(33,88,145.82),(33,92,173.37),(34,1,433.27),(34,7,360.00),(34,16,365.36),(34,20,210.94),(34,37,318.21),(34,42,165.80),(34,48,226.23),(34,53,223.70),(34,61,223.70),(34,84,360.00),(34,87,365.36);
/*!40000 ALTER TABLE `ingrediente_comida` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paciente`
--

DROP TABLE IF EXISTS `paciente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `paciente` (
  `ID_PACIENTE` int(11) NOT NULL,
  `NOMBRE` varchar(50) DEFAULT NULL,
  `ALTURA` decimal(5,2) DEFAULT NULL,
  `PESO` decimal(5,2) DEFAULT NULL,
  `EDAD` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID_PACIENTE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paciente`
--

LOCK TABLES `paciente` WRITE;
/*!40000 ALTER TABLE `paciente` DISABLE KEYS */;
INSERT INTO `paciente` VALUES (1,'Carlos Trejo',180.00,67.00,19),(2,'eduardo Trejo',164.00,80.00,45),(3,'Eliza Magdalena',157.00,75.00,34);
/*!40000 ALTER TABLE `paciente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `ID_USUARIO` int(11) NOT NULL,
  `PASSWORD` varchar(100) DEFAULT NULL,
  `CORREO` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID_USUARIO`),
  UNIQUE KEY `UNIQ_CORREO` (`CORREO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'$2a$10$m9knbqZRnceAovzzCFTOTuOrFjxk2I9UaagyDsxQi1zepNzn8H4SC','probandoregistro@cactus.moy');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'nutrimaker'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-10 14:14:09
