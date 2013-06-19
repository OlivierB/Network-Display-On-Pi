function Satellite3D(geometry, material, distance) {



	THREE.Object3D.call(this);

	// var pivot = new THREE.Object3D();
	this.rotation.z = Math.random() * Math.PI * 2;
	this.rotation.y = Math.random() * Math.PI * 2;
	this.rotation.x = Math.random() * Math.PI * 2;


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

	this.add(this.cube);
	// this.pivot = pivot;

}

Satellite3D.prototype = Object.create(THREE.Object3D.prototype);

Satellite3D.prototype.rotate = function(x, y, z) {
	this.rotation.z += x;
	this.rotation.y += y;
	this.rotation.x += z;
}

Satellite3D.prototype.getPosition = function() {
	return this.localToWorld(this.cube.position.clone());
}

Satellite3D.prototype.update = function() {
	this.rotate(this.dir[0] / 50, this.dir[1] / 50, this.dir[2] / 50);
}

// destroy: function(scene){
// 	scene.remove(this.pivot);
// 	delete this.pivot;
// }



