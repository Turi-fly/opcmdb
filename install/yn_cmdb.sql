-- MySQL dump 10.13  Distrib 5.6.33, for Linux (x86_64)
--
-- Host: localhost    Database: yn_cmdb
-- ------------------------------------------------------
-- Server version	5.6.33

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
-- Table structure for table `account_cnt`
--

DROP TABLE IF EXISTS `account_cnt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_cnt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `accounts` varchar(64) DEFAULT '' COMMENT '账号',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `asset`
--

DROP TABLE IF EXISTS `asset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `asset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sn` varchar(128) DEFAULT NULL COMMENT 'snç¼–å·',
  `inner_ip` varchar(128) DEFAULT '' COMMENT 'ç®¡ç†ipåœ°å€',
  `app_ip` varchar(128) DEFAULT '' COMMENT 'åº”ç”¨ipåœ°å€',
  `remote_ip` varchar(128) DEFAULT '' COMMENT 'è¿œç¨‹ç®¡ç†å¡ip',
  `mac` varchar(128) DEFAULT '' COMMENT 'macåœ°å€',
  `hostname` varchar(64) DEFAULT '' COMMENT 'ä¸»æœºå',
  `os` varchar(64) DEFAULT '' COMMENT 'æ“ä½œç³»ç»Ÿ',
  `cpu` varchar(64) DEFAULT NULL,
  `nu_ram` int(11) NOT NULL COMMENT 'å†…å­˜ä¸ªæ•°',
  `nu_disk` int(11) NOT NULL COMMENT 'ç¡¬ç›˜ä¸ªæ•°',
  `ram` int(11) NOT NULL COMMENT 'å†…å­˜(G)',
  `disk` int(11) NOT NULL COMMENT 'ç¡¬ç›˜å¤§å°(G)',
  `idc_id` int(11) DEFAULT NULL COMMENT 'æœºæˆ¿çš„ID',
  `raid_id` int(11) DEFAULT NULL,
  `raid_type` varchar(64) DEFAULT NULL,
  `admin` varchar(32) DEFAULT '' COMMENT 'ä½¿ç”¨è€…',
  `business` varchar(32) DEFAULT '' COMMENT 'ä¸šåŠ¡',
  `remote_card` varchar(64) DEFAULT '' COMMENT 'è¿œç¨‹ç®¡ç†å¡',
  `purchase_date` date DEFAULT '1970-11-11' COMMENT 'é‡‡è´­æ—¥æœŸ(å¹´)',
  `warranty` date DEFAULT '1970-11-11' COMMENT 'ä¿ä¿®æ—¥æœŸ',
  `type_id` int(11) DEFAULT NULL,
  `model_id` int(11) DEFAULT NULL,
  `remark` varchar(128) DEFAULT '' COMMENT 'å¤‡æ³¨',
  `status` int(11) DEFAULT '0',
  `cabinet_seat_id` int(11) DEFAULT NULL,
  `spec_id` int(11) DEFAULT NULL,
  `disk_type` varchar(64) DEFAULT NULL,
  `slot_ram` int(11) DEFAULT NULL,
  `slot_disk` int(11) DEFAULT NULL,
  `nu_cpu` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cabinet`
--

DROP TABLE IF EXISTS `cabinet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cabinet` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cabinet_num` varchar(128) DEFAULT NULL COMMENT 'æœºæŸœç¼–å·',
  `position` varchar(128) DEFAULT NULL COMMENT 'æœºå™¨ä½ç½®',
  `idc_id` int(11) DEFAULT NULL COMMENT 'æœºæˆ¿çš„ID',
  `physical` int(11) DEFAULT NULL,
  `switch` int(11) DEFAULT NULL,
  `vm` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cabinet_num` (`cabinet_num`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `des_use`
--

DROP TABLE IF EXISTS `des_use`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `des_use` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `identity` varchar(128) DEFAULT '' COMMENT 'èº«ä»½',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `idc`
--

DROP TABLE IF EXISTS `idc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `idc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT '' COMMENT 'æœºæˆ¿åç§°',
  `status` int(11) DEFAULT '0',
  `address` varchar(64) DEFAULT NULL,
  `phone` varchar(64) DEFAULT NULL,
  `physical` int(11) DEFAULT NULL,
  `switch` int(11) DEFAULT NULL,
  `vm` int(11) DEFAULT NULL,
  `ip_seg` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `model`
--

DROP TABLE IF EXISTS `model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `model` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `power`
--

DROP TABLE IF EXISTS `power`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `power` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL COMMENT '权限英文名',
  `name_cn` varchar(40) NOT NULL COMMENT '权限中文名',
  `url` varchar(128) NOT NULL COMMENT '权限对应的url',
  `comment` varchar(128) NOT NULL COMMENT '备注',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL COMMENT '项目名',
  `path` varchar(128) NOT NULL COMMENT '项目代码仓库路径',
  `principal` varchar(32) NOT NULL COMMENT '负责人',
  `p_user` varchar(32) DEFAULT NULL COMMENT '有权限的用户',
  `p_group` varchar(32) DEFAULT NULL COMMENT '有权限的组',
  `create_date` date NOT NULL COMMENT '创建时间',
  `is_lock` tinyint(1) unsigned DEFAULT '0' COMMENT '是否锁定 0-未锁定 1-锁定',
  `comment` varchar(256) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `project_apply`
