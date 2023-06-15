#!/usr/bin/env bash
set -eou pipefail
set -x
sudo rsync -ar ./bin/* /usr/local/bin/.
