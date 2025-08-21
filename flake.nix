{
  description = "Architecture documentation converter with Python dependencies and Mermaid CLI";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        
        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          markdown
          weasyprint
        ]);
        
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            pythonEnv
            nodejs
            nodePackages."@mermaid-js/mermaid-cli"
          ];
          
          shellHook = ''
            echo "🚀 Architecture documentation converter environment loaded!"
            echo "Available commands:"
            echo "  ./convert_markdown.py    - Run the converter"
            echo "  python3 -m pip list      - Check Python packages"
            echo "  mmdc --version           - Check Mermaid CLI"
            echo ""
          '';
        };
        
        packages.default = pkgs.writeShellScriptBin "architecture-converter" ''
          ${pythonEnv}/bin/python3 ${./convert_architecture.py} "$@"
        '';
        
        apps.default = {
          type = "app";
          program = "${self.packages.${system}.default}/bin/architecture-converter";
        };
      });
}
