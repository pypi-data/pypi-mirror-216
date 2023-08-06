#!/usr/bin/bash

echo "Compilling index.js for Radiant-Framework"
cat index.js
npx rollup -p @rollup/plugin-node-resolve index.js > material-$(npm view @material/web version).js
echo "Compiled as material-$(npm view @material/web version).js"
sed -i '/^import '\''@material\/web\// s/^/\/\//' material-$(npm view @material/web version).js
