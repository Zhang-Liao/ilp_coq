dune build
find data/ -name "*.sexpr" | xargs -i  _build/default/bin/main.exe -file {}
