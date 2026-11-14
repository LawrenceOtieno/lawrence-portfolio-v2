#!/bin/bash
echo "Building Tailwind..."
npm run build || { echo "Build failed - aborting push."; exit 1; }
git add static/css/output.css
echo "output.css built and staged."