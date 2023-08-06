#!/bin/sh

rsync -r --delete --progress _build/html/ monet:www/mrzv.org/software/dionysus2
