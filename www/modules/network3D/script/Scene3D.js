/**
 *
 *	App.Details3D define the quality of the 3D.
 *	1 being crappy and 10 beautiful.
 **/



function Scene3D(id) {

	// inheritance from WebSocketManager
	WebSocketManager.call(this, id + '-alert');

	this.id = id;
	this.detail3D = App.Details3D || 5;



	this.satellites = new Array();
	this.rays = [];

	// init
	this.initCamera();
	this.initController();


	this.scene = new THREE.Scene();

	this.initLight();
	this.initMaterial();
	this.initGeometry();



	// add the 'sun' (central spherical satellite)
	this.sphere = new Satellite3D(this.sphereGeometry, 'output', 0, this.OutputMaterial);
	this.sphere.scale.set(3, 3, 3)
	this.scene.add(this.sphere);
	this.satellites['internet'] = this.sphere;

	// this.initSatellites();

	this.initRender();
	this.onWindowResize();

	this.needDisplay = false;

	

}

// inheritance from WebSocketManager
Scene3D.prototype = Object.create(WebSocketManager.prototype);


Scene3D.prototype.dataManager = function(obj) {

	if (obj.remove_ip != null) {
		for (var i = 0; i < obj.remove_ip.length; i++) {
			// this.removeSatellite(obj.remove_ip[i]);
		}
	}

	if (obj.communications != null) {
		for (var i = 0; i < obj.communications.length; i++) {

			if (this.satellites[obj.communications[i].ip_src] == null) {
				this.addSatellite(obj.communications[i].ip_src);
				// console.log('ajout ' + obj.communications[i].ip_src);
			}

			if (this.satellites[obj.communications[i].ip_dst] == null) {
				this.addSatellite(obj.communications[i].ip_dst);
				// console.log('ajout ' + obj.communications[i].ip_dst);
			}

			// var scale = Math.log(obj.communications[i].size /600);
			// this.satellites[obj.communications[i].ip_dst].cube.scale.set(scale, scale, scale);

			this.addRay(
				this.satellites[obj.communications[i].ip_src],
				this.satellites[obj.communications[i].ip_dst],
				Math.random() * 0xffffff,
				this.fromSizeToTime(obj.communications[i].number));
		}
	}

	this.needDisplay = true;
}

Scene3D.prototype.fromSizeToTime = function(size) {
	return (Math.log(size * 0.8)) + 1;
}

Scene3D.prototype.initCamera = function() {
	// PerspectiveCamera(field of view, apsect, near, far)
	this.camera = new THREE.PerspectiveCamera(80, this.SCREEN_WIDTH / this.SCREEN_HEIGHT, 1, 3000);
	this.camera.position.z = 200;
	this.camera.position.x = 200;
	this.camera.position.y = 200;
}

Scene3D.prototype.initController = function() {
	this.controls = new THREE.OrbitControls(this.camera);
	this.controls.addEventListener('change', this.render.bind(this));
}

Scene3D.prototype.initLight = function() {
	// var ambientLight = new THREE.AmbientLight(0x222222);
	// this.scene.add(ambientLight);

	var light = new THREE.PointLight(0xffffff);
	light.position.set(0, 0, 0);
	this.scene.add(light);

	var spotLight = new THREE.SpotLight(0xffffff);
	spotLight.position.set(100, 200, 100);

	spotLight.castShadow = true;

	spotLight.shadowMapWidth = 1024;
	spotLight.shadowMapHeight = 1024;

	spotLight.shadowCameraNear = 500;
	spotLight.shadowCameraFar = 4000;
	spotLight.shadowCameraFov = 30;

	this.scene.add(spotLight);

	var ambientLight = new THREE.AmbientLight(0x999999);
	this.scene.add(ambientLight);
}

