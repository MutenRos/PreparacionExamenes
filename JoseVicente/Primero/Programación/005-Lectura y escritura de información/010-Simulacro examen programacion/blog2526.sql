-- MySQL dump 10.13  Distrib 8.0.43, for Linux (x86_64)
--
-- Host: localhost    Database: blog2526
-- ------------------------------------------------------
-- Server version	8.0.43-0ubuntu0.24.04.1

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
-- Table structure for table `autores`
--

DROP TABLE IF EXISTS `autores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `autores` (
  `Identificador` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL,
  `apellidos` varchar(255) NOT NULL,
  `email` varchar(150) NOT NULL,
  PRIMARY KEY (`Identificador`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `autores`
--

LOCK TABLES `autores` WRITE;
/*!40000 ALTER TABLE `autores` DISABLE KEYS */;
INSERT INTO `autores` VALUES (1,'Carlos','Pérez Gómez','carlos.perez@example.com'),(2,'María','López Sánchez','maria.lopez@example.com'),(3,'Javier','Martínez Ruiz','javier.martinez@example.com'),(4,'Lucía','García Torres','lucia.garcia@example.com'),(5,'Andrés','Ramírez Fernández','andres.ramirez@example.com'),(6,'Elena','Moreno Díaz','elena.moreno@example.com'),(7,'Sergio','Hernández Navarro','sergio.hernandez@example.com'),(8,'Patricia','Gómez León','patricia.gomez@example.com'),(9,'Raúl','Castillo Ortega','raul.castillo@example.com'),(10,'Laura','Santos Vega','laura.santos@example.com'),(11,'Diego','Cano Romero','diego.cano@example.com'),(12,'Marta','Jiménez Soto','marta.jimenez@example.com'),(13,'Rubén','Pardo Iglesias','ruben.pardo@example.com'),(14,'Nuria','Cruz Herrera','nuria.cruz@example.com'),(15,'Héctor','Vázquez Molina','hector.vazquez@example.com'),(16,'Adriana','Reyes Campos','adriana.reyes@example.com'),(17,'Pablo','Suárez Gil','pablo.suarez@example.com'),(18,'Sara','Nieto Rivas','sara.nieto@example.com'),(19,'Álvaro','Ruiz Pastor','alvaro.ruiz@example.com'),(20,'Clara','Ortega Lozano','clara.ortega@example.com');
/*!40000 ALTER TABLE `autores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entradas`
--

DROP TABLE IF EXISTS `entradas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `entradas` (
  `Identificador` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(150) NOT NULL,
  `contenido` varchar(255) NOT NULL,
  `fecha` varchar(50) NOT NULL,
  `autor` int NOT NULL,
  PRIMARY KEY (`Identificador`),
  KEY `autoresaentradas` (`autor`),
  CONSTRAINT `autoresaentradas` FOREIGN KEY (`autor`) REFERENCES `autores` (`Identificador`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entradas`
--

LOCK TABLES `entradas` WRITE;
/*!40000 ALTER TABLE `entradas` DISABLE KEYS */;
INSERT INTO `entradas` VALUES (1,'Titulo de prueba','Contenido de prueba','2025-05-05',2),(2,'Cómo crear tu primera página web con HTML y CSS','Aprende los fundamentos del diseño web con ejemplos prácticos.','2025-01-10',2),(3,'JavaScript moderno: funciones flecha y promesas','Exploramos las características modernas del lenguaje JavaScript.','2025-01-12',3),(4,'Instalar y configurar MySQL en Ubuntu','Guía paso a paso para instalar MySQL en sistemas basados en Linux.','2025-01-15',4),(5,'Buenas prácticas de seguridad en PHP','Cómo proteger tu aplicación web frente a ataques comunes.','2025-01-18',5),(6,'Introducción a Docker para desarrolladores','Aprende a crear contenedores para tus proyectos de desarrollo.','2025-01-20',6),(7,'Versionado de código con Git y GitHub','Todo lo que necesitas saber para trabajar en equipo con control de versiones.','2025-01-22',7),(8,'APIs RESTful con Flask y Python','Construye tus propias APIs usando el microframework Flask.','2025-01-25',8),(9,'Diseño responsivo con CSS Grid y Flexbox','Técnicas modernas para crear sitios adaptativos y elegantes.','2025-01-28',9),(10,'Automatización de tareas con Python','Ejemplos de cómo automatizar procesos repetitivos con scripts.','2025-02-02',10),(11,'Introducción a React.js','Cómo empezar a desarrollar interfaces modernas con React.','2025-02-05',11),(12,'Bases de datos NoSQL: una visión general','Compara MongoDB, Redis y otros sistemas de almacenamiento.','2025-02-07',12),(13,'Optimización de rendimiento en WordPress','Consejos para acelerar tu sitio web WordPress.','2025-02-10',13),(14,'Cómo desplegar una app en la nube con AWS','Pasos esenciales para llevar tu aplicación a producción.','2025-02-12',14),(15,'Aprendiendo Node.js paso a paso','Una introducción práctica al entorno de ejecución de JavaScript.','2025-02-14',15),(16,'Machine Learning con Python y scikit-learn','Primeros pasos en el aprendizaje automático.','2025-02-18',16),(17,'Cómo proteger tu red doméstica','Recomendaciones básicas de ciberseguridad para usuarios domésticos.','2025-02-20',17),(18,'Programación orientada a objetos en Java','Conceptos clave como clases, objetos, herencia y polimorfismo.','2025-02-22',18),(19,'Diseño de bases de datos relacionales','Cómo modelar tus datos correctamente con claves primarias y foráneas.','2025-02-25',19),(20,'Inteligencia artificial en la web moderna','Exploramos el papel de la IA en las aplicaciones actuales.','2025-02-28',20);
/*!40000 ALTER TABLE `entradas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `entradas_con_autores`
--

DROP TABLE IF EXISTS `entradas_con_autores`;
/*!50001 DROP VIEW IF EXISTS `entradas_con_autores`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `entradas_con_autores` AS SELECT 
 1 AS `titulo`,
 1 AS `contenido`,
 1 AS `fecha`,
 1 AS `nombre`,
 1 AS `apellidos`,
 1 AS `email`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `entradas_con_autores`
--

/*!50001 DROP VIEW IF EXISTS `entradas_con_autores`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `entradas_con_autores` AS select `entradas`.`titulo` AS `titulo`,`entradas`.`contenido` AS `contenido`,`entradas`.`fecha` AS `fecha`,`autores`.`nombre` AS `nombre`,`autores`.`apellidos` AS `apellidos`,`autores`.`email` AS `email` from (`entradas` left join `autores` on((`entradas`.`autor` = `autores`.`Identificador`))) */;
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

-- Dump completed on 2025-10-30 16:16:32
