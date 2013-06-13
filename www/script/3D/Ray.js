function Ray() {
	launchRay: function(src, target, color, time) {
		// console.log(src);


		var geometry = new THREE.Geometry();

		geometry.vertices.push(src);
		geometry.vertices.push(target);

		var material = new THREE.LineBasicMaterial({
			color: color,
			linewidth: 1
		});

		this.line = new THREE.Line(geometry, material);

		this.time = time;
		this.clock = THREE.Clock(true);
	},

	addToScene: function(scene){
		scene.add(this.line);
	}
}