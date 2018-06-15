#!/bin/bash

cd /work/$1 && npm install --registry https://registry.npm.taobao.org $$ npm run build
