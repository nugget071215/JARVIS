{
  description = "JARVIS - Linux voice assistant";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
      ];

      forAllSystems = nixpkgs.lib.genAttrs systems;

    in {
      packages = forAllSystems (system:
        let
          pkgs = import nixpkgs {
            inherit system;
          };

          pythonPackages = pkgs.python314.withPackages (ps: with ps; [
            sounddevice
            numpy
            scipy
            requests
            psutil
            pyyaml
            faster-whisper
          ]);

        in {
          default = pkgs.stdenv.mkDerivation {
            pname = "jarvis";
            version = "0.1.0";

            src = ./.;

            nativeBuildInputs = [
              pkgs.makeWrapper
            ];

            buildInputs = [
              pythonPackages
              pkgs.portaudio
              pkgs.ffmpeg
              pkgs.libsndfile
            ];

            installPhase = ''
              mkdir -p $out/bin
              mkdir -p $out/share/jarvis

              cp *.py $out/share/jarvis/

              makeWrapper ${pythonPackages}/bin/python $out/bin/jarvis \
                --add-flags "$out/share/jarvis/speech.py" \
                --prefix LD_LIBRARY_PATH : "${pkgs.lib.makeLibraryPath [
                  pkgs.portaudio
                  pkgs.libsndfile
                ]}"
            '';
          };
        });

      devShells = forAllSystems (system:
        let
          pkgs = import nixpkgs {
            inherit system;
          };

          python = pkgs.python314;

          pythonPackages = python.withPackages (ps: with ps; [
            sounddevice
            numpy
            scipy
            requests
            psutil
            pyyaml
            faster-whisper
          ]);

        in {
          default = pkgs.mkShell {
            packages = [
              pythonPackages

              # Audio
              pkgs.portaudio
              pkgs.ffmpeg
              pkgs.libsndfile

              # Build / discovery tools
              pkgs.pkg-config

              # Linux utilities
              pkgs.pulseaudio
              pkgs.wireplumber

              # Development
              pkgs.git
            ];

            shellHook = ''
              echo "🤖 JARVIS development environment"
              echo "Python: $(python --version)"
              echo

              export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath [
                pkgs.portaudio
                pkgs.libsndfile
              ]}:$LD_LIBRARY_PATH"

              echo "Audio backend: PipeWire / WirePlumber"
              echo "Ready."
            '';
          };
        });
    };
}
