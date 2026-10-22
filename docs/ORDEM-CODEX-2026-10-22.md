# Ordem de trabalho para o Codex — 2026/10/22 às 12:07 (America/Sao_Paulo, UTC-03:00)

**Atualização — 2026/10/22 às 20:37 (America/Sao_Paulo, UTC-03:00):** Passos4–6 executados: A4 registrada sem alterar critérios; candidato0.1.19/9fb4f3a validado744/744 em fonte/payload/Flatpak e aceitação81/81. Publicação retida; Windows e limites A6 no relatório. Passo7 aguarda instrução. Sem VM/B3; checklist45,13%, paridade0/25 e global indeterminado. [Resultados e pendências](PASSOS-4-6-A456-2026-10-22.md).

Pedido do usuário às 12:04: “deixe a ordem para o Codex continuar de forma minuciosa o que falta
ele fazer, e também todas as outras coisas restantes”. Escrita pelo Claude depois de conferir o
GitHub e a pasta do PC (só leitura; nada no PC foi alterado além das cópias `*-LOCAL.md` na raiz).

**Regras que continuam valendo:**

- Uma etapa por vez. Ao terminar cada passo numerado abaixo, registrar e **parar para o usuário**.
- A VM só com o usuário. A decisão D06 permite encerrar o processo residual do Foxit na E30.
- Não incorporar código do Foxit. IA excluída; nuvem por API e 3D adiados.
- Publicar release só com confirmação explícita do usuário. Nunca digitar tokens.
- Horários reais (`date`) no formato `AAAA/MM/DD às HH:mm (America/Sao_Paulo, UTC-03:00)`.
- Status e pesos dos critérios não mudam sem prova completa. Mudar a redação de critério é
  decisão do usuário (B3).

---

## Parte 1 — Onde o Codex parou

Situação encontrada às 12:04:

- **GitHub (`main`):** último commit `bd2eeb4` (Claude, 08:37), com as tarefas A1/A2/A3 do Claude.
  O último commit do Codex é o `b79aca7` (08:28), que só registra que ele assumiu A4, A5 e A6.
- **Pasta do PC:** o Codex trabalhou das 08:30 às 08:48 e parou. **Nada disso tem commit nem foi
  enviado.** A cópia do PC também ainda **não tem** os commits `32fc157` e `bd2eeb4` do Claude.

**Arquivos alterados ou novos na pasta do PC, sem commit:**

| Grupo | Arquivos |
|---|---|
| A4 (contratos) | `docs/A4-CONTRATOS-OPERACIONAIS-2026-10-22.md`, `docs/contratos-operacoes-v1.json`, `docs/contratos-funcionais.md`, `docs/especificacao-funcional.json`, `scripts/validate_functional_spec.py`, `tests/test_operation_contracts.py`, `testes/resultados/a4-2026-10-22/review.json` (conferir), `analysis-local/build_a4_contracts.py` |
| A6 JavaScript | `app/pdf_form_javascript.py`, `tests/test_form_javascript.py`, `tests/test_form_javascript_security.py`, `scripts/prepare_js_runtime.py`, `scripts/prepare_windows_js.py` |
| A6 XFA | `app/pdf_xfa_flow.py`, `app/xfa_window.py`, `tests/test_xfa_flow.py`, `tests/test_xfa_flow_security.py`, `tests/test_forms_a6_gtk.py` |
| A6 assinaturas | `app/pdf_preservation.py`, `app/signature_ocsp.py`, `app/pdf_signatures.py`, `app/signature_trust.py`, `app/signature_window.py`, `tests/test_signature_preservation.py`, `docs/A6-ASSINATURAS-PRESERVACAO.md` |
| A6 redação | `app/vector_redaction.py`, `app/pdf_redaction.py`, `tests/test_vector_redaction.py`, `tests/test_vector_redaction_review.py` |
| A6 recuperado/OCR/conversões | `app/recovered_edit.py`, `app/pdf_changes.py`, `app/pdf_ocr.py`, `app/ocr_window.py`, `app/pdf_conversion.py`, `app/conversion_window.py`, `tests/test_recovered_edit.py`, `tests/test_ocr_cleanup.py`, `tests/test_pdf_conversion.py` |
| A6 anotações | `app/annotation_editing.py`, `app/annotation_geometry.py` (08:48, **sem documento nem teste novo**) |
| Edição/segurança | `app/edit_dialogs.py`, `app/edit_window.py`, `app/pdf_edit_security.py`, `app/main.py`, `app/worker_cli.py`, `app/search_tasks.py` |
| A5 / Windows | `app/version.py`, `scripts/build_windows.py`, `scripts/check_windows_installer.py`, `scripts/build_flatpak.py`, `scripts/audit_delivery.py`, `packaging/windows/*` (conferir), `.github/workflows/windows-native.yml` (conferir) |
| Registros | `docs/A456-EXECUCAO-2026-10-22.md`, `docs/A6-FORMULARIOS-E-WINDOWS-2026-10-22.md`, `docs/arquitetura-componentes.json` |

