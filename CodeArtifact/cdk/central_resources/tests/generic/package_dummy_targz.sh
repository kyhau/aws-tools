#!/bin/bash
set -e

echo "CheckPt: Building ${PKG_NAME}"

cat <<EOT > app.sh
echo "dummy-app-1.0.0"
EOT

tar -czf ${PKG_NAME}.tar.gz app.sh

rm app.sh
