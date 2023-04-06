#!/bin/bash

# Fine-grained personal access token
# Expiraton day: 2024.03.31

NAME=jarmuiranyitas_2
TOKEN=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
REPO=https://oauth2:$TOKEN@github.com/istvan-knab/$NAME.git

[ -d $NAME ] || git clone $REPO
git -C $NAME pull

##create virtual env and install python packages
#cd $NAME
#[ -d venv ] || python3.10 -m venv venv
#source venv/bin/activate
#
#pip3 install --upgrade pip wheel --no-cache-dir
#pip3 install --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 --no-cache-dir
#pip3 install --upgrade scipy --no-cache-dir

#deactivate
