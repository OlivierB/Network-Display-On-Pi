-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 18, 2013 at 02:34 PM
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

--
-- Dumping data for table `layout`
--

INSERT INTO `layout` (`page`, `id_module`) VALUES
(0, 300),
(1, 357);

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

--
-- Dumping data for table `module`
--

INSERT INTO `module` (`id`, `name`, `description`) VALUES
(300, 'Map', 'zut'),
(357, 'Daily Traffic', 'This module shows the bandwith use for the last 24 hours. You can see the local, up and down flow. The protocol use is also displayed.');

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

--
-- Dumping data for table `module_composition_widget`
--

INSERT INTO `module_composition_widget` (`id`, `id_module`, `id_widget`, `x`, `y`, `width`, `height`, `id_widget_parameter_set`) VALUES
(259, 300, 244, 0, 0, 12, 2, 179),
(273, 357, 191, 0, 0, 4, 1, 109),
(274, 357, 191, 4, 0, 5, 1, 109);

-- --------------------------------------------------------

--
-- Table structure for table `server_informations`
--

CREATE TABLE IF NOT EXISTS `server_informations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `ip` varchar(15) NOT NULL,
  `port` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `server_informations`
--

INSERT INTO `server_informations` (`id`, `name`, `ip`, `port`) VALUES
(1, 'data_server', '192.168.1.144', 9000),
(2, 'freegeoip_server', '192.168.1.144', 8080);

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

--
-- Dumping data for table `widget`
--

INSERT INTO `widget` (`id`, `name`, `description`, `folder_name`, `updated`) VALUES
(191, 'Ajax Bandwidth chart', 'This widget shows the bandwidth data for a given number of days.', 'BandwidthChartAjax', 1),
(194, 'Snort table', 'This widget shows every alerts from the SNORT system. SNORT is a an open source network intrusion prevention and detection system (IDS/IPS) developed by Sourcefire (http://snort.org). The BASE GUI is used to display the datas (http://base.secureideas.net).', 'BaseAlert', 1),
(204, 'Total Bandwidth text', 'This widget shows the total bandwidth for a given number of days in a text form.', 'BandwidthTextAjax', 1),
(215, 'Protocol use chart', 'This widget shows rates of used protocol on the network data for a given number of days.', 'ProtocolUseChart', 1),
(221, 'DNS request list', 'Display the name of the domain requested by every DNS request going through the network in a list.', 'DnsText', 1),
(239, 'DNS request bubbles', 'Display the name of the domain requested by every DNS request going through the network as a bubble.', 'DnsBubble', 1),
(244, 'Map offline', 'Display source and target IPs from the packets going through the network. This display works with a local map but required to configure freegeoip on the configuration page.', 'MapOffline', 1),
(255, 'Map online', 'Display source and target IPs from the packets going through the network. This display works with OpenstreetMap and LeafletJS but required to configure freegeoip on the configuration page.', 'MapOnline', 1),
(286, 'Network 3D', 'This widget displays the incoming, outcoming and local packet going through the network. Each computer is an entity in the 3D scene and packets are displayed as rays between computer.', 'Network3D', 1),
(293, 'Server statistics', 'This widget shows memory, processor and swap use percentage.', 'ServerStat', 1),
(302, 'Summary bamdwidth', 'Displays the global bandwidth used since the first record in the database.', 'Summary', 1),
(320, 'Live bandwidth chart', 'This widget shows the current bandwidth data in a chart.', 'BandwidthChartWebsocket', 1),
(325, 'Live bandwidth text', 'This widget shows the current bandwidth in a text form.', 'BandwidthTextWebsocket', 1),
(339, 'Live ethernet protocol chart', 'This widget shows the current number of packets going through the network for each ethernet protocols (IPV4, IPV6, etc...) in a chart.', 'ProtocolEthernet', 1),
(362, 'Live IPV4 protocol chart', 'This widget shows the current number of packets going through the network for each IPV4 protocols (IPV4, IPV6, etc...) in a chart.', 'ProtocolIPV4', 1);

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

--
-- Dumping data for table `widget_parameter_design`
--

INSERT INTO `widget_parameter_design` (`id_widget`, `type`, `description`, `name`, `id`, `updated`) VALUES
(191, 'int', 'Number of milliseconds between two refreshes.', 'refresh_time', 146, 1),
(191, 'int', 'Number of days you want in the chart. 30 days means the chart will display the last 30 days.', 'nb_day', 147, 1),
(194, 'int', 'number of milliseconds between two refreshes', 'refresh_time', 151, 1),
(204, 'int', 'Number of milliseconds between two refreshes.', 'refresh_time', 168, 1),
(204, 'int', 'Number of days you want the statistics count for. 30 days means the statistics will be compute with ', 'nb_day', 169, 1),
(204, 'int', 'Size of the font.', 'font_size', 170, 1),
(215, 'int', 'Number of milliseconds between two refreshes.', 'refresh_time', 192, 1),
(215, 'int', 'Number of days you want in the chart. 30 days means the chart will display the last 30 days.', 'nb_day', 193, 1),
(215, 'str', 'Title of the chart.', 'title', 194, 1),
(221, 'int', 'Number of items in the list at any time.', 'nb_item', 205, 1),
(221, 'int', 'Size of the font use in the table.', 'font_size', 216, 1),
(286, 'int', 'Quality of the 3D from 1 to infinite. The bigger, the fancier.', 'quality', 310, 1),
(293, 'int', 'Speed of the animation.', 'speed', 319, 1),
(302, 'int', 'Number of milliseconds between 2 refreshes.', 'refresh_time', 332, 1),
(325, 'int', 'Size of the font.', 'font_size', 360, 1);

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

--
-- Dumping data for table `widget_parameter_set`
--

INSERT INTO `widget_parameter_set` (`id`, `name`, `id_widget`) VALUES
(150, '1 day', 215),
(128, 'Bigger daily', 204),
(109, 'default', 191),
(112, 'default', 194),
(127, 'default', 204),
(149, 'default', 215),
(156, 'default', 221),
(174, 'default', 239),
(179, 'default', 244),
(190, 'default', 255),
(221, 'default', 286),
(228, 'default', 293),
(237, 'default', 302),
(255, 'default', 320),
(260, 'default', 325),
(274, 'default', 339),
(297, 'default', 362),
(121, 'df', 191);

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
-- Dumping data for table `widget_parameter_value`
--

INSERT INTO `widget_parameter_value` (`id_set`, `id_param`, `value`) VALUES
(109, 146, '10004'),
(109, 147, '12'),
(112, 151, '10000'),
(121, 146, '10004'),
(121, 147, '1'),
(127, 168, '600000'),
(127, 169, '1'),
(127, 170, '15'),
(128, 168, '600000'),
(128, 169, '1'),
(128, 170, '45'),
(149, 192, '10000'),
(149, 193, '1'),
(149, 194, ''),
(150, 192, '10000'),
(150, 193, '1'),
(150, 194, '1 day'),
(156, 205, '15'),
(156, 216, '30'),
(221, 310, '5'),
(228, 319, '200'),
(237, 332, '100000'),
(260, 360, '35');

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
