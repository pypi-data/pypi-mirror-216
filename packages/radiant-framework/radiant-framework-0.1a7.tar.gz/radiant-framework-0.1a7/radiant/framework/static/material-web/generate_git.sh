#!/usr/bin/bash

npm install
npm install rollup @rollup/plugin-node-resolve
npm run build
rm -f index_git.js
echo "Generating index_git.js"
find * -mindepth 1 -maxdepth 1 -name "*.js" ! -name "*_test.js" -exec sh -c '
    if ! grep -q "harness" "$1"; then
        printf "import '"'"'./%s/%s'"'"';\n" "$(dirname "$1")" "$(basename "$1")" >> index_git.js
    fi
' _ {} \;
cat index_git.js
