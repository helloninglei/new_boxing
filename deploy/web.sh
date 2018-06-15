#!/bin/bash

cd .. && cd $1 && npm install --registry https://registry.npm.taobao.org $$ npm run build
