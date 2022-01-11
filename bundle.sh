#!/bin/bash
pyinstaller --onefile main.py
pyinstaller --onefile cliAssistant.py
exportDirectory="export/"`date +"%Y%m%d_%H%M%S"`
configDirectory="$exportDirectory/config"
mkdir -p $exportDirectory
cp -r dist/main.exe $exportDirectory
cp dist/cliAssistant.exe $exportDirectory
mkdir -p $configDirectory
cp config/config.json.example "$configDirectory/config.json"
