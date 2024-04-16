{
  description = "Description for the project";

  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    systems.url = "github:nix-systems/default";
  };
  outputs = inputs @ {flake-parts, ...}:
    flake-parts.lib.mkFlake {inherit inputs;} {
      systems = import inputs.systems;
      perSystem = {
        config,
        self',
        inputs',
        pkgs,
        system,
        ...
      }: {
        devShells.default = let
          # https://nixos.wiki/wiki/Python#micromamba
          fhs = pkgs.buildFHSUserEnv {
            name = "compas_mrr-dev";

            targetPkgs = _: [
              pkgs.micromamba
              pkgs.act
            ];

            profile = ''
              set -e
              eval "$(micromamba shell hook --shell=posix)"
              export MAMBA_ROOT_PREFIX=${builtins.getEnv "PWD"}/.mamba
              micromamba create -f environment.yml -y
              micromamba activate compas_mrr-dev
              pip install -e .
              set +e
            '';
          };
        in
          fhs.env;

        formatter = pkgs.alejandra;
      };
    };
}
