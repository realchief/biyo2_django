-- MySQL dump 10.13  Distrib 5.6.33, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: thrive2_database
-- ------------------------------------------------------
-- Server version	5.6.33-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_0e939a4f` (`group_id`),
  KEY `auth_group_permissions_8373b171` (`permission_id`),
  CONSTRAINT `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permission_group_id_689710a9a73b7457_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_417f1b1c` (`content_type_id`),
  CONSTRAINT `auth__content_type_id_508cf46651277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=139 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add content type',3,'add_contenttype'),(8,'Can change content type',3,'change_contenttype'),(9,'Can delete content type',3,'delete_contenttype'),(10,'Can add session',4,'add_session'),(11,'Can change session',4,'change_session'),(12,'Can delete session',4,'delete_session'),(13,'Can add log entry',5,'add_logentry'),(14,'Can change log entry',5,'change_logentry'),(15,'Can delete log entry',5,'delete_logentry'),(16,'Can add cors model',6,'add_corsmodel'),(17,'Can change cors model',6,'change_corsmodel'),(18,'Can delete cors model',6,'delete_corsmodel'),(19,'Can add display',7,'add_display'),(20,'Can change display',7,'change_display'),(21,'Can delete display',7,'delete_display'),(22,'Can add page',8,'add_page'),(23,'Can change page',8,'change_page'),(24,'Can delete page',8,'delete_page'),(25,'Can add element',9,'add_element'),(26,'Can change element',9,'change_element'),(27,'Can delete element',9,'delete_element'),(28,'Can add box',10,'add_box'),(29,'Can change box',10,'change_box'),(30,'Can delete box',10,'delete_box'),(31,'Can add picture',11,'add_picture'),(32,'Can change picture',11,'change_picture'),(33,'Can delete picture',11,'delete_picture'),(34,'Can add category',12,'add_category'),(35,'Can change category',12,'change_category'),(36,'Can delete category',12,'delete_category'),(37,'Can add tax rate',13,'add_taxrate'),(38,'Can change tax rate',13,'change_taxrate'),(39,'Can delete tax rate',13,'delete_taxrate'),(40,'Can add modifier group',14,'add_modifiergroup'),(41,'Can change modifier group',14,'change_modifiergroup'),(42,'Can delete modifier group',14,'delete_modifiergroup'),(43,'Can add modifier',15,'add_modifier'),(44,'Can change modifier',15,'change_modifier'),(45,'Can delete modifier',15,'delete_modifier'),(46,'Can add printer',16,'add_printer'),(47,'Can change printer',16,'change_printer'),(48,'Can delete printer',16,'delete_printer'),(49,'Can add historical product',17,'add_historicalproduct'),(50,'Can change historical product',17,'change_historicalproduct'),(51,'Can delete historical product',17,'delete_historicalproduct'),(52,'Can add product',18,'add_product'),(53,'Can change product',18,'change_product'),(54,'Can delete product',18,'delete_product'),(55,'Can add discount',19,'add_discount'),(56,'Can change discount',19,'change_discount'),(57,'Can delete discount',19,'delete_discount'),(58,'Can add store',20,'add_store'),(59,'Can change store',20,'change_store'),(60,'Can delete store',20,'delete_store'),(61,'Can add table section',21,'add_tablesection'),(62,'Can change table section',21,'change_tablesection'),(63,'Can delete table section',21,'delete_tablesection'),(64,'Can add table',22,'add_table'),(65,'Can change table',22,'change_table'),(66,'Can delete table',22,'delete_table'),(67,'Can add terminal',23,'add_terminal'),(68,'Can change terminal',23,'change_terminal'),(69,'Can delete terminal',23,'delete_terminal'),(70,'Can add reward',24,'add_reward'),(71,'Can change reward',24,'change_reward'),(72,'Can delete reward',24,'delete_reward'),(73,'Can add csv',25,'add_csv'),(74,'Can change csv',25,'change_csv'),(75,'Can delete csv',25,'delete_csv'),(76,'Can add shift',26,'add_shift'),(77,'Can change shift',26,'change_shift'),(78,'Can delete shift',26,'delete_shift'),(79,'Can add payout',27,'add_payout'),(80,'Can change payout',27,'change_payout'),(81,'Can delete payout',27,'delete_payout'),(82,'Can add payment',28,'add_payment'),(83,'Can change payment',28,'change_payment'),(84,'Can delete payment',28,'delete_payment'),(85,'Can add order',29,'add_order'),(86,'Can change order',29,'change_order'),(87,'Can delete order',29,'delete_order'),(88,'Can add order item',30,'add_orderitem'),(89,'Can change order item',30,'change_orderitem'),(90,'Can delete order item',30,'delete_orderitem'),(91,'Can add order option',31,'add_orderoption'),(92,'Can change order option',31,'change_orderoption'),(93,'Can delete order option',31,'delete_orderoption'),(94,'Can add order modifier',32,'add_ordermodifier'),(95,'Can change order modifier',32,'change_ordermodifier'),(96,'Can delete order modifier',32,'delete_ordermodifier'),(97,'Can add shared order',33,'add_sharedorder'),(98,'Can change shared order',33,'change_sharedorder'),(99,'Can delete shared order',33,'delete_sharedorder'),(100,'Can add employee',34,'add_employee'),(101,'Can change employee',34,'change_employee'),(102,'Can delete employee',34,'delete_employee'),(103,'Can add customer',35,'add_customer'),(104,'Can change customer',35,'change_customer'),(105,'Can delete customer',35,'delete_customer'),(106,'Can add time clock',36,'add_timeclock'),(107,'Can change time clock',36,'change_timeclock'),(108,'Can delete time clock',36,'delete_timeclock'),(109,'Can add csv customer',37,'add_csvcustomer'),(110,'Can change csv customer',37,'change_csvcustomer'),(111,'Can delete csv customer',37,'delete_csvcustomer'),(112,'Can add supplier',38,'add_supplier'),(113,'Can change supplier',38,'change_supplier'),(114,'Can delete supplier',38,'delete_supplier'),(115,'Can add token',39,'add_token'),(116,'Can change token',39,'change_token'),(117,'Can delete token',39,'delete_token'),(118,'Can add project version',40,'add_projectversion'),(119,'Can change project version',40,'change_projectversion'),(120,'Can delete project version',40,'delete_projectversion'),(121,'Can add customer group',41,'add_customergroup'),(122,'Can change customer group',41,'change_customergroup'),(123,'Can delete customer group',41,'delete_customergroup'),(124,'Can add special prices',42,'add_specialprices'),(125,'Can change special prices',42,'change_specialprices'),(126,'Can delete special prices',42,'delete_specialprices'),(127,'Can add db settings',43,'add_dbsettings'),(128,'Can change db settings',43,'change_dbsettings'),(129,'Can delete db settings',43,'delete_dbsettings'),(130,'Can add purchase',44,'add_purchase'),(131,'Can change purchase',44,'change_purchase'),(132,'Can delete purchase',44,'delete_purchase'),(133,'Can add purchase item',45,'add_purchaseitem'),(134,'Can change purchase item',45,'change_purchaseitem'),(135,'Can delete purchase item',45,'delete_purchaseitem'),(136,'Can add kv store',46,'add_kvstore'),(137,'Can change kv store',46,'change_kvstore'),(138,'Can delete kv store',46,'delete_kvstore');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `user_id` int(11) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `corsheaders_corsmodel`
--

DROP TABLE IF EXISTS `corsheaders_corsmodel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `corsheaders_corsmodel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cors` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `corsheaders_corsmodel`
--

LOCK TABLES `corsheaders_corsmodel` WRITE;
/*!40000 ALTER TABLE `corsheaders_corsmodel` DISABLE KEYS */;
/*!40000 ALTER TABLE `corsheaders_corsmodel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `displays_box`
--

DROP TABLE IF EXISTS `displays_box`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `displays_box` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `row` int(11) NOT NULL,
  `col` int(11) NOT NULL,
  `size_x` int(11) NOT NULL,
  `size_y` int(11) NOT NULL,
  `background_color` varchar(7) NOT NULL,
  `archived` tinyint(1) NOT NULL,
  `display_id` int(11) NOT NULL,
  `element_id` int(11),
  PRIMARY KEY (`id`),
  UNIQUE KEY `element_id` (`element_id`),
  KEY `displays_box_65d1b4b6` (`display_id`),
  CONSTRAINT `displays_box_display_id_1a2c30b8e9ab466c_fk_displays_display_id` FOREIGN KEY (`display_id`) REFERENCES `displays_display` (`id`),
  CONSTRAINT `displays_box_element_id_73bf0ef7ff48d456_fk_displays_element_id` FOREIGN KEY (`element_id`) REFERENCES `displays_element` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `displays_box`
--

