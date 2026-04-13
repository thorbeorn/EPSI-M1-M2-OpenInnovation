const canvas = document.getElementById('network');
const ctx = canvas.getContext('2d');

function resize() {
  canvas.width = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;
}
resize();
window.addEventListener('resize', resize);

const GREEN = '#1aff6e';
const nodes = [];
const COUNT = 55;

for (let i = 0; i < COUNT; i++) {
  nodes.push({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    vx: (Math.random() - 0.5) * 0.35,
    vy: (Math.random() - 0.5) * 0.35,
    r: Math.random() * 2 + 1,
    pulse: Math.random() * Math.PI * 2,
  });
}

[0, 7, 14, 21, 28].forEach(i => { nodes[i].home = true; nodes[i].r = 4; });

let mouse = { x: -999, y: -999 };
canvas.addEventListener('mousemove', e => {
  const r = canvas.getBoundingClientRect();
  mouse.x = e.clientX - r.left;
  mouse.y = e.clientY - r.top;
});

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  nodes.forEach(n => {
    n.x += n.vx;
    n.y += n.vy;
    n.pulse += 0.02;
    if (n.x < 0 || n.x > canvas.width)  n.vx *= -1;
    if (n.y < 0 || n.y > canvas.height) n.vy *= -1;
  });

  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const a = nodes[i], b = nodes[j];
      const dx = a.x - b.x, dy = a.y - b.y;
      const dist = Math.sqrt(dx*dx + dy*dy);
      if (dist < 130) {
        const alpha = (1 - dist / 130) * 0.35;
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.strokeStyle = `rgba(26,255,110,${alpha})`;
        ctx.lineWidth = (a.home || b.home) ? 0.8 : 0.4;
        ctx.stroke();
      }
    }
  }

  nodes.forEach(n => {
    const pulse = n.home ? Math.sin(n.pulse) * 0.4 + 0.8 : 1;
    const r = n.r * pulse;

    if (n.home) {
      ctx.beginPath();
      ctx.arc(n.x, n.y, r + 6, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(26,255,110,${0.04 * pulse})`;
      ctx.fill();
    }

    ctx.beginPath();
    ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
    ctx.fillStyle = n.home
      ? `rgba(26,255,110,${0.9 * pulse})`
      : `rgba(26,255,110,0.55)`;
    ctx.fill();
  });

  nodes.forEach(n => {
    const dx = n.x - mouse.x, dy = n.y - mouse.y;
    const dist = Math.sqrt(dx*dx + dy*dy);
    if (dist < 100) {
      ctx.beginPath();
      ctx.moveTo(n.x, n.y);
      ctx.lineTo(mouse.x, mouse.y);
      ctx.strokeStyle = `rgba(26,255,110,${(1 - dist/100) * 0.4})`;
      ctx.lineWidth = 0.6;
      ctx.stroke();
    }
  });

  requestAnimationFrame(draw);
}
draw();

const observer = new IntersectionObserver(entries => {
  entries.forEach((e, i) => {
    if (e.isIntersecting) {
      setTimeout(() => e.target.classList.add('visible'), i * 80);
      observer.unobserve(e.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));