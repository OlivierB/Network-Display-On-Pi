var scene3D = new Scene3D('content-canvas', Params.network3D);
scene3D.animate();
scene3D.connect(dispatcher, 'local_communication');