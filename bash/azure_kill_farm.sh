#!/usr/bin/env bash

# Script to automatically start the Azure renderfarm VMs one by one.

echo "Shutting down the whole farm."
azure vm shutdown Render01
azure vm shutdown RenderClient01
azure vm shutdown RenderClient02
azure vm shutdown RenderClient03
azure vm shutdown RenderClient04
