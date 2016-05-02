DROP TABLE IF EXISTS `Follow`;

CREATE TABLE `Follow` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `follower` char(25) NOT NULL,
  `followee` char(25) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `follower` (`follower`) USING HASH,
  KEY `followee` (`followee`) USING HASH
) ENGINE=MyISAM DEFAULT CHARSET=latin1;



DROP TABLE IF EXISTS `Forum`;

CREATE TABLE `Forum` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `short_name` char(35) NOT NULL,
  `user` char(25) NOT NULL,
  `name` char(35) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `short_name` (`short_name`) USING HASH,
  UNIQUE KEY `name` (`name`) USING HASH,
  KEY `user` (`user`) USING HASH
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `Forum` WRITE;
/*!40000 ALTER TABLE `Forum` DISABLE KEYS */;

INSERT INTO `Forum` (`id`, `short_name`, `user`, `name`)
VALUES
	(1691,'forum3','richard.nixon@example.com','Форум Три'),
	(1690,'forum2','example@mail.ru','Forum II'),
	(1689,'forum1','example3@mail.ru','Forum I'),
	(1688,'forumwithsufficientlylargename','example@mail.ru','Forum With Sufficiently Large Name');

/*!40000 ALTER TABLE `Forum` ENABLE KEYS */;
UNLOCK TABLES;


DROP TABLE IF EXISTS `Post`;

