#!/usr/bin/bash

echo "Compilling index.js for Radiant-Framework"
cat index_git.js
npx rollup -p @rollup/plugin-node-resolve index_git.js > material-git.js
echo "Compiled as material-git.js"
sed -i '/^import '\''@material\/web\// s/^/\/\//' material-git.js
