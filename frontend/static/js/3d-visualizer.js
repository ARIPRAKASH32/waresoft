/**
 * WareSoft DevNexus 3D Architecture Visualizer
 * Built on Three.js - Precision shaded node topology on a crisp light blueprint surface
 * Uses #0B1020 (Dark Navy), #3B82F6 (Electric Blue), and #06B6D4 (Cyan)
 */

window.initDevNexus3D = function(containerId) {
    const container = document.getElementById(containerId);
    if (!container || typeof THREE === 'undefined') return;

    container.innerHTML = '';

    const width = container.clientWidth || 600;
    const height = container.clientHeight || 360;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(42, width / height, 0.1, 1000);
    camera.position.set(0, 0.5, 16.5);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Subtle directional + ambient lighting for soft 3D material shading
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.75);
    scene.add(ambientLight);

    const keyLight = new THREE.DirectionalLight(0xffffff, 0.9);
    keyLight.position.set(8, 12, 10);
    scene.add(keyLight);

    const rimLight = new THREE.DirectionalLight(0x06B6D4, 0.4);
    rimLight.position.set(-8, -6, 6);
    scene.add(rimLight);

    const networkGroup = new THREE.Group();
    scene.add(networkGroup);

    // Subtle orbital ring around gateway core
    const ringGeo = new THREE.TorusGeometry(4.2, 0.025, 12, 72);
    const ringMat = new THREE.MeshBasicMaterial({
        color: 0xCBD5E1,
        transparent: true,
        opacity: 0.75
    });
    const ringMesh = new THREE.Mesh(ringGeo, ringMat);
    ringMesh.rotation.x = Math.PI / 2.6;
    networkGroup.add(ringMesh);

    const nodeCoords = [
        { name: 'Gateway',   x: 0,    y: 0,    z: 0,    color: 0x0B1020, size: 0.78 },
        { name: 'Auth',      x: -3.8, y: 1.9,  z: 1.1,  color: 0x06B6D4, size: 0.52 },
        { name: 'Projects',  x: 3.9,  y: 1.8,  z: -0.9, color: 0x3B82F6, size: 0.58 },
        { name: 'Kanban',    x: 3.1,  y: -2.2, z: 1.4,  color: 0x06B6D4, size: 0.50 },
        { name: 'QA & CI',   x: -3.3, y: -1.9, z: -1.0, color: 0x06B6D4, size: 0.46 },
        { name: 'Telemetry', x: 0.1,  y: 3.3,  z: 0.4,  color: 0x3B82F6, size: 0.44 },
        { name: 'Billing',   x: -0.2, y: -3.2, z: -0.4, color: 0x0B1020, size: 0.44 }
    ];

    const spheres = [];
    const sphereGeo = new THREE.SphereGeometry(1, 32, 32);

    nodeCoords.forEach(item => {
        const mat = new THREE.MeshStandardMaterial({
            color: item.color,
            roughness: 0.28,
            metalness: 0.15
        });
        const mesh = new THREE.Mesh(sphereGeo, mat);
        mesh.scale.setScalar(item.size);
        mesh.position.set(item.x, item.y, item.z);
        networkGroup.add(mesh);
        spheres.push({ mesh, originalY: item.y });
    });

    // Crisp slate lines connecting microservices
    const lineMat = new THREE.LineBasicMaterial({
        color: 0x94A3B8,
        transparent: true,
        opacity: 0.55
    });

    const connections = [
        [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6],
        [1, 4], [2, 3], [2, 5], [3, 6], [1, 5]
    ];

    connections.forEach(([i, j]) => {
        const points = [
            new THREE.Vector3(nodeCoords[i].x, nodeCoords[i].y, nodeCoords[i].z),
            new THREE.Vector3(nodeCoords[j].x, nodeCoords[j].y, nodeCoords[j].z)
        ];
        const lineGeo = new THREE.BufferGeometry().setFromPoints(points);
        const line = new THREE.Line(lineGeo, lineMat);
        networkGroup.add(line);
    });

    let targetRotationX = 0;
    let targetRotationY = 0;

    container.addEventListener('mousemove', (e) => {
        const rect = container.getBoundingClientRect();
        const mouseX = ((e.clientX - rect.left) / (rect.width || width) - 0.5) * 2;
        const mouseY = ((e.clientY - rect.top) / (rect.height || height) - 0.5) * 2;
        targetRotationY = mouseX * 0.45;
        targetRotationX = mouseY * 0.30;
    });

    const clock = new THREE.Clock();
    function animate() {
        requestAnimationFrame(animate);
        const elapsedTime = clock.getElapsedTime();

        networkGroup.rotation.y += (targetRotationY - networkGroup.rotation.y) * 0.05 + 0.002;
        networkGroup.rotation.x += (targetRotationX - networkGroup.rotation.x) * 0.05;
        ringMesh.rotation.z = elapsedTime * 0.15;

        spheres.forEach((s, idx) => {
            s.mesh.position.y = s.originalY + Math.sin(elapsedTime * 1.4 + idx) * 0.07;
        });

        renderer.render(scene, camera);
    }
    animate();

    window.addEventListener('resize', () => {
        if (!container) return;
        const newW = container.clientWidth;
        const newH = container.clientHeight;
        if (newW > 0 && newH > 0) {
            camera.aspect = newW / newH;
            camera.updateProjectionMatrix();
            renderer.setSize(newW, newH);
        }
    });
};
