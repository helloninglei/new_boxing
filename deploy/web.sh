#!/bin/bash

cd /work/$1 && yarn --registry https://registry.npm.taobao.org && yarn run build && chmod +x *_h5
