# Attention! Attention!

[![Built with Nix](https://builtwithnix.org/badge.svg)](https://builtwithnix.org)
[![Docker Image Build Status](https://github-actions.40ants.com/starcraft66/attention-attention/matrix.svg)](https://github.com/starcraft66/attention-attention)

`attention-attention` is a friendly discord bot to remind you over discord that school is closing soon, wheverver you are, even outside of school! Just be in voice chat at the right time and you'll hear the intercom!

## Development instructions

1. Install [Nix](https://nixos.org/download.html) on your system and enable flake support.
2. If you have `direnv` installed and set up, run `direnv allow`. Otherwise, enter the `devShell` using `nix develop`.
3. Hack away!
4. Run the program using `python -m attention_attention`.
5. Build the python package using `nix build .#`.

## Docker image instructions

1. Install [Nix](https://nixos.org/download.html) on your system and enable flake support.
2. Build the docker image using `nix build .#dockerImage.<system>` where `<system>` is your target system like `x86_64-linux` or `aarch64-linux`.
3. Load the docker image into your local registry with `docker load < result`.
4. Tag/push/run the image like you normally would using the docker cli!

## Runtime requirements

The only thing this bot needs to run is a discord bot token stored in the `DISCORD_TOKEN` environment variable.
