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
            nodejs
            nodePackages."@mermaid-js/mermaid-cli"
            pandoc
            go
            
            # Text processing and search tools
            pdfgrep
            jq
            yq-go
            miller
          ];
          
          shellHook = ''
            echo "🚀 Architecture documentation converter environment loaded!"
            echo "Available commands:"
            echo "  go run ./convert_markdown.go    - Run the Go converter (build with: go build)"
            echo "  go version               - Check Go version"
            echo "  mmdc --version           - Check Mermaid CLI"
            echo "  pdfgrep --version        - Check PDF search"
            echo "  jq --version             - Check JSON processor"
            echo "  yq --version             - Check YAML processor"
            echo "  mlr --version            - Check Miller data processor"
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
