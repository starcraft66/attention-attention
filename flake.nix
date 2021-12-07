{
  description = "attention-attention reference Nix architecture";

  # inputs.nixpkgs.url = "github:NixOS/nixpkgs";
  inputs.nixpkgs.url = "github:starcraft66/nixpkgs/attention-attention";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
      in
      rec {
        apps = {
          attention-attention = packages.attention-attention;
        };

        devShell = let
            customPython = pkgs.python38.withPackages (ps: with pkgs.python38.pkgs; [ discordpy aiocron tzlocal ]);
          in pkgs.mkShell {
          buildInputs = with pkgs; [
            customPython
          ];
        };

        packages.attention-attention = pkgs.python38Packages.buildPythonPackage rec {
          pname = "attention-attention";
          version = "v1.0.0";

          src = ./.;

          propagatedBuildInputs = with pkgs.python38.pkgs; [
            discordpy
            aiocron
          ];

          doCheck = false;
          pythonImportsCheck = [ "attention-attention" ];

          meta = with pkgs.lib; {
            description = "A friendly discord reminder that school's about to close!";
            homepage = "https://github.com/starcraft66/attention-attention/";
            license = licenses.mit;
            maintainers = [ maintainers.starcraft66 ];
          };
        };

        dockerImage = let
            customPython = pkgs.python38.withPackages (ps: [ packages.attention-attention ]);
          in pkgs.dockerTools.buildImage {
          name = "attention-attention";
          tag = packages.attention-attention.version;
          contents = with pkgs; [
            bashInteractive
            busybox
            tzdata
          ];
          config = {
            Env = [
              "TZ=America/Toronto"
              "SSL_CERT_FILE=${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
            ];
            Cmd = [ "${customPython}/bin/python" "-m" "attention-attention" ];
          };
        };

        defaultPackage = packages.attention-attention;
        defaultApp = apps.attention-attention;
      }
    );
}