CREATE TABLE `Post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `thread` int(11) NOT NULL,
  `user` char(25) NOT NULL,
  `forum` char(35) NOT NULL,
  `date` datetime NOT NULL,
  `message` text NOT NULL,
  `dislikes` smallint(6) NOT NULL DEFAULT '0',
  `likes` smallint(6) NOT NULL DEFAULT '0',
  `points` smallint(6) NOT NULL DEFAULT '0',
  `parent` int(11) DEFAULT NULL,
  `path` char(50) NOT NULL DEFAULT '',
  `isHighlighted` tinyint(1) NOT NULL DEFAULT '0',
  `isApproved` tinyint(1) NOT NULL DEFAULT '0',
  `isEdited` tinyint(1) NOT NULL DEFAULT '0',
  `isSpam` tinyint(1) NOT NULL DEFAULT '0',
  `isDeleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `parent` (`parent`),
  KEY `idx_post_fu` (`forum`,`user`),
  KEY `idx_post_fd` (`forum`,`date`),
  KEY `idx_post_td` (`thread`,`date`),
  KEY `idx_post_ud` (`user`,`date`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `Post` WRITE;
/*!40000 ALTER TABLE `Post` DISABLE KEYS */;

INSERT INTO `Post` (`id`, `thread`, `user`, `forum`, `date`, `message`, `dislikes`, `likes`, `points`, `parent`, `path`, `isHighlighted`, `isApproved`, `isEdited`, `isSpam`, `isDeleted`)
VALUES
	(14125,1675,'example4@mail.ru','forum3','2016-04-05 23:58:32','my message 5my message 5my message 5my message 5my message 5my message 5my message 5my message 5my message 5my message 5my message 5',0,0,0,NULL,'0.014125',1,0,0,1,0),
	(14126,1675,'example4@mail.ru','forum3','2016-04-19 23:58:38','my message 6my message 6my message 6my message 6my message 6my message 6my message 6my message 6my message 6my message 6my message 6my message 6my message 6',0,0,0,14122,'0.014120.014122.014126',0,1,1,0,0),
	(14127,1675,'example2@mail.ru','forum3','2016-04-27 12:41:37','my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7',0,0,0,NULL,'0.014127',0,1,1,0,0),
	(14128,1676,'example4@mail.ru','forum1','2014-04-18 10:51:58','my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0',0,0,0,NULL,'0.014128',0,0,1,1,0),
	(14129,1676,'example4@mail.ru','forum1','2016-04-30 15:18:41','my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1',0,0,0,14128,'0.014128.014129',1,0,0,1,0),
	(14130,1676,'example4@mail.ru','forum1','2016-04-30 18:26:29','my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2',0,0,0,14128,'0.014128.014130',0,0,0,0,0),
	(14131,1676,'richard.nixon@example.com','forum1','2016-04-30 20:30:59','my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3',0,0,0,NULL,'0.014131',1,1,1,0,0),
	(14132,1676,'example3@mail.ru','forum1','2016-05-01 04:25:39','my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4',0,0,0,NULL,'0.014132',0,0,0,1,0),
	(14133,1676,'example3@mail.ru','forum1','2016-05-02 11:14:34','my message 5my message 5my message 5my message 5my message 5my message 5my message 5my message 5my message 5my message 5my message 5',0,0,0,NULL,'0.014133',0,0,0,0,0),
	(14134,1676,'richard.nixon@example.com','forum1','2016-05-02 13:03:46','my message 6my message 6my message 6my message 6my message 6my message 6my message 6my message 6my message 6my message 6my message 6my message 6my message 6my message 6my message 6my message 6',0,0,0,14129,'0.014128.014129.014134',1,1,0,1,0),
	(14135,1676,'example3@mail.ru','forum1','2016-05-02 13:52:27','my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7',0,0,0,14131,'0.014131.014135',0,0,1,0,0),
	(14136,1676,'richard.nixon@example.com','forum1','2016-05-02 13:53:54','my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8',0,0,0,NULL,'0.014136',0,1,1,0,0),
	(14137,1676,'richard.nixon@example.com','forum1','2016-05-02 13:54:17','my message 9my message 9my message 9my message 9my message 9my message 9my message 9my message 9my message 9my message 9my message 9my message 9my message 9my message 9my message 9my message 9my message 9my message 9my message 9',0,0,0,14131,'0.014131.014137',1,1,0,1,0),
	(14138,1677,'example4@mail.ru','forumwithsufficientlylargename','2015-01-21 13:22:49','my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0',0,0,0,NULL,'0.014138',1,0,0,0,0),
	(14139,1677,'example2@mail.ru','forumwithsufficientlylargename','2015-08-11 18:03:57','my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1',0,0,0,14138,'0.014138.014139',0,0,1,0,0),
	(14140,1677,'example4@mail.ru','forumwithsufficientlylargename','2015-09-15 18:14:10','my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2',0,0,0,14138,'0.014138.014140',1,1,1,0,0),
	(14141,1677,'example3@mail.ru','forumwithsufficientlylargename','2016-01-11 07:01:17','my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3',0,0,0,14140,'0.014138.014140.014141',1,1,1,1,0),
	(14142,1677,'example@mail.ru','forumwithsufficientlylargename','2016-01-28 14:15:06','my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4',0,0,0,14138,'0.014138.014142',1,1,1,1,0),
	(14143,1677,'richard.nixon@example.com','forumwithsufficientlylargename','2016-04-03 12:15:20','my message 5my message 5my message 5my message 5my message 5my message 5my message 5my message 5my message 5my message 5my message 5my message 5my message 5my message 5my message 5my message 5my message 5my message 5',0,0,0,14138,'0.014138.014143',1,0,0,0,0),
	(14144,1677,'richard.nixon@example.com','forumwithsufficientlylargename','2016-05-02 13:51:25','my message 6my message 6my message 6my message 6my message 6my message 6my message 6my message 6my message 6my message 6',0,0,0,NULL,'0.014144',0,0,1,0,0),
	(14145,1677,'example4@mail.ru','forumwithsufficientlylargename','2016-05-02 13:54:15','my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7',0,0,0,14141,'0.014138.014140.014141.014145',1,0,0,0,0),
	(14146,1677,'example3@mail.ru','forumwithsufficientlylargename','2016-05-02 13:54:22','my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8',0,0,0,14139,'0.014138.014139.014146',0,0,1,1,0),
	(14147,1678,'richard.nixon@example.com','forum2','2014-03-30 23:13:04','my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0',0,0,0,NULL,'0.014147',0,1,0,0,0),
	(14148,1678,'example3@mail.ru','forum2','2015-11-19 11:23:25','my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1',0,0,0,14147,'0.014147.014148',0,0,1,1,0),
	(14149,1678,'example3@mail.ru','forum2','2016-04-19 05:37:05','my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2',0,0,0,NULL,'0.014149',1,0,1,0,0),
	(14150,1678,'example2@mail.ru','forum2','2016-04-21 18:30:25','my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3',0,0,0,14149,'0.014149.014150',1,1,1,1,0),
	(14151,1678,'example4@mail.ru','forum2','2016-04-21 21:43:40','my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4',0,0,0,14147,'0.014147.014151',0,0,0,0,0),
	(14152,1678,'example@mail.ru','forum2','2016-04-27 21:08:40','my message 5my message 5my message 5my message 5my message 5my message 5my message 5my message 5my message 5my message 5my message 5',0,0,0,NULL,'0.014152',1,0,1,0,0),
	(14153,1678,'richard.nixon@example.com','forum2','2016-04-29 07:33:48','my message 6my message 6my message 6my message 6my message 6my message 6my message 6my message 6my message 6my message 6my message 6my message 6my message 6',0,0,0,NULL,'0.014153',1,1,1,1,0),
	(14154,1678,'example@mail.ru','forum2','2016-05-02 05:31:24','my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7my message 7',0,0,0,14153,'0.014153.014154',1,1,1,1,0),
	(14155,1678,'example@mail.ru','forum2','2016-05-02 07:00:53','my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8my message 8',0,0,0,14152,'0.014152.014155',0,0,0,0,0),
	(14156,1678,'example4@mail.ru','forum2','2016-05-02 10:35:31','my message 9my message 9my message 9my message 9my message 9my message 9my message 9my message 9my message 9my message 9my message 9my message 9',1,0,-1,14154,'0.014153.014154.014156',0,0,0,1,0),
	(14121,1675,'example3@mail.ru','forum3','2015-05-29 03:25:22','my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1my message 1',0,0,0,NULL,'0.014121',0,0,1,1,0),
	(14122,1675,'example2@mail.ru','forum3','2015-06-04 22:49:05','my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2my message 2',0,0,0,14120,'0.014120.014122',1,0,0,0,0),
	(14123,1675,'example2@mail.ru','forum3','2015-11-20 01:41:52','my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3my message 3',0,0,0,14122,'0.014120.014122.014123',1,0,1,1,0),
	(14124,1675,'example2@mail.ru','forum3','2015-12-22 08:57:57','my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4my message 4',0,0,0,14123,'0.014120.014122.014123.014124',0,1,1,0,0),
	(14120,1675,'example3@mail.ru','forum3','2015-02-04 06:03:53','my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0my message 0',0,0,0,NULL,'0.014120',1,0,1,0,0);

/*!40000 ALTER TABLE `Post` ENABLE KEYS */;
UNLOCK TABLES;

DELIMITER ;;
/*!50003 SET SESSION SQL_MODE="NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`localhost` */ /*!50003 TRIGGER `ins_post` BEFORE INSERT ON `Post` FOR EACH ROW BEGIN

SET NEW.path=CONCAT(IFNULL((select path from Post where id = NEW.parent), '0'), '.', (SELECT lpad(AUTO_INCREMENT, 6, 0) FROM information_schema.tables WHERE table_name = 'Post' limit 1));

CALL update_thread(NEW.thread, NEW.isDeleted);

END */;;
DELIMITER ;
/*!50003 SET SESSION SQL_MODE=@OLD_SQL_MODE */;


DROP TABLE IF EXISTS `Subscribe`;

CREATE TABLE `Subscribe` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` char(25) NOT NULL,
  `thread` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user` (`user`) USING HASH,
  KEY `thread` (`thread`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `Subscribe` WRITE;
/*!40000 ALTER TABLE `Subscribe` DISABLE KEYS */;

INSERT INTO `Subscribe` (`id`, `user`, `thread`)
VALUES
	(2088,'example4@mail.ru',1677),
	(2087,'example@mail.ru',1676),
	(2086,'richard.nixon@example.com',1675),
	(2085,'richard.nixon@example.com',1677),
	(2084,'example4@mail.ru',1677);

/*!40000 ALTER TABLE `Subscribe` ENABLE KEYS */;
UNLOCK TABLES;


DROP TABLE IF EXISTS `Thread`;

CREATE TABLE `Thread` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `forum` char(35) NOT NULL,
  `user` char(25) NOT NULL,
  `title` char(50) CHARACTER SET utf8 NOT NULL,
  `date` datetime NOT NULL,
  `message` text NOT NULL,
  `slug` char(50) NOT NULL,
  `isDeleted` tinyint(1) NOT NULL DEFAULT '0',
  `isClosed` tinyint(1) NOT NULL DEFAULT '0',
  `dislikes` smallint(6) NOT NULL DEFAULT '0',
  `likes` smallint(6) NOT NULL DEFAULT '0',
  `points` smallint(6) NOT NULL DEFAULT '0',
  `posts` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `slug` (`slug`) USING HASH,
  KEY `forum` (`forum`) USING HASH,
  KEY `idx_thread_ud` (`user`,`date`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `Thread` WRITE;
/*!40000 ALTER TABLE `Thread` DISABLE KEYS */;

INSERT INTO `Thread` (`id`, `forum`, `user`, `title`, `date`, `message`, `slug`, `isDeleted`, `isClosed`, `dislikes`, `likes`, `points`, `posts`)
VALUES
	(1676,'forum1','example4@mail.ru','Thread I','2013-12-31 00:01:01','hey!','newslug',0,0,0,0,0,10),
	(1677,'forumwithsufficientlylargename','richard.nixon@example.com','Thread II','2013-12-30 00:01:01','hey hey!','thread2',0,0,0,0,0,9),
	(1678,'forum2','example3@mail.ru','Тред Три','2013-12-29 00:01:01','hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! hey hey hey! ','thread3',0,0,0,1,1,10),
	(1675,'forum3','example@mail.ru','Thread With Sufficiently Large Title','2014-01-01 00:00:01','hey hey hey hey!','Threadwithsufficientlylargetitle',0,1,0,0,0,8);

/*!40000 ALTER TABLE `Thread` ENABLE KEYS */;
UNLOCK TABLES;


DROP TABLE IF EXISTS `User`;

CREATE TABLE `User` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` char(25) DEFAULT NULL,
  `email` char(25) NOT NULL,
  `about` text,
  `name` char(25) DEFAULT NULL,
  `isAnonymous` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`) USING HASH,
  KEY `name` (`name`) USING HASH
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;

INSERT INTO `User` (`id`, `username`, `email`, `about`, `name`, `isAnonymous`)
VALUES
	(2119,'user3','example3@mail.ru','Wowowowow!!!','NewName2',0),
	(2120,'user4','example4@mail.ru','hello im user4','Jim',0),
	(2118,'user2','example2@mail.ru','Wowowowow','NewName',0),
	(2117,NULL,'richard.nixon@example.com',NULL,NULL,1),
	(2116,'user1','example@mail.ru','hello im user1','John',0);

/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;



--
-- Dumping routines (PROCEDURE) for database 'forum_db'
--
DELIMITER ;;

# Dump of PROCEDURE update_thread
# ------------------------------------------------------------

/*!50003 DROP PROCEDURE IF EXISTS `update_thread` */;;
/*!50003 SET SESSION SQL_MODE="NO_ENGINE_SUBSTITUTION"*/;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `update_thread`(in thread_id INT, isDeleted INT)
BEGIN
CASE isDeleted
WHEN 0
THEN
	UPDATE Thread SET posts = posts+1 WHERE  id = thread_id;
ELSE
	BEGIN END;
END CASE;
END */;;

/*!50003 SET SESSION SQL_MODE=@OLD_SQL_MODE */;;
DELIMITER ;

/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
