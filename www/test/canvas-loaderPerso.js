


var SCREEN_WIDTH = window.innerWidth,
	SCREEN_HEIGHT = window.innerHeight,



	windowHalfX = window.innerWidth / 2,
	windowHalfY = window.innerHeight / 2,

	camera, scene, renderer;

init();
animate();

function init() {



	camera = new THREE.PerspectiveCamera(80, SCREEN_WIDTH / SCREEN_HEIGHT, 1, 3000);
	camera.position.z = 200;
	camera.position.x = 200;
	camera.position.y = 200;

	scene = new THREE.Scene();

	controls = new THREE.OrbitControls(camera);
	controls.addEventListener('change', render);

	// var ambientLight = new THREE.AmbientLight(0x222222);
	// scene.add(ambientLight);

	var light = new THREE.PointLight(0xffffff);
	light.position.set(0, 0, 0);
	scene.add(light);

	var spotLight = new THREE.SpotLight(0xffffff);
	spotLight.position.set(100, 200, 100);

	spotLight.castShadow = true;
	
	spotLight.shadowMapWidth = 1024;
	spotLight.shadowMapHeight = 1024;

	spotLight.shadowCameraNear = 500;
	spotLight.shadowCameraFar = 4000;
	spotLight.shadowCameraFov = 30;
	scene.add(spotLight);


	
	var material = new THREE.MeshLambertMaterial({
		color: 0xF9A30E,
		doubleSided: false,
		wireframe: false,
		overdraw: true
	});

	parents = [];
	dir = [];
	// parent
	parent = new THREE.Object3D();
	scene.add(parent);
	// pivots
	// var pivot1 = new THREE.Object3D();
	// var pivot2 = new THREE.Object3D();
	// var pivot3 = new THREE.Object3D();

	// pivot1.rotation.z = 0;
	// pivot2.rotation.z = 2 * Math.PI / 3;
	// pivot3.rotation.z = 4 * Math.PI / 3;

	// parent.add(pivot1);
	// parent.add(pivot2);
	// parent.add(pivot3);

	var sphereGeometry = new THREE.SphereGeometry(20, 10, 10, false);
	var sphere = new THREE.Mesh(sphereGeometry, material);
	scene.add(sphere);


	var cubeGeometry = new THREE.CubeGeometry(20, 20, 20, false);
	for (var i = 1; i < 30; i++) {
		parent = new THREE.Object3D();
		scene.add(parent);



		var pivot = new THREE.Object3D();
		pivot.rotation.z = Math.random() * Math.PI *2;
		pivot.rotation.y = Math.random() * Math.PI *2;
		pivot.rotation.x = Math.random() * Math.PI *2;
		parent.add(pivot);

		var vx = Math.random() / 3;
		var vy = (Math.random() * (1 - vx)) / 2;
		var vz = 1 - vx - vy;

		dir.push({0:vx-0.33, 1:vy-0.33, 2:vz-0.33});
		// console.log(dir[i-1]);
		var sphere2 = new THREE.Mesh(cubeGeometry, material);
		sphere2.position.set( 150, 0, 0);

		pivot.add( sphere2 );
		parents.push(parent);

		// scene.add(sphere2);
	}


	var axes = THREE.AxisHelper(100);
	scene.add(axes);





	renderer = new THREE.WebGLRenderer({
		antialias: true
	});
	renderer.setSize(SCREEN_WIDTH, SCREEN_HEIGHT);
	document.getElementById('content-canvas').appendChild(renderer.domElement);



	window.addEventListener('resize', onWindowResize, false);


	
	
}

function onWindowResize() {

	windowHalfX = window.innerWidth / 2;
	windowHalfY = window.innerHeight / 2;

	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();

	renderer.setSize(window.innerWidth, window.innerHeight);

}



function animate() {
	controls.update();

	requestAnimationFrame(animate);

	render();

}

function render() {

	// camera.position.x += .05;
	camera.lookAt(scene.position);

	
	for (var i = 1; i < parents.length; i++) {
		parent = parents[i];
		parent.rotation.z += dir[i][0] / 50;
		parent.rotation.y += dir[i][1] / 50;
		parent.rotation.x += dir[i][2] / 50;
	}

	renderer.render(scene, camera);
}