LOCK TABLES `displays_box` WRITE;
/*!40000 ALTER TABLE `displays_box` DISABLE KEYS */;
/*!40000 ALTER TABLE `displays_box` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `displays_display`
--

DROP TABLE IF EXISTS `displays_display`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `displays_display` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `background_color` varchar(7) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `displays_display`
--

LOCK TABLES `displays_display` WRITE;
/*!40000 ALTER TABLE `displays_display` DISABLE KEYS */;
/*!40000 ALTER TABLE `displays_display` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `displays_element`
--

DROP TABLE IF EXISTS `displays_element`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `displays_element` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` int(11) NOT NULL,
  `value` varchar(128) NOT NULL,
  `archived` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `displays_element`
--

LOCK TABLES `displays_element` WRITE;
/*!40000 ALTER TABLE `displays_element` DISABLE KEYS */;
/*!40000 ALTER TABLE `displays_element` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `displays_page`
--

DROP TABLE IF EXISTS `displays_page`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `displays_page` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `display_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `displays_page_65d1b4b6` (`display_id`),
  CONSTRAINT `displays_page_display_id_17c5784e96b391b9_fk_displays_display_id` FOREIGN KEY (`display_id`) REFERENCES `displays_display` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `displays_page`
--

LOCK TABLES `displays_page` WRITE;
/*!40000 ALTER TABLE `displays_page` DISABLE KEYS */;
/*!40000 ALTER TABLE `displays_page` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `displays_picture`
--

DROP TABLE IF EXISTS `displays_picture`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `displays_picture` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file` varchar(100) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `box_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `displays_picture_2dbcba41` (`slug`),
  KEY `displays_picture_d5c14c0d` (`box_id`),
  CONSTRAINT `displays_picture_box_id_1170bc65fd7f92a8_fk_displays_box_id` FOREIGN KEY (`box_id`) REFERENCES `displays_box` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `displays_picture`
--

LOCK TABLES `displays_picture` WRITE;
/*!40000 ALTER TABLE `displays_picture` DISABLE KEYS */;
/*!40000 ALTER TABLE `displays_picture` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_417f1b1c` (`content_type_id`),
  KEY `django_admin_log_e8701ad4` (`user_id`),
  CONSTRAINT `djang_content_type_id_697914295151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_l_user_id_52fdd58701c5f563_fk_employees_employee_id` FOREIGN KEY (`user_id`) REFERENCES `employees_employee` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2017-11-06 10:43:35','1','Category1',1,'New Item has been created',12,1),(2,'2017-11-06 10:44:37','1','Product1',1,'New Item has been created',18,1),(3,'2017-11-06 10:45:46','2','Product2',1,'New Item has been created',18,1),(4,'2017-11-06 12:25:26','3','fdkjfljwo',1,'New Item has been created',18,1),(5,'2017-11-06 12:25:45','4','efef',1,'New Item has been created',18,1),(6,'2017-11-06 12:26:08','4','efef',3,'Object has been archived',18,1),(7,'2017-11-06 12:26:16','3','fdkjfljwo',3,'Object has been archived',18,1),(8,'2017-11-06 12:26:21','1','Product1',3,'Object has been archived',18,1),(9,'2017-11-06 12:26:25','2','Product2',3,'Object has been archived',18,1),(10,'2017-11-06 12:33:58','5','ddd',1,'New Item has been created',18,1),(11,'2017-11-06 12:34:26','6','dgrgr',1,'New Item has been created',18,1),(12,'2017-11-06 13:08:09','7','dfegeg',1,'New Item has been created',18,1),(13,'2017-11-06 13:34:31','8','product3',1,'New Item has been created',18,1),(14,'2017-11-06 13:40:45','9','product4',1,'New Item has been created',18,1),(15,'2017-11-06 13:50:08','10','aaa',1,'New Item has been created',18,1),(16,'2017-11-06 14:25:59','11','ghthth',1,'New Item has been created',18,1),(17,'2017-11-06 14:27:56','12','yi7i7i',1,'New Item has been created',18,1),(18,'2017-11-06 14:34:51','13','fgrgrg',1,'New Item has been created',18,1),(19,'2017-11-06 14:45:06','14','aaa',1,'New Item has been created',18,1),(20,'2017-11-06 14:45:41','15','aaa',1,'New Item has been created',18,1),(21,'2017-11-06 14:52:49','16','Image',1,'New Item has been created',18,1),(22,'2017-11-06 14:53:00','15','aaa',3,'Object has been archived',18,1),(23,'2017-11-06 14:53:23','17','Image',1,'New Item has been created',18,1),(24,'2017-11-06 14:53:39','16','Image',3,'Object has been archived',18,1),(25,'2017-11-06 14:53:46','17','Image',3,'Object has been archived',18,1),(26,'2017-11-06 15:06:59','18','img_1',1,'New Item has been created',18,1),(27,'2017-11-06 15:43:09','19','img_1',1,'New Item has been created',18,1),(28,'2017-11-06 15:43:42','14','aaa',2,'Object has been changed',18,1),(29,'2017-11-06 15:44:06','10','aaa',2,'Object has been changed',18,1),(30,'2017-11-06 15:44:36','5','ddd',2,'Object has been changed',18,1),(31,'2017-11-06 15:44:42','5','ddd',3,'Object has been archived',18,1),(32,'2017-11-06 16:15:53','14','aaa',3,'Object has been archived',18,1),(33,'2017-11-06 16:16:07','10','aaa',3,'Object has been archived',18,1),(34,'2017-11-06 16:16:53','7','dfegeg',3,'Object has been archived',18,1),(35,'2017-11-06 16:16:58','6','dgrgr',3,'Object has been archived',18,1),(36,'2017-11-06 16:17:02','13','fgrgrg',3,'Object has been archived',18,1),(37,'2017-11-06 16:17:06','11','ghthth',3,'Object has been archived',18,1),(38,'2017-11-06 16:17:10','18','img_1',3,'Object has been archived',18,1),(39,'2017-11-06 16:17:14','19','img_1',3,'Object has been archived',18,1),(40,'2017-11-06 16:17:18','8','product3',3,'Object has been archived',18,1),(41,'2017-11-06 16:17:21','9','product4',3,'Object has been archived',18,1),(42,'2017-11-06 16:17:25','12','yi7i7i',3,'Object has been archived',18,1),(43,'2017-11-06 16:17:38','20','aaa',1,'New Item has been created',18,1),(44,'2017-11-06 16:21:07','20','aaa',2,'Object has been changed',18,1),(45,'2017-11-06 16:38:49','21','aaa',1,'New Item has been created',18,1),(46,'2017-11-06 16:42:46','21','aaa',3,'Object has been archived',18,1),(47,'2017-11-06 16:42:46','21','aaa',3,'Object has been archived',18,1),(48,'2017-11-06 16:42:53','20','aaa',3,'Object has been archived',18,1),(49,'2017-11-06 16:53:29','22','aaa',1,'New Item has been created',18,1),(50,'2017-11-06 16:55:30','23','aaa',1,'New Item has been created',18,1),(51,'2017-11-06 17:18:12','24','aaa',1,'New Item has been created',18,1),(52,'2017-11-06 17:18:23','24','aaa',3,'Object has been archived',18,1),(53,'2017-11-06 17:49:19','25','aaa',1,'New Item has been created',18,1),(54,'2017-11-06 17:53:57','26','bbb',1,'New Item has been created',18,1),(55,'2017-11-06 18:00:25','27','bbb',1,'New Item has been created',18,1),(56,'2017-11-06 18:03:39','28','bbb',1,'New Item has been created',18,1),(57,'2017-11-06 18:09:21','29','bbb',1,'New Item has been created',18,1),(58,'2017-11-06 18:09:53','30','ddd',1,'New Item has been created',18,1),(59,'2017-11-06 18:10:26','22','aaa',3,'Object has been archived',18,1),(60,'2017-11-06 18:10:31','23','aaa',3,'Object has been archived',18,1),(61,'2017-11-06 18:10:38','27','bbb',3,'Object has been archived',18,1),(62,'2017-11-06 18:10:49','28','bbb',3,'Object has been archived',18,1),(63,'2017-11-06 18:10:59','25','aaa',3,'Object has been archived',18,1),(64,'2017-11-06 18:11:04','29','bbb',3,'Object has been archived',18,1),(65,'2017-11-06 18:11:10','30','ddd',3,'Object has been archived',18,1),(66,'2017-11-06 18:11:14','26','bbb',3,'Object has been archived',18,1),(67,'2017-11-06 18:11:39','31','aaa',1,'New Item has been created',18,1),(68,'2017-11-06 18:12:52','32','aaa',1,'New Item has been created',18,1),(69,'2017-11-06 18:13:30','33','aaa',1,'New Item has been created',18,1),(70,'2017-11-06 18:17:58','34','aaa',1,'New Item has been created',18,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_45f3b1d93ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'content type','contenttypes','contenttype'),(4,'session','sessions','session'),(5,'log entry','admin','logentry'),(6,'cors model','corsheaders','corsmodel'),(7,'display','displays','display'),(8,'page','displays','page'),(9,'element','displays','element'),(10,'box','displays','box'),(11,'picture','displays','picture'),(12,'category','products','category'),(13,'tax rate','products','taxrate'),(14,'modifier group','products','modifiergroup'),(15,'modifier','products','modifier'),(16,'printer','products','printer'),(17,'historical product','products','historicalproduct'),(18,'product','products','product'),(19,'discount','products','discount'),(20,'store','products','store'),(21,'table section','products','tablesection'),(22,'table','products','table'),(23,'terminal','products','terminal'),(24,'reward','products','reward'),(25,'csv','products','csv'),(26,'shift','payments','shift'),(27,'payout','payments','payout'),(28,'payment','payments','payment'),(29,'order','order','order'),(30,'order item','order','orderitem'),(31,'order option','order','orderoption'),(32,'order modifier','order','ordermodifier'),(33,'shared order','order','sharedorder'),(34,'employee','employees','employee'),(35,'customer','employees','customer'),(36,'time clock','employees','timeclock'),(37,'csv customer','employees','csvcustomer'),(38,'supplier','employees','supplier'),(39,'token','authtoken','token'),(40,'project version','terminalapi','projectversion'),(41,'customer group','taskin','customergroup'),(42,'special prices','taskin','specialprices'),(43,'db settings','dbsettings','dbsettings'),(44,'purchase','purchase','purchase'),(45,'purchase item','purchase','purchaseitem'),(46,'kv store','thumbnail','kvstore');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'employees','0001_initial','2017-11-06 09:20:32'),(2,'contenttypes','0001_initial','2017-11-06 09:20:33'),(3,'admin','0001_initial','2017-11-06 09:20:36'),(4,'auth','0001_initial','2017-11-06 09:20:42'),(5,'order','0001_initial','2017-11-06 09:20:45'),(6,'products','0001_initial','2017-11-06 09:21:15'),(7,'dbsettings','0001_initial','2017-11-06 09:21:19'),(8,'dbsettings','0002_auto_20160222_0114','2017-11-06 09:21:20'),(9,'dbsettings','0003_auto_20160226_0140','2017-11-06 09:21:22'),(10,'dbsettings','0004_auto_20160226_0141','2017-11-06 09:21:23'),(11,'dbsettings','0005_auto_20160226_0144','2017-11-06 09:21:23'),(12,'dbsettings','0006_auto_20160226_0150','2017-11-06 09:21:25'),(13,'displays','0001_initial','2017-11-06 09:21:34'),(14,'taskin','0001_initial','2017-11-06 09:21:37'),(15,'employees','0002_auto_20160217_2031','2017-11-06 09:21:48'),(16,'employees','0003_auto_20160217_2041','2017-11-06 09:21:51'),(17,'employees','0004_csvcustomer','2017-11-06 09:21:52'),(18,'employees','0005_supplier','2017-11-06 09:21:53'),(19,'employees','0006_auto_20160415_1329','2017-11-06 09:21:54'),(20,'employees','0007_auto_20160415_1334','2017-11-06 09:21:55'),(21,'employees','0008_employee_photo','2017-11-06 09:21:57'),(22,'employees','0009_auto_20171026_1433','2017-11-06 09:21:59'),(23,'payments','0001_initial','2017-11-06 09:22:15'),(24,'order','0002_auto_20160217_2031','2017-11-06 09:22:39'),(25,'order','0003_auto_20160326_0100','2017-11-06 09:22:41'),(26,'order','0004_auto_20161207_1713','2017-11-06 09:22:43'),(27,'order','0005_auto_20161208_1712','2017-11-06 09:22:44'),(28,'order','0006_auto_20170617_1416','2017-11-06 09:22:44'),(29,'order','0007_auto_20170622_1740','2017-11-06 09:22:47'),(30,'order','0008_auto_20170803_1700','2017-11-06 09:22:47'),(31,'payments','0002_payment_check_number','2017-11-06 09:22:49'),(32,'products','0002_historicalproduct','2017-11-06 09:22:51'),(33,'products','0003_auto_20160303_1908','2017-11-06 09:22:55'),(34,'products','0004_product_suppliers','2017-11-06 09:22:59'),(35,'products','0005_auto_20161201_1044','2017-11-06 09:23:00'),(36,'products','0006_auto_20161202_1041','2017-11-06 09:23:03'),(37,'products','0007_auto_20161202_1107','2017-11-06 09:23:04'),(38,'products','0008_auto_20161202_1108','2017-11-06 09:23:05'),(39,'products','0009_auto_20161207_1348','2017-11-06 09:23:09'),(40,'products','0010_original_data_migration','2017-11-06 09:23:10'),(41,'purchase','0001_initial','2017-11-06 09:23:18'),(42,'purchase','0002_auto_20160415_1842','2017-11-06 09:23:20'),(43,'purchase','0003_auto_20160415_2017','2017-11-06 09:23:22'),(44,'purchase','0004_auto_20160426_1723','2017-11-06 09:23:25'),(45,'purchase','0005_auto_20160517_1112','2017-11-06 09:23:28'),(46,'sessions','0001_initial','2017-11-06 09:23:28'),(47,'terminalapi','0001_initial','2017-11-06 09:23:29'),(48,'terminalapi','0002_auto_20160303_0201','2017-11-06 09:23:29');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('2edhbedzg0xmv0ueppsurbz3qq9737rp','YWM2ZGRlMTkwYjNhODU3MjNlMGViMjZkZTk2M2MyMzE5MGM1OGY5MDp7Il9hdXRoX3VzZXJfaWQiOjEsInJlc3VsdF9xcyI6IlNFTEVDVCBgcHJvZHVjdHNfcHJvZHVjdGAuYGlkYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBuYW1lYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBkZXNjcmlwdGlvbmAsIGBwcm9kdWN0c19wcm9kdWN0YC5gaW1hZ2VgLCBgcHJvZHVjdHNfcHJvZHVjdGAuYGNvbG9yYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBzb3J0aW5nYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBjb3N0YCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBwcmljZWAsIGBwcm9kdWN0c19wcm9kdWN0YC5gYmFyY29kZWAsIGBwcm9kdWN0c19wcm9kdWN0YC5gc3RvY2tgLCBgcHJvZHVjdHNfcHJvZHVjdGAuYHRheF9yYXRlX2lkYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmB0YXhfc3RhdHVzYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBhY3RpdmVgLCBgcHJvZHVjdHNfcHJvZHVjdGAuYGFyY2hpdmVkYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBwcmljZV9hZGp1c3RgLCBgcHJvZHVjdHNfcHJvZHVjdGAuYHByaW50X3RvYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBwcmludGVyX2lkYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBjaGFuZ2VfcmVhc29uYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBzdG9ja19jaGFuZ2VgIEZST00gYHByb2R1Y3RzX3Byb2R1Y3RgIFdIRVJFIChgcHJvZHVjdHNfcHJvZHVjdGAuYGFyY2hpdmVkYCA9IEZhbHNlIEFORCBOT1QgKGBwcm9kdWN0c19wcm9kdWN0YC5gaWRgID0gLTEpKSBPUkRFUiBCWSBgcHJvZHVjdHNfcHJvZHVjdGAuYG5hbWVgIEFTQyIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2NTA4YzUyODI3MTRkMzljYjNiYmIyNzU2MzA1ZmZjMDdlMWM3YWIiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJlbXBsb3llZXMuYmFja2VuZC5Pd25lckF1dGhNb2RlbEJhY2tlbmQifQ==','2017-11-06 11:10:58'),('bajmvq0pw0m1wht8me5uew7qx38c0j2b','ZDY5YjhmMTkxYWMyYjQ1NjVmZTczYjU3ODkxZDE0NGM4NTU2Mzc4MDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImVtcGxveWVlcy5iYWNrZW5kLk93bmVyQXV0aE1vZGVsQmFja2VuZCIsInJlc3VsdF9xcyI6IlNFTEVDVCBgcHJvZHVjdHNfcHJvZHVjdGAuYGlkYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBuYW1lYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBkZXNjcmlwdGlvbmAsIGBwcm9kdWN0c19wcm9kdWN0YC5gaW1hZ2VgLCBgcHJvZHVjdHNfcHJvZHVjdGAuYGNvbG9yYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBzb3J0aW5nYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBjb3N0YCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBwcmljZWAsIGBwcm9kdWN0c19wcm9kdWN0YC5gYmFyY29kZWAsIGBwcm9kdWN0c19wcm9kdWN0YC5gc3RvY2tgLCBgcHJvZHVjdHNfcHJvZHVjdGAuYHRheF9yYXRlX2lkYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmB0YXhfc3RhdHVzYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBhY3RpdmVgLCBgcHJvZHVjdHNfcHJvZHVjdGAuYGFyY2hpdmVkYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBwcmljZV9hZGp1c3RgLCBgcHJvZHVjdHNfcHJvZHVjdGAuYHByaW50X3RvYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBwcmludGVyX2lkYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBjaGFuZ2VfcmVhc29uYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBzdG9ja19jaGFuZ2VgIEZST00gYHByb2R1Y3RzX3Byb2R1Y3RgIFdIRVJFIChgcHJvZHVjdHNfcHJvZHVjdGAuYGFyY2hpdmVkYCA9IEZhbHNlIEFORCBOT1QgKGBwcm9kdWN0c19wcm9kdWN0YC5gaWRgID0gLTEpKSBPUkRFUiBCWSBgcHJvZHVjdHNfcHJvZHVjdGAuYG5hbWVgIEFTQyIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2NTA4YzUyODI3MTRkMzljYjNiYmIyNzU2MzA1ZmZjMDdlMWM3YWIiLCJfYXV0aF91c2VyX2lkIjoxfQ==','2017-11-06 18:37:59'),('g7f3hj3pwxc03vo4hd0cscir9lg99p51','MGZkNzY0MDNmYzMzNTlhMzE0MmE5MDYxMDJjMjI3MTk4OTEzZGViYjp7InVybCI6Ij9zdGFydD1Ob3ZlbWJlcjA4LDIwMTcxMjowMEFNJmVuZD1Ob3ZlbWJlcjA4LDIwMTcxMTo1OVBNJm9wdGlvbj0wIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTY1MDhjNTI4MjcxNGQzOWNiM2JiYjI3NTYzMDVmZmMwN2UxYzdhYiIsIl9hdXRoX3VzZXJfaWQiOjEsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImVtcGxveWVlcy5iYWNrZW5kLk93bmVyQXV0aE1vZGVsQmFja2VuZCJ9','2017-11-08 13:59:23'),('m2dir763luwflcf4ounujkgj6rre6oyi','ODExNzg3YTNlOGEwN2FmZTA4NWE5ZWQ4YzAxYmEwMThhY2ExOGFkYjp7Il9hdXRoX3VzZXJfaGFzaCI6ImE2NTA4YzUyODI3MTRkMzljYjNiYmIyNzU2MzA1ZmZjMDdlMWM3YWIiLCJfYXV0aF91c2VyX2lkIjoxLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJlbXBsb3llZXMuYmFja2VuZC5Pd25lckF1dGhNb2RlbEJhY2tlbmQifQ==','2017-11-06 09:46:08'),('qiwh8kn8a83krsvbkjdr9a4ysn09ucum','YWM2ZGRlMTkwYjNhODU3MjNlMGViMjZkZTk2M2MyMzE5MGM1OGY5MDp7Il9hdXRoX3VzZXJfaWQiOjEsInJlc3VsdF9xcyI6IlNFTEVDVCBgcHJvZHVjdHNfcHJvZHVjdGAuYGlkYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBuYW1lYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBkZXNjcmlwdGlvbmAsIGBwcm9kdWN0c19wcm9kdWN0YC5gaW1hZ2VgLCBgcHJvZHVjdHNfcHJvZHVjdGAuYGNvbG9yYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBzb3J0aW5nYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBjb3N0YCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBwcmljZWAsIGBwcm9kdWN0c19wcm9kdWN0YC5gYmFyY29kZWAsIGBwcm9kdWN0c19wcm9kdWN0YC5gc3RvY2tgLCBgcHJvZHVjdHNfcHJvZHVjdGAuYHRheF9yYXRlX2lkYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmB0YXhfc3RhdHVzYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBhY3RpdmVgLCBgcHJvZHVjdHNfcHJvZHVjdGAuYGFyY2hpdmVkYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBwcmljZV9hZGp1c3RgLCBgcHJvZHVjdHNfcHJvZHVjdGAuYHByaW50X3RvYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBwcmludGVyX2lkYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBjaGFuZ2VfcmVhc29uYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBzdG9ja19jaGFuZ2VgIEZST00gYHByb2R1Y3RzX3Byb2R1Y3RgIFdIRVJFIChgcHJvZHVjdHNfcHJvZHVjdGAuYGFyY2hpdmVkYCA9IEZhbHNlIEFORCBOT1QgKGBwcm9kdWN0c19wcm9kdWN0YC5gaWRgID0gLTEpKSBPUkRFUiBCWSBgcHJvZHVjdHNfcHJvZHVjdGAuYG5hbWVgIEFTQyIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2NTA4YzUyODI3MTRkMzljYjNiYmIyNzU2MzA1ZmZjMDdlMWM3YWIiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJlbXBsb3llZXMuYmFja2VuZC5Pd25lckF1dGhNb2RlbEJhY2tlbmQifQ==','2017-11-06 13:28:09'),('wzinfngmfg5nysh1lhdcgm99xzpiy9ha','YWM2ZGRlMTkwYjNhODU3MjNlMGViMjZkZTk2M2MyMzE5MGM1OGY5MDp7Il9hdXRoX3VzZXJfaWQiOjEsInJlc3VsdF9xcyI6IlNFTEVDVCBgcHJvZHVjdHNfcHJvZHVjdGAuYGlkYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBuYW1lYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBkZXNjcmlwdGlvbmAsIGBwcm9kdWN0c19wcm9kdWN0YC5gaW1hZ2VgLCBgcHJvZHVjdHNfcHJvZHVjdGAuYGNvbG9yYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBzb3J0aW5nYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBjb3N0YCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBwcmljZWAsIGBwcm9kdWN0c19wcm9kdWN0YC5gYmFyY29kZWAsIGBwcm9kdWN0c19wcm9kdWN0YC5gc3RvY2tgLCBgcHJvZHVjdHNfcHJvZHVjdGAuYHRheF9yYXRlX2lkYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmB0YXhfc3RhdHVzYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBhY3RpdmVgLCBgcHJvZHVjdHNfcHJvZHVjdGAuYGFyY2hpdmVkYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBwcmljZV9hZGp1c3RgLCBgcHJvZHVjdHNfcHJvZHVjdGAuYHByaW50X3RvYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBwcmludGVyX2lkYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBjaGFuZ2VfcmVhc29uYCwgYHByb2R1Y3RzX3Byb2R1Y3RgLmBzdG9ja19jaGFuZ2VgIEZST00gYHByb2R1Y3RzX3Byb2R1Y3RgIFdIRVJFIChgcHJvZHVjdHNfcHJvZHVjdGAuYGFyY2hpdmVkYCA9IEZhbHNlIEFORCBOT1QgKGBwcm9kdWN0c19wcm9kdWN0YC5gaWRgID0gLTEpKSBPUkRFUiBCWSBgcHJvZHVjdHNfcHJvZHVjdGAuYG5hbWVgIEFTQyIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2NTA4YzUyODI3MTRkMzljYjNiYmIyNzU2MzA1ZmZjMDdlMWM3YWIiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJlbXBsb3llZXMuYmFja2VuZC5Pd25lckF1dGhNb2RlbEJhY2tlbmQifQ==','2017-11-06 12:58:33');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employees_csvcustomer`
--

DROP TABLE IF EXISTS `employees_csvcustomer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `employees_csvcustomer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_csv` varchar(100) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees_csvcustomer`
--

LOCK TABLES `employees_csvcustomer` WRITE;
/*!40000 ALTER TABLE `employees_csvcustomer` DISABLE KEYS */;
/*!40000 ALTER TABLE `employees_csvcustomer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employees_customer`
--

DROP TABLE IF EXISTS `employees_customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `employees_customer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(32) NOT NULL,
  `last_name` varchar(32) NOT NULL,
  `email` varchar(75) DEFAULT NULL,
  `phone` varchar(32) DEFAULT NULL,
  `profile_key` varchar(32) DEFAULT NULL,
  `address` varchar(32) DEFAULT NULL,
  `rewards_points` int(11) DEFAULT NULL,
  `account_number` varchar(64) NOT NULL,
  `notes` longtext,
  `archived` tinyint(1) NOT NULL,
  `created` datetime NOT NULL,
  `city` varchar(58) DEFAULT NULL,
  `state` varchar(2) DEFAULT NULL,
  `zipcode` varchar(8) DEFAULT NULL,
  `group_id` int(11),
  PRIMARY KEY (`id`),
  KEY `employees_customer_0e939a4f` (`group_id`),
  CONSTRAINT `employees_c_group_id_767904501b477272_fk_taskin_customergroup_id` FOREIGN KEY (`group_id`) REFERENCES `taskin_customergroup` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees_customer`
--

LOCK TABLES `employees_customer` WRITE;
/*!40000 ALTER TABLE `employees_customer` DISABLE KEYS */;
/*!40000 ALTER TABLE `employees_customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employees_employee`
--

DROP TABLE IF EXISTS `employees_employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `employees_employee` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `email` varchar(75) NOT NULL,
  `name` varchar(32) NOT NULL,
  `address` varchar(32) DEFAULT NULL,
  `address2` varchar(32) DEFAULT NULL,
  `city` varchar(32) DEFAULT NULL,
  `state` varchar(2) DEFAULT NULL,
  `zipcode` varchar(8) DEFAULT NULL,
  `phone` varchar(60) DEFAULT NULL,
  `pin` int(11) DEFAULT NULL,
  `role` int(11) NOT NULL,
  `vein_string` longtext NOT NULL,
  `hourly_rate` decimal(5,2) DEFAULT NULL,
  `archived` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created` datetime NOT NULL,
  `store_id` int(11) DEFAULT NULL,
  `photo` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `employees_employee_pin_52e5bb59b62b5799_uniq` (`pin`),
  KEY `employees_employee_7473547c` (`store_id`),
  CONSTRAINT `employees_employe_store_id_704c1ee44e5f5f04_fk_products_store_id` FOREIGN KEY (`store_id`) REFERENCES `products_store` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees_employee`
--

LOCK TABLES `employees_employee` WRITE;
/*!40000 ALTER TABLE `employees_employee` DISABLE KEYS */;
INSERT INTO `employees_employee` VALUES (1,'pbkdf2_sha256$15000$wo5ZGt5P79JW$u6mFB9BWpGgACHUy4kKmVcaiLdZhqk7weUPT+XKKP1s=','2017-11-08 13:36:35',1,'root@root.com','default',NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,'',NULL,0,1,1,'2017-11-06 09:24:52',NULL,'');
/*!40000 ALTER TABLE `employees_employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employees_employee_groups`
--

DROP TABLE IF EXISTS `employees_employee_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `employees_employee_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `employee_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `employee_id` (`employee_id`,`group_id`),
  KEY `employees_employee_groups_dcc97e32` (`employee_id`),
  KEY `employees_employee_groups_0e939a4f` (`group_id`),
  CONSTRAINT `employees__employee_id_2339a0df6e38c28a_fk_employees_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `employees_employee` (`id`),
  CONSTRAINT `employees_employee_gr_group_id_509384a1266ba692_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees_employee_groups`
--

LOCK TABLES `employees_employee_groups` WRITE;
/*!40000 ALTER TABLE `employees_employee_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `employees_employee_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employees_employee_user_permissions`
--

DROP TABLE IF EXISTS `employees_employee_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `employees_employee_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `employee_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `employee_id` (`employee_id`,`permission_id`),
  KEY `employees_employee_user_permissions_dcc97e32` (`employee_id`),
  KEY `employees_employee_user_permissions_8373b171` (`permission_id`),
  CONSTRAINT `employees__employee_id_52c8d4ae5919d44c_fk_employees_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `employees_employee` (`id`),
  CONSTRAINT `employees_em_permission_id_42c044487793717_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees_employee_user_permissions`
--

LOCK TABLES `employees_employee_user_permissions` WRITE;
/*!40000 ALTER TABLE `employees_employee_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `employees_employee_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employees_supplier`
--

DROP TABLE IF EXISTS `employees_supplier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `employees_supplier` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `supplier` varchar(32) NOT NULL,
  `default_markup` int(10) unsigned NOT NULL,
  `description` longtext NOT NULL,
  `company` varchar(32) NOT NULL,
  `first_name` varchar(32) NOT NULL,
  `last_name` varchar(32) NOT NULL,
  `archived` tinyint(1) NOT NULL,
  `created` datetime NOT NULL,
  `phone` varchar(60) DEFAULT NULL,
  `mobile` varchar(60) DEFAULT NULL,
  `fax` varchar(60) DEFAULT NULL,
  `email` varchar(75) NOT NULL,
  `website` varchar(200) DEFAULT NULL,
  `street` varchar(32) DEFAULT NULL,
  `suburb` varchar(32) DEFAULT NULL,
  `postcode` varchar(8) DEFAULT NULL,
  `state` varchar(2) DEFAULT NULL,
  `country` varchar(2) NOT NULL,
  `city` varchar(32),
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees_supplier`
--

LOCK TABLES `employees_supplier` WRITE;
/*!40000 ALTER TABLE `employees_supplier` DISABLE KEYS */;
/*!40000 ALTER TABLE `employees_supplier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employees_timeclock`
--

DROP TABLE IF EXISTS `employees_timeclock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `employees_timeclock` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time_in` datetime NOT NULL,
  `time_out` datetime DEFAULT NULL,
  `archived` tinyint(1) NOT NULL,
  `employee_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `employees_timeclock_dcc97e32` (`employee_id`),
  CONSTRAINT `employees__employee_id_47be08eb07b2ae28_fk_employees_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `employees_employee` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees_timeclock`
--

LOCK TABLES `employees_timeclock` WRITE;
/*!40000 ALTER TABLE `employees_timeclock` DISABLE KEYS */;
/*!40000 ALTER TABLE `employees_timeclock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_order`
--

DROP TABLE IF EXISTS `order_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `number` varchar(32) NOT NULL,
  `subtotal` double NOT NULL,
  `tax_total` double NOT NULL,
  `discount_total` double NOT NULL,
  `grand_total` double NOT NULL,
  `balance_remaining` double DEFAULT NULL,
  `open_date` datetime DEFAULT NULL,
  `hold_date` datetime DEFAULT NULL,
  `close_date` datetime DEFAULT NULL,
  `status` int(11) NOT NULL,
  `description` varchar(128) DEFAULT NULL,
  `discount_orders` double DEFAULT NULL,
  `terminal_id` int(11),
  `customer_id` int(11),
  `emp_close_id` int(11),
  `emp_open_id` int(11),
  `shift_id` int(11),
  PRIMARY KEY (`id`),
  KEY `order_order_cb24373b` (`customer_id`),
  KEY `order_order_5629d4f3` (`emp_close_id`),
  KEY `order_order_c0f4937d` (`emp_open_id`),
  KEY `order_order_92547d67` (`shift_id`),
  CONSTRAINT `order_ord_emp_close_id_7bccb039918a913e_fk_employees_employee_id` FOREIGN KEY (`emp_close_id`) REFERENCES `employees_employee` (`id`),
  CONSTRAINT `order_orde_customer_id_39b6d97ea93ecc28_fk_employees_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `employees_customer` (`id`),
  CONSTRAINT `order_orde_emp_open_id_42127e7ff649c63d_fk_employees_employee_id` FOREIGN KEY (`emp_open_id`) REFERENCES `employees_employee` (`id`),
  CONSTRAINT `order_order_shift_id_33d9dcbf8e8cab0f_fk_payments_shift_id` FOREIGN KEY (`shift_id`) REFERENCES `payments_shift` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_order`
--

LOCK TABLES `order_order` WRITE;
/*!40000 ALTER TABLE `order_order` DISABLE KEYS */;
INSERT INTO `order_order` VALUES (-1,'-1',0,0,0,0,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `order_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_orderitem`
--

DROP TABLE IF EXISTS `order_orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_orderitem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `price` double NOT NULL,
  `cost` double NOT NULL,
  `discount` double NOT NULL,
  `tax` double NOT NULL,
  `void_status` int(11) DEFAULT NULL,
  `quantity` double NOT NULL,
  `terminal_id` int(11),
  `employee_id` int(11),
  `order_id` int(11) NOT NULL,
  `product_id` int(11),
  `create_at` datetime,
  `voided_at` datetime,
  PRIMARY KEY (`id`),
  KEY `order_orderitem_dcc97e32` (`employee_id`),
  KEY `order_orderitem_69dfcb07` (`order_id`),
  KEY `order_orderitem_9bea82de` (`product_id`),
  CONSTRAINT `order_orde_employee_id_4fa81c11d949d9c9_fk_employees_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `employees_employee` (`id`),
  CONSTRAINT `order_orderit_product_id_60f2917df56d825b_fk_products_product_id` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`),
  CONSTRAINT `order_orderitem_order_id_106c2c8cde864eb4_fk_order_order_id` FOREIGN KEY (`order_id`) REFERENCES `order_order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_orderitem`
--

LOCK TABLES `order_orderitem` WRITE;
/*!40000 ALTER TABLE `order_orderitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_orderitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_ordermodifier`
--

DROP TABLE IF EXISTS `order_ordermodifier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_ordermodifier` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `cost` double NOT NULL,
  `price` double NOT NULL,
  `void_status` tinyint(1) NOT NULL,
  `group_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `oryginal_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_ordermodifier_0e939a4f` (`group_id`),
  KEY `order_ordermodifier_82bfda79` (`item_id`),
  KEY `order_ordermodifier_3d6e7283` (`oryginal_id`),
  CONSTRAINT `order_ord_group_id_47f063b91332bf83_fk_products_modifiergroup_id` FOREIGN KEY (`group_id`) REFERENCES `products_modifiergroup` (`id`),
  CONSTRAINT `order_order_oryginal_id_73ec91f8d6975f36_fk_products_modifier_id` FOREIGN KEY (`oryginal_id`) REFERENCES `products_modifier` (`id`),
  CONSTRAINT `order_ordermodifi_item_id_30c7cefd50f8dc3a_fk_order_orderitem_id` FOREIGN KEY (`item_id`) REFERENCES `order_orderitem` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_ordermodifier`
--

LOCK TABLES `order_ordermodifier` WRITE;
/*!40000 ALTER TABLE `order_ordermodifier` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_ordermodifier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_orderoption`
--

DROP TABLE IF EXISTS `order_orderoption`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_orderoption` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `cost` double NOT NULL,
  `price` double NOT NULL,
  `item_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_orderoption_82bfda79` (`item_id`),
  KEY `order_orderoption_9bea82de` (`product_id`),
  CONSTRAINT `order_orderop_product_id_1826423c38bfb99d_fk_products_product_id` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`),
  CONSTRAINT `order_orderoption_item_id_6afba887a109b5fc_fk_order_orderitem_id` FOREIGN KEY (`item_id`) REFERENCES `order_orderitem` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_orderoption`
--

LOCK TABLES `order_orderoption` WRITE;
/*!40000 ALTER TABLE `order_orderoption` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_orderoption` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_sharedorder`
--

DROP TABLE IF EXISTS `order_sharedorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_sharedorder` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `identifier` varchar(512) NOT NULL,
  `order_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_sharedorder_69dfcb07` (`order_id`),
  CONSTRAINT `order_sharedorder_order_id_7500a406fc7e269e_fk_order_order_id` FOREIGN KEY (`order_id`) REFERENCES `order_order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_sharedorder`
--

LOCK TABLES `order_sharedorder` WRITE;
/*!40000 ALTER TABLE `order_sharedorder` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_sharedorder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments_payment`
--

