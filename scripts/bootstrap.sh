#!/usr/bin/env sh
set -eu
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
kubectl create namespace idp-dev --dry-run=client -o yaml | kubectl apply -f -
