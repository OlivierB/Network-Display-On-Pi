-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Aug 28, 2013 at 03:46 PM
-- Server version: 5.5.31
-- PHP Version: 5.4.4-14+deb7u2




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
(0, 371),
(1, 372),
(2, 373),
(4, 377),
(5, 378),
(3, 381);

-- --------------------------------------------------------

--
-- Table structure for table `module`
--

CREATE TABLE IF NOT EXISTS `module` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=383 ;

--
-- Dumping data for table `module`
--

INSERT INTO `module` (`id`, `name`, `description`) VALUES
(370, 'Network 3D', 'Display communications between machins in a 3D scene.'),
(371, 'Live statistics', 'Display the current data about the bandwidth and type of protocols.'),
(372, 'Daily statistics', 'Display the data for the last 24 hours about the bandwidth and type of protocols.'),
(373, 'Weekly statistics', 'Display data for the last 7 days about the bandwidth and type of protocols.'),
(374, 'Monthly statistics', 'Network statistics for the last 30 days.'),
(375, 'DNS Bubble', 'A display for DNS requests as bubble.'),
(376, 'DNS request', 'Display dns requests in a table.'),
(377, 'IP map offline', 'Display the location of IPs source or target of packets going through the network. This display don''''t use the openStreetMap database.'),
(378, 'IP map online', 'Display the location of IPs source or target of packet going through the network. Map from Leaflet and OpenStreetMap.'),
(379, 'NDOP Server statistics', 'Dysplay the state of the machine hosting the NDOP program.'),
(380, 'SNORT IDS', 'Display alerts from the SNORT IDS. You need to install SNORT on your system to use this module.'),
(381, 'Summary', 'Display the total bandwidth used by the network.'),
(382, 'test', 'ptocols\n');

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=427 ;

--
-- Dumping data for table `module_composition_widget`
--

INSERT INTO `module_composition_widget` (`id`, `id_module`, `id_widget`, `x`, `y`, `width`, `height`, `id_widget_parameter_set`) VALUES
(373, 370, 868, 0, 0, 12, 2, 824),
(374, 371, 870, 0, 0, 8, 1, 826),
(375, 371, 860, 8, 0, 4, 1, 816),
(376, 371, 869, 0, 1, 6, 1, 825),
(377, 371, 866, 6, 1, 6, 1, 822),
(394, 375, 865, 0, 0, 12, 2, 821),
(395, 376, 858, 0, 0, 12, 2, 814),
(396, 377, 862, 0, 0, 12, 2, 818),
(397, 378, 872, 0, 0, 12, 2, 828),
(398, 379, 863, 3, 0, 6, 1, 819),
(399, 380, 857, 0, 0, 12, 2, 813),
(400, 381, 861, 2, 0, 8, 2, 817),
(406, 382, 884, 0, 0, 12, 2, 852),
(411, 372, 859, 0, 0, 8, 1, 1079),
(412, 372, 864, 8, 0, 4, 1, 838),
(413, 372, 867, 0, 1, 6, 1, 832),
(414, 372, 871, 6, 1, 6, 1, 835),
(419, 374, 859, 0, 0, 8, 1, 1081),
(420, 374, 864, 8, 0, 4, 1, 840),
(421, 374, 867, 0, 1, 6, 1, 834),
(422, 374, 871, 6, 1, 6, 1, 837),
(423, 373, 864, 8, 0, 4, 1, 839),
(424, 373, 867, 0, 1, 6, 1, 833),
(425, 373, 871, 6, 1, 6, 1, 836),
(426, 373, 859, 0, 0, 8, 1, 1080);

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
  `database_name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;



-- --------------------------------------------------------

--
-- Table structure for table `slide_configuration`
--

CREATE TABLE IF NOT EXISTS `slide_configuration` (
  `interval` int(11) NOT NULL DEFAULT '15000',
  `auto_start` tinyint(1) NOT NULL DEFAULT '1',
  `pause_on_hover` tinyint(1) NOT NULL DEFAULT '0',
  `update_id` int(11) NOT NULL,
  `update_check_interval` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `slide_configuration`
--

INSERT INTO `slide_configuration` (`interval`, `auto_start`, `pause_on_hover`, `update_id`, `update_check_interval`) VALUES
(15000, 0, 0, 13, 1000);

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1462 ;

--
-- Dumping data for table `widget`
--

INSERT INTO `widget` (`id`, `name`, `description`, `folder_name`, `updated`) VALUES
(857, 'Snort table', 'This widget shows every alerts from the SNORT system. SNORT is a an open source network intrusion prevention and detection system (IDS/IPS) developed by Sourcefire (http://snort.org). The BASE GUI is used to display the datas (http://base.secureideas.net).', 'BaseAlert', 1),
(858, 'DNS request list', 'Display the name of the domain requested by every DNS request going through the network in a list.', 'DnsText', 1),
(859, 'Ajax Bandwidth chart', 'This widget shows the bandwidth data for a given number of days.', 'BandwidthChartAjax', 1),
(860, 'Live bandwidth text', 'This widget shows the current bandwidth in a text form.', 'BandwidthTextWebsocket', 1),
(861, 'Summary bamdwidth', 'Displays the global bandwidth used since the first record in the database.', 'Summary', 1),
(862, 'Map offline', 'Display source and target IPs from the packets going through the network. This display works with a local map but required to configure freegeoip on the configuration page.', 'MapOffline', 1),
(863, 'Server statistics', 'This widget shows memory, processor and swap use percentage.', 'ServerStat', 1),
(864, 'Total Bandwidth text', 'This widget shows the total bandwidth for a given number of days in a text form.', 'BandwidthTextAjax', 1),
(865, 'DNS request bubbles', 'Display the name of the domain requested by every DNS request going through the network as a bubble.', 'DnsBubble', 1),
(866, 'Live IPV4 protocol chart', 'This widget shows the current number of packets going through the network for each IPV4 protocols (TCP, UDP, etc...) in a chart.', 'ProtocolIPV4Websocket', 1),
(867, 'Ethernet protocol use chart', 'This widget shows rates of used protocols on the network.', 'ProtocolEthernetChartAjax', 1),
(868, 'Network 3D', 'This widget displays the incoming, outcoming and local packet going through the network. Each computer is an entity in the 3D scene and packets are displayed as rays between computer. Be careful, it does not work on Raspberry pi Chromium and it might even cause trouble to other widgets on this plateform.', 'Network3D', 1),
(869, 'Live ethernet protocol chart', 'This widget shows the current number of packets going through the network for each ethernet protocols (IPV4, IPV6, etc...) in a chart.', 'ProtocolEthernetWebsocket', 1),
(870, 'Live bandwidth chart', 'This widget shows the current bandwidth data in a chart.', 'BandwidthChartWebsocket', 1),
(871, 'IPV4 subProtocol use chart', 'This widget shows the use of IPV4 subprotocols on the network. Datas are given for a number of days.', 'ProtocolIPV4Ajax', 1),
(872, 'Map online', 'Display source and target IPs from the packets going through the network. This display works with OpenstreetMap and LeafletJS but required to configure freegeoip on the configuration page.', 'MapOnline', 1),
(884, 'Top Used Protocols', 'This widget shows the most used protocols.', 'TopProtocolsWebsocket', 1);

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2429 ;

--
-- Dumping data for table `widget_parameter_design`
--

INSERT INTO `widget_parameter_design` (`id_widget`, `type`, `description`, `name`, `id`, `updated`) VALUES
(857, 'int', 'Number of milliseconds between two refreshes', 'refresh_time', 1129, 1),
(858, 'int', 'Number of items in the list at any time.', 'nb_item', 1130, 1),
(858, 'int', 'Size of the font use in the table.', 'font_size', 1131, 1),
(859, 'int', 'Number of milliseconds between two refreshes.', 'refresh_time', 1132, 1),
(859, 'int', 'Number of days you want in the chart. 30 days means the chart will display the last 30 days.', 'nb_day', 1133, 1),
(860, 'int', 'Size of the font.', 'font_size', 1134, 1),
(861, 'int', 'Number of milliseconds between 2 refreshes.', 'refresh_time', 1135, 1),
(862, 'int', 'Size of the random dither in px.', 'dither', 1136, 1),
(862, 'float', 'Opacity of each point on the map&#44; between 0 and 1.', 'opacity', 1137, 1),
(863, 'int', 'Speed of the animation.', 'speed', 1138, 1),
(864, 'int', 'Number of milliseconds between two refreshes.', 'refresh_time', 1139, 1),
(864, 'int', 'Number of days you want the statistics count for. 30 days means the statistics will be compute with the last 30 days.', 'nb_day', 1140, 1),
(864, 'int', 'Size of the font.', 'font_size', 1141, 1),
(865, 'int', 'Size of the font used in the bubble in px.', 'font_size', 1142, 1),
(865, 'bool', 'Indicate wether the text will be in a bubble or not. true or false.', 'draw_bubble', 1143, 1),
(867, 'int', 'Number of milliseconds between two refreshes.', 'refresh_time', 1144, 1),
(867, 'int', 'Number of days you want in the chart. 30 days means the chart will display the last 30 days.', 'nb_day', 1145, 1),
(867, 'str', 'Title of the chart.', 'title', 1146, 1),
(867, 'str', 'You can group results by packet to get an easier to read chart. You can choose&#44; HOUR&#44; DAY&#44; WEEK&#44; MONTH. If you don''t want to group your data&#44; choose NONE.', 'group_by', 1147, 1),
(868, 'int', 'Quality of the 3D from 1 to infinite. The bigger&#44; the fancier.', 'quality', 1148, 1),
(868, 'str', 'You can change the color of some IPs by giving an address&#44; a mask&#44; a background color and a font color. The exemple below makes the 192.168.1.144 IP displayed in blue and black and every other IP from the 192.168.1.0/24 range in blue and white. If an element corresponds to several criterias&#44; it will respect the first it will meet. So you have to put the more precise criterias in the first places.<br>\n	{<br>\n		&nbsp;&nbsp;&nbsp;address: ''192.168.1.144''&#44;<br>\n		&nbsp;&nbsp;&nbsp;mask: 32&#44;<br>\n		&nbsp;&nbsp;&nbsp;textureColor: ''#7DC3F7''&#44;<br>\n		&nbsp;&nbsp;&nbsp;fontColor: ''black''<br>\n	}&#44;{<br>\n		&nbsp;&nbsp;&nbsp;address: ''192.168.1.0''&#44;<br>\n		&nbsp;&nbsp;&nbsp;mask: 24&#44;<br>\n		&nbsp;&nbsp;&nbsp;textureColor: ''blue''&#44;<br>\n		&nbsp;&nbsp;&nbsp;fontColor: ''#FFFFFF''<br>\n	}<br>', 'mask_customize', 1149, 1),
(871, 'int', 'Number of milliseconds between two refreshes.', 'refresh_time', 1150, 1),
(871, 'int', 'Number of days you want in the chart. 30 days means the chart will display the last 30 days.', 'nb_day', 1151, 1),
(871, 'str', 'Title of the chart.', 'title', 1152, 1),
(871, 'str', 'You can group results by packet to get an easier to read chart. You can choose&#44; HOUR&#44; DAY&#44; WEEK&#44; MONTH. If you don''t want to group your data&#44; choose NONE.', 'group_by', 1153, 1),
(872, 'int', 'Size of the random dither in degree.', 'dither', 1154, 1),
(872, 'float', 'Opacity of each point on the map&#44; between 0 and 1.', 'opacity', 1155, 1),
(857, 'str', 'Address of your snort database. For example 192.168.1.134.', 'address', 1157, 1),
(857, 'int', 'Port of your snort database. The default port for a mysql database is 3306.', 'port', 1158, 1),
(857, 'str', 'Name of your snort database.', 'name', 1159, 1),
(857, 'str', 'Login of your snort database user.', 'login', 1160, 1),
(857, 'str', 'Passoword of your snort database user.', 'password', 1161, 1),
(857, 'str', 'The type of database the snort datas are stored in. Can be : ''mysql''&#44; ''postgres''&#44; ''mssql'' (MS SQL Server)&#44; ''oci8'' (Oracle)&#44; without the quotes.', 'type', 1195, 1),
(857, 'int', 'Size of the font in the table.', 'font_size', 1223, 1),
(859, 'string', 'Style of the line in the chart. Can be ''line''&#44; ''spline''&#44; ''area''&#44; ''stackedColumn''&#44; ''stackedArea''&#44; ''stackedColumn100''&#44; ''stackedArea100'' (The last two options will display value as percentage!).', 'style_line', 1622, 1),
(870, 'string', 'Style of the line in the chart. Can be ''line''&#44; ''spline''&#44; ''area''&#44; ''stackedColumn''&#44; ''stackedArea''&#44; ''stackedColumn100''&#44; ''stackedArea100'' (The last two options will display value as percentage!).', 'style_line', 1674, 1),
(862, 'string', 'IP or hostname of your freegoip server. You can use the online website (freegeoip.net) but you will be limited to 10&#44;000 queries per hour. The best solution is to create your own server by using the github (https://github.com/fiorix/freegeoip).', 'freegeoip_address', 2370, 1),
(872, 'string', 'IP or hostname of your freegoip server. You can use the online website (freegeoip.net) but you will be limited to 10&#44;000 queries per hour. The best solution is to create your own server by using the github (https://github.com/fiorix/freegeoip).', 'freegeoip_address', 2390, 1);

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1433 ;

--
-- Dumping data for table `widget_parameter_set`
--

INSERT INTO `widget_parameter_set` (`id`, `name`, `id_widget`) VALUES
(1079, 'Daily', 859),
(838, 'daily', 864),
(832, 'daily', 867),
(835, 'daily', 871),
(813, 'default', 857),
(814, 'default', 858),
(1418, 'default', 859),
(816, 'default', 860),
(817, 'default', 861),
(818, 'default', 862),
(819, 'default', 863),
(820, 'default', 864),
(821, 'default', 865),
(822, 'default', 866),
(823, 'default', 867),
(824, 'default', 868),
(825, 'default', 869),
(826, 'default', 870),
(827, 'default', 871),
(828, 'default', 872),
(852, 'default', 884),
(1081, 'Monthly', 859),
(840, 'monthly', 864),
(834, 'monthly', 867),
(837, 'monthly', 871),
(1080, 'Weekly', 859),
(839, 'weekly', 864),
(833, 'weekly', 867),
(836, 'weekly', 871);

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
(813, 1129, '30000'),
(813, 1157, '192.168.1.144'),
(813, 1158, '3306'),
(813, 1159, 'snort'),
(813, 1160, 'snort'),
(813, 1161, 'snortpass'),
(813, 1195, 'mysql'),
(813, 1223, '25'),
(814, 1130, '15'),
(814, 1131, '30'),
(816, 1134, '45'),
(817, 1135, '65000'),
(818, 1136, '10'),
(818, 1137, '0.25'),
(818, 2370, '192.168.1.144:8080'),
(819, 1138, '100'),
(820, 1139, '600000'),
(820, 1140, '1'),
(820, 1141, '45'),
(821, 1142, '20'),
(821, 1143, 'false'),
(823, 1144, '10000'),
(823, 1145, '1'),
(823, 1146, ''),
(823, 1147, 'NONE'),
(824, 1148, '5'),
(824, 1149, ''),
(826, 1674, 'line'),
(827, 1150, '10000'),
(827, 1151, '1'),
(827, 1152, ''),
(827, 1153, 'NONE'),
(828, 1154, '2'),
(828, 1155, '0.25'),
(828, 2390, 'freegeoip.net'),
(832, 1144, '600000'),
(832, 1145, '1'),
(832, 1146, 'Daily protocol use '),
(832, 1147, 'NONE'),
(833, 1144, '2100000'),
(833, 1145, '7'),
(833, 1146, 'Weekly protocol use '),
(833, 1147, 'HOUR'),
(834, 1144, '4500000'),
(834, 1145, '30'),
(834, 1146, 'Monthly protocol use '),
(834, 1147, 'DAY'),
(835, 1150, '600000'),
(835, 1151, '1'),
(835, 1152, 'Daily IPV4 subprotocols use'),
(835, 1153, 'NONE'),
(836, 1150, '2100000'),
(836, 1151, '7'),
(836, 1152, 'Weekly IPV4 subprotocols use'),
(836, 1153, 'HOUR'),
(837, 1150, '4500000'),
(837, 1151, '30'),
(837, 1152, 'Monthly IPV4 subprotocols use'),
(837, 1153, 'DAY'),
(838, 1139, '600000'),
(838, 1140, '1'),
(838, 1141, '45'),
(839, 1139, '2100000'),
(839, 1140, '7'),
(839, 1141, '45'),
(840, 1139, '4500000'),
(840, 1140, '30'),
(840, 1141, '45'),
(1079, 1132, '600000'),
(1079, 1133, '1'),
(1079, 1622, 'line'),
(1080, 1132, '2100000'),
(1080, 1133, '7'),
(1080, 1622, 'line'),
(1081, 1132, '4500000'),
(1081, 1133, '30'),
(1081, 1622, 'line'),
(1418, 1132, '10000'),
(1418, 1133, '1'),
(1418, 1622, 'line');

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
