#!/usr/bin/env bash
set -eou pipefail
set -x
sudo rsync aliases.sh /etc/profile.d