Scene3D.prototype.initMaterial = function() {
	this.YellowMaterial = new THREE.MeshLambertMaterial({
		color: 0xF9A30E,
		doubleSided: false,
		wireframe: false,
		overdraw: true
	});

	if (this.detail3D > 5) {
		this.OutputMaterial = new THREE.MeshLambertMaterial({
			map: new THREE.ImageUtils.loadTexture('/modules/network3D/res/img/texture/Earth-Clouds.jpg')
		});
	} else {
		this.OutputMaterial = new THREE.MeshLambertMaterial({
			color: 0x0000cb,
			doubleSided: false,
			wireframe: false,
			overdraw: true
		});
	}
	truc = this.scene;
}

Scene3D.prototype.initGeometry = function() {
	var segmentsWidth = this.detail3D * 10 - 50;
	var segmentsHeight = this.detail3D * 10 - 50;

	this.sphereGeometry = new THREE.SphereGeometry(10, segmentsWidth, segmentsHeight, false);
	this.cubeGeometry = new THREE.CubeGeometry(15, 15, 15, false);
}

Scene3D.prototype.initAxisHelper = function() {
	var axes = THREE.AxisHelper(100);
	this.scene.add(axes);
}



Scene3D.prototype.addSatellite = function(ip) {
	if (this.detail3D > 5)
		var sat = new Satellite3D(this.sphereGeometry, ip.split('.')[3], Math.random() * 150 + 100);
	else
		var sat = new Satellite3D(this.cubeGeometry, ip.split('.')[3], Math.random() * 150 + 100);


	// sat.addToScene(this.scene);
	this.scene.add(sat);

	this.satellites[ip] = sat;

	// if (this.detail3D > 5)
	// 	var sat = new Satellite3D(this.sphereGeometry, ip >> 24, Math.random() * 150 + 100);
	// else
	// 	var sat = new Satellite3D(this.cubeGeometry,  ip >> 24, Math.random() * 150 + 100);


	// sat.addToScene(this.scene);
	this.scene.add(sat);

	this.satellites[ip] = sat;
}

Scene3D.prototype.removeSatellite = function(ip) {
	if (this.satellites[ip] != null) {
		this.scene.remove(this.satellites[ip]);
		delete this.satellites[ip];
	}
}

Scene3D.prototype.addRay = function(satellite_src, satellite_target, color, time) {
	if (!this.needDisplay) {
		var ray = new Ray(satellite_src, satellite_target, color, time);
		this.scene.add(ray);
		this.rays.push(ray);

		this.numberSatellitesAddedSinceRefresh++;
	}
}

Scene3D.prototype.initRender = function() {
	this.renderer = new THREE.WebGLRenderer({
		antialias: true
	});
	this.renderer.setSize(this.SCREEN_WIDTH, this.SCREEN_HEIGHT);
	document.getElementById(this.id).appendChild(this.renderer.domElement);


	window.addEventListener('resize', this.onWindowResize.bind(this), false);
}

Scene3D.prototype.onWindowResize = function() {

	// Window sixe
	this.SCREEN_WIDTH = $('#' + this.id).width();
	this.SCREEN_HEIGHT = window.innerHeight;

	this.windowHalfX = this.SCREEN_WIDTH / 2;
	this.windowHalfY = this.SCREEN_HEIGHT / 2;



	this.camera.aspect = this.SCREEN_WIDTH / this.SCREEN_HEIGHT;
	this.camera.updateProjectionMatrix();

	this.renderer.setSize(this.SCREEN_WIDTH, this.SCREEN_HEIGHT);

}

Scene3D.prototype.animate = function() {
	this.controls.update();

	requestAnimationFrame(this.animate.bind(this));

	this.render();
}

Scene3D.prototype.render = function() {


	// console.log('ajout depuis rafr : ' + this.numberSatellitesAddedSinceRefresh);
	this.needDisplay = false;


	for (var index in this.satellites) {
		this.satellites[index].update();
	}


	var i = this.rays.length;
	for ( ;i--;) {
		// console.log(i);
		var ray = this.rays[i];

		if (!ray.update()) {
			// destruction of the ray
			this.scene.remove(ray);
			delete ray;
			this.rays.splice(i, 1);
		}
	}

	this.renderer.render(this.scene, this.camera);
		
}