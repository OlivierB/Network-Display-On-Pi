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

	this.line = new THREE.Line(geometry, material);

	this.time = time;
	this.clock = new THREE.Clock(true);
	// console.log(THREE.Clock(true));


}

Ray.prototype = {
	constructor: Ray,

	addToScene: function(scene) {
		scene.add(this.line);
	},

	update: function() {

		if (this.clock.getElapsedTime() < this.time) {
			// console.log('update');
			this.line.geometry.vertices[0] = this.satellite_src.getPosition();
			this.line.geometry.vertices[1] = this.satellite_target.getPosition();
			// this.line.updateMatrix()
			this.line.geometry.verticesNeedUpdate = true;

			return true;
		}else
		{
			return false;
		}
	},

	destroy: function(scene){
		scene.remove(this.line);
		delete this.line;
	}
}