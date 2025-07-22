// scripts/generate-cert.js
const selfsigned = require('selfsigned');
const fs = require('fs');
const path = require('path');

const attrs = [{ name: 'commonName', value: 'localhost' }];
const options = {
  keySize: 2048,
  days: 365,
  algorithm: 'sha256',
  extensions: [
    {
      name: 'basicConstraints',
      cA: true,
    },
    {
      name: 'subjectAltName',
      altNames: [
        { type: 2, value: 'localhost' },
        { type: 7, ip: '127.0.0.1' },
      ],
    },
  ],
};

const pems = selfsigned.generate(attrs, options);

// Caminho para salvar os certificados
const certDir = path.resolve(__dirname, '../services/auth/cert');
if (!fs.existsSync(certDir)) fs.mkdirSync(certDir, { recursive: true });

fs.writeFileSync(path.join(certDir, 'cert.pem'), pems.cert);
fs.writeFileSync(path.join(certDir, 'key.pem'), pems.private);

console.log('✔ Certificados HTTPS gerados com sucesso em:');
console.log(`  ${path.join(certDir, 'cert.pem')}`);
console.log(`  ${path.join(certDir, 'key.pem')}`);
