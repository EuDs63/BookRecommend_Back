SET foreign_key_checks = 0;

DROP TABLE IF EXISTS `books`; 

DROP TABLE IF EXISTS `user_comment`;
DROP TABLE IF EXISTS `user_rating`;
DROP TABLE IF EXISTS `user_collect`;

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,	
  `password` varchar(256) NOT NULL,
  `register_time` datetime NOT NULL,
  `is_admin` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `books` (
  `book_id` int NOT NULL AUTO_INCREMENT,
  `isbn` varchar(20) NOT NULL,
  `title` varchar(256) NOT NULL, 
  `author` varchar(64) NOT NULL,
  `publisher` varchar(128) NOT NULL,
  `publish_date` datetime NOT NULL,
  `page_num` int NOT NULL,
  `category` varchar(64) NOT NULL,
  `cover_image` varchar(2048) NOT NULL,
  `description` text NOT NULL,
  `rating_num` int NOT NULL DEFAULT '0',
  `rating_avg` decimal(2,1) NOT NULL DEFAULT '0',
  `comment_count` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `user_collect` (
  `collect_id` int NOT NULL AUTO_INCREMENT,
  `collect_type` tinyint NOT NULL,
  `user_id` int NOT NULL,
  `book_id` int NOT NULL,
  `collect_time` datetime NOT NULL,
  PRIMARY KEY (`collect_id`),
  KEY `user_id` (`user_id`),
  KEY `book_id` (`book_id`),
  CONSTRAINT `user_collect_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`),
  CONSTRAINT `user_collect_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `Books` (`book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `user_rating` (
  `rating_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `book_id` int NOT NULL,
  `rating` decimal(2,1) NOT NULL,
  `rating_time` datetime NOT NULL,
  PRIMARY KEY (`rating_id`),
  KEY `user_id` (`user_id`),
  KEY `book_id` (`book_id`),
  CONSTRAINT `user_rating_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`),
  CONSTRAINT `user_rating_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `Books` (`book_id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `user_comment` (
  `comment_id` int NOT NULL AUTO_INCREMENT,
  `book_id` int NOT NULL,
  `user_id` int NOT NULL,
  `content` varchar(500) NOT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`comment_id`),
  KEY `book_id` (`book_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_comment_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `Books` (`book_id`),
  CONSTRAINT `user_comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET foreign_key_checks = 1;

INSERT INTO users (username, password,register_time,is_admin) values('eric','123456',NOW(),0);