{
  description = "attention-attention reference Nix architecture";

  inputs.nixpkgs.url = "github:nixos/nixpkgs";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
      in
      rec {
        apps = {
          attention-attention = {
            type = "app";
            program =
              let
                customPython = pkgs.python314.withPackages (ps: [ self.packages.${system}.attention-attention ]);
                wrapper = pkgs.writeScriptBin "attention-attention" ''
                  ${customPython}/bin/python3 -m attention_attention $@
                '';
              in
              "${wrapper}/bin/attention-attention";
          };
        };

        devShell =
          let
            customPython = pkgs.python314.withPackages (
              ps: with pkgs.python314.pkgs; [
                discordpy
                aiocron
                tzlocal
              ]
            );
          in
          pkgs.mkShell {
            buildInputs = with pkgs; [
              customPython
            ];
          };

        packages.attention-attention = pkgs.python314Packages.buildPythonPackage rec {
          pname = "attention-attention";
          version = "v1.0.2";

          src = ./.;

          pyproject = true;
          build-system = [ pkgs.python314Packages.setuptools ];

          propagatedBuildInputs = with pkgs.python314.pkgs; [
            discordpy
            aiocron
          ];

          doCheck = false;
          pythonImportsCheck = [ "attention_attention" ];

          meta = with pkgs.lib; {
            description = "A friendly discord reminder that school's about to close!";
            homepage = "https://github.com/starcraft66/attention-attention/";
            license = licenses.gpl3Plus;
            maintainers = [ maintainers.starcraft66 ];
          };
        };

        dockerImage =
          let
            customPython = pkgs.python314.withPackages (ps: [ packages.attention-attention ]);
          in
          pkgs.dockerTools.buildImage {
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
              Cmd = [
                "${customPython}/bin/python"
                "-m"
                "attention_attention"
              ];
            };
          };

        defaultPackage = packages.attention-attention;
        defaultApp = apps.attention-attention;
      }
    );
}
