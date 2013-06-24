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




// 192.168.5.123
var ip = 0xC0A8057B;



var mask = 0xFFFFFFFF;

mask = mask << (32 - 24);

var res = (ip & mask);
console.log(ip);
console.log(mask);

console.log((res >>> 1)*2);

console.log(maskIp(ip, 24));





</script>