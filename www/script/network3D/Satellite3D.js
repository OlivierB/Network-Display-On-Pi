/**
 * Satellite3D, represents and displays one IP as a Satellite (any form given by the parameter geometry)
 * @author Matrat Erwan
 **/

function Satellite3D(geometry, ip, distance, material, textureColor, fontColor) {


    // inheritance of THREE.Object3D
    THREE.Object3D.call(this);

    // initial location
    this.rotation.z = Math.random() * Math.PI * 2;
    this.rotation.y = Math.random() * Math.PI * 2;
    this.rotation.x = Math.random() * Math.PI * 2;


    // initialize the movement
    var vx = Math.random() / 3;
    var vy = (Math.random() * (1 - vx)) / 2;
    var vz = 1 - vx - vy;

    this.dir = [
        (vx - 0.33)/50,
        (vy - 0.33)/50,
        (vz - 0.33)/50
    ];

    // if no material is given, it will be created to display the IP via a canvas
    material =  material || this.createMaterialFromIp(ip, textureColor, fontColor);



    this.cube = new THREE.Mesh(geometry, material);
    this.cube.position.set(distance, 0, 0);

    this.add(this.cube);

}

// inherirance
Satellite3D.prototype = Object.create(THREE.Object3D.prototype);

Satellite3D.prototype.rotate = function(x, y, z) {
    this.rotation.z += x;
    this.rotation.y += y;
    this.rotation.x += z;
};

// transform the position from the local coordinates to the world coordinates
Satellite3D.prototype.getPosition = function() {
    return this.localToWorld(this.cube.position.clone());
};

Satellite3D.prototype.update = function() {
    this.rotate(this.dir[0], this.dir[1], this.dir[2]);
};

Satellite3D.prototype.createMaterialFromIp = function(ip, textureColor, fontColor){
    // create a canvas element
        var canvas = document.createElement('canvas');
        var context = canvas.getContext('2d');
        context.canvas.width = 300;
        context.canvas.height = 300;
        context.fillStyle = textureColor || "#F9A30E";

        context.fillRect(0, 0, 300, 300);


        context.font = "Bold 80px Arial";
        context.fillStyle = fontColor || "rgba(255,0,0,0.95)";


        context.fillText(ip, 55, 175);

        // canvas contents will be used for a texture
        var texture = new THREE.Texture(canvas);
        texture.needsUpdate = true;

        return new THREE.MeshLambertMaterial({
            map: texture
        });
};