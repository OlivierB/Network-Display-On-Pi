<?php

function getProtocol($connection, $date_begin, $date_end, $table){
	// request the protocol list
	$sql = 'SELECT distinct `protocol` FROM `'.$table.'`  WHERE date BETWEEN ('. $date_begin .') AND ('. $date_end .')';

	$req = $connection->prepare($sql);
	$req->execute();

	// PDO::FETCH_NUM : request only an array without associative index
	$result = $req->fetchAll(PDO::FETCH_NUM);

	// final container
	$obj = array();

	// build of the protocol list 
	$tab = array();
	foreach ($result as $row) {
		$tab[] = $row[0];
	}
	$obj['listProt'] = $tab;



	// request the protocol use
	$sql = 'SELECT * FROM `'.$table.'`  WHERE date BETWEEN ('. $date_begin .') AND ('. $date_end .')';

	$req = $connection->prepare($sql);
	$req->execute();

	// PDO::FETCH_ASSOC : request with associative array
	$result = $req->fetchAll(PDO::FETCH_ASSOC);

	$date = '';
	$tab = array();
	$i = -1;

	// build of the list of protocol use
	foreach ($result as $row) {
		
		// group result per day, create a new group when a new date appears
		if($row['date'] != $date){
			$i++;
			$date = $row['date'];

			$tab[] = array();
			$tab[$i]['date'] = $date;
			$tab[$i]['value'] = array();
		}
		$tab[$i]['value'][$row['protocol']] = $row['number'];
	}
	$obj['listValue'] = $tab;

	return $obj;
}



function getProtocolEthernet($connection, $date_begin, $date_end){
	return getProtocol($connection, $date_begin, $date_end, 'protocols_ether');
}

function getSubProtocolIpv4($connection, $date_begin, $date_end){
	return getProtocol($connection, $date_begin, $date_end, 'protocols_ip');
}



function getBandwidth($connection, $date_begin, $date_end){
	// request average flow for each entry in teh table between the two date
	$sql = 'SELECT `global`/`dtime_s` as global, `local`/`dtime_s` as local,`incoming`/`dtime_s` as incoming,`outcoming`/`dtime_s` as outcoming, date  FROM bandwidth  WHERE date BETWEEN ('.$date_begin.') AND ( '.$date_end.')';

	$req = $connection->prepare($sql);
	$req->execute();

	$result = $req->fetchAll(PDO::FETCH_ASSOC);
	return $result;
}

function getTotalBandwidth($connection, $date_begin, $date_end){
	// request the sum of the bandwidth between the two date
	$sql = 'SELECT SUM(`global`) as Ko, SUM(`local`) as loc_Ko, SUM(`incoming`) as in_Ko, SUM(`outcoming`) as out_Ko FROM bandwidth  WHERE date BETWEEN ('.$date_begin.') AND ('.$date_end.')';
	$req = $connection->prepare($sql);
	$req->execute();
	$result = $req->fetchAll(PDO::FETCH_ASSOC);
	return $result;
}





?>