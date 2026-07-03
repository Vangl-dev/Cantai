#!/bin/bash
cd "$(dirname "$0")/cantai"
source .venv/bin/activate
python -m cantai preview
