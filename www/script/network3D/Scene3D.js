/**
 * Scene3D, class displaying the global scene of the network.
 * @author Matrat Erwan
 **/



function Scene3D(id, quality) {

    // inheritance from WebSocketManager
    WebSocketManager.call(this, id + '-alert');

    this.id = id;
    this.detail3D = quality || 5;



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
    this.sphere = new Satellite3D(this.sphereGeometry, 'output', 0, this.OutputMaterial);
    this.sphere.scale.set(3, 3, 3);
    this.scene.add(this.sphere);
    this.satellites[-1] = this.sphere;


    this.initRender();
    this.onWindowResize();

    this.needDisplay = false;

    this.infoDisplay = new InformationsDisplay(id);


}

// inheritance from WebSocketManager
Scene3D.prototype = Object.create(WebSocketManager.prototype);

// function needed by the WebSocketManager inheritance
Scene3D.prototype.dataManager = function(obj) {

    // if (obj.remove_ip != null) {
    //     for (var i = 0; i < obj.remove_ip.length; i++) {
    //         // this.removeSatellite(obj.remove_ip[i]);
    //     }
    // }

    if ('communications' in obj) {
        for (var i = 0; i < obj.communications.length; i++) {

            if (!(obj.communications[i].ip_src in this.satellites)) {
                this.addSatellite(obj.communications[i].ip_src);
            }

            if (!(obj.communications[i].ip_dst in this.satellites)) {
                this.addSatellite(obj.communications[i].ip_dst);
            }

            this.addRay(
                this.satellites[obj.communications[i].ip_src],
                this.satellites[obj.communications[i].ip_dst],
                Math.random() * 0xffffff,
                this.fromSizeToTime(obj.communications[i].number));
        }
    }

    this.needDisplay = true;
};

Scene3D.prototype.fromSizeToTime = function(size) {
    return (Math.log(size * 0.8)) + 1;
};

Scene3D.prototype.initCamera = function() {
    // PerspectiveCamera(field of view, apsect, near, far)
    this.camera = new THREE.PerspectiveCamera(80, this.SCREEN_WIDTH / this.SCREEN_HEIGHT, 1, 3000);
    this.camera.position.z = 200;
    this.camera.position.x = 200;
    this.camera.position.y = 200;
};

Scene3D.prototype.initController = function() {
    this.controls = new THREE.OrbitControls(this.camera);
    this.controls.addEventListener('change', this.render.bind(this));
};

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
};

Scene3D.prototype.initMaterial = function() {
    this.YellowMaterial = new THREE.MeshLambertMaterial({
        color: 0xF9A30E,
        doubleSided: false,
        wireframe: false,
        overdraw: true
    });

    if (this.detail3D > 5) {
        this.OutputMaterial = new THREE.MeshLambertMaterial({
            map: new THREE.ImageUtils.loadTexture('res/img/Earth-Clouds.jpg')
        });
    } else {
        this.OutputMaterial = new THREE.MeshLambertMaterial({
            color: 0x0000cb,
            doubleSided: false,
            wireframe: false,
            overdraw: true
        });
    }
};

Scene3D.prototype.initGeometry = function() {
    var segmentsWidth = this.detail3D * 10 - 50;
    var segmentsHeight = this.detail3D * 10 - 50;

    this.sphereGeometry = new THREE.SphereGeometry(10, segmentsWidth, segmentsHeight, false);
    this.cubeGeometry = new THREE.CubeGeometry(15, 15, 15, false);
};

Scene3D.prototype.initAxisHelper = function() {
    var axes = THREE.AxisHelper(100);
    this.scene.add(axes);
};



Scene3D.prototype.addSatellite = function(ip) {

    var style = this.infoDisplay.addIp(ip);
    var texture, font;
    if(style){
        texture = style.textureColor;
        font = style.fontColor;
    }
    var sat;
    if (this.detail3D > 5){
        sat = new Satellite3D(this.sphereGeometry, ip >>> 24, Math.random() * 150 + 100, null, texture, font);
    }else{
        sat = new Satellite3D(this.cubeGeometry,  ip >>> 24, Math.random() * 150 + 100, null, texture, font);
    }

    this.scene.add(sat);

    this.satellites[ip] = sat;
};

Scene3D.prototype.removeSatellite = function(ip) {
    if (ip in this.satellites) {
        this.scene.remove(this.satellites[ip]);
        delete this.satellites[ip];
    }
};

Scene3D.prototype.addRay = function(satellite_src, satellite_target, color, time) {
    if (!this.needDisplay) {
        var ray = new Ray(satellite_src, satellite_target, color, time);
        this.scene.add(ray);
        this.rays.push(ray);

        this.numberSatellitesAddedSinceRefresh++;
    }
};

Scene3D.prototype.initRender = function() {
    this.renderer = new THREE.WebGLRenderer({
        antialias: true
    });
    this.renderer.setSize(this.SCREEN_WIDTH, this.SCREEN_HEIGHT);
    document.getElementById(this.id).appendChild(this.renderer.domElement);


    window.addEventListener('resize', this.onWindowResize.bind(this), false);
};

Scene3D.prototype.onWindowResize = function() {

    // Window size
    this.SCREEN_WIDTH = $('#' + this.id).width();
    this.SCREEN_HEIGHT = window.innerHeight;

    this.windowHalfX = this.SCREEN_WIDTH / 2;
    this.windowHalfY = this.SCREEN_HEIGHT / 2;



    this.camera.aspect = this.SCREEN_WIDTH / this.SCREEN_HEIGHT;
    this.camera.updateProjectionMatrix();

    this.renderer.setSize(this.SCREEN_WIDTH, this.SCREEN_HEIGHT);

};

Scene3D.prototype.animate = function() {
    this.controls.update();

    requestAnimationFrame(this.animate.bind(this));

    this.render();
};

Scene3D.prototype.render = function() {
    this.needDisplay = false;


    for (var index in this.satellites) {
        this.satellites[index].update();
    }


    var i = this.rays.length;
    for ( ;i--;) {
        var ray = this.rays[i];

        if (!ray.update()) {
            // destruction of the ray
            this.scene.remove(ray);
            // delete ray;
            this.rays.splice(i, 1);
        }
    }

    this.renderer.render(this.scene, this.camera);

};

