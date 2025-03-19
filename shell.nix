{
  pkgs ? import <nixpkgs> { },
}:
pkgs.mkShell {
  buildInputs = with pkgs; [
    pkgs.pkg-config
    pkgs.python312Packages.pygame
    pkgs.bashInteractive
  ];
  

  "terminal.integrated.defaultProfile.linux" = "null";
  "terminal.integrated.shell.linux" = "/run/current-system/sw/bin/bash";
}
