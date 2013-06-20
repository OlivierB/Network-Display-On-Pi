function Ray(satellite_src, satellite_target, color, time) {



	this.satellite_target = satellite_target;
	this.satellite_src = satellite_src;

	var geometry = new THREE.Geometry();

	geometry.vertices.push(satellite_src.getPosition());
	geometry.vertices.push(satellite_target.getPosition());
	geometry.dynamic = true;

	var material = new THREE.LineBasicMaterial({
		color: color,
		linewidth: 1
	});

	THREE.Line.call(this, geometry, material);
	// this.line = new THREE.Line(geometry, material);

	this.time = time;
	this.clock = new THREE.Clock(true);
	// console.log(THREE.Clock(true));




	this.packet = new THREE.Mesh(new THREE.CubeGeometry(3, 3, 3, false), new THREE.MeshLambertMaterial({
		color: 0xF9A30E,
		doubleSided: false,
		wireframe: false,
		overdraw: true
	})); 

	this.add(this.packet);


}

Ray.prototype = Object.create(THREE.Line.prototype);

Ray.prototype.update = function() {

	if (this.clock.getElapsedTime() < this.time && this.satellite_src != null && this.satellite_target != null) {
		// console.log('update');
		this.geometry.vertices[0] = this.satellite_src.getPosition();
		this.geometry.vertices[1] = this.satellite_target.getPosition();
		// this.line.updateMatrix()
		this.geometry.verticesNeedUpdate = true;

		this.packet.position = this.geometry.vertices[1].sub(this.geometry.vertices[0]).multiplyScalar(this.clock.getElapsedTime() / this.time).add(this.geometry.vertices[0]);

		// console.log(this.packet.position);

		return true;
	} else {
		return false;
	}
}