**Evidências locais (fora do Git, em `analysis-local/`):**

- `a6-js-01.json`: 10/10.
- `a6-xfa-01.json`: 9/9.
- `a6-form-regression.json`: 19 aprovados e 1 GTK não executado.
- `a6-xfa-regression.json`: 15/15.
- Também: `a6-vector-tests-*`, `signature-preservation-20261022-*`, `a6-recover-01`, `a6-ocr-01`,
  `js-/xfa-security-*` e `a456_ci.py`.

O próprio Codex escreveu: **“implementação em validação”**. A suíte completa no Linux, a aceitação,
o CI e o candidato 0.1.19 **ainda não foram executados**.

---

## Parte 2 — Ordem minuciosa para o Codex (A4, A5 e A6)

Fazer na ordem. Cada passo termina com registro e parada.

### Passo 1 — Salvar o trabalho e sincronizar (sem perder nada)

1. `git status` e `git stash list`. Confirmar que os arquivos da tabela acima estão lá.
2. Criar um ramo de segurança com tudo: `git switch -c codex-a456-wip`, `git add -A`, conferir que
   `__pycache__/` e `analysis-local/` **não** entraram (estão no `.gitignore`), e fazer o commit.
3. `git fetch origin`, depois `git rebase origin/main` (traz `32fc157` e `bd2eeb4` do Claude).
   - Conflitos esperados: nenhum ou poucos. O Claude mexeu em `docs/fluxos.md`,
     `docs/O-QUE-FAZER-AGORA-2026-10-22.md`, `docs/AVISOS-E-STATUS.md`,
     `progresso/progresso.json`, `progresso/notas-continuidade.md`, `progresso/etapas-pequenas.json`,
     `engenharia-reversa/funcoes.csv` e nos novos `docs/REA-FLUXO-*`.
   - Em notas e avisos: **manter as duas entradas**, em ordem de horário.
   - Nunca apagar arquivos do Claude.
4. **Não enviar ainda para a `main`.** Enviar o ramo (`git push -u origin codex-a456-wip`) só como
   cópia de segurança, para o trabalho não ficar apenas no PC.

### Passo 2 — Fechar as lacunas antes de testar

1. **Dependência nova (QuickJS-NG 0.15.1.1 e `python-quickjs-ng`, MIT):**
   - registrar a proveniência e a licença, como foi feito para o pypdf e o snowball
     (`docs/proveniencia-*.json`, avisos de licença no pacote);
   - conferir que o Flatpak compila sem rede, com fonte fixada e SHA-256 (`build_flatpak.py`,
     manifesto em `packaging/`);
   - conferir que o `audit_delivery.py` inclui o motor nos avisos.
2. **`annotation_editing.py`/`annotation_geometry.py` (alterados às 08:48):** dizer o que mudou,
   criar teste para isso, ou desfazer a alteração se estiver incompleta. A “edição universal de
   anotações” não pode aparecer como feita sem documento e teste.
3. **Item “OCR melhor no Flatpak”:** a `a6-ocr-01` testou limpeza de contraste e limiar. Falta
   provar **no Flatpak instalado** (idiomas, tesseract do runtime).
4. **Catálogo e arquitetura:** rodar
   - `python scripts/check_architecture.py`;
   - `python scripts/check_operation_catalog.py` (se mudou código fixado, usar
     `refresh_operation_pins.py --apply --accept` e explicar o motivo);
   - `python scripts/validate_functional_spec.py --check-render docs/contratos-funcionais.md`.

### Passo 3 — Suíte completa no Linux e aceitação limpa

