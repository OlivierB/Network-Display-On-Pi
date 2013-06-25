<!doctype html>
<html lang="fr">
<head>
	<meta charset="utf-8">
	<title>Titre de la page</title>

</head>
<body>
	<?php
	
	// phpinfo();
	try {
// Nouvel objet de base SQLite 
		$db_handle = new PDO('sqlite:test.sqlite');
// Quelques options
		$db_handle->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
   // On prépare et éxécute la requête
		$req = $db_handle->prepare('SELECT * FROM DaylyFlow');

		$req->execute();

// On change la réponse SQL en réponse PHP.
// Ici, on transforme toute la réponse en un gros tableau
// (au lieu de faire ligne par ligne dans une boucle while() par exemple)
		$result = $req->fetchAll(PDO::FETCH_ASSOC);


		echo json_encode($result);
	} catch (Exception $e) {

		die ('Erreur : '.$e->getMessage());
	}
// [{"date":"2013-06-24","0":"2013-06-24","id":"1","1":"1","flow":"457.15","2":"457.15"}]

	?>

</body>
</html>

