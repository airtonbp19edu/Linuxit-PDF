# O que pode ser feito agora — 2026/10/22 às 00:45 (America/Sao_Paulo, UTC-03:00)

**Atualização — 2026/10/22 às 20:49 (America/Sao_Paulo, UTC-03:00):** arquivos compartilhados conferidos local/remoto em7558bce, sem novos commits do Claude. Passo7 registrado:E32/A4 eE33/candidato concluídos no escopo delimitado;E34/A6 em andamento, Windows com instalação não validada. Codex assumeS1/busca estática como segundo trabalho autorizado. Candidato0.1.19:744/744 por ambiente, aceitação81/81, não publicado. VM intacta;B3 pendente, critérios/pesos preservados.

Lista compartilhada entre o Claude e o Codex, pedida pelo usuário. Situação geral:
[RETOMADA-2026-10-21.md](RETOMADA-2026-10-21.md) e [AVISOS-E-STATUS.md](AVISOS-E-STATUS.md).

**Regra:** fazer uma etapa por vez e parar ao final de cada uma, aguardando o usuário. Antes de
começar, avisar na nota de continuidade quem pegou a tarefa, para os dois não fazerem a mesma.

## Ferramentas confirmadas

- **REA 6.7.0 no PC:** o doctor do Ghidra 12.1.4 está saudável, com o Temurin JDK 21. O REA está
  **registrado no Codex** (`[mcp_servers.rea]` no `config.toml`, estado `aligned`); o próprio
  Codex rodou o `setup` e um teste MCP às 00:39 de 22/10. Os arquivos estão em
  `analysis-local/rea-instalacao/`, fora do Git.
- **REA na nuvem do Claude:** 6.7.0, com o Ghidra montado a partir dos módulos copiados do PC. O
  contêiner é temporário; refazer a montagem conforme o `RETOMADA-2026-10-21.md`.
- **VM:** só com o usuário ligando a máquina. A decisão D06 permite encerrar o processo residual
  do Foxit no início da E30 e entre casos.

**Atualização 2026/10/22 às 12:07:** o Codex escreveu A4/A5/A6 no PC (08:30–08:48), mas sem
commit, sem envio e sem CI. A ordem detalhada para ele continuar, e a lista completa do que falta
no projeto, está em [ORDEM-CODEX-2026-10-22.md](ORDEM-CODEX-2026-10-22.md).

## Tarefas que não dependem de nada do usuário

| # | Tarefa | Critério que pode fechar | Pontos | Quem pode fazer |
|---|---|---|---:|---|
| A1 ✅ (22/10, Claude) | Busca: thread `+0x1e3c` e laço de busca, chamadores de `0x1770e90`, campos `+3/+6/+7/+0xc/+0x10` das opções, algoritmo `0x1003f6b0` da DLL e diagrama final do fluxo | Etapa 8, “Fluxo completo de busca” | 1,74 | Codex no PC (REA MCP) ou Claude na nuvem |
| A2 ✅ (22/10, Claude) | Impressão: contexto de `0x138` bytes, serviços de imagem, concorrência e diagrama final | Etapa 8, “Fluxo completo de impressão” | 1,74 | Codex ou Claude |
| A3 ✅ (22/10, Claude) | Diagramas e estados por subsistema, a partir das evidências já preservadas | Etapa 9, “Diagramas e estados” | 1,27 | Qualquer um (não precisa do Foxit) |
| A4 ✅ (E32, contrato delimitado; critério12 parcial) | Entradas, saídas e erros detalhados por funcionalidade nas 25 famílias da especificação | Etapa 12 | 1,5 | Qualquer um |
| A5 ✅ (E33, candidato testado; sem publicação) | Montar o candidato 0.1.19 com a E31, mantendo os workflows iguais aos da `main` | — | — | Claude ou Codex; publicar só com a confirmação do usuário |
| A6 🔄 (E34, oito recortes Linux; Windows parcial) | Desenvolvimento próprio (ver a lista abaixo) | Etapas 15 e 16, parciais | — | Qualquer um |

**Itens de desenvolvimento próprio (A6):**

- XFA dinâmico;
- JavaScript de formulários;
- gravar DSS/LTV, OCSP e criar carimbo de tempo;
- redação sem rasterizar;
- edição universal de anotações;
- edição de documento recuperado;
- OCR melhor no Flatpak;
- mais conversões;
- instalador e suíte completa no Windows.

**Para A1 e A2:**

- Consultar `engenharia-reversa/funcoes.csv` (343 entradas, conferidas em22/10; referência336 abaixo é histórica) antes de escolher sementes e não
  repetir entradas.
- Usar o pipeline: `scripts/analyze_foxit_headless.py` → `check_foxit_machine.py` →
  `catalog_foxit_headless.py` → `catalog_foxit_functions.py`.
- Os resultados brutos ficam em `analysis-local/`.
- Um critério só passa para `done` com o fluxo inteiro documentado e as lacunas declaradas, nunca
  por um lote parcial.

## Tarefas que dependem do usuário

| # | Tarefa | Depende de | Pontos possíveis |
|---|---|---|---:|
| B1 | E30: UI01 com documento aberto, UI02, UI05, UI09 e UI10; D10–D20 restantes; repetir a busca que deixou o comentário de fora | VM ligada | 2,4 + 3,0 (etapas 10 e 11) e mais, nas etapas 18 e 19 |
| B2 | E23: impressora física, leitor de tela, áudio, monitores e cliente de sincronização real | Equipamentos | — |
| B3 | Decidir se “todas as famílias/funções” nos critérios passa a significar o inventário fixo (25 famílias e 116 operações), para o índice avançar família por família | Decisão do usuário | Até cerca de 41 pontos ficariam mensuráveis |

## Ao terminar uma tarefa

1. Testes próprios e, se o código mudou, a aceitação.
2. Registrar com data e horário reais em `docs/AVISOS-E-STATUS.md` e em
   `progresso/notas-continuidade.md`.
3. Atualizar `progresso/etapas-pequenas.json` e regenerar com `scripts/render_small_steps.py`.
4. Publicar no GitHub e copiar `AVISOS-LOCAL.md` e `ETAPAS-LOCAL.md` para a pasta local.
