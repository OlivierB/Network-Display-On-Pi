-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 26, 2013 at 12:51 PM
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

--
-- Dumping data for table `layout`
--

INSERT INTO `layout` (`page`, `id_module`) VALUES
(0, 358);

-- --------------------------------------------------------

--
-- Table structure for table `module`
--

CREATE TABLE IF NOT EXISTS `module` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=370 ;

--
-- Dumping data for table `module`
--

INSERT INTO `module` (`id`, `name`, `description`) VALUES
(358, 'Network 3D', 'Display communications between machins in a 3D scene.'),
(359, 'Live statistics', 'Display the current data about the bandwidth and type of protocols.'),
(360, 'Daily statistics', 'Display the data for the last 4 hours about the bandwidth and type of protocols.'),
(361, 'Weekly traffic', 'Network Statistics for the last 7 days.'),
(362, 'Monthly statistics', 'Network statistics for the last 30 days.'),
(363, 'DNS Bubble', 'A display for DNS requests as bubble.'),
(364, 'DNS request', 'Display dns requests in a table.'),
(365, 'IP map offline', 'Display the location of IPs source or target of packets going through the network. This display don''t use the openStreetMap database.'),
(366, 'IP map online', 'Display the location of IPs source or target of packet going through the network. Map from Leaflet and OpenStreetMap.'),
(367, 'NDOP Server statistics', 'Dysplay the state of the machine hosting the NDOP program.'),
(368, 'SNORT IDS', 'Display alerts from the SNORT IDS. You need to install SNORT on your system to use this module.'),
(369, 'Summary', 'Display the total bandwidth used by the network.');

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=372 ;

--
-- Dumping data for table `module_composition_widget`
--

INSERT INTO `module_composition_widget` (`id`, `id_module`, `id_widget`, `x`, `y`, `width`, `height`, `id_widget_parameter_set`) VALUES
(341, 360, 365, 0, 0, 8, 1, 314),
(342, 360, 371, 8, 0, 4, 1, 322),
(343, 360, 403, 0, 1, 6, 1, 374),
(344, 360, 407, 6, 1, 6, 1, 393),
(345, 361, 365, 0, 0, 8, 1, 317),
(346, 361, 371, 8, 0, 4, 1, 321),
(347, 361, 403, 0, 1, 6, 1, 391),
(348, 361, 407, 6, 1, 6, 1, 394),
(349, 362, 365, 0, 0, 8, 1, 318),
(350, 362, 371, 8, 0, 4, 1, 323),
(351, 362, 403, 0, 1, 6, 1, 392),
(352, 362, 407, 6, 1, 6, 1, 395),
(353, 363, 372, 0, 0, 12, 2, 307),
(354, 364, 364, 0, 0, 12, 2, 299),
(358, 368, 363, 0, 0, 12, 2, 298),
(359, 369, 368, 2, 0, 8, 2, 303),
(365, 359, 375, 0, 0, 8, 1, 310),
(366, 359, 366, 8, 0, 4, 1, 313),
(367, 359, 402, 0, 1, 6, 1, 351),
(368, 365, 369, 0, 0, 12, 2, 304),
(369, 367, 370, 3, 0, 6, 1, 305),
(370, 366, 377, 0, 0, 12, 2, 312);

-- --------------------------------------------------------

--
-- Table structure for table `server_information`
--

CREATE TABLE IF NOT EXISTS `server_information` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `ip` varchar(150) NOT NULL,
  `port` int(11) NOT NULL,
  `login` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;


-- --------------------------------------------------------

--
-- Table structure for table `widget`
--

