/* Badge "RS 3" in 3D (three.js r147): lettere cromate + blocco rosso, riflessi da ambiente studio.
   Si inclina col mouse, gira con lo scroll ed entra in scena quando diventa visibile. */
(() => {
  const host = document.getElementById('badge3d');
  if (!host || !window.THREE || !window.RS_FONT) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
  } catch (e) {
    host.classList.add('no-webgl');
    return;
  }
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 2));
  renderer.outputEncoding = THREE.sRGBEncoding;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;
  host.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new THREE.RoomEnvironment(), 0.04).texture;

  const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 100);
  camera.position.set(0, 0.2, 9.5);

  // luci: chiave bianca + rim verde + rim rossa
  const key = new THREE.DirectionalLight(0xffffff, 1.6); key.position.set(3, 4, 6); scene.add(key);
  const rimG = new THREE.PointLight(0x8fe31a, 30, 20); rimG.position.set(-4, 1.5, -2); scene.add(rimG);
  const rimR = new THREE.PointLight(0xff3040, 18, 20); rimR.position.set(4, -1.5, -2); scene.add(rimR);

  const font = new THREE.FontLoader().parse(window.RS_FONT);
  const chrome = new THREE.MeshStandardMaterial({ color: 0xf5f5f5, metalness: 1, roughness: 0.1, envMapIntensity: 1.35 });
  const chromeDark = new THREE.MeshStandardMaterial({ color: 0x040504, metalness: 0.75, roughness: 0.38, envMapIntensity: 0.35 });
  const red = new THREE.MeshStandardMaterial({ color: 0xc40018, metalness: 0.35, roughness: 0.32, envMapIntensity: 0.22, emissive: 0x220004 });

  // three r147: i colori esadecimali sono sRGB, il renderer lavora in lineare
  [chrome, chromeDark, red].forEach((m) => { m.color.convertSRGBToLinear(); m.emissive.convertSRGBToLinear(); });

  const italic = new THREE.Matrix4().makeShear(0, 0, 0.22, 0, 0, 0); // x += 0.22 * y

  const text = (str, size) => {
    const g = new THREE.TextGeometry(str, {
      font, size, height: 0.34, curveSegments: 10,
      bevelEnabled: true, bevelThickness: 0.05, bevelSize: 0.035, bevelSegments: 5,
    });
    g.applyMatrix4(italic);
    g.computeBoundingBox();
    return g;
  };

  const badge = new THREE.Group();

  // blocco rosso inclinato dietro alla "R"
  const rs = text('RS', 1.55);
  const rsW = rs.boundingBox.max.x - rs.boundingBox.min.x;
  const h = 1.55;
  const sk = 0.22 * (h + 0.5);
  const plate = new THREE.Shape();
  const pw = rsW * 0.52, px = -0.28, py = -0.25;
  plate.moveTo(px, py);
  plate.lineTo(px + pw, py);
  plate.lineTo(px + pw + sk, py + h + 0.5);
  plate.lineTo(px + sk, py + h + 0.5);
  plate.closePath();
  const plateGeo = new THREE.ExtrudeGeometry(plate, { depth: 0.22, bevelEnabled: true, bevelThickness: 0.05, bevelSize: 0.05, bevelSegments: 4 });
  const plateMesh = new THREE.Mesh(plateGeo, red);
  plateMesh.position.z = -0.12;

  const rsMesh = new THREE.Mesh(rs, chrome);
  rsMesh.position.z = 0.08;

  const three = text('3', 1.55);
  const threeMesh = new THREE.Mesh(three, chrome);
  threeMesh.position.set(rsW + 0.55, 0, 0.08);

  // cornice scura dietro a tutto (effetto badge)
  const totalW = rsW + 0.55 + (three.boundingBox.max.x - three.boundingBox.min.x);
  const back = new THREE.Shape();
  const bx = -0.6, by = -0.55, bw = totalW + 1.2 + sk, bh = h + 1.1, r = 0.35;
  back.moveTo(bx + r, by);
  back.lineTo(bx + bw - r, by); back.quadraticCurveTo(bx + bw, by, bx + bw, by + r);
  back.lineTo(bx + bw, by + bh - r); back.quadraticCurveTo(bx + bw, by + bh, bx + bw - r, by + bh);
  back.lineTo(bx + r, by + bh); back.quadraticCurveTo(bx, by + bh, bx, by + bh - r);
  back.lineTo(bx, by + r); back.quadraticCurveTo(bx, by, bx + r, by);
  const backMesh = new THREE.Mesh(
    new THREE.ExtrudeGeometry(back, { depth: 0.18, bevelEnabled: true, bevelThickness: 0.06, bevelSize: 0.06, bevelSegments: 5 }),
    chromeDark,
  );
  backMesh.position.z = -0.45;

  badge.add(backMesh, plateMesh, rsMesh, threeMesh);
  // centra il gruppo
  const box = new THREE.Box3().setFromObject(badge);
  const c = box.getCenter(new THREE.Vector3());
  badge.children.forEach((m) => m.position.sub(new THREE.Vector3(c.x, c.y, 0)));
  const badgeW = box.max.x - box.min.x;
  const pivot = new THREE.Group();
  pivot.add(badge);
  scene.add(pivot);

  // ombra morbida a terra
  const sh = document.createElement('canvas'); sh.width = sh.height = 128;
  const sctx = sh.getContext('2d');
  const grd = sctx.createRadialGradient(64, 64, 0, 64, 64, 64);
  grd.addColorStop(0, 'rgba(143,227,26,.55)'); grd.addColorStop(1, 'rgba(143,227,26,0)');
  sctx.fillStyle = grd; sctx.fillRect(0, 0, 128, 128);
  const shadow = new THREE.Mesh(
    new THREE.PlaneGeometry(9, 2.2),
    new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(sh), transparent: true, depthWrite: false }),
  );
  shadow.rotation.x = -Math.PI / 2;
  shadow.position.y = -1.9;
  scene.add(shadow);

  // dimensioni
  const fit = () => {
    const w = host.clientWidth, hh = host.clientHeight;
    renderer.setSize(w, hh);
    camera.aspect = w / hh;
    // allontana la camera sugli schermi stretti per far stare tutto il badge
    const need = (badgeW * 1.18) / (2 * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)) * camera.aspect);
    camera.position.z = Math.max(9.5, need);
    camera.updateProjectionMatrix();
  };
  fit();
  addEventListener('resize', fit);

  // interazione
  let mx = 0, my = 0, tx = 0, ty = 0, intro = 0, visible = false, t0 = 0;
  host.addEventListener('pointermove', (e) => {
    const r = host.getBoundingClientRect();
    mx = ((e.clientX - r.left) / r.width - 0.5) * 2;
    my = ((e.clientY - r.top) / r.height - 0.5) * 2;
  });
  host.addEventListener('pointerleave', () => { mx = 0; my = 0; });
  new IntersectionObserver(([e]) => {
    visible = e.isIntersecting;
    if (visible && !t0) t0 = performance.now();
  }, { threshold: 0.2 }).observe(host);

  const clock = new THREE.Clock();
  const loop = () => {
    requestAnimationFrame(loop);
    if (!visible) return;
    const t = clock.getElapsedTime();
    // ingresso: da girato di spalle e piccolo a frontale
    intro = reduced ? 1 : Math.min((performance.now() - t0) / 1600, 1);
    const ease = 1 - Math.pow(1 - intro, 4);
    // scroll: rotazione leggera mentre la sezione attraversa lo schermo
    const r = host.getBoundingClientRect();
    const sp = (r.top + r.height / 2 - innerHeight / 2) / innerHeight; // -1..1
    tx += (mx - tx) * 0.06; ty += (my - ty) * 0.06;
    pivot.rotation.y = (1 - ease) * Math.PI * 1.2 + tx * 0.45 + sp * 0.5 + (reduced ? 0 : Math.sin(t * 0.6) * 0.08);
    pivot.rotation.x = ty * 0.25 + (reduced ? 0 : Math.sin(t * 0.8) * 0.03);
    pivot.position.y = reduced ? 0 : Math.sin(t * 1.1) * 0.08;
    pivot.scale.setScalar(0.6 + 0.4 * ease);
    shadow.material.opacity = 0.6 + Math.sin(t * 1.1) * 0.15;
    rimG.position.x = -4 + Math.sin(t * 0.7) * 2;
    renderer.render(scene, camera);
  };
  loop();
})();