DROP TABLE IF EXISTS `payments_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payments_payment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `amount` double NOT NULL,
  `amount_paid` double DEFAULT NULL,
  `tips` double DEFAULT NULL,
  `change_amount` double NOT NULL,
  `card_lastfour` varchar(4) DEFAULT NULL,
  `payment_type` varchar(255) NOT NULL,
  `payment_date` datetime NOT NULL,
  `payment_form` varchar(64) DEFAULT NULL,
  `authorization` varchar(64) DEFAULT NULL,
  `transaction_type` int(11) NOT NULL,
  `processor_response` varchar(100) NOT NULL,
  `batch_num` varchar(100) DEFAULT NULL,
  `approval_code` int(11) DEFAULT NULL,
  `transaction_id` varchar(100) DEFAULT NULL,
  `terminal_id` int(11) DEFAULT NULL,
  `signature` longtext,
  `void_ref` int(11) DEFAULT NULL,
  `employee_id` int(11) DEFAULT NULL,
  `order_id` int(11) NOT NULL,
  `shift_id` int(11),
  `check_number` varchar(20),
  PRIMARY KEY (`id`),
  KEY `payments_payment_dcc97e32` (`employee_id`),
  KEY `payments_payment_69dfcb07` (`order_id`),
  KEY `payments_payment_92547d67` (`shift_id`),
  CONSTRAINT `payments_p_employee_id_23bee1294f2ae9a4_fk_employees_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `employees_employee` (`id`),
  CONSTRAINT `payments_payment_order_id_656d0e9a60e08287_fk_order_order_id` FOREIGN KEY (`order_id`) REFERENCES `order_order` (`id`),
  CONSTRAINT `payments_payment_shift_id_58fa1cf5020fba2d_fk_payments_shift_id` FOREIGN KEY (`shift_id`) REFERENCES `payments_shift` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments_payment`
--

LOCK TABLES `payments_payment` WRITE;
/*!40000 ALTER TABLE `payments_payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments_payout`
--

DROP TABLE IF EXISTS `payments_payout`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payments_payout` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `payout_type` varchar(7) NOT NULL,
  `payout_value` double DEFAULT NULL,
  `payout_time` datetime DEFAULT NULL,
  `payout_note` varchar(100) DEFAULT NULL,
  `employee_id` int(11) NOT NULL,
  `shift_id` int(11),
  `terminal_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `payments_payout_dcc97e32` (`employee_id`),
  KEY `payments_payout_92547d67` (`shift_id`),
  KEY `payments_payout_d6d2c654` (`terminal_id`),
  CONSTRAINT `payments_p_employee_id_2cc33ecc78780d23_fk_employees_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `employees_employee` (`id`),
  CONSTRAINT `payments_payo_terminal_id_862aa11d5f41a5_fk_products_terminal_id` FOREIGN KEY (`terminal_id`) REFERENCES `products_terminal` (`id`),
  CONSTRAINT `payments_payout_shift_id_69fbe9c7d155030e_fk_payments_shift_id` FOREIGN KEY (`shift_id`) REFERENCES `payments_shift` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments_payout`
--

LOCK TABLES `payments_payout` WRITE;
/*!40000 ALTER TABLE `payments_payout` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments_payout` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments_shift`
--

DROP TABLE IF EXISTS `payments_shift`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payments_shift` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `shift_open_date` datetime NOT NULL,
  `shift_update_date` datetime NOT NULL,
  `shift_close_date` datetime DEFAULT NULL,
  `opening_amount` double DEFAULT NULL,
  `total_cashtenders` double DEFAULT NULL,
  `total_cashreturns` double DEFAULT NULL,
  `total_drops` double DEFAULT NULL,
  `total_payouts` double DEFAULT NULL,
  `closing_amount` double DEFAULT NULL,
  `over_shortage` double DEFAULT NULL,
  `close_shift_employee_id` int(11) DEFAULT NULL,
  `open_shift_employee_id` int(11) NOT NULL,
  `terminal_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `payments_shift_53ea5063` (`close_shift_employee_id`),
  KEY `payments_shift_8b528328` (`open_shift_employee_id`),
  KEY `payments_shift_d6d2c654` (`terminal_id`),
  CONSTRAINT `D4dc4d09a7327a0db90a9c24b0b404f5` FOREIGN KEY (`close_shift_employee_id`) REFERENCES `employees_employee` (`id`),
  CONSTRAINT `f93f983ef25a4bb4a0e3904b8183c72d` FOREIGN KEY (`open_shift_employee_id`) REFERENCES `employees_employee` (`id`),
  CONSTRAINT `payments_sh_terminal_id_74b9d1811867f91c_fk_products_terminal_id` FOREIGN KEY (`terminal_id`) REFERENCES `products_terminal` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments_shift`
