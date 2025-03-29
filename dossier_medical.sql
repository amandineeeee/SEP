-- MySQL dump 10.13  Distrib 8.0.41, for Linux (x86_64)
--
-- Host: localhost    Database: dossier_medical
-- ------------------------------------------------------
-- Server version	8.0.41-0ubuntu0.22.04.1

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
-- Table structure for table `Analyse`
--

DROP TABLE IF EXISTS `Analyse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Analyse` (
  `id_analyse` int NOT NULL AUTO_INCREMENT,
  `id_patient` int DEFAULT NULL,
  `type_analyse` varchar(50) DEFAULT NULL,
  `date_analyse` date DEFAULT NULL,
  `resultats` text,
  `document_scanne` longblob,
  PRIMARY KEY (`id_analyse`),
  KEY `id_patient` (`id_patient`),
  CONSTRAINT `Analyse_ibfk_1` FOREIGN KEY (`id_patient`) REFERENCES `Patient` (`id_patient`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Analyse`
--

LOCK TABLES `Analyse` WRITE;
/*!40000 ALTER TABLE `Analyse` DISABLE KEYS */;
INSERT INTO `Analyse` VALUES (1,1,'IRM','2024-02-15','Lésions cérébrales visibles',NULL),(2,2,'Prise de sang','2024-03-01','Taux normal',NULL),(3,3,'IRM','2024-01-20','Lésions minimes',NULL),(4,4,'Prise de sang','2024-03-05','Inflammation détectée',NULL),(5,5,'IRM','2024-02-28','Aucune anomalie détectée',NULL),(16,15,'IRM','2024-02-21','Pas de nouvelles tâches de démyélinisation\r\nCela semble indiquer une stabilité dans l\'évolution de la maladie',NULL),(17,15,'Prise de sang','2024-02-15','Pas d\'évolution significative des marqueurs',NULL),(32,20,'IRM','2016-02-29','Des tâches de démyélinisation sont visibles\r\nCela indiquerait un potentiel développement d\'une SEP',NULL),(33,20,'Ponction lombaire','2016-02-29','La ponction lombaire nous permet de dire que la SEP est de forme secondaire progressive',NULL);
/*!40000 ALTER TABLE `Analyse` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Consultation`
--

DROP TABLE IF EXISTS `Consultation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Consultation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `date_consultation` date NOT NULL,
  `plan_soins` text,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `Consultation_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `Patient` (`id_patient`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Consultation`
--

LOCK TABLES `Consultation` WRITE;
/*!40000 ALTER TABLE `Consultation` DISABLE KEYS */;
INSERT INTO `Consultation` VALUES (8,15,'2025-03-17','Reprendre les séances de kinésithérapie\r\nContinuer le suivi neurologique'),(12,20,'2016-02-29','Reprendre les séances de kinésithérapie et continuer le suivi neurologique');
/*!40000 ALTER TABLE `Consultation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Jumeau_numerique`
--

DROP TABLE IF EXISTS `Jumeau_numerique`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Jumeau_numerique` (
  `id_jumeau` int NOT NULL AUTO_INCREMENT,
  `id_patient` int DEFAULT NULL,
  `type_simulation` enum('traitement','évolution sans traitement') DEFAULT NULL,
  `resultat_simulation` text,
  `date_simulation` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_jumeau`),
  KEY `id_patient` (`id_patient`),
  CONSTRAINT `Jumeau_numerique_ibfk_1` FOREIGN KEY (`id_patient`) REFERENCES `Patient` (`id_patient`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Jumeau_numerique`
--

LOCK TABLES `Jumeau_numerique` WRITE;
/*!40000 ALTER TABLE `Jumeau_numerique` DISABLE KEYS */;
INSERT INTO `Jumeau_numerique` VALUES (1,1,'traitement','Évolution ralentie, amélioration légère','2025-03-12 14:42:32'),(2,2,'évolution sans traitement','Pas d’évolution notable','2025-03-12 14:42:32'),(3,3,'traitement','Amélioration stable','2025-03-12 14:42:32'),(4,4,'évolution sans traitement','Progression lente des symptômes','2025-03-12 14:42:32'),(5,5,'traitement','Maintien de l’état stable','2025-03-12 14:42:32');
/*!40000 ALTER TABLE `Jumeau_numerique` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Patient`
--

DROP TABLE IF EXISTS `Patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Patient` (
  `id_patient` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) DEFAULT NULL,
  `prenom` varchar(50) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `sexe` enum('H','F','Autre') DEFAULT NULL,
  `mode_vie` text,
  `date_inscription` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `date_diagnostic` date DEFAULT NULL,
  `forme_sep` text,
  `score_edss` int DEFAULT NULL,
  `symptomes` text,
  `traitement_actuel_id` int DEFAULT NULL,
  `traitement_anterieur_id` int DEFAULT NULL,
  `date_de_naissance` date DEFAULT NULL,
  PRIMARY KEY (`id_patient`),
  KEY `fk_traitement_actuel` (`traitement_actuel_id`),
  KEY `fk_traitement_anterieur` (`traitement_anterieur_id`),
  CONSTRAINT `fk_traitement_actuel` FOREIGN KEY (`traitement_actuel_id`) REFERENCES `Traitement` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_traitement_anterieur` FOREIGN KEY (`traitement_anterieur_id`) REFERENCES `Traitement` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Patient`
--

LOCK TABLES `Patient` WRITE;
/*!40000 ALTER TABLE `Patient` DISABLE KEYS */;
INSERT INTO `Patient` VALUES (1,'Dupont','Jean',45,'H','Fumeur, sédentaire','2025-03-12 14:42:13',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,'Martin','Sophie',32,'F','Sportive, alimentation équilibrée','2025-03-12 14:42:13',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(3,'Bernard','Luc',60,'H','Ancien fumeur, marche quotidienne','2025-03-12 14:42:13',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(4,'Durand','Claire',28,'F','Végétarienne, sportive','2025-03-12 14:42:13',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(5,'Lemoine','Paul',55,'H','Travail de bureau, peu d’activité physique','2025-03-12 14:42:13',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(15,'DUTRONC','Albert',31,'H','Alimentation saine\r\nSédentaire','2025-03-17 13:03:52','2003-01-31','pp',5,'Maux de tête\r\nFatigue\r\nOublis \r\nSpasticité \r\nPerte d\'équilibre',NULL,NULL,NULL),(20,'Test','Test1',37,'F','Active','2025-03-17 14:58:08','2016-02-29','rémittente-récurrente',2,'Maux de tête\r\nspasticité',NULL,NULL,'1988-01-31');
/*!40000 ALTER TABLE `Patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Patient_traitement`
--

DROP TABLE IF EXISTS `Patient_traitement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Patient_traitement` (
  `id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `traitement_id` int NOT NULL,
  `type_traitement` enum('actuel','anterieur') NOT NULL,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  KEY `traitement_id` (`traitement_id`),
  CONSTRAINT `Patient_traitement_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `Patient` (`id_patient`) ON DELETE CASCADE,
  CONSTRAINT `Patient_traitement_ibfk_2` FOREIGN KEY (`traitement_id`) REFERENCES `Traitement` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Patient_traitement`
--

LOCK TABLES `Patient_traitement` WRITE;
/*!40000 ALTER TABLE `Patient_traitement` DISABLE KEYS */;
INSERT INTO `Patient_traitement` VALUES (17,15,17,'anterieur'),(18,15,18,'anterieur'),(19,15,19,'actuel'),(38,20,38,'actuel'),(39,20,39,'actuel');
/*!40000 ALTER TABLE `Patient_traitement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Prediction`
--

DROP TABLE IF EXISTS `Prediction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Prediction` (
  `id_pred` int NOT NULL AUTO_INCREMENT,
  `id_patient` int DEFAULT NULL,
  `date_prediction` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `resultat` enum('SEP probable','SEP non probable') DEFAULT NULL,
  `score_confiance` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`id_pred`),
  KEY `id_patient` (`id_patient`),
  CONSTRAINT `Prediction_ibfk_1` FOREIGN KEY (`id_patient`) REFERENCES `Patient` (`id_patient`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Prediction`
--

LOCK TABLES `Prediction` WRITE;
/*!40000 ALTER TABLE `Prediction` DISABLE KEYS */;
INSERT INTO `Prediction` VALUES (1,1,'2025-03-12 14:42:26','SEP probable',85.50),(2,2,'2025-03-12 14:42:26','SEP non probable',95.00),(3,3,'2025-03-12 14:42:26','SEP probable',72.30),(4,4,'2025-03-12 14:42:26','SEP non probable',89.70),(5,5,'2025-03-12 14:42:26','SEP non probable',92.10);
/*!40000 ALTER TABLE `Prediction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Traitement`
--

DROP TABLE IF EXISTS `Traitement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Traitement` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) NOT NULL,
  `frequence_dosage` varchar(255) NOT NULL,
  `informations_complementaire` text,
  `actuel` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Traitement`
--

LOCK TABLES `Traitement` WRITE;
/*!40000 ALTER TABLE `Traitement` DISABLE KEYS */;
INSERT INTO `Traitement` VALUES (1,'Frexalimab','10 mg','','0'),(2,'Imurel','10 ml','','1'),(3,'Kinésithérapie','2 fois par semaine','Renforcement musculaire\r\nTravail de l\'équilibre','1'),(4,'Imurel','10 ml','','0'),(5,'Kinésithérapie','2 fois par semaine','Travail de l\'équilibre','0'),(6,'','','','1'),(7,'Imurel','10 ml','','0'),(8,'Kinésithérapie','2 fois par semaine','Travail de l\'équilibre','0'),(9,'Imurel','10 ml','','0'),(10,'Kinésithérapie','2 fois par semaine','Travail de l\'équilibre','0'),(11,'Imurel','10 ml','','0'),(12,'Kinésithérapie','2 fois par semaine','Travail de l\'équilibre','0'),(13,'Imurel','10 ml','','0'),(14,'Kinésithérapie','2 fois par semaine','Travail de l\'équilibre','0'),(15,'Imurel','10 ml','','0'),(16,'Kinésithérapie','2 fois par semaine','Travail de l\'équilibre','0'),(17,'Frexalimab','10 ml','','0'),(18,'Imurel','10mg','','0'),(19,'Kinésithérapie','2 fois par semaine','Renforcement musculaire\r\nTravail de l\'équilibre','1'),(32,'Imurel','10 mg','','0'),(33,'Frexalimab','10 ml','La patient a bénéficié des essais cliniques du Frexalimab mais n\'a pas été réceptive car sa forme de SEP ne le permet pas ','1'),(34,'Kinésithérapie','2 fois par semaine','Travail de l\'équilibre','1'),(35,'Imurel','10 mg','','0'),(36,'Frexalimab','10 ml','La patient a bénéficié des essais cliniques du Frexalimab mais n\'a pas été réceptive car sa forme de SEP ne le permet pas ','1'),(37,'Kinésithérapie','2 fois par semaine','Travail de l\'équilibre','1'),(38,'Frexalimab','10 ml','La patient a bénéficié des essais cliniques du Frexalimab mais n\'a pas été réceptive car sa forme de SEP ne le permet pas ','1'),(39,'Kinésithérapie','2 fois par semaine','Travail de l\'équilibre','1');
/*!40000 ALTER TABLE `Traitement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Utilisateur`
--

DROP TABLE IF EXISTS `Utilisateur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Utilisateur` (
  `id_utilisateur` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('medecin','administrateur') NOT NULL,
  PRIMARY KEY (`id_utilisateur`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Utilisateur`
--

LOCK TABLES `Utilisateur` WRITE;
/*!40000 ALTER TABLE `Utilisateur` DISABLE KEYS */;
INSERT INTO `Utilisateur` VALUES (1,'admin','scrypt:32768:8:1$F37CSCc7PI0hvNED$18973d0ea6bd72a476c2b8b7e777b86e3d1fbb102abeb7b39ae7f22d2734b99ea8ea7a6abe7d0304710d78f7827694d5264206dd6d607ad574e4a3ba0c94cb99','administrateur'),(2,'medecin1','scrypt:32768:8:1$tq03GnmRqmVSrfVr$7e349979b6da7d233dc4cbb9eed4c21a0ec8817d20be8c924e82cde1f87a56cc58f650512a63046b090170cec8770bb99469fd7525b8bef5eb916a7ee4b3d22e','medecin'),(7,'amandineHENRY','scrypt:32768:8:1$ZUZpRz6xiOfbw6C9$dbdde30cec0661291a54f1063cc1f0266e9c36e44fd3e57e0f72262215c95c4c81de11c29152a85b096c4c79a6afa654ae9ed81126f597a2b6f6315b90678087','medecin');
/*!40000 ALTER TABLE `Utilisateur` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-23 15:38:16
