#!/usr/bin/env sh
set -eu
kubectl delete namespace idp-dev --ignore-not-found
