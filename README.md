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

## Commands

This bot implements a few interactions (a.k.a. "slash commands"):
|Command|Description|
|-|-|
|`/attention`|Prints an "Attention! Attention!" message|
|`/about`|Prints the bot version and invite link|
|`/sync`|Performs a full command tree sync -- This command is only available to the bot owner in the administrative guild|

## Runtime requirements

There are a few environment variables that can control the runtime behaviour of the bot:

|Environment Variable|Description|
|-|-|
|`DISCORD_TOKEN`|The discord bot token to log in with|
|`LIBOPUS_PATH`|The path to the libopus library if it cannot be determined automatically by python|
|`DISCORD_COMMAND_SYNC`|Set this to any value to perform a full command tree sync on launch. This is required to perform the initial command tree sync when bootstrapping the bot. Once this is done, the `/sync` command in the administrative guid can be used for subsequent command tree syncs.|
