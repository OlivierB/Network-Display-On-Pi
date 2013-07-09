-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 09, 2013 at 11:22 AM
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
-- Table structure for table `modules`
--

CREATE TABLE IF NOT EXISTS `modules` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `folder_name` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `description` text NOT NULL,
  `updated` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `folder_name` (`folder_name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=284 ;

--
-- Dumping data for table `modules`
--

INSERT INTO `modules` (`id`, `folder_name`, `name`, `description`, `updated`) VALUES
(83, 'dnsBubble', 'DNS Bubble', 'A funny display of the dns request of the monitored network. Each request is a bubble!', 1),
(111, 'traffic', 'Live traffic', 'This module shows the live traffic with a bandwidth chart and text. There is also informations about the current use of each ethernet protocol and IPV4 protocol.', 1),
(114, 'alertBase', 'Alert Snort', 'This module shows every alerts from the SNORT system. SNORT is a an open source network intrusion prevention and detection system (IDS/IPS) developed by Sourcefire (http://snort.org). The BASE GUI is used to display the datas (http://base.secureideas.net).', 1),
(127, 'dailyTraffic', 'Daily traffic', 'This module shows the bandwith use for the last 24 hours. You can see the local, up and down flow. The protocol use is also displayed.', 1),
(130, 'dns', 'DNS table', 'Show every dns request going through the monitored network. The dns name are displayed in a table.', 1),
(139, 'monthlyTraffic', 'Monthly traffic', 'This module shows the bandwith use for the last 30 days. You can see the local, up and down flow. The protocol use is also displayed.', 1),
(142, 'weeklyTraffic', 'Weekly traffic', 'This module shows the bandwith use for the last 7 days. You can see the local, up and down flow. The protocol use is also displayed.', 1),
(169, 'network3D', 'Network in 3D', 'This module represent each ip address on the network by a 3D form graviting around a SUN. Each communication is represented by a ray from the source to the recipient. If one of the ip address is outside the local network, the externam address is represented by the SUN. A table show the number of ip from every network.', 1),
(189, 'serverStat', 'Server statistics', 'Display several informations about the state of the data server. Processor load, memory load, swap load and packet loss.', 1),
(200, 'stressServer', 'Server stress', 'Show the live rate of packet loss with the number of packet received. A second chart show the same informatoins on a longer time.', 1),
(209, 'summary', 'Summary bandwidth', 'Display a simple chart with the total bandwidth use from the beginning of the record.', 1),
(251, 'introduction', 'Introduction', 'Just a module displayed when there is nothing else to do.', 1),
(252, 'mapOffline', 'Ip Location Offline', 'This module displays on a map the location of every ip going through the monitored network. The location is given by the freegeopip database. You can use your own freegeoip database.', 1),
(269, 'mapOnline', 'Ip Location Online', 'This module displays on a map the location of every ip going through the monitored network. The location is given by the freegeopip database. You can use your own freegeoip database. This module need an internet access to reach the OpenStreetMap database.', 1);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
