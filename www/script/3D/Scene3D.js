function Scene3D() {

	// to handle callback
	that = this;

	// Window sixe
	this.SCREEN_WIDTH = window.innerWidth,
	this.SCREEN_HEIGHT = window.innerHeight,

	this.windowHalfX = window.innerWidth / 2,
	this.windowHalfY = window.innerHeight / 2,



	// init
	this.initCamera();
	this.initController();



	this.scene = new THREE.Scene();

	this.initLight();
	this.initMaterial();
	this.initGeometry();



	// add the 'sun'
	var sphere = new THREE.Mesh(this.sphereGeometry, this.YellowMaterial);
	this.scene.add(sphere);


	this.initSatellites();

	this.initRender();



}

Scene3D.prototype = {
	constructor: Scene3D,

	initCamera: function() {
		// PerspectiveCamera(field of view, apsect, near, far)
		this.camera = new THREE.PerspectiveCamera(80, this.SCREEN_WIDTH / this.SCREEN_HEIGHT, 1, 3000);
		this.camera.position.z = 200;
		this.camera.position.x = 200;
		this.camera.position.y = 200;
	},

	initController: function() {
		this.controls = new THREE.OrbitControls(this.camera);
		this.controls.addEventListener('change', this.render);
	},

	initLight: function() {
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
	},

	initMaterial: function() {
		this.YellowMaterial = new THREE.MeshLambertMaterial({
			color: 0xF9A30E,
			doubleSided: false,
			wireframe: false,
			overdraw: true
		});
	},

	initGeometry: function() {
		this.sphereGeometry = new THREE.SphereGeometry(10, 10, 10, false);
		this.cubeGeometry = new THREE.CubeGeometry(20, 20, 20, false);
	},

	initAxisHelper: function() {
		var axes = THREE.AxisHelper(100);
		this.scene.add(axes);
	},

	initSatellites: function() {
		this.satellites = [];



		for (var i = 0; i < 30; i++) {
			var sat = new Satellite3D(this.cubeGeometry, this.YellowMaterial);

			sat.addToScene(this.scene);

			this.satellites.push(sat);

		}
	},

	initRender: function() {
		this.renderer = new THREE.WebGLRenderer({
			antialias: true
		});
		this.renderer.setSize(this.SCREEN_WIDTH, this.SCREEN_HEIGHT);
		document.getElementById('content-canvas').appendChild(this.renderer.domElement);


		window.addEventListener('resize', this.onWindowResize, false);
	},

	onWindowResize: function() {

		that.windowHalfX = window.innerWidth / 2;
		that.windowHalfY = window.innerHeight / 2;

		that.camera.aspect = window.innerWidth / window.innerHeight;
		that.camera.updateProjectionMatrix();

		that.renderer.setSize(window.innerWidth, window.innerHeight);

	},

	animate: function() {
		that.controls.update();

		requestAnimationFrame(that.animate);

		that.render();
	},

	render: function() {

		// that.camera.lookAt(that.scene.position);


		for (var i = 1; i < that.satellites.length; i++) {
			var sat = that.satellites[i];
			sat.rotate(sat.dir[0] / 50, sat.dir[1] / 50, sat.dir[2] / 50);
		}

		that.renderer.render(that.scene, that.camera);
	}
}