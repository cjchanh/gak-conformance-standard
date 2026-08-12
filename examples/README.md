# Adapter skeleton

Copy `adapter_skeleton.py`. Point `--adapter` at your `module:Class`.

The skeleton **raises**. A score of the untouched file is FAIL, not a mark.

See spec §6 for the contract. See the repository README Journey B.

`--out receipt.json` writes a §5.1 receipt. `--out certification.json --certify` writes a §5.2 certification. `digest --receipt` refuses a certification. `verify --cert` refuses a receipt.
