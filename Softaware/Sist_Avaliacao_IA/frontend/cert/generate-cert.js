const fs = require("fs");
const path = require("path");
const selfsigned = require("selfsigned");

const attrs = [{ name: "commonName", value: "localhost" }];
const pems = selfsigned.generate(attrs, {
  days: 365,
  keySize: 2048,
  algorithm: "sha256",
});

const certDir = path.resolve(__dirname);
fs.writeFileSync(path.join(certDir, "cert.pem"), pems.cert);
fs.writeFileSync(path.join(certDir, "key.pem"), pems.private);

console.log("✅ Certificados HTTPS gerados com sucesso em ./cert");