O Codex está no Windows, então a suíte Linux roda no CI. Por isso, o ramo precisa ir para a `main`
neste passo.

1. No PC, rodar o que for possível: `python scripts/run_tests.py` e anotar falhas, erros e skips
   **separando** o que é exclusivo do Linux.
2. Fazer **commits temáticos** na ordem:
   1. A4 contratos;
   2. A6 JavaScript;
   3. A6 XFA;
   4. A6 assinaturas;
   5. A6 redação;
   6. A6 recuperado, OCR e conversões;
   7. instalador Windows;
   8. A5 versão.
3. `git rebase origin/main` de novo e `git push origin HEAD:main`.
4. Acompanhar `no-vm-validation.yml`, que é a suíte Debian 13 com aceitação.
   - Meta: **666 + os testes novos**, todos aprovados, sem skips novos sem justificativa.
   - Meta na aceitação: **81/81** mais os casos novos.
   - Os 3 testes GTK de `test_forms_a6_gtk.py` precisam **rodar de verdade** com xvfb. Compilar
     não conta como aprovação.
5. Se falhar: corrigir **antes** de qualquer outra coisa e registrar em
   `docs/CI-FALHAS-E-CORRECOES.md`, como na E31. Os verificadores preservados (campanha C18,
   `smoke_linuxit.py`) também precisam continuar verdes.
6. **Parar e avisar o usuário** com os números.

### Passo 4 — A4: registrar sem inflar o índice

1. Anexar como evidência no critério “Entradas/saídas/erros e critérios detalhados por
   funcionalidade” (etapa 12): `contratos-operacoes-v1.json`, `contratos-funcionais.md` e o
   `review.json` da A4.
2. **Manter o critério `partial`.** O próprio relatório da A4 explica por quê: o universo do Foxit
   continua aberto. O critério só fecha se o usuário decidir a **B3** (inventário fixo de 25
   famílias e 116 operações como denominador). Nesse caso, pedir a decisão por escrito e registrá-la
   como D07 em `progresso/etapas-pequenas.json`.
3. Rodar `scripts/update_progress.py`. O índice deve continuar **45,13%**, a menos que a B3 tenha
   sido decidida.

### Passo 5 — A5: candidato 0.1.19 (sem publicar)

1. Antes de tudo, confirmar a regra da E29: os workflows do commit candidato precisam ser **idênticos
   aos da `main`** (mesma árvore `.github/workflows`).
2. Rodar `linux-flatpak.yml` no commit candidato. Metas:
   - fonte, payload e sandbox com 100% dos testes, sem skips;
   - smoke 5/5 e launcher 3/3;
   - arquivos da fonte iguais aos do pacote;
   - inventário do runtime.
3. Registrar em `testes/resultados/0.1.19/` e `releases/manifest-0.1.19.json`, com
   `releases/notes-0.1.19.md` explicando E31 e A6 e os limites de cada recurso.
4. Conferência da publicação **sem publicar**: `publish-devel-release.yml` com `version: 0.1.19` e
   `check_only: true`, como na 0.1.18 (execução 39528468258). O plano esperado é `create_release`.
5. **Parar e pedir a confirmação do usuário para publicar.** Só depois disso:
   - publicar;
   - conferir o download público;
   - rodar `delivery-audit.yml` e `desktop-integrations.yml`;
   - atualizar `manifest.json` e `SHA256SUMS`.
6. O instalador Windows (`windows-native.yml`) é um **candidato de desenvolvimento sem assinatura**.
   Registrar o resultado da primeira execução real (build NSIS, UCRT64, instalação, suíte, aceitação,
   desinstalação). Se falhar, isso **não bloqueia** a 0.1.19 do Linux; abrir um passo próprio.

### Passo 6 — A6: fechar item por item, com prova

Situação de cada item da lista A6 depois do trabalho local:

