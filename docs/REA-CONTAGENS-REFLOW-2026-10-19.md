# Contagens de grupos de reflow —19/10/2026

Mesmo original fixado,perfil Ghidra12.1.4/JDK21/REAseeds e conferência Capstone
dos lotes anteriores de hoje. Duas entradas novas,total4instruções/10bytes.
0x15cb840 retorna1;0x15cbb90 retorna o campo+0x78(N). No caminho direto examinado
de0x15cd860,as contagens A/B do relatório anterior tornam-se A=1 e B=N.
Assim os arrays são3c:4Nbytes,40:4bytes,44:4(N+1)bytes,além dos mapas48/4c:4Nbytes.
Isso delimita um grupo em um eixo e N posições no outro;orientação visual,
unidades e nomes finais de eixos ainda não foram demonstrados neste recorte.

Seis entradas inéditas examinadas hoje,266instruções/803bytes. Catálogo329entradas
(152REA+177diretas exclusivas). Não são seis funcionalidades completas nem
prova do domínio de todos os índices,ownership,exceções ou concorrência.
O conteúdo completo dos projetos e pseudocódigo continua fora do Git.

[Metadados](windows-evidence/foxit-rea/headless-cross-checks-static-reflow-counts-2026-10-19.json),
[sementes](windows-evidence/foxit-rea/static-reflow-counts-2026-10-19-seeds.tsv),
[conferência](../testes/resultados/static-reflow-counts-2026-10-19/machine-checks.json).
Raw/projeto:analysis-local/headless/static-reflow-counts-2026-10-19/.
Não houve execução do original ou comando à VM.
