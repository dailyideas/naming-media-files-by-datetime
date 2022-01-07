#!/bin/bash
pyinstaller main.py
pyinstaller --onefile cliAssistant.py
exportPath="export/"`date +"%Y%m%d_%H%M%S"`
mkdir -p $exportPath
cp -r dist/main/* $exportPath
cp dist/cliAssistant.exe $exportPath
cp -r config/ $exportPath
