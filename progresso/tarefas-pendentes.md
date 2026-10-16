# Retomada

1. Ler `projeto.json`, `progresso.json`, matriz de paridade e histórico. Conferir Git local/remoto; não reiniciar a análise geral.
2. Retomar os resultados REA/Ghidra e o projeto headless preservado. O main default expirou; usar seeds/perfil dirigido e registrar novos resultados separadamente.
3. Retomar a inicialização no runtime Wine/i386 sob QEMU já validado pelo controle cmd.exe. O kernel não executa ELF x86 nativo. Foxit carrega, mas encerra após CInvalidArgException e INT 0x29 antes da UI; diagnosticar a exceção inicial, preservando contenção e bytes do original.
4. Executar o corpus sintético no original e comparar busca/escopos/ordem/navegação. Paridade permanece 0/25 famílias enquanto não houver testes diferenciais.
5. Construtores, pontos GDI StartDoc/StartPage e as três entradas `0x1668ac0`, `0x1663a80`, `0x1663410` já foram examinados. Seguir `0x1668750`, `0x1667fe0`, `0x1655e00`, `0x16561c0`, `0x1665780` e `0x166fe90`; ver docs/REA-IMPRESSAO-WINDOWS.md. Ainda não há geometria completa, imposição ou impressão física equivalente. A rodada Windows preservou um projeto Ghidra local; a análise automática MCP expirou, e os novos resultados são do backend direto `-noanalysis`.
6. Workers e parte do argumento de 24 bytes já examinados; ver docs/REA-BUSCA-IMPRESSAO.md. Completar significado dos bytes 3/5/6/7 e dwords 12/16/20, stemming e caminhos completos de anexos. Não exibir controles sem implementação.
7. Ampliar gradualmente edição/persistência de marcadores, comentários, formulários e demais famílias da matriz; separar recursos Reader/Editor e serviços externos inacessíveis.
8. Validar abertura/gravação por portal, impressão física, Linux em desktop real e adaptador Windows. Os testes atuais usam PDF sintético e tela X11 virtual.
9. Publicar cada marco, conferir hashes/HEAD remoto, atualizar indicadores e preservar provas locais não redistribuíveis. Não declarar 100% enquanto as obrigações das 21 etapas permanecerem abertas.
