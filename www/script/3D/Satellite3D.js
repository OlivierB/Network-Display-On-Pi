function Satellite3D(geometry, material) {

	this.parent = new THREE.Object3D();


	var pivot = new THREE.Object3D();
	pivot.rotation.z = Math.random() * Math.PI * 2;
	pivot.rotation.y = Math.random() * Math.PI * 2;
	pivot.rotation.x = Math.random() * Math.PI * 2;

	this.parent.add(pivot);

	var vx = Math.random() / 3;
	var vy = (Math.random() * (1 - vx)) / 2;
	var vz = 1 - vx - vy;

	this.dir = {
		0: vx - 0.33,
		1: vy - 0.33,
		2: vz - 0.33
	};

	var cube = new THREE.Mesh(geometry, material);
	cube.position.set(150, 0, 0);

	pivot.add(cube);


}

Satellite3D.prototype = {
	constructor: Satellite3D,

	addToScene: function(scene) {
		scene.add(this.parent);
	},

	rotate: function(x, y, z) {
		this.parent.rotation.z += x;
		this.parent.rotation.y += y;
		this.parent.rotation.x += z;
	}

}