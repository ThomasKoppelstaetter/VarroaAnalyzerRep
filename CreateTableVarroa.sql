DROP DATABASE IF EXISTS varroaanalyzer;
CREATE DATABASE varroaanalyzer;
USE varroaanalyzer;

CREATE TABLE `Wabe` (
  `wID` int PRIMARY KEY AUTO_INCREMENT,
  `Datum` DATETIME
);

CREATE TABLE `Zelle` (
  `zID` int PRIMARY KEY AUTO_INCREMENT,
  `wID` int NOT NULL,
  `PosX` int,
  `PosY` int,
  `Stadium` varchar(255)
);

CREATE TABLE `Bilder` (
  `bID` int PRIMARY KEY AUTO_INCREMENT,
  `zID` int NOT NULL,
  `Namen` varchar(255),
  `Pfad` varchar(255),
  `Varroaanzahl` int
);

ALTER TABLE `Zelle` ADD FOREIGN KEY (`wID`) REFERENCES `Wabe` (`wID`);
ALTER TABLE `Bilder` ADD FOREIGN KEY (`zID`) REFERENCES `Zelle` (`zID`);