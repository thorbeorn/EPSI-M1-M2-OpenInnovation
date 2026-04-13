const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;
const PUBLIC_DIR = path.join(__dirname, 'public');

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css':  'text/css; charset=utf-8',
  '.js':   'application/javascript; charset=utf-8',
  '.ico':  'image/x-icon',
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.svg':  'image/svg+xml',
  '.woff2':'font/woff2',
  '.woff': 'font/woff',
};

const server = http.createServer((req, res) => {
  // Normalise l'URL : "/" → "/index.html"
  let urlPath = req.url.split('?')[0];
  if (urlPath === '/') urlPath = '/index.html';

  const filePath = path.join(PUBLIC_DIR, urlPath);

  // Sécurité : empêche le path traversal (ex: ../../etc/passwd)
  if (!filePath.startsWith(PUBLIC_DIR)) {
    res.writeHead(403);
    return res.end('Forbidden');
  }

  fs.readFile(filePath, (err, data) => {
    if (err) {
      if (err.code === 'ENOENT') {
        // 404 — sert index.html en fallback (utile pour les SPA)
        fs.readFile(path.join(PUBLIC_DIR, 'index.html'), (e, html) => {
          if (e) { res.writeHead(500); return res.end('Server error'); }
          res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
          res.end(html);
        });
      } else {
        res.writeHead(500);
        res.end('Server error');
      }
      return;
    }

    const ext = path.extname(filePath);
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    res.writeHead(200, {
      'Content-Type': contentType,
      'Cache-Control': ext === '.html' ? 'no-cache' : 'public, max-age=86400',
    });
    res.end(data);
  });
});

server.listen(PORT, () => {
  console.log(`\n  🟢 MyNodeHost vitrine`);
  console.log(`  → http://localhost:${PORT}\n`);
});