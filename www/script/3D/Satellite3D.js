function Satellite3D(geometry, material, distance) {

	var pivot = new THREE.Object3D();
	pivot.rotation.z = Math.random() * Math.PI * 2;
	pivot.rotation.y = Math.random() * Math.PI * 2;
	pivot.rotation.x = Math.random() * Math.PI * 2;


	var vx = Math.random() / 3;
	var vy = (Math.random() * (1 - vx)) / 2;
	var vz = 1 - vx - vy;

	this.dir = {
		0: vx - 0.33,
		1: vy - 0.33,
		2: vz - 0.33
	};

	this.cube = new THREE.Mesh(geometry, material);
	this.cube.position.set(distance, 0, 0);

	pivot.add(this.cube);
	this.pivot = pivot;

}

Satellite3D.prototype = {
	constructor: Satellite3D,

	addToScene: function(scene) {
		scene.add(this.pivot);
	},

	rotate: function(x, y, z) {
		this.pivot.rotation.z += x;
		this.pivot.rotation.y += y;
		this.pivot.rotation.x += z;
	},

	getPosition: function() {
		return this.pivot.localToWorld(this.cube.position.clone());
	}



}