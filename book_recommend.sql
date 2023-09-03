SET foreign_key_checks = 0;

DROP TABLE IF EXISTS `users`; 
DROP TABLE IF EXISTS `books`; 

DROP TABLE IF EXISTS `user_comment`;
DROP TABLE IF EXISTS `user_rating`;
DROP TABLE IF EXISTS `user_collect`;

DROP TABLE IF EXISTS `user_collect`;

DROP TABLE IF EXISTS `categories`;
DROP TABLE IF EXISTS `book_categories`;
DROP TABLE IF EXISTS `tags`;
DROP TABLE IF EXISTS `book_tags`;

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
  `isbn` varchar(20) NOT NULL DEFAULT '',
  `title` varchar(256) NOT NULL DEFAULT '', 
  `author` varchar(64) NOT NULL DEFAULT '',
  `publisher` varchar(128) NOT NULL DEFAULT '',
  `publish_date` VARCHAR(12) NOT NULL DEFAULT '',
  `page_num` int NOT NULL DEFAULT 0,
  `cover_image_url` varchar(512) NOT NULL DEFAULT '',
  `description` text ,
  `rating_num` int NOT NULL DEFAULT 0,
  `rating_avg` decimal(3,2) NOT NULL DEFAULT 0.0,
  `comment_count` int NOT NULL DEFAULT 0,
  PRIMARY KEY (`book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `categories` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `book_categories` (
  `book_id` int NOT NULL,
  `category_id` int NOT NULL,
  PRIMARY KEY (`book_id`, `category_id`),
  FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`) ON DELETE CASCADE,
  FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `tags` (
  `tag_id` int NOT NULL AUTO_INCREMENT,
  `tag_name` varchar(64) NOT NULL,
  PRIMARY KEY (`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `book_tags` (
  `book_id` int NOT NULL,
  `tag_id` int NOT NULL,
  PRIMARY KEY (`book_id`, `tag_id`),
  FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`) ON DELETE CASCADE,
  FOREIGN KEY (`tag_id`) REFERENCES `tags` (`tag_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `user_collect` (
  `collect_id` int NOT NULL AUTO_INCREMENT,
  `collect_type` tinyint NOT NULL,
  `user_id` int NOT NULL,
  `book_id` int NOT NULL,
  `collect_time` datetime NOT NULL DEFAULT NOW(),
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
  `rating_time` datetime NOT NULL DEFAULT NOW(),
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
  `create_time` datetime NOT NULL DEFAULT NOW(),
  PRIMARY KEY (`comment_id`),
  KEY `book_id` (`book_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_comment_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `Books` (`book_id`),
  CONSTRAINT `user_comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET foreign_key_checks = 1;

INSERT INTO users (username, password,register_time,is_admin) values('eric','123456',NOW(),0);
INSERT INTO categories (name) VALUES
("文学"),
("流行"),
("文化"),
("生活"),
("经管"),
("科技"),
("杂类");
