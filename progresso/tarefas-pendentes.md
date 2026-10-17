# Retomada

Preparação do usuário para desbloquear a etapa 10: [Como continuar](../docs/COMO-CONTINUAR.md).

Trabalho atual: [etapa 15](../docs/ETAPA-15.md), backend de anexos planos
implementado com 14 testes portáveis aprovados. Critério amplo `partial`;
integrar listagem/extração à UI em Linux como próximo passo sem VM. IA do Foxit e
recursos generativos foram excluídos pelo usuário: [escopo](../docs/ESCOPO.md).
Portfólios, /Kids, senha não vazia e anexos por anotação ainda não implementados.
Todas as pendências estão em [pendencias-analises.md](pendencias-analises.md)
e `.json`: 21 critérios, 14 etapas. Causas VM/análise/implementação/runtime
separadas; timeouts registrados e causa por tokens ainda não confirmada.
Salvar checkpoint por lote e antes de mudar de etapa, com alvo restante e
publicação. Validar o registro com `python scripts/check_architecture.py`.

Trabalho paralelo autorizado: etapa 11 estática, conforme [relatório](../docs/ETAPA-11.md).
Nove entradas examinadas; catálogo 209. Seguir `0x859920`, `0x687ae0`, `0x5f5370`
e `0x48f10ef`; esclarecer contexto dos IDs 7911/7913. Validar UI01–UI10 na VM.
Os critérios da etapa 11 continuam 25% verificados; condições estáticas não
substituem a observação de disponibilidade/comportamento.

Etapa 12 solicitada em 17/10/2026: [contratos e limites](../docs/ETAPA-12.md).
Foram detalhadas 25 famílias, com 50 cenários planejados; o critério está
`partial`, a fase A segue aberta e os 12,5% verificados não aumentaram.
Especializar as fixtures e transformar os cenários em casos executáveis,
começando pelos subconjuntos de abertura, busca, navegação e prévia.
Conferir o registro derivado com `scripts/validate_functional_spec.py`.
Onze famílias continuam propostas; não adotar requisitos próprios como
comportamento recuperado do Foxit. Comparação diferencial depende da VM.

1. Ler `projeto.json`, `progresso.json`, matriz de paridade e histórico. Conferir Git local/remoto; não reiniciar a análise geral.
2. Retomar os resultados REA/Ghidra e o projeto headless preservado. O main default expirou; usar seeds/perfil dirigido e registrar novos resultados separadamente.
3. Pendência de ambiente: etapa 10. Seguir `docs/ETAPA-10.md` e os 20 cenários de `testes/cenarios-dinamicos.json`. O kit foi gerado e passou em cinco testes de preparação, mas não executou o original. Windows 11 Home local sem Sandbox, WSL não instalado, usuário sem VM. Disponibilizar guest Windows offline descartável ou recuperar a contenção Linux/Wine. No histórico Wine/i386 sob QEMU, cmd.exe passou, mas Foxit encerrou após CInvalidArgException e INT 0x29 antes da UI; preservar contenção e bytes do original.
4. Executar o corpus sintético no original e comparar busca/escopos/ordem/navegação. Os 20 casos da nova campanha continuam `not_run`; preparação não é observação. Paridade permanece 0/25 famílias enquanto não houver testes diferenciais.
5. Construtores, pontos GDI StartDoc/StartPage, as três entradas do primeiro marco Windows e as seis de geometria/consumidores já foram examinados. Ver `docs/REA-IMPRESSAO-CONSUMIDORES.md`; esse marco tinha 200 entradas (152 REA + 48 diretas exclusivas), antes das nove entradas de interface que elevaram o catálogo a 209. Seguir `0x166d050`, `0x165f5d0`, `0x16678c0`, `0x16678d0`, `0x16678e0`, `0x16678f0`, `0x1665a30`, `0x1664c00`, `0x2d226d0` e `0x1b5baf0`. Não copiar assinaturas provisórias: uma comparação inteira usa slot tipado como float pelo decompilador. Ainda não há geometria completa, imposição ou impressão física equivalente. Projetos locais preservados em `analysis-local/headless/windows-print-01` e `windows-print-02`; resultados novos são do backend direto `-noanalysis`, com conferência Capstone.
6. Workers e parte do argumento de 24 bytes já examinados; ver docs/REA-BUSCA-IMPRESSAO.md. Completar significado dos bytes 3/5/6/7 e dwords 12/16/20, stemming e caminhos completos de anexos. Não exibir controles sem implementação.
7. Ampliar gradualmente edição/persistência de marcadores, comentários, formulários e demais famílias da matriz; separar recursos Reader/Editor e serviços externos inacessíveis.
8. Validar abertura/gravação por portal, impressão física, Linux em desktop real e adaptador Windows. Os testes atuais usam PDF sintético e tela X11 virtual.
9. Publicar cada marco, conferir hashes/HEAD remoto, atualizar indicadores e preservar provas locais não redistribuíveis. Não declarar 100% enquanto as obrigações das 21 etapas permanecerem abertas.