CREATE TABLE IF NOT EXISTS `widget` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `folder_name` varchar(100) NOT NULL,
  `updated` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `folder_name` (`folder_name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=713 ;

--
-- Dumping data for table `widget`
--

INSERT INTO `widget` (`id`, `name`, `description`, `folder_name`, `updated`) VALUES
(363, 'Snort table', 'This widget shows every alerts from the SNORT system. SNORT is a an open source network intrusion prevention and detection system (IDS/IPS) developed by Sourcefire (http://snort.org). The BASE GUI is used to display the datas (http://base.secureideas.net).', 'BaseAlert', 1),
(364, 'DNS request list', 'Display the name of the domain requested by every DNS request going through the network in a list.', 'DnsText', 1),
(365, 'Ajax Bandwidth chart', 'This widget shows the bandwidth data for a given number of days.', 'BandwidthChartAjax', 1),
(366, 'Live bandwidth text', 'This widget shows the current bandwidth in a text form.', 'BandwidthTextWebsocket', 1),
(368, 'Summary bamdwidth', 'Displays the global bandwidth used since the first record in the database.', 'Summary', 1),
(369, 'Map offline', 'Display source and target IPs from the packets going through the network. This display works with a local map but required to configure freegeoip on the configuration page.', 'MapOffline', 1),
(370, 'Server statistics', 'This widget shows memory, processor and swap use percentage.', 'ServerStat', 1),
(371, 'Total Bandwidth text', 'This widget shows the total bandwidth for a given number of days in a text form.', 'BandwidthTextAjax', 1),
(372, 'DNS request bubbles', 'Display the name of the domain requested by every DNS request going through the network as a bubble.', 'DnsBubble', 1),
(375, 'Live bandwidth chart', 'This widget shows the current bandwidth data in a chart.', 'BandwidthChartWebsocket', 1),
(377, 'Map online', 'Display source and target IPs from the packets going through the network. This display works with OpenstreetMap and LeafletJS but required to configure freegeoip on the configuration page.', 'MapOnline', 1),
(402, 'Live IPV4 protocol chart', 'This widget shows the current number of packets going through the network for each IPV4 protocols (TCP, UDP, etc...) in a chart.', 'ProtocolIPV4Websocket', 1),
(403, 'Ethernet protocol use chart', 'This widget shows rates of used protocols on the network.', 'ProtocolEthernetChartAjax', 1),
(405, 'Live ethernet protocol chart', 'This widget shows the current number of packets going through the network for each ethernet protocols (IPV4, IPV6, etc...) in a chart.', 'ProtocolEthernetWebsocket', 1),
(407, 'IPV4 subProtocol use chart', 'This widget shows the use of IPV4 subprotocols on the network. Datas are given for a number of days.', 'ProtocolIPV4Ajax', 1),
(596, 'Network 3D', 'This widget displays the incoming, outcoming and local packet going through the network. Each computer is an entity in the 3D scene and packets are displayed as rays between computer.', 'Network3D', 1);

-- --------------------------------------------------------

--
-- Table structure for table `widget_parameter_design`
--

CREATE TABLE IF NOT EXISTS `widget_parameter_design` (
  `id_widget` int(11) NOT NULL,
  `type` varchar(15) NOT NULL,
  `description` text NOT NULL,
  `name` varchar(50) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `updated` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_widget` (`id_widget`,`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=886 ;

--
-- Dumping data for table `widget_parameter_design`
--

INSERT INTO `widget_parameter_design` (`id_widget`, `type`, `description`, `name`, `id`, `updated`) VALUES
(363, 'int', 'number of milliseconds between two refreshes', 'refresh_time', 361, 1),
(364, 'int', 'Number of items in the list at any time.', 'nb_item', 362, 1),
(364, 'int', 'Size of the font use in the table.', 'font_size', 363, 1),
(365, 'int', 'Number of milliseconds between two refreshes.', 'refresh_time', 364, 1),
(365, 'int', 'Number of days you want in the chart. 30 days means the chart will display the last 30 days.', 'nb_day', 365, 1),
(366, 'int', 'Size of the font.', 'font_size', 366, 1),
(368, 'int', 'Number of milliseconds between 2 refreshes.', 'refresh_time', 367, 1),
(370, 'int', 'Speed of the animation.', 'speed', 368, 1),
(371, 'int', 'Number of milliseconds between two refreshes.', 'refresh_time', 369, 1),
(371, 'int', 'Number of days you want the statistics count for. 30 days means the statistics will be compute with the last 30 days.', 'nb_day', 370, 1),
(371, 'int', 'Size of the font.', 'font_size', 371, 1),
(403, 'int', 'Number of milliseconds between two refreshes.', 'refresh_time', 403, 1),
(403, 'int', 'Number of days you want in the chart. 30 days means the chart will display the last 30 days.', 'nb_day', 404, 1),
(403, 'str', 'Title of the chart.', 'title', 405, 1),
(403, 'str', 'You can group results by packet to get an easier to read chart. You can choose&#44; HOUR&#44; DAY&#44; WEEK&#44; MONTH. If you don''t want to group your data&#44; choose NONE.', 'group_by', 406, 1),
(407, 'int', 'Number of milliseconds between two refreshes.', 'refresh_time', 408, 1),
(407, 'int', 'Number of days you want in the chart. 30 days means the chart will display the last 30 days.', 'nb_day', 409, 1),
(407, 'str', 'Title of the chart.', 'title', 410, 1),
(407, 'str', 'You can group results by packet to get an easier to read chart. You can choose&#44; HOUR&#44; DAY&#44; WEEK&#44; MONTH. If you don''t want to group your data&#44; choose NONE.', 'group_by', 411, 1),
(369, 'int', 'Size of the random dither in px.', 'dither', 459, 1),
(369, 'float', 'Opacity of each point on the map&#44; between 0 and 1.', 'opacity', 460, 1),
(377, 'int', 'Size of the random dither in degree.', 'dither', 496, 1),
(377, 'float', 'Opacity of each point on the map&#44; between 0 and 1.', 'opacity', 497, 1),
(372, 'int', 'Size of the font used in the bubble in px.', 'font_size', 535, 1),
(372, 'bool', 'Indicate wether the text will be in a bubble or not. true or false.', 'draw_bubble', 561, 1),
(596, 'int', 'Quality of the 3D from 1 to infinite. The bigger&#44; the fancier.', 'quality', 697, 1);

-- --------------------------------------------------------

--
-- Table structure for table `widget_parameter_set`
--

CREATE TABLE IF NOT EXISTS `widget_parameter_set` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `id_widget` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`,`id_widget`),
  KEY `id_widget` (`id_widget`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=669 ;

--
-- Dumping data for table `widget_parameter_set`
--

INSERT INTO `widget_parameter_set` (`id`, `name`, `id_widget`) VALUES
(313, 'Big text', 366),
(314, 'daily', 365),
(322, 'daily', 371),
(374, 'daily', 403),
(393, 'daily', 407),
(298, 'default', 363),
(299, 'default', 364),
(300, 'default', 365),
(301, 'default', 366),
(303, 'default', 368),
(304, 'default', 369),
(305, 'default', 370),
(306, 'default', 371),
(307, 'default', 372),
(310, 'default', 375),
(312, 'default', 377),
(351, 'default', 402),
(352, 'default', 403),
(354, 'default', 405),
(356, 'default', 407),
(552, 'default', 596),
(318, 'monthly', 365),
(323, 'monthly', 371),
(392, 'monthly', 403),
(395, 'monthly', 407),
(317, 'weekly', 365),
(321, 'Weekly', 371),
(391, 'weekly', 403),
(394, 'weekly', 407);

-- --------------------------------------------------------

--
-- Table structure for table `widget_parameter_value`
--

CREATE TABLE IF NOT EXISTS `widget_parameter_value` (
  `id_set` int(11) NOT NULL,
  `id_param` int(11) NOT NULL,
  `value` text NOT NULL,
  UNIQUE KEY `id_set_2` (`id_set`,`id_param`),
  KEY `id_param` (`id_param`),
  KEY `id_set` (`id_set`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `widget_parameter_value`
--

INSERT INTO `widget_parameter_value` (`id_set`, `id_param`, `value`) VALUES
(298, 361, '10000'),
(299, 362, '15'),
(299, 363, '30'),
(300, 364, '10000'),
(300, 365, '1'),
(301, 366, '15'),
(303, 367, '100000'),
(304, 459, '7'),
(304, 460, '0.25'),
(305, 368, '100'),
(306, 369, '600000'),
(306, 370, '1'),
(306, 371, '15'),
(307, 535, '30'),
(307, 561, 'false'),
(312, 496, '2'),
(312, 497, '0.25'),
(313, 366, '45'),
(314, 364, '10000'),
(314, 365, '1'),
(317, 364, '10000'),
(317, 365, '7'),
(318, 364, '10000'),
(318, 365, '30'),
(321, 369, '600000'),
(321, 370, '7'),
(321, 371, '45'),
(322, 369, '600000'),
(322, 370, '1'),
(322, 371, '45'),
(323, 369, '600000'),
(323, 370, '30'),
(323, 371, '45'),
(352, 403, '10000'),
(352, 404, '1'),
(352, 405, ''),
(352, 406, 'NONE'),
(356, 408, '10000'),
(356, 409, '1'),
(356, 410, ''),
(356, 411, 'NONE'),
(374, 403, '10000'),
(374, 404, '1'),
(374, 405, 'Daily protocol use'),
(374, 406, 'NONE'),
(391, 403, '10000'),
(391, 404, '7'),
(391, 405, 'Weekly protocol use'),
(391, 406, 'HOUR'),
(392, 403, '10000'),
(392, 404, '30'),
(392, 405, 'Monthly protocol use'),
(392, 406, 'DAY'),
(393, 408, '10000'),
(393, 409, '1'),
(393, 410, 'Daily IPV4 subprotocols use'),
(393, 411, 'NONE'),
(394, 408, '10000'),
(394, 409, '7'),
(394, 410, 'Weekly IPV4 subprotocols use'),
(394, 411, 'HOUR'),
(395, 408, '10000'),
(395, 409, '30'),
(395, 410, 'Monthly  IPV4 subprotocols use'),
(395, 411, 'DAY'),
(552, 697, '5');

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