--

DROP TABLE IF EXISTS `project_apply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project_apply` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `project_id` int(10) NOT NULL COMMENT '对应project项目ID',
  `info` varchar(64) NOT NULL COMMENT '发布简介',
  `applicant` varchar(64) NOT NULL COMMENT '申请人',
  `version` varchar(64) DEFAULT NULL COMMENT '发布版本',
  `commit` varchar(64) NOT NULL COMMENT '代码最新版本',
  `apply_date` datetime NOT NULL COMMENT '申请时间',
  `status` int(10) DEFAULT '0' COMMENT '发布状态',
  `detail` text COMMENT '发布详情',
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_id` (`project_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `project_deploy`
--

DROP TABLE IF EXISTS `project_deploy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project_deploy` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `project_id` int(10) NOT NULL COMMENT '对应project的项目ID',
  `info` varchar(64) NOT NULL COMMENT '发布简介',
  `version` varchar(64) DEFAULT NULL COMMENT '发布版本',
  `commit` varchar(64) NOT NULL COMMENT '代码最新版本',
  `applicant` varchar(64) NOT NULL COMMENT '操作人',
  `apply_date` datetime NOT NULL COMMENT '操作时间',
  `status` int(10) DEFAULT '0' COMMENT '发布状态',
  `detail` text COMMENT '发布详情',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `project_test`
--

DROP TABLE IF EXISTS `project_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project_test` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `project_id` int(10) NOT NULL COMMENT '对应project项目ID',
  `host` varchar(64) NOT NULL COMMENT '测试主机',
  `commit` varchar(64) NOT NULL COMMENT '推送版本号',
  `pusher` varchar(128) NOT NULL COMMENT '推送人',
  `push_date` datetime NOT NULL COMMENT '推送时间',
  `comment` varchar(256) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `raid`
--

DROP TABLE IF EXISTS `raid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `raid` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `raid_level` varchar(16) DEFAULT NULL COMMENT 'raidçº§åˆ«',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL COMMENT 'è§’è‰²å',
  `name_cn` varchar(40) NOT NULL COMMENT 'è§’è‰²ä¸­æ–‡å',
  `p_id` varchar(20) NOT NULL COMMENT 'æƒé™idï¼Œå…è®¸å¤šä¸ªp_id,å­˜ä¸ºå­—ç¬¦ä¸²ç±»åž‹',
  `info` varchar(50) DEFAULT NULL COMMENT 'è§’è‰²æè¿°ä¿¡æ¯',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `spec`
--

DROP TABLE IF EXISTS `spec`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spec` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `spec` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `type`
--

DROP TABLE IF EXISTS `type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(40) NOT NULL COMMENT '用户名',
  `password` varchar(64) NOT NULL COMMENT '密码',
  `name` varchar(80) NOT NULL COMMENT '姓名',
  `email` varchar(64) NOT NULL COMMENT '公司邮箱',
  `mobile` varchar(16) DEFAULT NULL COMMENT '手机号',
  `r_id` varchar(32) NOT NULL COMMENT '角色id,允许多个r_id,存为字符串类型',
  `is_lock` tinyint(1) unsigned NOT NULL COMMENT '是否锁定 0-未锁定 1-锁定',
  `join_date` datetime DEFAULT NULL COMMENT '注册时间',
  `last_login` datetime DEFAULT NULL COMMENT '最后登录时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vm`
--

DROP TABLE IF EXISTS `vm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vm` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(128) DEFAULT NULL COMMENT 'uuid å”¯ä¸€æ ‡è¯†å·',
  `ip` varchar(64) DEFAULT '' COMMENT 'è™šæ‹Ÿæœºipåœ°å€',
  `mac` varchar(64) NOT NULL COMMENT 'è™šæ‹Ÿæœºçš„macåœ°å€',
  `cpu` varchar(64) DEFAULT NULL,
  `ram` int(11) NOT NULL COMMENT 'è™šæ‹Ÿæœºçš„å†…å­˜',
  `disk` int(11) NOT NULL COMMENT 'ç¡¬ç›˜çš„å¤§å°',
  `vm` varchar(64) NOT NULL COMMENT 'è™šæ‹Ÿæœºåç§°',
  `business` varchar(128) DEFAULT '' COMMENT 'ä¸šåŠ¡ç”¨é€”',
  `admin` varchar(32) DEFAULT '' COMMENT 'ä½¿ç”¨äºº',
  `remark` varchar(128) DEFAULT '' COMMENT 'å¤‡æ³¨',
  `status` int(11) DEFAULT '0' COMMENT 'çŠ¶æ€',
  `host_id` int(11) DEFAULT NULL COMMENT 'å®¿ä¸»æœºid',
  `use_status` int(2) DEFAULT '0',
  `des_use_id` int(4) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=331 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-31 15:11:45
