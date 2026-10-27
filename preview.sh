#!/bin/bash
# Abre o site localmente em http://localhost:8000
cd "$(dirname "$0")"
PYTHONPATH=src python3 -m cantai.cli preview