| Item A6 | O que existe localmente | O que falta para contar como entregue |
|---|---|---|
| JavaScript de formulários | QuickJS isolado, eventos K/V/C/F, AF* numéricos, 10/10 local | CI Linux, teste no Flatpak instalado, Windows UCRT64 |
| XFA dinâmico | Layout fluido próprio (`tb`), instâncias, 9/9 + 15/15 | CI Linux, 3 GTK reais. Layout posicionado e FormCalc ficam **fora** (registrar como limite) |
| DSS/LTV, OCSP, carimbo | DSS incremental, OCSP offline, RFC 3161 em duas fases | CI Linux com OpenSSL; não afirmar PAdES-LTA |
| Redação sem rasterizar | Redação vetorial conservadora, casos adversariais | CI Linux; registrar o que é recusado (`Tr=1/2` etc.) |
| Edição universal de anotações | Alteração sem documento (08:48) | Ver o Passo 2.2 |
| Edição de documento recuperado | `recovered_edit.py`, `a6-recover-01` | CI Linux; usar o corpus danificado da E17 |
| OCR melhor no Flatpak | Limpeza de contraste e limiar | Prova no Flatpak instalado |
| Mais conversões | Texto, PNG/JPEG em ZIP, TIFF multipágina | CI Linux; teste de reabertura das saídas |
| Instalador e suíte no Windows | Scripts, NSIS, workflow | Primeira execução real do `windows-native.yml` |

Para cada item aprovado: anexar evidência nos critérios parciais das etapas 15 (“Todas as demais
famílias implementadas e testadas”) e 16 (“Demais interações e integrações funcionais”). **Manter
os dois critérios `partial`.** Eles falam em “todas”, e fechar depende de B3 e da comparação
com o Foxit.

### Passo 7 — Registro final do bloco A4–A6

1. Novas etapas pequenas em `progresso/etapas-pequenas.json`: **E32** (A4), **E33** (A5) e **E34**
   (A6, com subitens). Depois, `scripts/render_small_steps.py`.
2. Avisos em `docs/AVISOS-E-STATUS.md` e nota em `progresso/notas-continuidade.md`, com horário real.
3. Marcar A4, A5 e A6 em `docs/O-QUE-FAZER-AGORA-2026-10-22.md` (✅ ou 🔄, com o motivo).
4. Copiar `AVISOS-LOCAL.md` e `ETAPAS-LOCAL.md` para a raiz da pasta do PC.
5. **Parar** e mostrar ao usuário: números do CI, o que entrou, o que ficou como limite, e o pedido
   de confirmação para publicar a 0.1.19.

---

## Parte 3 — Todas as outras coisas restantes (Claude, Codex ou o usuário)

### 3.1 Os 19 critérios abertos (índice 45,13% · 39 de 58 · 54,87 pontos em aberto)

| Etapa | Critério | Situação | Pontos | Depende de |
|---|---|---|---:|---|
| 3 | Motor PDF e fronteiras de todos os subsistemas | pendente | 2,00 | B3 e análise estática |
| 5 | Ciclo de vida de todos os componentes | pendente | 2,29 | B3 e análise estática |
| 7 | Universo relevante e assinaturas/saídas de todas as funções | pendente | 3,33 | B3 |
| 8 | Fluxo completo de impressão | parcial | 1,74 | Estática (S2) |
| 8 | Fluxo completo de busca | parcial | 1,74 | Estática (S1) |
| 8 | Demais famílias investigadas profundamente | pendente | 5,22 | B3 e estática (S4) |
| 9 | Diagramas e estados por subsistema | parcial | 1,27 | Estática (S3) |
| 9 | Algoritmos completos de todas as famílias | pendente | 5,09 | B3 e estática (S4) |
| 10 | Cenários locais observados (D01–D20) | parcial | 2,40 | VM (B1/E30) |
| 10 | Integrações e casos excepcionais | parcial | 2,40 | VM e equipamentos (B1, B2) |
| 11 | Todas as interações observadas (UI01–UI10) | parcial | 3,00 | VM (B1/E30) |
| 12 | Entradas/saídas/erros por funcionalidade | parcial | 1,50 | A4 (Codex) e B3 |
| 12 | Fase A consolidada sem lacunas não declaradas | pendente | 2,00 | Fim das etapas 3–12 |
| 15 | Todas as demais famílias implementadas e testadas | parcial | 6,00 | A6 (Codex) e B3 |
| 16 | Demais interações e integrações | parcial | 4,67 | A6, B2 e B3 |
| 18 | Cenários diferenciais no original e no Linuxit | parcial | 3,50 | VM (B1) |
| 18 | Resultados e divergências por família | parcial | 2,80 | VM (B1) e B3 |
| 19 | Divergências medidas e corrigidas | parcial | 3,43 | VM (B1), depois correções |
| 21 | Obrigações viáveis encerradas e bloqueios declarados | pendente | 0,50 | Último passo |

