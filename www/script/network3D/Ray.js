/**
 * Ray, represents and display a communication via two IPs as a Ray.
 * A ray is programmed to live for time given.
 * @author Matrat Erwan
 **/

function Ray(satellite_src, satellite_target, color, time) {

    this.satellite_target = satellite_target;
    this.satellite_src = satellite_src;

    var geometry = new THREE.Geometry();

    // create the ray
    geometry.vertices.push(satellite_src.getPosition());
    geometry.vertices.push(satellite_target.getPosition());
    // allow to change its position afterwards
    geometry.dynamic = true;

    var material = new THREE.LineBasicMaterial({
        color: color,
        linewidth: 1
    });
    // inerhitance of THREE.Line
    THREE.Line.call(this, geometry, material);

    this.time = time;
    this.clock = new THREE.Clock(true);

    // create the small cube representing the packet
    this.packet = new THREE.Mesh(new THREE.CubeGeometry(3, 3, 3, false), new THREE.MeshLambertMaterial({
        color: 0xF9A30E,
        doubleSided: false,
        wireframe: false,
        overdraw: true
    }));

    this.add(this.packet);


}
// inerhitance of THREE.Line
Ray.prototype = Object.create(THREE.Line.prototype);

// update the position and return false if its time is outdated
Ray.prototype.update = function() {
    if (this.clock.getElapsedTime() < this.time) {
        this.geometry.vertices[0] = this.satellite_src.getPosition();
        this.geometry.vertices[1] = this.satellite_target.getPosition();

        this.geometry.verticesNeedUpdate = true;

        this.packet.position = this.geometry.vertices[1].sub(this.geometry.vertices[0]).multiplyScalar(this.clock.getElapsedTime() / this.time).add(this.geometry.vertices[0]);

        return true;
    } else {
        return false;
    }
};
