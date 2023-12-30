#!/bin/bash

echo "Preparing artifact dirs"
mkdir -p build/python
mkdir -p staticbuild
mkdir -p templatesbuild

echo "Installing Python module dependencies"
pip install -r requirements.txt --target build/python

echo "Installing Python module"
pip install --no-dependencies --target build/python .

echo "Compiling SAM template"
PYTHONPATH=build/python python3 bin/compile_sam.py

echo "Building static"
cp -r static{,build/}

echo "Building templates"
cp -r templates{,build/}
