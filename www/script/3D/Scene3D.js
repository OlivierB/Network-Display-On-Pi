function Scene3D(id) {

	// inheritance from WebSocketManager
	WebSocketManager.call(this, id + '-alert');

	this.id = id;

	// Window sixe
	this.SCREEN_WIDTH = window.innerWidth,
	this.SCREEN_HEIGHT = window.innerHeight,

	this.windowHalfX = window.innerWidth / 2,
	this.windowHalfY = window.innerHeight / 2,

	this.satellites = [];
	this.rays = [];

	// init
	this.initCamera();
	this.initController();


	this.scene = new THREE.Scene();

	this.initLight();
	this.initMaterial();
	this.initGeometry();



	// add the 'sun' (central spherical satellite)
	this.sphere = new Satellite3D(this.sphereGeometry, this.YellowMaterial, 0);
	this.sphere.addToScene(this.scene);

	this.initSatellites();

	this.initRender();


	// this.addRay(this.satellites[4], this.satellites[5], 0x00fff0, 6);
}

// inheritance from WebSocketManager
Scene3D.prototype = Object.create(WebSocketManager.prototype);


Scene3D.prototype.dataManager = function(obj) {
	if (obj.add_ip != null) {
		for (var i = 0; i < obj.add_ip.length; i++) {
			this.addSatellite(obj.add_ip[i]);
		}
	}

	if (obj.remove_ip != null) {
		for (var i = 0; i < obj.remove_ip.length; i++) {
			this.removeSatellite(obj.remove_ip[i]);
		}
	}

	if (obj.communications != null) {
		for (var i = 0; i < obj.communications.length; i++) {
			this.addRay(
				this.satellites[obj.communications[i].ip_src],
				this.satellites[obj.communications[i].ip_dst],
				this.color_code[obj.communications[i].protocole],
				this.fromSizeToTime(obj.communications[i].size));
		}
	}
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
}

Scene3D.prototype.initMaterial = function() {
	this.YellowMaterial = new THREE.MeshLambertMaterial({
		color: 0xF9A30E,
		doubleSided: false,
		wireframe: false,
		overdraw: true
	});
}

Scene3D.prototype.initGeometry = function() {
	this.sphereGeometry = new THREE.SphereGeometry(10, 10, 10, false);
	this.cubeGeometry = new THREE.CubeGeometry(20, 20, 20, false);
}

Scene3D.prototype.initAxisHelper = function() {
	var axes = THREE.AxisHelper(100);
	this.scene.add(axes);
}

Scene3D.prototype.initSatellites = function() {
	for (var i = 0; i < 30; i++) {
		this.addSatellite(i);
	}
}

Scene3D.prototype.addSatellite = function(ip) {
	var sat = new Satellite3D(this.cubeGeometry, this.YellowMaterial, Math.random() * 150 + 100);

	sat.addToScene(this.scene);

	this.satellites[ip] = sat;
}

Scene3D.prototype.removeSatellite = function(ip) {
	sat.destroy(scene);
	this.satellites.splice(ip, 1);
}

Scene3D.prototype.addRay = function(satellite_src, satellite_target, color, time) {
	var ray = new Ray(satellite_src, satellite_target, color, time);
	ray.addToScene(this.scene);

	this.rays.push(ray);

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

	this.windowHalfX = window.innerWidth / 2;
	this.windowHalfY = window.innerHeight / 2;

	this.camera.aspect = window.innerWidth / window.innerHeight;
	this.camera.updateProjectionMatrix();

	this.renderer.setSize(window.innerWidth, window.innerHeight);

}

Scene3D.prototype.animate = function() {
	this.controls.update();

	requestAnimationFrame(this.animate.bind(this));

	this.render();
}

Scene3D.prototype.render = function() {


	for (var index in this.satellites) {
		var sat = this.satellites[index];
		sat.update();
	}


	for (var i = 0; i < this.rays.length; i++) {
		var ray = this.rays[i];

		if (!ray.update()) {
			// destruction of the ray
			this.rays.splice(i, 1);
			ray.destroy(this.scene);

			i--;
		}
	}

	this.renderer.render(this.scene, this.camera);
}



// connect: function(address, protocol) {

// 	that = this;
// 	this.alertContainer = $('#content-canvas-alert');

// 	// console.log('tentative de connexion live ' + App.serverAddress + '/' + App.bandwidtProtocol);

// 	this.address = address || App.serverAddress || 'localhost';
// 	this.prot = protocol || App.localCommication || 'local_communication';


// 	this.connection = new WebSocket(this.address, this.prot);


// 	// When the connection is open, send some data to the server
// 	this.connection.onopen = function() {
// 		console.log("connexion");
// 		that.alertContainer.html('');
// 		that.connection.send('Ping'); // Send the message 'Ping' to the server

// 	};

// 	// Log errors
// 	this.connection.onerror = function(error) {
// 		console.log('WebSocket Error ' + error);
// 		that.alertContainer.text('Connection error : ' + error);
// 	};

// 	// Log messages from the server
// 	this.connection.onmessage = function(e) {
// 		var obj = JSON.parse(e.data);
// if (obj.add_ip != null) {
// 		for (var i = 0; i < obj.add_ip.length; i++) {
// 			that.addSatellite(obj.add_ip[i]);
// 		}
// 	}

// 	if (obj.remove_ip != null) {
// 		for (var i = 0; i < obj.remove_ip.length; i++) {
// 			that.removeSatellite(obj.remove_ip[i]);
// 		}
// 	}

// 	if (obj.communications != null) {
// 		for (var i = 0; i < obj.communications.length; i++) {
// 			that.addRay(
// 				that.satellites[obj.communications[i].ip_src],
// 				that.satellites[obj.communications[i].ip_dst],
// 				that.color_code[obj.communications[i].protocole],
// 				that.fromSizeToTime(obj.communications[i].size));
// 		}
// 	}

// 	};

// 	this.connection.onclose = function(e) {
// 		// console.log('Deconnexion tentative de reconnexion dans 5 sec ' + App.serverAddress + '/' + App.bandwidtProtocol);
// 		that.alertContainer.html('<span class="alert">Disconnected from server. Next try in 5 seconds.</span>');
// 		setTimeout(function() {
// 			that.connect(that.address, that.prot);
// 		}, 5000);
// 	};

// }
// }