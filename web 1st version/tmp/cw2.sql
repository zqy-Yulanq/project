/*
 Navicat Premium Data Transfer

 Source Server         : MYSQL57
 Source Server Type    : MySQL
 Source Server Version : 50725
 Source Host           : localhost:3306
 Source Schema         : cw2

 Target Server Type    : MySQL
 Target Server Version : 50725
 File Encoding         : 65001

 Date: 03/01/2021 12:27:48
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for actor
-- ----------------------------
DROP TABLE IF EXISTS `actor`;
CREATE TABLE `actor`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `update_time` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of actor
-- ----------------------------
INSERT INTO `actor` VALUES (1, '杨洋', '2021-01-03 12:22:28');

-- ----------------------------
-- Table structure for actor_tv_rel
-- ----------------------------
DROP TABLE IF EXISTS `actor_tv_rel`;
CREATE TABLE `actor_tv_rel`  (
  `tv_id` int(11) NULL DEFAULT NULL,
  `actor_id` int(11) NULL DEFAULT NULL,
  INDEX `actor_id`(`actor_id`) USING BTREE,
  INDEX `tv_id`(`tv_id`) USING BTREE,
  CONSTRAINT `actor_tv_rel_ibfk_1` FOREIGN KEY (`actor_id`) REFERENCES `actor` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `actor_tv_rel_ibfk_2` FOREIGN KEY (`tv_id`) REFERENCES `tv` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of actor_tv_rel
-- ----------------------------
INSERT INTO `actor_tv_rel` VALUES (1, 1);

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version`  (
  `version_num` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`version_num`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO `alembic_version` VALUES ('0c567669773d');

-- ----------------------------
-- Table structure for tv
-- ----------------------------
DROP TABLE IF EXISTS `tv`;
CREATE TABLE `tv`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `image` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `area` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `update_time` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tv
-- ----------------------------
INSERT INTO `tv` VALUES (1, 'IMG_3012.JPG', '旋风少女', 'Love', 'China', '2021-01-03 12:22:28');

-- ----------------------------
-- Table structure for tvrecord
-- ----------------------------
DROP TABLE IF EXISTS `tvrecord`;
CREATE TABLE `tvrecord`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tv_id` int(11) NULL DEFAULT NULL,
  `score` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `view_time` datetime(0) NULL DEFAULT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `update_time` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `tv_id`(`tv_id`) USING BTREE,
  CONSTRAINT `tvrecord_ibfk_1` FOREIGN KEY (`tv_id`) REFERENCES `tv` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tvrecord
-- ----------------------------
INSERT INTO `tvrecord` VALUES (1, 1, '7', '2020-01-03 12:26:00', '超级好看！', '2021-01-03 12:27:03');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `telephone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `gender` enum('MALE','FEMALE','SECRET','UNKNOW') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `image` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `introduce` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `join_time` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `email`(`email`) USING BTREE,
  UNIQUE INDEX `telephone`(`telephone`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, '15238681389', 'zqy', '947440142@qq.com', 'pbkdf2:sha256:150000$sFgS1itn$ee43446e208051b9d43667a21df75517184c3e0c32a469a1e25b4a502a5eb35a', 'FEMALE', 'timg.jpg', '我真的好喜欢看电视剧啊！！', '2021-01-03 12:20:51');

-- ----------------------------
-- Table structure for user_tvrecord_rel
-- ----------------------------
DROP TABLE IF EXISTS `user_tvrecord_rel`;
CREATE TABLE `user_tvrecord_rel`  (
  `tvrecord_id` int(11) NULL DEFAULT NULL,
  `user_id` int(11) NULL DEFAULT NULL,
  INDEX `tvrecord_id`(`tvrecord_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `user_tvrecord_rel_ibfk_1` FOREIGN KEY (`tvrecord_id`) REFERENCES `tvrecord` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `user_tvrecord_rel_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_tvrecord_rel
-- ----------------------------
INSERT INTO `user_tvrecord_rel` VALUES (1, 1);

SET FOREIGN_KEY_CHECKS = 1;
