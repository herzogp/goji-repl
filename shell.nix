let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    pkgs.python3
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.pytest
      python-pkgs.requests
      python-pkgs.mypy
    ]))
  ];
}
