/**
 * WareSoft DevNexus 3D Architecture Visualizer
 * Built on Three.js - Precision node topology showing interconnected microservices
 * Deliberate, lightweight, hardware-accelerated, zero-slop visuals
 */

window.initDevNexus3D = function(containerId) {
    const container = document.getElementById(containerId);
    if (!container || typeof THREE === 'undefined') return;

    // Clear previous canvas if any
    container.innerHTML = '';

    const width = container.clientWidth || 600;
    const height = container.clientHeight || 400;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.set(0, 0, 18);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Group for nodes and connectivity lines
    const networkGroup = new THREE.Group();
    scene.add(networkGroup);

    // Node definitions (Core Service Architecture Nodes)
    const nodeCoords = [
        { name: 'Gateway', x: 0, y: 0, z: 0, color: 0x3B82F6, size: 0.7 },
        { name: 'Auth', x: -4, y: 2, z: 1, color: 0x06B6D4, size: 0.5 },
        { name: 'Projects', x: 4, y: 2, z: -1, color: 0x3B82F6, size: 0.55 },
        { name: 'Kanban', x: 3, y: -2.5, z: 1.5, color: 0x06B6D4, size: 0.5 },
        { name: 'QA & CI', x: -3.5, y: -2, z: -1, color: 0x10B981, size: 0.45 },
        { name: 'Telemetry', x: 0, y: 3.5, z: 0.5, color: 0x06B6D4, size: 0.4 },
        { name: 'Billing', x: 0, y: -3.5, z: -0.5, color: 0x3B82F6, size: 0.4 }
    ];

    const spheres = [];
    const sphereGeo = new THREE.SphereGeometry(1, 24, 24);

    nodeCoords.forEach(item => {
        const mat = new THREE.MeshBasicMaterial({
            color: item.color,
            wireframe: false
        });
        const mesh = new THREE.Mesh(sphereGeo, mat);
        mesh.scale.setScalar(item.size);
        mesh.position.set(item.x, item.y, item.z);
        networkGroup.add(mesh);
        spheres.push({ mesh, originalY: item.y });
    });

    // Connecting Lines (Service Bus Topology)
    const lineMat = new THREE.LineBasicMaterial({
        color: 0x334155,
        transparent: true,
        opacity: 0.6
    });

    const connections = [
        [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6],
        [1, 4], [2, 3], [2, 5], [3, 6]
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

    // Gentle orbit interaction
    let mouseX = 0;
    let mouseY = 0;
    let targetRotationX = 0;
    let targetRotationY = 0;

    container.addEventListener('mousemove', (e) => {
        const rect = container.getBoundingClientRect();
        mouseX = ((e.clientX - rect.left) / width - 0.5) * 2;
        mouseY = ((e.clientY - rect.top) / height - 0.5) * 2;
        targetRotationY = mouseX * 0.4;
        targetRotationX = mouseY * 0.3;
    });

    // Animation Loop
    let clock = new THREE.Clock();
    function animate() {
        requestAnimationFrame(animate);
        const elapsedTime = clock.getElapsedTime();

        // Subtle gentle continuous drift + mouse orbit response
        networkGroup.rotation.y += (targetRotationY - networkGroup.rotation.y) * 0.05 + 0.002;
        networkGroup.rotation.x += (targetRotationX - networkGroup.rotation.x) * 0.05;

        // Micro pulsation on nodes
        spheres.forEach((s, idx) => {
            s.mesh.position.y = s.originalY + Math.sin(elapsedTime * 1.5 + idx) * 0.08;
        });

        renderer.render(scene, camera);
    }
    animate();

    // Resize Handler
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
