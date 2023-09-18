#!/usr/bin/env bash
set -eou pipefail
sudo cp ip.service /etc/systemd/system/.
sudo systemctl enable --now ip.service
