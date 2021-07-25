#!/bin/bash
#create dabase scrapbooks and table scrappedbooks

db_name="scrapbookdb"
table_name="scrappedbooks"
db_user="myadmin"

function setup_database(){
    echo "setting database"
    echo -n "enter mysql admin password - "
    sudo mysql -u${db_user} -p << MYSQL
CREATE DATABASE IF NOT EXISTS ${db_name} CHARACTER SET utf8 COLLATE utf8_general_ci;
USE ${db_name};
CREATE TABLE IF NOT EXISTS scrapbookstb (
    id          int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    category	varchar(40) NOT NULL,
	title       varchar(200) NOT NULL,	
    price		DECIMAL NOT NULL,
	rating      char(10) NOT NULL,
	stock		char(10) NOT NULL,
    extract_date timestamp default current_timestamp
);
MYSQL
}

##############
#### MAIN ####
##############
setup_database
