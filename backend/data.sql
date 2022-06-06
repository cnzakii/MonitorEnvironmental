/*
 Navicat Premium Data Transfer

 Source Server         : sensor
 Source Server Type    : MySQL
 Source Server Version : 50650
 Source Host           : 43.138.132.187:3306
 Source Schema         : data

 Target Server Type    : MySQL
 Target Server Version : 50650
 File Encoding         : 65001

 Date: 02/06/2022 00:17:33
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for data
-- ----------------------------
DROP TABLE IF EXISTS `data`;
CREATE TABLE `data` (
  `time` timestamp NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  `co2` double DEFAULT NULL,
  `temperature` double DEFAULT NULL,
  `humidity` double DEFAULT NULL,
  PRIMARY KEY (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for path
-- ----------------------------
DROP TABLE IF EXISTS `path`;
CREATE TABLE `path` (
  `time` timestamp NOT NULL,
  `tfile` varchar(255) DEFAULT NULL,
  `cfile` varchar(255) DEFAULT NULL,
  `rfile` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
