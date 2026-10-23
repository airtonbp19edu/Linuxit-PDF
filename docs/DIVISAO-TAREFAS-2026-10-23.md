# Divisão de tarefas Claude × Codex — 2026/10/23 às 00:50 (America/Sao_Paulo, UTC-03:00)

**Estado de 2026/10/23 às 05:46:** Claude escreveu PEGUEI E30 às02:17, após ausência de sinal do Codex. Na retomada05:30, Codex confirmou essa reserva e não abriu VM/VirtualBox; continua S1/S3/S2/S4 estáticos. Não há LIBEREI posterior no minichat consultado. Retorno pontual Codex executado e automação removida. As combinações e os horários anteriores abaixo são históricos; esta reserva prevalece enquanto não houver entrega explícita. App/tests/aceitação permanecem com Claude. [Checkpoint](VM-E30-INTERRUPCAO-E-RETOMADA-2026-10-23.md).

Pedido do usuário às 00:44:

- combinar com o Codex para fazer todas as tarefas, os dois trabalhando **ao mesmo tempo**;
- tentar fazer tudo o que for possível sozinhos e com a VM;
- se houver interrupção, o **Claude volta às 05:10** e o **Codex volta às 05:30**;
- os dois devem programar esse retorno na agenda.

**Autorização desta rodada:** o usuário mandou seguir sem parar a cada etapa ("tentem fazer tudo que
puderem sozinhos e com a VM"). Isso vale para este bloco de trabalho, até ele dizer outra coisa.

**Continuam proibidos sem o usuário:**

- publicar a 0.1.19 ou qualquer release;
- decidir a B3 ou mudar critérios e pesos;
- executar o Foxit fora da VM;
- incorporar código do Foxit;
- usar IA, nuvem por API ou 3D.

---

## Quem faz o quê

| Frente | Dono | Tarefa | Onde mexe |
|---|---|---|---|
| **K1** | Claude | **E34 — instalador do Windows** (diagnóstico em andamento no CI 39895160350); corrigir, instalar, desinstalar e rodar a suíte e a aceitação no Windows | ramo `claude/windows-installer`: `scripts/check_windows_installer.py`, `scripts/build_windows.py`, `packaging/windows/*` e `.github/workflows/windows-native.yml` |
| **K2** | Claude | **E30 — comparação na VM**: UI01 (com documento), UI02, UI05, UI09, UI10; D10–D20 que faltam; repetir a busca da E24 (comentário ausente) | VM e `docs/VM-E30-*.md`, `testes/resultados/vm-2026-10-23-e30/` |
| **K3** | Claude | **C3** — kit da E23 (passo a passo e verificadores para impressora, leitor de tela, áudio, monitores e sincronização) | `docs/E23-KIT-*.md`, `scripts/check_e23_*.py` |
| **K4** | Claude | **C4** — proposta escrita da B3 (texto dos critérios e efeito no índice), só para o usuário decidir | `docs/PROPOSTA-B3-*.md` |
| **K5** | Claude | **C5** — revisão independente do candidato 0.1.19 (sem publicar) | `testes/resultados/0.1.19/revisao-claude-*.json` |
| **X1** | Codex | **E35/S1** — fechar as três subfrentes (opções, objetos da UI, Unicode) e registrar | `docs/REA-S1-*`, `engenharia-reversa/funcoes.csv`, `docs/windows-evidence/` |
| **X2** | Codex | **C1/S3** — diagramas e estados de anotações, formulários, assinaturas e camadas | `docs/fluxos.md` e documento próprio |
| **X3** | Codex | **S2** — laço de impressão, DEVMODE, spooler e contexto `0x138` | `docs/REA-*IMPRESSAO*` |
| **X4** | Codex | **S4** — demais famílias em profundidade | `docs/REA-*`, catálogo |
| **X5** | Codex | **Etapa 19** — corrigir no Linuxit as divergências que o Claude achar na VM (K2), quando forem defeito claro. Escolha de comportamento (seguir ou não o Foxit) **vai para o usuário**, como na D05 | `app/`, `tests/`, `testes/aceitacao/` |

**Ordem dentro de cada agente:**

- Claude: K1 → K2 (enquanto a VM estiver disponível) → K3 → K4 → K5.
- Codex: X1 → X2 → X3 → X4. X5 entra sempre que o Claude mandar uma divergência no chat.

---

## Regras para trabalhar ao mesmo tempo

1. **Chat primeiro.** `CHAT-IA.txt` na raiz da pasta do PC. Escrever PEGUEI antes de cada frente,
   TERMINEI ao fechar e LIBEREI ao parar no meio. Ler o chat a cada commit.
2. **Arquivos com dono:**
   - `app/`, `tests/` e `testes/aceitacao/` são do Codex (X5). O Claude só altera os arquivos de
     empacotamento do Windows, e só no ramo próprio.
   - `engenharia-reversa/funcoes.csv` e `docs/windows-evidence/` são do Codex.
   - Os registros da VM são do Claude.
   - **Só um agente usa a VM por vez: o Claude (K2).** O Codex não abre a VM nem o VirtualBox
     enquanto o chat mostrar PEGUEI de K2 sem LIBEREI.
3. **Arquivos compartilhados** (`docs/AVISOS-E-STATUS.md`, `progresso/notas-continuidade.md`,
   `progresso/etapas-pequenas.json`, `progresso/progresso.json`, `docs/O-QUE-FAZER-AGORA-2026-10-22.md`):
   - `git pull --rebase` antes de cada commit;
   - em conflito, **manter as duas entradas** em ordem de horário;
   - em `progresso.json`, cada um mexe só nos critérios da própria frente.
4. **Divergência da VM → Codex:** o Claude escreve no chat uma linha AVISO com o caso, o resultado
   do Foxit, o do Linuxit e o arquivo de registro. O Codex responde PEGUEI X5 ou PERGUNTA.
5. **Commits:**
   - Claude: autor `Claude`, com o trailer do Claude.
   - Codex: autor `Airtonbp19`, com `Co-authored-by: Codex <noreply@openai.com>` (escolha do
     usuário em 00:39).
6. **Registro de cada avanço:** horário real, avisos, nota de continuidade, cópias `*-LOCAL.md`
   no PC.

---

## Retorno após interrupção

| Agente | Horário | Como está agendado |
|---|---|---|
| Claude | **05:10** de 23/10 | Mensagem agendada para esta mesma sessão. Se o Claude já estiver trabalhando, ela só serve de verificação |
| Codex | **05:30** de 23/10 | O Codex precisa criar o próprio agendamento (automação ou lembrete do Codex). O Claude não consegue agendar o Codex |

**Ao voltar, cada um:**

1. lê o `CHAT-IA.txt` e este documento;
2. faz `git pull`;
3. retoma a primeira frente sem TERMINEI;
4. avisa no chat.

---

## Ajuste combinado às 01:05 (Claude aceita a proposta do Codex das 00:48)

- **VM (E30): passa para o Codex**, como operador exclusivo. Ele está no próprio PC, o que é
  mais rápido que o controle remoto do Claude. O Claude não abre a VM nesta rodada.
- **O Claude não assume S2, S3/C1 nem S4.** São o mesmo tipo de análise que foi interrompida com o
  Claude. Ficam com o Codex.
- **Correções no app (antiga X5): passam para o Claude.** O Codex manda pelo chat cada divergência
  da VM (caso, resultado do Foxit, resultado do Linuxit, registro). Quando for defeito claro, o
  Claude corrige em `app/`, `tests/` e `testes/aceitacao/` e roda a suíte. Escolha de
  comportamento vai para o usuário.
- **Fica com o Claude:** K1 instalador do Windows, correções vindas da VM, K3 kit da E23,
  K4 proposta da B3 e K5 revisão da 0.1.19.
- **Fica com o Codex:** S1, VM/E30, S2, S3/C1 e S4.
- **Arquivos com dono:**
  - `app/`, `tests/` e `testes/aceitacao/` passam a ser do Claude enquanto houver correções da VM.
    O Codex avisa no chat antes de mexer neles.
  - Os registros da VM são do Codex.
- **Chat:** cada um escreve só no próprio arquivo: `CHAT-CLAUDE.txt` (Claude) e `CHAT-CODEX.txt`
  (Codex). Às 00:46 as gravações do `CHAT-IA.txt` apagaram linhas dos dois.
- **Retorno:** Codex agendou 05:30 (`retomar-linuxit-pdf-s-05-30`), Claude 05:10.

---

## Regra de assunção da VM — pedido do usuário às 00:57

"Caso ele não consiga concluir a VM, você assume." O Codex continua sendo o operador da E30, e o
Claude assume **só** em um destes casos:

1. O Codex escreve **LIBEREI** ou **BLOQUEADO** para a VM/E30 no `CHAT-CODEX.txt`.
2. O Codex fica **mais de 60 minutos** sem nenhuma linha nova no `CHAT-CODEX.txt` e sem commit novo,
   com a E30 ainda pendente.

**Passos do Claude antes de assumir:**

- No caso 2: se houver sinal de que o Codex está ativo (por exemplo, perto da retomada dele às
  05:30), escrever PERGUNTA no `CHAT-CLAUDE.txt` e esperar até 15 minutos pela resposta.
- Escrever **PEGUEI E30** no `CHAT-CLAUDE.txt`, com o caso em que o Codex parou, e conferir que ele
  não está operando a VM.
- Continuar do ponto registrado pelo Codex, sem repetir casos já concluídos e sem apagar os
  registros dele.

**O Codex, ao voltar:** se encontrar PEGUEI E30 do Claude, não abre a VM; combina pelo chat quem
continua. Nunca os dois operam a VM ao mesmo tempo.

D06 continua valendo para encerrar o Foxit residual, sempre registrando PID e horário.

---

## Sinal de vida da VM — pedido do usuário às 00:58

"Fique monitorando ele (caso não gaste tokens) ou peça para ele mandar atualizações sobre a VM;
caso pare, você assume de imediato."

**O Codex, enquanto opera a VM (E30), a cada 15 minutos no máximo e a cada caso concluído:**

- atualiza o ramo `codex/vm-status` com um commit vazio (pode ser forçado, sem tocar a `main`):

```text
git commit --allow-empty -m "VM-STATUS: ATIVO | caso UI02 | <resumo curto>"
git push --force origin HEAD:codex/vm-status
```

- usa no texto um destes estados: `ATIVO`, `LIBEREI` (parou e libera para o Claude), `BLOQUEADO`
  (não consegue seguir) ou `CONCLUIDO` (E30 terminada), sempre com o último caso feito.

**O Claude** deixa um vigia em segundo plano que confere esse ramo a cada 2 minutos. O vigia não
gasta nada enquanto o sinal está em dia e chama o Claude quando:

- o estado é `LIBEREI` ou `BLOQUEADO`;
- o sinal fica mais de **45 minutos** sem atualizar;
- o ramo não aparece em 45 minutos.

Nesses casos o Claude **assume de imediato**:

1. confere o `CHAT-CODEX.txt`;
2. escreve PEGUEI E30;
3. continua do último caso informado.

Com `CONCLUIDO`, o vigia para. O vigia expira a cada 2 horas e é rearmado pelo Claude; na
retomada das 05:10 ele também é rearmado.
