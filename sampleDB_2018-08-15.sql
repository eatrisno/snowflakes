# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: pixel.mynaworks.com (MySQL 5.7.22)
# Database: sampleDB
# Generation Time: 2018-08-15 00:47:23 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table product_data
# ------------------------------------------------------------

CREATE TABLE `product_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL DEFAULT '0001-01-01',
  `data_pid` int(11) NOT NULL,
  `data_cid` int(11) NOT NULL,
  `shop_name` char(100) NOT NULL DEFAULT '',
  `name` varchar(250) NOT NULL DEFAULT '',
  `price` bigint(15) NOT NULL,
  `url` varchar(300) NOT NULL DEFAULT '',
  `image` varchar(500) DEFAULT '',
  `insert_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `status` int(2) DEFAULT NULL,
  PRIMARY KEY (`data_pid`,`date`),
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table product_detail
# ------------------------------------------------------------

CREATE TABLE `product_detail` (
  `data_pid` int(11) NOT NULL,
  `image` text,
  `name` varchar(250) DEFAULT NULL,
  `etalase` char(50) DEFAULT NULL,
  `min_buy` int(5) DEFAULT '1',
  `price` int(11) DEFAULT NULL,
  `condition` char(50) DEFAULT NULL,
  `description` text CHARACTER SET utf8,
  `video` tinytext,
  `variant` text,
  `weight` char(10) DEFAULT NULL,
  `insurance` char(10) DEFAULT NULL,
  `insert_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `status` int(2) DEFAULT NULL,
  PRIMARY KEY (`data_pid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
