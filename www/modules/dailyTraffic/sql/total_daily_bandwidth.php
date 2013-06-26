<?php

	// Connection au serveur
	try {
		$dns = 'mysql:host=192.168.1.144;dbname=NDOP';
		$utilisateur = 'ndop';
		$motDePasse = 'ndop';
		$connection = new PDO( $dns, $utilisateur, $motDePasse );


		// $today = 0;
		$sql = 'SELECT SUM(`global`) as Ko, SUM(`local`) as loc_Ko, SUM(`incoming`) as in_Ko, SUM(`outcoming`) as out_Ko FROM bandwidth  WHERE date BETWEEN (NOW( ) - INTERVAL 1 DAY) AND NOW( )';



		$req = $connection->prepare($sql);

		$req->execute();

		// On change la réponse SQL en réponse PHP.
		// Ici, on transforme toute la réponse en un gros tableau
		// (au lieu de faire ligne par ligne dans une boucle while() par exemple)
		$result = $req->fetchAll(PDO::FETCH_ASSOC);


		echo json_encode($result);

	} catch ( Exception $e ) {
		echo "Connection à MySQL impossible : ", $e->getMessage();
		die();
	}

	?>