# Pendências classificadas — 2026/10/23 às 11:40 (America/Sao_Paulo, UTC-03:00)

Pedido do usuário às 11:38: porcentagem atual e etapas restantes ou parciais, separadas em (1) o que
Claude/Codex fazem sozinhos, (2) o que precisa do usuário, (3) o que usa a VM. Fonte:
`progresso/progresso.json` (critérios e pesos inalterados) e `progresso/etapas-pequenas.json`.

## Números

- **Índice histórico do checklist: 45,13%** (39 critérios concluídos, 19 abertos; 54,87 pontos em aberto).
  Não mudou hoje: Windows e anotações avançam dentro de critérios amplos que só contam quando fecham inteiros.
- Inventário fixo: **104/116 operações com código próprio**; **0/116 comparadas** por completo com o Foxit;
  paridade **0/25** famílias. Conclusão global da recodificação: indeterminada.

## 1. Claude ou Codex fazem sozinhos (sem usuário, sem VM) — 8,25 pontos fecháveis

| Etapa | Critério | Pontos | Quem |
|---|---|---:|---|
| 8 | Fluxo completo de impressão (S2) | 1,74 | Codex |
| 8 | Fluxo completo de busca (S1) | 1,74 | Codex |
| 9 | Diagramas e estados por subsistema (S3) | 1,27 | Codex |
| 12 | Entradas/saídas/erros por funcionalidade | 1,50 | Claude ou Codex |
| 12 | Fase A consolidada sem lacunas não declaradas | 2,00 | Claude ou Codex, depois dos anteriores |

Desenvolvimento próprio que avança E15/E16 (sem fechar o critério sem a B3), fila do Claude: redação em
metadados/marcadores/anexos; XFA posicionado e FormCalc básico; API JavaScript ampliada; DSS/VRI completo;
exportação ODT/DOCX; OCR e mídia no Windows; Flatpak de teste dos ramos. Codex: S4 e lotes estáticos.

Trabalho amplo que pode ser feito sozinho mas, com a redação atual ("todas as funções do Foxit"), não
fecha nunca — 28,60 pontos: E3 2,00; E5 2,29; E7 3,33; E8 demais famílias 5,22; E9 algoritmos 5,09;
E15 6,00; E16 4,67. Ver B3.

## 2. Precisa do usuário

| Decisão ou ação | Efeito |
|---|---|
| B3: régua do inventário (opções A/B/C) | Torna mensuráveis os 28,60 pontos acima (31,6 com E11) |
| Publicar a 0.1.19 e integrar os ramos `claude/windows-installer` e `claude/anotacoes-universais` à `main` | Entrega; fecha a pendência de publicação automática (E29) |
| E23: impressora física, leitor de tela, áudio, dois monitores, cliente de sincronização | Parte de E10 (integrações) e E16 |
| Ligar a VM para a E30 | Libera o grupo 3 |
| Nuvem direta e 3D interativo (adiados), RMS (serviço Microsoft) | Só se quiser retomar |

## 3. Usa a VM (Foxit original) — 17,53 pontos

| Etapa | Critério | Pontos |
|---|---|---:|
| 10 | Cenários locais observados e registrados | 2,40 |
| 10 | Integrações autorizadas e casos excepcionais (parte com equipamentos) | 2,40 |
| 11 | Todas as interações observadas | 3,00 |
| 18 | Cenários diferenciais no original e na reconstrução | 3,50 |
| 18 | Resultados e divergências por família | 2,80 |
| 19 | Divergências medidas e corrigidas (correção feita sem VM depois) | 3,43 |

Casos da E30 que faltam: UI05, UI09, UI10, D13, D14, D16, D20 (sem digitar) e D10–D12, senha,
salvar com nome (exigem teclado virtual do guest). Reserva da VM: Claude, sem uso desde 05:55.

E21 (0,50): fecha no fim, quando os demais estiverem encerrados ou declarados bloqueados.
