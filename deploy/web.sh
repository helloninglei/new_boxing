#!/bin/bash

cd /work/$1 && yarn --registry https://registry.npm.taobao.org && yarn run build && cd /work && chmod +x *_h5
