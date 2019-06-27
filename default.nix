let
  inherit (import <nixpkgs> {}) fetchFromGitHub;
  nixpkgs = (import (fetchFromGitHub {
    owner = "NixOS";
    repo = "nixpkgs-channels";
    rev = "f52505fac8c82716872a616c501ad9eff188f97f"; # version: 19.03
    sha256 = "0q2m2qhyga9yq29yz90ywgjbn9hdahs7i8wwlq7b55rdbyiwa5dy";
  })) {};

  overrides = self: super: {
        hypothesis = super.hypothesis.overridePythonAttrs { doCheck=false; };
  };
  pypkgs = nixpkgs.python37Packages.override { inherit overrides; };
  nbval = pypkgs.buildPythonPackage rec {
    name = "nbval-0.9.0";
    src = nixpkgs.fetchurl {
      url = "https://pypi.python.org/packages/58/ce/d705c865bdec10ab94c1c57b76e77f07241ef5c11c4976ec7e00de259f92/nbval-0.9.0.tar.gz";
      sha256 = "dec2a26bb32a29f92a577554b7142f960b8a91bca8cfaf23f4238718197bf7f3";
    };
    doCheck=false;
    buildInputs = [
      pypkgs.ipython
      pypkgs.jupyter_client
      pypkgs.tornado
      pypkgs.nbformat
      pypkgs.ipykernel
      pypkgs.coverage
      pypkgs.pytest
    ];
  };
in
  pypkgs.buildPythonPackage rec {
    pname = "pidgin";
    version = "dev";
    env = nixpkgs.buildEnv { name=pname; paths=nativeBuildInputs; };
    nativeBuildInputs = [
      nbval
      pypkgs.notebook
      pypkgs.setuptools
      pypkgs.ipywidgets
      pypkgs.pytest
      pypkgs.jsonschema
      pypkgs.hypothesis
      pypkgs.jupyter
      pypkgs.jupyter_client
      pypkgs.ipython
      pypkgs.pip
      pypkgs.matplotlib
      pypkgs.tkinter
      nixpkgs.pkgs.pandoc
      pypkgs.sympy
      (pypkgs.pandas.overridePythonAttrs { doCheck=false; })
      nixpkgs.pkgs.graphviz
      pypkgs.graphviz
    ];
    propagatedBuildInputs=nativeBuildInputs;
    src=builtins.filterSource (path: type: type != "directory" || baseNameOf path != ".git") ./.;
    preShellHook = ''
      jupyter nbextension install --py widgetsnbextension --user
      jupyter nbextension enable widgetsnbextension --user --py

      SOURCE_DATE_EPOCH=$(date +%s)
      export PYTHONUSERBASE=$PWD/.local
      export USER_SITE=`python -c "import site; print(site.USER_SITE)"`
      export PYTHONPATH=$PYTHONPATH:$USER_SITE
      export PATH=$PATH:$PYTHONUSERBASE/bin

    '';
  }
