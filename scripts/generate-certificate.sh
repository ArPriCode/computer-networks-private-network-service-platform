#!/bin/bash
set -euo pipefail

PROJECT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SSL_DIR="$PROJECT/ssl"
mkdir -p "$SSL_DIR"

openssl req -x509 -newkey rsa:2048 -sha256 -nodes -days 365 \
  -keyout "$SSL_DIR/teamx-ca.key" \
  -out "$SSL_DIR/teamx-ca.crt" \
  -subj "/O=StackHackers/CN=StackHackers TeamX Root CA"

openssl req -newkey rsa:2048 -nodes \
  -keyout "$SSL_DIR/key.pem" \
  -out "$SSL_DIR/teamx.csr" \
  -subj "/O=StackHackers/CN=app.teamX.test"

cat > "$SSL_DIR/teamx.ext" <<'EOF'
subjectAltName=DNS:app.teamX.test,DNS:api.teamX.test
extendedKeyUsage=serverAuth
keyUsage=digitalSignature,keyEncipherment
EOF

openssl x509 -req -days 365 -sha256 \
  -in "$SSL_DIR/teamx.csr" \
  -CA "$SSL_DIR/teamx-ca.crt" \
  -CAkey "$SSL_DIR/teamx-ca.key" \
  -CAcreateserial \
  -extfile "$SSL_DIR/teamx.ext" \
  -out "$SSL_DIR/cert.pem"

chmod 600 "$SSL_DIR/key.pem" "$SSL_DIR/teamx-ca.key"
echo "Generated TeamX certificate and local CA in $SSL_DIR"
