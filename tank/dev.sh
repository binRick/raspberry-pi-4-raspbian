#!/usr/bin/env bash
set -eou pipefail
cleanup(){
	reset
}
#trap cleanup EXIT
nodemon -I -w . -e py,sh -x ./run.sh 
