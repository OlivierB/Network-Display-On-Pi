<?php

function getProtocol($connection, $date_begin, $date_end, $table, $group){

	if($date_begin != '' && $date_end != ''){
		$where_statement = '  WHERE date BETWEEN ('. $date_begin .') AND ('. $date_end .')';
	}else{
		$where_statement = '';
	}


	// request the protocol list
	$sql = 'SELECT distinct `protocol` FROM `'.$table.'` '.$where_statement;

	$req = $connection->prepare($sql);
	$req->execute();

	// PDO::FETCH_COLUMN, 0 : request only the first column
	$result = $req->fetchAll(PDO::FETCH_COLUMN, 0);

	// final container
	$obj = array();

	$obj['listProt'] = $result;

	// handle the group by statement. To make sure every protocols stay in the same group, we add 
	// an id_date wich corresponds to the group statement
	if($group == "HOUR"){
		$group_by = "HOUR(`date`), DAYOFYEAR(`date`), YEAR(`date`)";
		$concat_id_date = "CONCAT(HOUR(`date`), '-',DAYOFYEAR(`date`),'-', YEAR(`date`))";

	}elseif($group == "DAY"){
		$group_by = "DAYOFYEAR(`date`), YEAR(`date`)";
		$concat_id_date = "CONCAT(DAYOFYEAR(`date`),'-', YEAR(`date`))";

	}elseif ($group == "WEEK") {
		$group_by = "WEEKOFYEAR(`date`), YEAR(`date`)";
		$concat_id_date = "CONCAT(WEEKOFYEAR(`date`),'-', YEAR(`date`))";

	}elseif ($group == "MONTH") {
		$group_by = "MONTH(`date`), YEAR(`date`)";
		$concat_id_date = "CONCAT(MONTH(`date`),'-', YEAR(`date`))";

	}else{
		$group_by = "";
		$concat_id_date = "`date`";
	}

	if($group_by != ''){
		$group_statement = 'GROUP BY '.$group_by.' , `protocol` ';
	}else{
		$group_statement = 'GROUP BY `date`, `protocol` ';
	}

	// request the protocol use
	$sql = 'SELECT '.$concat_id_date.' as id_date, `date`, `protocol`, SUM(`number`) as number FROM `'.$table.'` '.$where_statement.' '.$group_statement .'ORDER BY `date`';
	$req = $connection->prepare($sql);
	$req->execute();


	// PDO::FETCH_ASSOC : request with associative array
	$result = $req->fetchAll(PDO::FETCH_ASSOC);

	$date = '';
	$tab = array();
	$i = -1;

	// build of the list of protocol use
	foreach ($result as $row) {
		
		// group result per group, create a new group when a new id_date appears
		// here we use the id_date we create earlier
		if($row['id_date'] != $date){
			$i++;
			$date = $row['id_date'];

			$tab[] = array();
			$tab[$i]['date'] = $row['date'];
			$tab[$i]['value'] = array();
		}
		$tab[$i]['value'][$row['protocol']] = $row['number'];
	}
	$obj['listValue'] = $tab;

	return $obj;
}



function getProtocolEthernet($connection, $date_begin, $date_end, $group){
	return getProtocol($connection, $date_begin, $date_end, 'protocols_ether', $group);
}

function getSubProtocolIpv4($connection, $date_begin, $date_end, $group){
	return getProtocol($connection, $date_begin, $date_end, 'protocols_ip', $group);
}

function buildGroupStatement($group){

	// handle the group by statement. To make sure every protocols stay in the same group, we add 
	// an id_date wich corresponds to the group statement
	if($group == "HOUR"){
		$group_by = "HOUR(`date`), DAYOFYEAR(`date`), YEAR(`date`)";

	}elseif($group == "DAY"){
		$group_by = "DAYOFYEAR(`date`), YEAR(`date`)";

	}elseif ($group == "WEEK") {
		$group_by = "WEEKOFYEAR(`date`), YEAR(`date`)";

	}elseif ($group == "MONTH") {
		$group_by = "MONTH(`date`), YEAR(`date`)";

	}else{
		$group_by = "";
	}

	if($group_by != ''){
		$group_statement = 'GROUP BY '.$group_by.' ';
	}else{
		$group_statement = 'GROUP BY `date` ';
	}

	return $group_statement;
}

function getBandwidth($connection, $date_begin, $date_end, $group){

	if($date_begin != '' && $date_end != ''){
		$where_statement = 'WHERE date BETWEEN ('.$date_begin.') AND ( '.$date_end.')';
	}else{
		$where_statement = '';
	}

	$group = buildGroupStatement($group);

	$order = "ORDER BY `date`";

	// request sum for each entry in teh table between the two date
	$sql = 'SELECT SUM(`global`) as global, SUM(`local`) as local, SUM(`incoming`) as incoming, SUM(`outcoming`) as outcoming, date  FROM bandwidth  '.$where_statement.' '.$group.' '.$order;
	// echo $sql;
	$req = $connection->prepare($sql);
	$req->execute();

	$result = $req->fetchAll(PDO::FETCH_ASSOC);
	return $result;
}

function getTotalBandwidth($connection, $date_begin, $date_end){

	if($date_begin != '' && $date_end != ''){
		$where_statement = ' WHERE date BETWEEN ('.$date_begin.') AND ('.$date_end.')';
	}else{
		$where_statement = '';
	}

	// request the sum of the bandwidth between the two date
	$sql = 'SELECT SUM(`global`) as Ko, SUM(`local`) as loc_Ko, SUM(`incoming`) as in_Ko, SUM(`outcoming`) as out_Ko FROM bandwidth  '.$where_statement;
	$req = $connection->prepare($sql);
	$req->execute();
	$array = $req->fetchAll(PDO::FETCH_ASSOC)[0];

	$result['list'] = $array;
	
	$sql = 'SELECT `date` FROM `bandwidth` '.$where_statement.' ORDER BY `date` LIMIT 1';
	// echo $sql;
	$req = $connection->prepare($sql);
	$req->execute();
	$date_begin = $req->fetch(PDO::FETCH_ASSOC)['date'];
	
	
	$result['date_begin'] = $date_begin;
	return $result;
}

function getPacketLoss($connection, $date_begin, $date_end){

	if($date_begin != '' && $date_end != ''){
		$where_statement = ' WHERE date BETWEEN ('.$date_begin.') AND ('.$date_end.')';
	}else{
		$where_statement = '';
	}

	// request the sum of the bandwidth between the two date
	$sql = 'SELECT * FROM packet_loss  '.$where_statement;
	// echo $sql;
	$req = $connection->prepare($sql);
	$req->execute();
	$array = $req->fetchAll(PDO::FETCH_ASSOC);

	
	
	
	return $array;
}





?>