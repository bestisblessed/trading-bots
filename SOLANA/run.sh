#!/bin/bash
rm -rf data && mkdir data
node inspect_wallet.js
node inspect_token_details_advanced.js
