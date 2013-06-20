<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Titre de la page</title>
  
</head>
<body>

</body>
</html>


<script type="text/javascript">

  var ip = 108;

  var canvas1 = document.createElement('canvas');
  var context1 = canvas1.getContext('2d');
  context1.canvas.width = 300;
  context1.canvas.height = 300;
  context1.fillStyle = "#F9A30E";

  context1.fillRect(0,0,context1.canvas.width,context1.canvas.height);


  context1.font = "Bold 90px Arial";
  context1.fillStyle = "rgba(255,0,0,0.95)";

  // context1.fillText('45', 25, 90);
  // context1.fillText('45', 155, 180);
  // context1.fillText('45', 25, 270);

  context1.save();

  context1.fillText(ip, 55, 175);
  // context1.fillText('45', 125, 120);
  // context1.fillText('45', 225, 65);

  //  context1.translate(300, 300);
  // context1.rotate(Math.PI);

  // context1.fillText(ip, 25, 95);
  // context1.fillText('45', 125, 120);
  // context1.fillText('45', 225, 65);

  // context1.translate(-150, -150);
  // context1.restore();

// context1.fillText('45', 25, 65);
//   context1.fillText('45', 125, 120);
//   context1.fillText('45', 225, 65);

    
  // canvas contents will be used for a texture
  // var texture1 = new THREE.Texture(canvas1) ;
  // texture1.wrapS = texture1.wrapT = THREE.RepeatWrapping;
  // texture1.repeat.set( 2, 2 );
  // texture1.needsUpdate = true;




  document.body.appendChild(canvas1);

</script>