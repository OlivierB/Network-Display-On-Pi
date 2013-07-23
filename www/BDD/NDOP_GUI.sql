-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 19, 2013 at 05:06 PM
-- Server version: 5.5.31
-- PHP Version: 5.4.4-14+deb7u2

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `NDOP_GUI`
--
CREATE DATABASE `NDOP_GUI` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `NDOP_GUI`;

-- --------------------------------------------------------

--
-- Table structure for table `layout`
--

CREATE TABLE IF NOT EXISTS `layout` (
  `page` int(11) NOT NULL,
  `id_module` int(11) NOT NULL,
  PRIMARY KEY (`page`),
  KEY `id_module` (`id_module`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `module`
--

CREATE TABLE IF NOT EXISTS `module` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=358 ;

-- --------------------------------------------------------

--
-- Table structure for table `module_composition_widget`
--

CREATE TABLE IF NOT EXISTS `module_composition_widget` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_module` int(11) NOT NULL,
  `id_widget` int(11) NOT NULL,
  `x` int(11) NOT NULL,
  `y` int(11) NOT NULL,
  `width` int(11) NOT NULL,
  `height` int(11) NOT NULL,
  `id_widget_parameter_set` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_widget` (`id_widget`),
  KEY `id_widget_parameter_set` (`id_widget_parameter_set`),
  KEY `id_module` (`id_module`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=275 ;

-- --------------------------------------------------------

--
-- Table structure for table `server_information`
--

CREATE TABLE IF NOT EXISTS `server_information` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `ip` varchar(15) NOT NULL,
  `port` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

-- --------------------------------------------------------

--
-- Table structure for table `widget`
--

CREATE TABLE IF NOT EXISTS `widget` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `description` text NOT NULL,
  `folder_name` varchar(50) NOT NULL,
  `updated` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `folder_name` (`folder_name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=363 ;

-- --------------------------------------------------------

--
-- Table structure for table `widget_parameter_design`
--

CREATE TABLE IF NOT EXISTS `widget_parameter_design` (
  `id_widget` int(11) NOT NULL,
  `type` varchar(10) NOT NULL,
  `description` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `updated` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_widget` (`id_widget`,`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=361 ;

-- --------------------------------------------------------

--
-- Table structure for table `widget_parameter_set`
--

CREATE TABLE IF NOT EXISTS `widget_parameter_set` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `id_widget` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`,`id_widget`),
  KEY `id_widget` (`id_widget`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=298 ;

-- --------------------------------------------------------

--
-- Table structure for table `widget_parameter_value`
--

CREATE TABLE IF NOT EXISTS `widget_parameter_value` (
  `id_set` int(11) NOT NULL,
  `id_param` int(11) NOT NULL,
  `value` varchar(50) NOT NULL,
  UNIQUE KEY `id_set_2` (`id_set`,`id_param`),
  KEY `id_param` (`id_param`),
  KEY `id_set` (`id_set`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `layout`
--
ALTER TABLE `layout`
  ADD CONSTRAINT `layout_ibfk_2` FOREIGN KEY (`id_module`) REFERENCES `module` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `module_composition_widget`
--
ALTER TABLE `module_composition_widget`
  ADD CONSTRAINT `module_composition_widget_ibfk_4` FOREIGN KEY (`id_module`) REFERENCES `module` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `module_composition_widget_ibfk_5` FOREIGN KEY (`id_widget`) REFERENCES `widget` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `module_composition_widget_ibfk_6` FOREIGN KEY (`id_widget_parameter_set`) REFERENCES `widget_parameter_set` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `widget_parameter_design`
--
ALTER TABLE `widget_parameter_design`
  ADD CONSTRAINT `widget_parameter_design_ibfk_1` FOREIGN KEY (`id_widget`) REFERENCES `widget` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `widget_parameter_set`
--
ALTER TABLE `widget_parameter_set`
  ADD CONSTRAINT `widget_parameter_set_ibfk_1` FOREIGN KEY (`id_widget`) REFERENCES `widget` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `widget_parameter_value`
--
ALTER TABLE `widget_parameter_value`
  ADD CONSTRAINT `widget_parameter_value_ibfk_1` FOREIGN KEY (`id_set`) REFERENCES `widget_parameter_set` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `widget_parameter_value_ibfk_2` FOREIGN KEY (`id_param`) REFERENCES `widget_parameter_design` (`id`) ON DELETE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
