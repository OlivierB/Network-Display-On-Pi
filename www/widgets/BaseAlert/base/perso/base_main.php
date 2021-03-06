<?php
/*
** Copyright (C) 2004 Kevin Johnson
** Copyright (C) 2000 Carnegie Mellon University
**
** Author: Kevin Johnson <kjohnson@secureideas.net>
** Project Leads: Kevin Johnson <kjohnson@secureideas.net>
**                Sean Muller <samwise_diver@users.sourceforge.net>
** Built upon work by Roman Danyliw <rdd@cert.org>, <roman@danyliw.com>
**
** This program is free software; you can redistribute it and/or modify
** it under the terms of the GNU General Public License as published by
** the Free Software Foundation; either version 2 of the License, or
** (at your option) any later version.
**
** This program is distributed in the hope that it will be useful,
** but WITHOUT ANY WARRANTY; without even the implied warranty of
** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
** GNU General Public License for more details.
**
** You should have received a copy of the GNU General Public License
** along with this program; if not, write to the Free Software
** Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
*/

/*  
 * Basic Analysis and Security Engine (BASE) by Kevin Johnson
 * based upon Analysis Console for Incident Databases (ACID) by Roman Danyliw
 *
 * See http://sourceforge.net/projects/secureideas for the most up to date 
 * information and documentation about this application.
 *
 * Purpose:
 *
 *   BASE is an PHP-based analysis engine to search and process 
 *   a database of security incidents generated by the NIDS Snort.
 *
 * Configuration:
 *
 *   See the 'docs/README' file, and 'base_conf.php'
 *
 */

  $start = time();
   require("./base_conf.php");
   include_once("$BASE_path/includes/base_auth.inc.php");
   include_once("$BASE_path/includes/base_db.inc.php");
   include_once("$BASE_path/includes/base_output_html.inc.php");
   include_once("$BASE_path/base_common.php");
   include_once("$BASE_path/base_db_common.php");
   include_once("$BASE_path/includes/base_cache.inc.php");
   include_once("$BASE_path/includes/base_state_criteria.inc.php");

  
  function DBLink()
  {
      // generate the link to select the other database....
      GLOBAL $archive_exists;
   
      if ( (isset($_COOKIE['archive']) && $_COOKIE['archive'] == 1) || (isset($_GET['archive']) && $_GET['archive'] == 1)) {
          echo '<a href="base_main.php?archive=no">' . _USEALERTDB . '</a>';
      } elseif ($archive_exists != 0) {
          echo ('<a href="base_main.php?archive=1">' . _USEARCHIDB . '</a>');
      }
  }
?>

<?php
PrintFreshPage($refresh_stat_page, $stat_page_refresh_time);
$archiveDisplay = (isset($_COOKIE['archive']) && $_COOKIE['archive'] == 1) ? "-- ARCHIVE" : "";
echo ('<title>' . _TITLE . $BASE_VERSION . $archiveDisplay . '</title>
<link rel="stylesheet" type="text/css" href="styles/' . $base_style . '">');
?>
</head>
<body>
  <div class="mainheadertitle">&nbsp;<?php echo _TITLE . $archiveDisplay; ?></div>
<?php
if ($debug_mode == 1) {
    PrintPageHeader();
}

/* Check that PHP was built correctly */
$tmp_str = verify_php_build($DBtype);
if ($tmp_str != "") {
    echo $tmp_str;
    die();
}

/* Connect to the Alert database */
$db = NewBASEDBConnection($DBlib_path, $DBtype);
$db->baseDBConnect($db_connect_method, $alert_dbname, $alert_host, $alert_port, $alert_user, $alert_password);

/* Check that the DB schema is recent */
$tmp_str = verify_db($db, $alert_dbname, $alert_host);
if ($tmp_str != "") {
    echo $tmp_str;
    die();
}
?>


<?php
    PrintProtocolProfileGraphs($db);

?>