### 3.2 Análise estática que continua aberta (sem VM; Claude na nuvem ou Codex com REA)

- **S1 — Busca (fecha 1,74)** — *2026/10/22 às 18:47: o Claude começou a S1 a pedido do usuário, mas não concluiu; a tarefa continua aberta e livre. Nada novo foi catalogado e nenhum status mudou.*
  - algoritmo da `fxLuceneLib.dll` em `0x1003f6b0` (BooleanQuery, 7.655 bytes);
  - bytes 3/5/6/7/`+0xc`/`+0x10` das opções;
  - classes concretas de `+0x1f34` (slot `+0x1c`) e `+0x2044` (slot `+0x14`).
  - Ver [REA-FLUXO-BUSCA-2026-10-22.md](REA-FLUXO-BUSCA-2026-10-22.md).
- **S2 — Impressão (fecha 1,74):**
  - laço por página de `CReader_BasePrinter` (slots da vtable `0x53d7788`);
  - montagem do DEVMODE e chamadas ao spooler (referências a `StartDocW`/`StartPage`/`EndPage`);
  - contexto de `0x138` bytes do `CPDF_BackgroundDrawer`;
  - significado do `0x48` em `+0x8c`.
  - Ver [REA-FLUXO-IMPRESSAO-2026-10-22.md](REA-FLUXO-IMPRESSAO-2026-10-22.md).
- **S3 — Diagramas (fecha 1,27):** anotações, formulários, assinaturas e camadas no mesmo nível de
  busca e impressão, em `docs/fluxos.md`.
- **S4 — Demais famílias:**
  - descompilação profunda e algoritmos família por família;
  - arrays do reflow pendentes de [REA-ARRAYS-REFLOW-2026-10-19.md](REA-ARRAYS-REFLOW-2026-10-19.md).
  - Só fecha com B3 (universo definido).
- Sempre: consultar `engenharia-reversa/funcoes.csv` (**343** entradas) antes de escolher sementes;
  usar o pipeline `analyze_foxit_headless.py` → `check_foxit_machine.py` →
  `catalog_foxit_headless.py` → `catalog_foxit_functions.py`.
- **Coordenação:** quem pegar S1–S4 anota antes na nota de continuidade, como foi feito com A1–A6.

### 3.3 O que depende do usuário

- **B1/E30 — VM ligada:**
  - UI01 com documento aberto, UI02, UI05, UI09 e UI10;
  - D10–D20 restantes;
  - repetir a primeira busca após reabrir o Foxit, para entender o comentário ausente na E24.
  - D06 autoriza encerrar o processo residual do Foxit (registrar PID e horário).
- **B2/E23 — equipamentos reais:** impressora física, leitor de tela, áudio, dois monitores e um
  cliente de sincronização real.
- **B3 — decisão:** adotar o inventário fixo (25 famílias e 116 operações) como significado de
  “todas as famílias/funções”. Deixaria cerca de 41 pontos mensuráveis família por família.
- **Publicar a 0.1.19:** confirmação explícita depois do Passo 5.

### 3.4 Adiado ou excluído (não fazer)

- Recursos de IA: **excluídos**.
- Integração direta com nuvem por API: **adiada**. O fluxo atual usa pastas sincronizadas por
  programas externos.
- 3D (U3D/PRC): **adiado** (D04); guia em [ESTUDO-3D-U3D-PRC.md](ESTUDO-3D-U3D-PRC.md).

### 3.5 Ordem recomendada para o projeto inteiro

1. Codex: Passos 1–3 acima (salvar, sincronizar, CI verde). **Urgente**, porque o trabalho existe
   só no PC.
2. Codex: Passos 4–7 (A4 registrada, candidato 0.1.19, A6 por item).
3. Usuário: decidir B3 e confirmar a publicação da 0.1.19.
4. Claude ou Codex: S1, S2 e S3 (estática, cerca de 4,75 pontos possíveis).
5. Usuário e uma IA: E30 na VM (B1), depois as correções da etapa 19.
6. Usuário: E23 com equipamentos (B2).
7. Por último: fase A consolidada (etapa 12) e auditoria final (etapa 21).
