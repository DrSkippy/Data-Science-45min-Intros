
# tell RDS which database to use (very important!)
USE zzzRST;

#####
# new table creation (when necessary)
#####
DROP TABLE IF EXISTS `users_personal` ;

CREATE TABLE `users_personal` (
  `user_id` int(10) NOT NULL,
  `fav_color` CHAR (50) NOT NULL,
  `pet_name` CHAR (50) NOT NULL,
  `fav_dino` CHAR (50) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM CHARSET=utf8 COLLATE=utf8_unicode_ci;


DROP TABLE IF EXISTS `users_work` ;

CREATE TABLE `users_work` (
  `user_id` int(10) NOT NULL,
  `first_name` CHAR (50) NOT NULL,
  `last_name` CHAR (50) NOT NULL,
  `department` CHAR (50) NOT NULL,
  `company` CHAR (50) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM CHARSET=utf8 COLLATE=utf8_unicode_ci;




#######
# load local data to db table (modify path as needed)
#######
LOAD DATA LOCAL INFILE '/path/to/repo/Data-Science-45min-Intros/SQL-201/data/personal.tsv' INTO TABLE `users_personal`
   FIELDS TERMINATED BY '\t'
   LINES TERMINATED BY '\n'
   (`user_id`,
    `fav_color`,
    `pet_name`,
    `fav_dino`
    );

LOAD DATA LOCAL INFILE '/path/to/repo/Data-Science-45min-Intros/SQL-201/data/work.tsv' INTO TABLE `users_work`
   FIELDS TERMINATED BY '\t'
   LINES TERMINATED BY '\n'
   (`user_id`,
    `first_name`,
    `last_name`,
    `department`,
    `company`
    );

#######
# create indexes on important columns (more efficient to do this after loading data)
#######
CREATE INDEX dinoidx ON `users_personal` (fav_dino);
CREATE INDEX companyidx ON `users_work` (company);
CREATE INDEX nameidx ON `users_work` (first_name, last_name);

