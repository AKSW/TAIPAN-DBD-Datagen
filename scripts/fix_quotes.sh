grep '".*".*"' ./triples_fixed/* | wc -l
sed -E 's#(".*)"(.*")#\1\\"\2#' ./triples_fixed/0066d295-02e0-45f5-a8b3-40073b975e91.nt