--

LOCK TABLES `payments_shift` WRITE;
/*!40000 ALTER TABLE `payments_shift` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments_shift` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_category`
--

DROP TABLE IF EXISTS `products_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `color` int(11) NOT NULL,
  `sorting` int(11) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `archived` tinyint(1) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `products_category_6be37982` (`parent_id`),
  CONSTRAINT `products_cate_parent_id_3715c35667b8fc22_fk_products_category_id` FOREIGN KEY (`parent_id`) REFERENCES `products_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_category`
--

LOCK TABLES `products_category` WRITE;
/*!40000 ALTER TABLE `products_category` DISABLE KEYS */;
INSERT INTO `products_category` VALUES (1,'Category1',1,0,1,'',0,NULL);
/*!40000 ALTER TABLE `products_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_csv`
--

DROP TABLE IF EXISTS `products_csv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_csv` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_csv` varchar(100) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_csv`
--

LOCK TABLES `products_csv` WRITE;
/*!40000 ALTER TABLE `products_csv` DISABLE KEYS */;
/*!40000 ALTER TABLE `products_csv` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_discount`
--

DROP TABLE IF EXISTS `products_discount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_discount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `value` double NOT NULL,
  `type` int(11) NOT NULL,
  `archived` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_discount`
--

LOCK TABLES `products_discount` WRITE;
/*!40000 ALTER TABLE `products_discount` DISABLE KEYS */;
/*!40000 ALTER TABLE `products_discount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_historicalproduct`
--

DROP TABLE IF EXISTS `products_historicalproduct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_historicalproduct` (
  `id` int(11) NOT NULL,
  `name` varchar(64) NOT NULL,
  `image` longtext,
  `color` int(11) DEFAULT NULL,
  `sorting` int(11) DEFAULT NULL,
  `cost` double DEFAULT NULL,
  `price` double DEFAULT NULL,
  `barcode` varchar(250) DEFAULT NULL,
  `stock` int(11) DEFAULT NULL,
  `tax_status` int(11) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `archived` tinyint(1) NOT NULL,
  `price_adjust` int(11) NOT NULL,
  `print_to` tinyint(1) NOT NULL,
  `history_id` int(11) NOT NULL AUTO_INCREMENT,
  `history_date` datetime NOT NULL,
  `history_type` varchar(1) NOT NULL,
  `history_user_id` int(11) DEFAULT NULL,
  `printer_id` int(11) DEFAULT NULL,
  `tax_rate_id` int(11) DEFAULT NULL,
  `change_reason` varchar(100),
  `stock_change` int(11) NOT NULL,
  `description` varchar(224),
  PRIMARY KEY (`history_id`),
  KEY `products_historicalproduct_b80bb774` (`id`),
  KEY `products_historicalproduct_e7d5ef68` (`history_user_id`),
  KEY `products_historicalproduct_54c293f7` (`printer_id`),
  KEY `products_historicalproduct_b88bc50f` (`tax_rate_id`),
  CONSTRAINT `produc_history_user_id_19d9ab2180805d5a_fk_employees_employee_id` FOREIGN KEY (`history_user_id`) REFERENCES `employees_employee` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_historicalproduct`
--

LOCK TABLES `products_historicalproduct` WRITE;
/*!40000 ALTER TABLE `products_historicalproduct` DISABLE KEYS */;
INSERT INTO `products_historicalproduct` VALUES (1,'Product1','product_images/Ideal-landscape.jpg',1,0,1,1,'1',0,1,1,0,0,0,1,'2017-11-06 10:44:37','+',1,NULL,1,'Update product',0,'Product1'),(2,'Product2','product_images/thumb-1920-16347.jpg',1,0,0,0,'',0,1,1,0,0,0,2,'2017-11-06 10:45:45','+',1,NULL,1,'Update product',0,'Product2'),(3,'fdkjfljwo','product_images/Ideal-landscape_FFNhU89.jpg',1,0,0,0,'',0,1,1,0,0,0,3,'2017-11-06 12:25:25','+',1,NULL,1,'Update product',0,'dfjoejfoiej'),(4,'efef','product_images/thumb-1920-16347_jkkkKsl.jpg',1,0,0,0,'',0,1,1,0,0,0,4,'2017-11-06 12:25:45','+',1,NULL,1,'Update product',0,'dfef'),(4,'efef','product_images/thumb-1920-16347_jkkkKsl.jpg',1,0,0,0,'',0,1,1,1,0,0,5,'2017-11-06 12:26:08','~',1,NULL,1,'Update product',0,'dfef'),(3,'fdkjfljwo','product_images/Ideal-landscape_FFNhU89.jpg',1,0,0,0,'',0,1,1,1,0,0,6,'2017-11-06 12:26:16','~',1,NULL,1,'Update product',0,'dfjoejfoiej'),(1,'Product1','product_images/Ideal-landscape.jpg',1,0,1,1,'1',0,1,1,1,0,0,7,'2017-11-06 12:26:21','~',1,NULL,1,'Update product',0,'Product1'),(2,'Product2','product_images/thumb-1920-16347.jpg',1,0,0,0,'',0,1,1,1,0,0,8,'2017-11-06 12:26:25','~',1,NULL,1,'Update product',0,'Product2'),(5,'ddd','product_images/Ideal-landscape_5g4MNhc.jpg',1,0,0,0,'',0,1,1,0,0,0,9,'2017-11-06 12:33:58','+',1,NULL,1,'Update product',0,'ddd'),(6,'dgrgr','product_images/thumb-1920-16347_lynaZ0t.jpg',1,0,0,0,'',0,1,1,0,0,0,10,'2017-11-06 12:34:25','+',1,NULL,1,'Update product',0,'rgrgrg'),(7,'dfegeg','product_images/Ideal-landscape_AgHIfyY.jpg',1,0,0,0,'',0,1,1,0,0,0,11,'2017-11-06 13:08:08','+',1,NULL,1,'Update product',0,'egegeg'),(8,'product3','product_images/Ideal-landscape_k6vXvnx.jpg',1,0,12,10,'',0,1,1,0,0,0,12,'2017-11-06 13:34:31','+',1,NULL,1,'Update product',0,'aaa'),(9,'product4','product_images/applewatch_productred_brown.jpg',1,0,1,1,'',0,1,1,0,0,0,13,'2017-11-06 13:40:45','+',1,NULL,1,'Update product',0,'product4'),(10,'aaa','product_images/20160909120530-108060944-A.jpeg',1,0,0,0,'',0,1,1,0,0,0,14,'2017-11-06 13:50:08','+',1,NULL,1,'Update product',0,'aaa'),(11,'ghthth','product_images/applewatch_productred_brown_82vEiyf.jpg',1,0,0,0,'',0,1,1,0,0,0,15,'2017-11-06 14:25:42','+',1,NULL,1,'Update product',0,'tjtjtj'),(12,'yi7i7i','product_images/applewatch_productred_brown_PnMvUe2.jpg',1,0,0,0,'',0,1,1,0,0,0,16,'2017-11-06 14:27:56','+',1,NULL,1,'Update product',0,'7i7i7i'),(13,'fgrgrg','product_images/applewatch_productred_brown_IrvXB3J.jpg',1,0,0,0,'',0,1,1,0,0,0,17,'2017-11-06 14:34:51','+',1,NULL,1,'Update product',0,'rtrfdferf'),(14,'aaa','product_images/applewatch_productred_brown_mez01dS.jpg',1,0,0,0,'',0,1,1,0,0,0,18,'2017-11-06 14:39:14','+',1,NULL,1,'Update product',0,'aaaa'),(15,'aaa','product_images/20160909120530-108060944-A_Wk7SX7o.jpeg',4,0,0,0,'',0,1,1,0,0,0,19,'2017-11-06 14:45:41','+',1,NULL,1,'Update product',0,'aaaa'),(16,'Image','product_images/20160909120530-108060944-A_jinii0U.jpeg',1,0,0,0,'',0,1,1,0,0,0,20,'2017-11-06 14:52:48','+',1,NULL,1,'Update product',0,'image'),(15,'aaa','product_images/20160909120530-108060944-A_Wk7SX7o.jpeg',4,0,0,0,'',0,1,1,1,0,0,21,'2017-11-06 14:53:00','~',1,NULL,1,'Update product',0,'aaaa'),(17,'Image','product_images/20160909120530-108060944-A_xFa3gyK.jpeg',1,0,0,0,'',0,1,1,0,0,0,22,'2017-11-06 14:53:23','+',1,NULL,1,'Update product',0,''),(16,'Image','product_images/20160909120530-108060944-A_jinii0U.jpeg',1,0,0,0,'',0,1,1,1,0,0,23,'2017-11-06 14:53:38','~',1,NULL,1,'Update product',0,'image'),(17,'Image','product_images/20160909120530-108060944-A_xFa3gyK.jpeg',1,0,0,0,'',0,1,1,1,0,0,24,'2017-11-06 14:53:46','~',1,NULL,1,'Update product',0,''),(18,'img_1','product_images/applewatch_productred_brown_9kqU3F8.jpg',1,0,0,0,'',0,1,1,0,0,0,25,'2017-11-06 15:06:59','+',1,NULL,1,'Update product',0,''),(19,'img_1','product_images/20160909120530-108060944-A_QbiY1ig.jpeg',1,0,0,0,'',0,1,1,0,0,0,26,'2017-11-06 15:43:03','+',1,NULL,1,'Update product',0,''),(14,'aaa','',1,0,0,0,'',0,1,1,0,0,0,27,'2017-11-06 15:43:42','~',1,NULL,1,'Update product',0,'aaaa'),(10,'aaa','',1,0,0,0,'',0,1,1,0,0,0,28,'2017-11-06 15:44:06','~',1,NULL,1,'Update product',0,'aaa'),(5,'ddd','',1,0,0,0,'',0,1,1,0,0,0,29,'2017-11-06 15:44:36','~',1,NULL,1,'Update product',0,'ddd'),(5,'ddd','',1,0,0,0,'',0,1,1,1,0,0,30,'2017-11-06 15:44:42','~',1,NULL,1,'Update product',0,'ddd'),(14,'aaa','',1,0,0,0,'',0,1,1,1,0,0,31,'2017-11-06 16:15:53','~',1,NULL,1,'Update product',0,'aaaa'),(10,'aaa','',1,0,0,0,'',0,1,1,1,0,0,32,'2017-11-06 16:16:07','~',1,NULL,1,'Update product',0,'aaa'),(7,'dfegeg','product_images/Ideal-landscape_AgHIfyY.jpg',1,0,0,0,'',0,1,1,1,0,0,33,'2017-11-06 16:16:53','~',1,NULL,1,'Update product',0,'egegeg'),(6,'dgrgr','product_images/thumb-1920-16347_lynaZ0t.jpg',1,0,0,0,'',0,1,1,1,0,0,34,'2017-11-06 16:16:58','~',1,NULL,1,'Update product',0,'rgrgrg'),(13,'fgrgrg','product_images/applewatch_productred_brown_IrvXB3J.jpg',1,0,0,0,'',0,1,1,1,0,0,35,'2017-11-06 16:17:02','~',1,NULL,1,'Update product',0,'rtrfdferf'),(11,'ghthth','product_images/applewatch_productred_brown_82vEiyf.jpg',1,0,0,0,'',0,1,1,1,0,0,36,'2017-11-06 16:17:06','~',1,NULL,1,'Update product',0,'tjtjtj'),(18,'img_1','product_images/applewatch_productred_brown_9kqU3F8.jpg',1,0,0,0,'',0,1,1,1,0,0,37,'2017-11-06 16:17:10','~',1,NULL,1,'Update product',0,''),(19,'img_1','product_images/20160909120530-108060944-A_QbiY1ig.jpeg',1,0,0,0,'',0,1,1,1,0,0,38,'2017-11-06 16:17:14','~',1,NULL,1,'Update product',0,''),(8,'product3','product_images/Ideal-landscape_k6vXvnx.jpg',1,0,12,10,'',0,1,1,1,0,0,39,'2017-11-06 16:17:18','~',1,NULL,1,'Update product',0,'aaa'),(9,'product4','product_images/applewatch_productred_brown.jpg',1,0,1,1,'',0,1,1,1,0,0,40,'2017-11-06 16:17:21','~',1,NULL,1,'Update product',0,'product4'),(12,'yi7i7i','product_images/applewatch_productred_brown_PnMvUe2.jpg',1,0,0,0,'',0,1,1,1,0,0,41,'2017-11-06 16:17:25','~',1,NULL,1,'Update product',0,'7i7i7i'),(20,'aaa','product_images/applewatch_productred_brown_6LL9Qup.jpg',1,0,0,0,'',0,1,1,0,0,0,42,'2017-11-06 16:17:38','+',1,NULL,1,'Update product',0,'bbb'),(20,'aaa','',1,0,0,0,'',0,1,1,0,0,0,43,'2017-11-06 16:21:07','~',1,NULL,1,'Update product',0,'bbb'),(21,'aaa','product_images/applewatch_productred_brown_W4BhC68.jpg',1,0,0,0,'',0,1,1,0,0,0,44,'2017-11-06 16:38:42','+',1,NULL,1,'Update product',0,''),(21,'aaa','product_images/applewatch_productred_brown_W4BhC68.jpg',1,0,0,0,'',0,1,1,1,0,0,45,'2017-11-06 16:42:46','~',1,NULL,1,'Update product',0,''),(21,'aaa','product_images/applewatch_productred_brown_W4BhC68.jpg',1,0,0,0,'',0,1,1,1,0,0,46,'2017-11-06 16:42:46','~',1,NULL,1,'Update product',0,''),(20,'aaa','',1,0,0,0,'',0,1,1,1,0,0,47,'2017-11-06 16:42:52','~',1,NULL,1,'Update product',0,'bbb'),(22,'aaa','product_images/applewatch_productred_brown.jpg',1,0,0,0,'',0,1,1,0,0,0,48,'2017-11-06 16:53:28','+',1,NULL,1,'Update product',0,''),(23,'aaa','product_images/applewatch_productred_brown.jpg',1,0,0,0,'',0,1,1,0,0,0,49,'2017-11-06 16:55:30','+',1,NULL,1,'Update product',0,''),(24,'aaa','product_images/applewatch_productred_brown.jpg',1,0,0,0,'',0,1,1,0,0,0,50,'2017-11-06 17:18:09','+',1,NULL,1,'Update product',0,''),(24,'aaa','product_images/applewatch_productred_brown.jpg',1,0,0,0,'',0,1,1,1,0,0,51,'2017-11-06 17:18:23','~',1,NULL,1,'Update product',0,''),(25,'aaa','product_images/applewatch_productred_brown.png',1,0,0,0,'',0,1,1,0,0,0,52,'2017-11-06 17:49:19','+',1,NULL,1,'Update product',0,''),(26,'bbb','product_images/20160909120530-108060944-A.png',1,0,0,0,'',0,1,1,0,0,0,53,'2017-11-06 17:53:57','+',1,NULL,1,'Update product',0,''),(27,'bbb','product_images/20160909120530-108060944-A.png',1,0,0,0,'',0,1,1,0,0,0,54,'2017-11-06 18:00:25','+',1,NULL,1,'Update product',0,''),(28,'bbb','product_images/20160909120530-108060944-A.png',1,0,0,0,'',0,1,1,0,0,0,55,'2017-11-06 18:03:38','+',1,NULL,1,'Update product',0,''),(29,'bbb','product_images/applewatch_productred_brown.jpg',1,0,0,0,'',0,1,1,0,0,0,56,'2017-11-06 18:09:21','+',1,NULL,1,'Update product',0,''),(30,'ddd','product_images/20160909120530-108060944-A_6Ao77zl.png',1,0,0,0,'',0,1,1,0,0,0,57,'2017-11-06 18:09:53','+',1,NULL,1,'Update product',0,''),(22,'aaa','product_images/applewatch_productred_brown.jpg',1,0,0,0,'',0,1,1,1,0,0,58,'2017-11-06 18:10:26','~',1,NULL,1,'Update product',0,''),(23,'aaa','product_images/applewatch_productred_brown.jpg',1,0,0,0,'',0,1,1,1,0,0,59,'2017-11-06 18:10:31','~',1,NULL,1,'Update product',0,''),(27,'bbb','product_images/20160909120530-108060944-A.png',1,0,0,0,'',0,1,1,1,0,0,60,'2017-11-06 18:10:38','~',1,NULL,1,'Update product',0,''),(28,'bbb','product_images/20160909120530-108060944-A.png',1,0,0,0,'',0,1,1,1,0,0,61,'2017-11-06 18:10:49','~',1,NULL,1,'Update product',0,''),(25,'aaa','product_images/applewatch_productred_brown.png',1,0,0,0,'',0,1,1,1,0,0,62,'2017-11-06 18:10:59','~',1,NULL,1,'Update product',0,''),(29,'bbb','product_images/applewatch_productred_brown.jpg',1,0,0,0,'',0,1,1,1,0,0,63,'2017-11-06 18:11:04','~',1,NULL,1,'Update product',0,''),(30,'ddd','product_images/20160909120530-108060944-A_6Ao77zl.png',1,0,0,0,'',0,1,1,1,0,0,64,'2017-11-06 18:11:10','~',1,NULL,1,'Update product',0,''),(26,'bbb','product_images/20160909120530-108060944-A.png',1,0,0,0,'',0,1,1,1,0,0,65,'2017-11-06 18:11:14','~',1,NULL,1,'Update product',0,''),(31,'aaa','product_images/20160909120530-108060944-A.png',1,0,0,0,'',0,1,1,0,0,0,66,'2017-11-06 18:11:39','+',1,NULL,1,'Update product',0,''),(32,'aaa','product_images/20160909120530-108060944-A.png',1,0,0,0,'',0,1,1,0,0,0,67,'2017-11-06 18:12:52','+',1,NULL,1,'Update product',0,''),(33,'aaa','product_images/applewatch_productred_brown.png',1,0,0,0,'',0,1,1,0,0,0,68,'2017-11-06 18:13:29','+',1,NULL,1,'Update product',0,''),(34,'aaa','product_images/PNG_transparency_demonstration_1.png',1,0,0,0,'',0,1,1,0,0,0,69,'2017-11-06 18:17:58','+',1,NULL,1,'Update product',0,'');
/*!40000 ALTER TABLE `products_historicalproduct` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_modifier`
--

DROP TABLE IF EXISTS `products_modifier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_modifier` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `cost` double NOT NULL,
  `price` double NOT NULL,
  `active` tinyint(1) NOT NULL,
  `archived` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_modifier`
--

LOCK TABLES `products_modifier` WRITE;
/*!40000 ALTER TABLE `products_modifier` DISABLE KEYS */;
/*!40000 ALTER TABLE `products_modifier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_modifier_group`
--

DROP TABLE IF EXISTS `products_modifier_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_modifier_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modifier_id` int(11) NOT NULL,
  `modifiergroup_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `modifier_id` (`modifier_id`,`modifiergroup_id`),
  KEY `products_modifier_group_ec903c61` (`modifier_id`),
  KEY `products_modifier_group_3331850c` (`modifiergroup_id`),
  CONSTRAINT `pr_modifiergroup_id_a58c0cdb92f4bec_fk_products_modifiergroup_id` FOREIGN KEY (`modifiergroup_id`) REFERENCES `products_modifiergroup` (`id`),
  CONSTRAINT `products_mo_modifier_id_2b39d6816d7f374a_fk_products_modifier_id` FOREIGN KEY (`modifier_id`) REFERENCES `products_modifier` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_modifier_group`
--

LOCK TABLES `products_modifier_group` WRITE;
/*!40000 ALTER TABLE `products_modifier_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `products_modifier_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_modifiergroup`
--

DROP TABLE IF EXISTS `products_modifiergroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_modifiergroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `select_multiple` tinyint(1) NOT NULL,
  `archived` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_modifiergroup`
--

LOCK TABLES `products_modifiergroup` WRITE;
/*!40000 ALTER TABLE `products_modifiergroup` DISABLE KEYS */;
/*!40000 ALTER TABLE `products_modifiergroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_printer`
--

DROP TABLE IF EXISTS `products_printer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_printer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `local_ip` varchar(128) DEFAULT NULL,
  `archived` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_printer`
--

LOCK TABLES `products_printer` WRITE;
/*!40000 ALTER TABLE `products_printer` DISABLE KEYS */;
/*!40000 ALTER TABLE `products_printer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_product`
--

DROP TABLE IF EXISTS `products_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `color` int(11) DEFAULT NULL,
  `sorting` int(11) DEFAULT NULL,
  `cost` double DEFAULT NULL,
  `price` double DEFAULT NULL,
  `barcode` varchar(250) DEFAULT NULL,
  `stock` int(11) DEFAULT NULL,
  `tax_status` int(11) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `archived` tinyint(1) NOT NULL,
  `price_adjust` int(11) NOT NULL,
  `print_to` tinyint(1) NOT NULL,
  `printer_id` int(11) DEFAULT NULL,
  `tax_rate_id` int(11) NOT NULL,
  `change_reason` varchar(100),
  `stock_change` int(11) NOT NULL,
  `description` varchar(224),
  PRIMARY KEY (`id`),
  KEY `products_product_54c293f7` (`printer_id`),
  KEY `products_product_b88bc50f` (`tax_rate_id`),
  CONSTRAINT `products_pro_tax_rate_id_654587d4c2b0692e_fk_products_taxrate_id` FOREIGN KEY (`tax_rate_id`) REFERENCES `products_taxrate` (`id`),
  CONSTRAINT `products_prod_printer_id_52096244492c7389_fk_products_printer_id` FOREIGN KEY (`printer_id`) REFERENCES `products_printer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_product`
--

LOCK TABLES `products_product` WRITE;
/*!40000 ALTER TABLE `products_product` DISABLE KEYS */;
INSERT INTO `products_product` VALUES (-1,'Custom','',1,0,0,0,NULL,0,1,1,0,0,0,NULL,1,'',0,''),(1,'Product1','product_images/Ideal-landscape.jpg',1,0,1,1,'1',0,1,1,1,0,0,NULL,1,'Update product',0,'Product1'),(2,'Product2','product_images/thumb-1920-16347.jpg',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,'Product2'),(3,'fdkjfljwo','product_images/Ideal-landscape_FFNhU89.jpg',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,'dfjoejfoiej'),(4,'efef','product_images/thumb-1920-16347_jkkkKsl.jpg',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,'dfef'),(5,'ddd','',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,'ddd'),(6,'dgrgr','product_images/thumb-1920-16347_lynaZ0t.jpg',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,'rgrgrg'),(7,'dfegeg','product_images/Ideal-landscape_AgHIfyY.jpg',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,'egegeg'),(8,'product3','product_images/Ideal-landscape_k6vXvnx.jpg',1,0,12,10,'',0,1,1,1,0,0,NULL,1,'Update product',0,'aaa'),(9,'product4','product_images/applewatch_productred_brown.jpg',1,0,1,1,'',0,1,1,1,0,0,NULL,1,'Update product',0,'product4'),(10,'aaa','',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,'aaa'),(11,'ghthth','product_images/applewatch_productred_brown_82vEiyf.jpg',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,'tjtjtj'),(12,'yi7i7i','product_images/applewatch_productred_brown_PnMvUe2.jpg',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,'7i7i7i'),(13,'fgrgrg','product_images/applewatch_productred_brown_IrvXB3J.jpg',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,'rtrfdferf'),(14,'aaa','',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,'aaaa'),(15,'aaa','product_images/20160909120530-108060944-A_Wk7SX7o.jpeg',4,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,'aaaa'),(16,'Image','product_images/20160909120530-108060944-A_jinii0U.jpeg',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,'image'),(17,'Image','product_images/20160909120530-108060944-A_xFa3gyK.jpeg',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,''),(18,'img_1','product_images/applewatch_productred_brown_9kqU3F8.jpg',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,''),(19,'img_1','product_images/20160909120530-108060944-A_QbiY1ig.jpeg',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,''),(20,'aaa','',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,'bbb'),(21,'aaa','product_images/applewatch_productred_brown_W4BhC68.jpg',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,''),(22,'aaa','product_images/applewatch_productred_brown.jpg',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,''),(23,'aaa','product_images/applewatch_productred_brown.jpg',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,''),(24,'aaa','product_images/applewatch_productred_brown.jpg',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,''),(25,'aaa','product_images/applewatch_productred_brown.png',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,''),(26,'bbb','product_images/20160909120530-108060944-A.png',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,''),(27,'bbb','product_images/20160909120530-108060944-A.png',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,''),(28,'bbb','product_images/20160909120530-108060944-A.png',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,''),(29,'bbb','product_images/applewatch_productred_brown.jpg',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,''),(30,'ddd','product_images/20160909120530-108060944-A_6Ao77zl.png',1,0,0,0,'',0,1,1,1,0,0,NULL,1,'Update product',0,''),(31,'aaa','product_images/20160909120530-108060944-A.png',1,0,0,0,'',0,1,1,0,0,0,NULL,1,'Update product',0,''),(32,'aaa','product_images/20160909120530-108060944-A.png',1,0,0,0,'',0,1,1,0,0,0,NULL,1,'Update product',0,''),(33,'aaa','product_images/applewatch_productred_brown.png',1,0,0,0,'',0,1,1,0,0,0,NULL,1,'Update product',0,''),(34,'aaa','product_images/PNG_transparency_demonstration_1.png',1,0,0,0,'',0,1,1,0,0,0,NULL,1,'Update product',0,'');
/*!40000 ALTER TABLE `products_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_product_categories`
--

DROP TABLE IF EXISTS `products_product_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_product_categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_id` (`product_id`,`category_id`),
  KEY `products_product_categories_9bea82de` (`product_id`),
  KEY `products_product_categories_b583a629` (`category_id`),
  CONSTRAINT `products_pr_category_id_73d3fc020dbc11ca_fk_products_category_id` FOREIGN KEY (`category_id`) REFERENCES `products_category` (`id`),
  CONSTRAINT `products_prod_product_id_69783a905e61b960_fk_products_product_id` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_product_categories`
--

LOCK TABLES `products_product_categories` WRITE;
/*!40000 ALTER TABLE `products_product_categories` DISABLE KEYS */;
INSERT INTO `products_product_categories` VALUES (1,1,1),(2,2,1),(3,3,1),(4,4,1),(22,5,1),(6,6,1),(7,7,1),(8,8,1),(9,9,1),(21,10,1),(11,11,1),(12,12,1),(13,13,1),(20,14,1),(15,15,1),(16,16,1),(17,17,1),(18,18,1),(19,19,1),(24,20,1),(25,21,1),(26,22,1),(27,23,1),(28,24,1),(29,25,1),(30,26,1),(31,27,1),(32,28,1),(33,29,1),(34,30,1),(35,31,1),(36,32,1),(37,33,1),(38,34,1);
/*!40000 ALTER TABLE `products_product_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_product_modifier_groups`
--

DROP TABLE IF EXISTS `products_product_modifier_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_product_modifier_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `modifiergroup_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_id` (`product_id`,`modifiergroup_id`),
  KEY `products_product_modifier_groups_9bea82de` (`product_id`),
  KEY `products_product_modifier_groups_3331850c` (`modifiergroup_id`),
  CONSTRAINT `p_modifiergroup_id_4f63bbb818392e24_fk_products_modifiergroup_id` FOREIGN KEY (`modifiergroup_id`) REFERENCES `products_modifiergroup` (`id`),
  CONSTRAINT `products_prod_product_id_6728484027975f55_fk_products_product_id` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_product_modifier_groups`
--

LOCK TABLES `products_product_modifier_groups` WRITE;
/*!40000 ALTER TABLE `products_product_modifier_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `products_product_modifier_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_product_suppliers`
--

DROP TABLE IF EXISTS `products_product_suppliers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_product_suppliers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `supplier_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_id` (`product_id`,`supplier_id`),
  KEY `products_product_suppliers_9bea82de` (`product_id`),
  KEY `products_product_suppliers_c5bcd634` (`supplier_id`),
  CONSTRAINT `products_p_supplier_id_54e889bb0d373582_fk_employees_supplier_id` FOREIGN KEY (`supplier_id`) REFERENCES `employees_supplier` (`id`),
  CONSTRAINT `products_produ_product_id_745ebe69b8196fc_fk_products_product_id` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_product_suppliers`
--

LOCK TABLES `products_product_suppliers` WRITE;
/*!40000 ALTER TABLE `products_product_suppliers` DISABLE KEYS */;
/*!40000 ALTER TABLE `products_product_suppliers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_reward`
--

DROP TABLE IF EXISTS `products_reward`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_reward` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) NOT NULL,
  `points_redeem` int(11) NOT NULL,
  `discount` varchar(250) NOT NULL,
  `discount_type` varchar(250) NOT NULL,
  `discount_value` varchar(128) DEFAULT NULL,
  `discount_text` varchar(250) DEFAULT NULL,
  `reward_type` int(11) NOT NULL,
  `archived` tinyint(1) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `discount_type_item_id` int(11) DEFAULT NULL,
  `store_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `products_reward_24a232a7` (`discount_type_item_id`),
  KEY `products_reward_7473547c` (`store_id`),
  CONSTRAINT `pr_discount_type_item_id_692e6e98fe14855f_fk_products_product_id` FOREIGN KEY (`discount_type_item_id`) REFERENCES `products_product` (`id`),
  CONSTRAINT `products_reward_store_id_70c6e351dbae992b_fk_products_store_id` FOREIGN KEY (`store_id`) REFERENCES `products_store` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_reward`
--

LOCK TABLES `products_reward` WRITE;
/*!40000 ALTER TABLE `products_reward` DISABLE KEYS */;
/*!40000 ALTER TABLE `products_reward` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_store`
--

DROP TABLE IF EXISTS `products_store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_store` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `archived` tinyint(1) NOT NULL,
  `name` varchar(128) NOT NULL,
  `logo` varchar(100) DEFAULT NULL,
  `number` int(11) NOT NULL,
  `address` varchar(128) NOT NULL,
  `address_2` varchar(128) DEFAULT NULL,
  `city` varchar(128) NOT NULL,
  `state` varchar(100) NOT NULL,
  `zipcode` varchar(128) NOT NULL,
  `phone` varchar(16) DEFAULT NULL,
  `fax` varchar(16) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  `website` varchar(200) DEFAULT NULL,
  `package` int(11) NOT NULL,
  `timezone` varchar(64) NOT NULL,
  `xweb_url` varchar(128) NOT NULL,
  `xweb_id` varchar(128) NOT NULL,
  `xweb_terminal_id` varchar(128) NOT NULL,
  `xweb_auth_key` varchar(128) NOT NULL,
  `xweb_industry` varchar(128) NOT NULL,
  `tax_rate_id` int(11),
  PRIMARY KEY (`id`),
  KEY `products_store_b88bc50f` (`tax_rate_id`),
  CONSTRAINT `products_sto_tax_rate_id_5a1c8561ac556c52_fk_products_taxrate_id` FOREIGN KEY (`tax_rate_id`) REFERENCES `products_taxrate` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_store`
--

LOCK TABLES `products_store` WRITE;
/*!40000 ALTER TABLE `products_store` DISABLE KEYS */;
INSERT INTO `products_store` VALUES (1,0,'My Store','',1,'1 Biyo Way','','New York','NY','10016','315-325-0050','','support@biyowallet.com','biyowallet.com',1,'US/Central','','','','','',1);
/*!40000 ALTER TABLE `products_store` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_table`
--

DROP TABLE IF EXISTS `products_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_table` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `archived` tinyint(1) NOT NULL,
  `table_name` varchar(128) NOT NULL,
  `table_image` int(11) DEFAULT NULL,
  `x_value` double DEFAULT NULL,
  `y_value` double DEFAULT NULL,
  `number_people` int(11) NOT NULL,
  `current_order_id` int(11) DEFAULT NULL,
  `section_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `products_table_dc86d18c` (`current_order_id`),
  KEY `products_table_730f6511` (`section_id`),
  CONSTRAINT `products_section_id_621f746b6a3abeeb_fk_products_tablesection_id` FOREIGN KEY (`section_id`) REFERENCES `products_tablesection` (`id`),
  CONSTRAINT `products_tab_current_order_id_15ba452a18f117c2_fk_order_order_id` FOREIGN KEY (`current_order_id`) REFERENCES `order_order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_table`
--

LOCK TABLES `products_table` WRITE;
/*!40000 ALTER TABLE `products_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `products_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_tablesection`
--

DROP TABLE IF EXISTS `products_tablesection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_tablesection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `archived` tinyint(1) NOT NULL,
  `section_name` varchar(128) NOT NULL,
  `store_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `products_tablesection_7473547c` (`store_id`),
  CONSTRAINT `products_tablesec_store_id_1da19e678567bbfb_fk_products_store_id` FOREIGN KEY (`store_id`) REFERENCES `products_store` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_tablesection`
--

LOCK TABLES `products_tablesection` WRITE;
/*!40000 ALTER TABLE `products_tablesection` DISABLE KEYS */;
/*!40000 ALTER TABLE `products_tablesection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_taxrate`
--

DROP TABLE IF EXISTS `products_taxrate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_taxrate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rate` double NOT NULL,
  `name` varchar(64) NOT NULL,
  `archived` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_taxrate`
--

LOCK TABLES `products_taxrate` WRITE;
/*!40000 ALTER TABLE `products_taxrate` DISABLE KEYS */;
INSERT INTO `products_taxrate` VALUES (1,8,'NY Tax Rate',0);
/*!40000 ALTER TABLE `products_taxrate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_terminal`
--

DROP TABLE IF EXISTS `products_terminal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_terminal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `mac_id` varchar(128) NOT NULL,
  `pole_display` varchar(128) DEFAULT NULL,
  `mode` int(11) DEFAULT NULL,
  `local_ip` varchar(128) DEFAULT NULL,
  `receipt_printer` varchar(128) DEFAULT NULL,
  `station_number` int(11) DEFAULT NULL,
  `master` int(11) DEFAULT NULL,
  `archived` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_terminal`
--

LOCK TABLES `products_terminal` WRITE;
/*!40000 ALTER TABLE `products_terminal` DISABLE KEYS */;
INSERT INTO `products_terminal` VALUES (-1,'First Terminal','*','pole1',2,NULL,NULL,NULL,NULL,0);
/*!40000 ALTER TABLE `products_terminal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase_purchase`
--

DROP TABLE IF EXISTS `purchase_purchase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `purchase_purchase` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `document_number` varchar(200) DEFAULT NULL,
  `status` varchar(10) NOT NULL,
  `note` longtext,
  `shipped_dt` datetime DEFAULT NULL,
  `accepted_dt` datetime DEFAULT NULL,
  `created_dt` datetime NOT NULL,
  `employee_created_id` int(11) NOT NULL,
  `employee_update_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `purchase_purchase_badf75ae` (`employee_created_id`),
  KEY `purchase_purchase_8f184ee7` (`employee_update_id`),
  CONSTRAINT `pu_employee_created_id_47a52231e0896fc7_fk_employees_employee_id` FOREIGN KEY (`employee_created_id`) REFERENCES `employees_employee` (`id`),
  CONSTRAINT `pur_employee_update_id_619faf0cc8149c5d_fk_employees_employee_id` FOREIGN KEY (`employee_update_id`) REFERENCES `employees_employee` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_purchase`
--

LOCK TABLES `purchase_purchase` WRITE;
/*!40000 ALTER TABLE `purchase_purchase` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchase_purchase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase_purchaseitem`
--

DROP TABLE IF EXISTS `purchase_purchaseitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `purchase_purchaseitem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `entered_stock` decimal(20,2) NOT NULL,
  `accepted_stock` decimal(20,2) DEFAULT NULL,
  `scan_dt` datetime DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `purchase_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `purchase_purchaseitem_9bea82de` (`product_id`),
  KEY `purchase_purchaseitem_f0ce900c` (`purchase_id`),
  CONSTRAINT `purchase_pu_purchase_id_4c38dd85620e587a_fk_purchase_purchase_id` FOREIGN KEY (`purchase_id`) REFERENCES `purchase_purchase` (`id`),
  CONSTRAINT `purchase_purc_product_id_20d8365abecafbcb_fk_products_product_id` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_purchaseitem`
--

LOCK TABLES `purchase_purchaseitem` WRITE;
/*!40000 ALTER TABLE `purchase_purchaseitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchase_purchaseitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `settings_settings`
--

DROP TABLE IF EXISTS `settings_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `settings_settings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(50) DEFAULT NULL,
  `description` longtext NOT NULL,
  `terminal_id` int(11) DEFAULT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `settings_settings_name_54803bec5d2fcc24_uniq` (`name`,`terminal_id`),
  KEY `settings_settings_d6d2c654` (`terminal_id`),
  CONSTRAINT `settings_set_terminal_id_c18492c6017a43e_fk_products_terminal_id` FOREIGN KEY (`terminal_id`) REFERENCES `products_terminal` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `settings_settings`
--

LOCK TABLES `settings_settings` WRITE;
/*!40000 ALTER TABLE `settings_settings` DISABLE KEYS */;
/*!40000 ALTER TABLE `settings_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `taskin_customergroup`
--

DROP TABLE IF EXISTS `taskin_customergroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `taskin_customergroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(125) NOT NULL,
  `archived` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `taskin_customergroup`
--

LOCK TABLES `taskin_customergroup` WRITE;
/*!40000 ALTER TABLE `taskin_customergroup` DISABLE KEYS */;
/*!40000 ALTER TABLE `taskin_customergroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `taskin_specialprices`
--

DROP TABLE IF EXISTS `taskin_specialprices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `taskin_specialprices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `price` double NOT NULL,
  `archived` tinyint(1) NOT NULL,
  `group_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `taskin_specialprices_0e939a4f` (`group_id`),
  KEY `taskin_specialprices_9bea82de` (`product_id`),
  CONSTRAINT `taskin_spec_group_id_7eeef45ca65f12c6_fk_taskin_customergroup_id` FOREIGN KEY (`group_id`) REFERENCES `taskin_customergroup` (`id`),
  CONSTRAINT `taskin_specia_product_id_79e52d73779734b0_fk_products_product_id` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `taskin_specialprices`
--

LOCK TABLES `taskin_specialprices` WRITE;
/*!40000 ALTER TABLE `taskin_specialprices` DISABLE KEYS */;
/*!40000 ALTER TABLE `taskin_specialprices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `terminalapi_projectversion`
--

DROP TABLE IF EXISTS `terminalapi_projectversion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `terminalapi_projectversion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `version` varchar(10) NOT NULL,
  `installer` varchar(100) NOT NULL,
  `password` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `terminalapi_projectversion`
--

LOCK TABLES `terminalapi_projectversion` WRITE;
/*!40000 ALTER TABLE `terminalapi_projectversion` DISABLE KEYS */;
/*!40000 ALTER TABLE `terminalapi_projectversion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `thumbnail_kvstore`
--

DROP TABLE IF EXISTS `thumbnail_kvstore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `thumbnail_kvstore` (
  `key` varchar(200) NOT NULL,
  `value` longtext NOT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `thumbnail_kvstore`
--

LOCK TABLES `thumbnail_kvstore` WRITE;
/*!40000 ALTER TABLE `thumbnail_kvstore` DISABLE KEYS */;
/*!40000 ALTER TABLE `thumbnail_kvstore` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-11-08 15:56:55
