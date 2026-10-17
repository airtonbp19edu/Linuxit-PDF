# Retomada do Linuxit PDF

Fonte em desenvolvimento **0.1.6**: `docs/BUSCA-COLECOES.md`. Busca em anexos,
coringas/proximidade e coleção persistente;32 métodos portáveis aprovados,
seis GTK aguardam Linux.28 módulos/26 interfaces,19 subconjuntos/seis propostas.
Catálogo245(152REA+93diretas); nova rodada5 entradas/517 instruções/1572bytes.
Entrega publicada/auditada permanece0.1.5 até validar um novo pacote.
Os checkpoints históricos abaixo não substituem este estado da fonte.

Atualizado em 2026-10-17T16:14:01-03:00. Pedido ativo: avançar as frentes sem VM,
publicar cada marco e registrar evidências para outras IAs.

## Estado atual

**Fonte e Flatpak 0.1.5/devel**, entrega incremental em Linux x86_64.
[Novas operações](COPIA-EDITADA.md): marcador principal, nota Text e campo
AcroForm Tx em cópia nova; preserva fonte e recusa sobrescrita. Anexos de
árvores Kids e anotações, busca e impressão anteriores continuam presentes.

**152/152 testes em cada ambiente**: fonte Linux, payload e sandbox instalado;
zero falhas/erros/skips, smoke 5/5 e launcher 3/3. Inclui cinco métodos GTK novos
com diálogos reais e worker. [Relatórios](../testes/resultados/0.1.5/validation-review.json)
e [CI](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39060979871). A campanha preservada passou 17/17, mesmos oito arquivos e protocolos.

Catálogo **240 entradas** (152 REA +88 exclusivas diretas). Nesta execução:
31 entradas novas em quatro lotes; Capstone conferiu 3.934 instruções/12.315 bytes.
Raw e projetos em `analysis-local/headless/no-vm-*-2026-10-17/`, ignorados.
[Resultados e alvos](AVANCO-SEM-VM.md); **não repetir** lotes examinados.

Roteiro **43,33%**, paridade **0/25**, cobertura global de RE desconhecida.
37 critérios concluídos e 21 abertos em 14 etapas; pesos/estados preservados.
A auditoria/publicação deve ser consultada no manifesto, progresso e últimas
[notas datadas](../progresso/notas-continuidade.md), sem presumir estado remoto.

## Primeiro ao retomar

1. Ler `progresso/projeto.json`, `progresso/progresso.json`,
   `progresso/tarefas-pendentes.md` e `progresso/matriz-paridade.csv`.
2. Conferir Git local/remoto e preservar mudanças alheias. Publicação de marcos
   está autorizada; sem reset destrutivo/force push. Não precisa criar worktree.
3. Ler o registro de [pendências](../progresso/pendencias-analises.md) e o
   [escopo sem IA](ESCOPO.md). UPDF e assistente generativo permanecem excluídos.
4. Continuar de um alvo/contrato específico; não reiniciar análise geral.
   Atualizar notas com data/hora real de São Paulo após cada lote.

## Próximas frentes

- Estática03/05/07/08/09/11:16664e0,1b8a7a0,1b8ae20,15c6550,872f20;
  tipos/ownership, campos desconhecidos da busca e contexto dos IDs7911/7913.
- Contratos12/lógica15/UI16: ampliar operações e as nove famílias propostas,
  mantendo16 subconjuntos parciais.23 módulos/18 interfaces documentados.
- Runtime: desktop real, portais, AT-SPI, impressora física e serviços externos
  precisam de seus ambientes/equipamentos/contas. Isso é distinto da VM Foxit.
- VM10/11/18/19: observar original offline, D01–D20 eUI01–UI10, importar hashes/
  protocolos/evidências da campanha preservada e medir diferenças. Zero casos
  originais observados e50 cenários completos de aceitação ainda not_run.
- API01: detalhes das regras remotas retornaram403 por plano. Não alterar
  faturamento, visibilidade ou proteções para obter leitura.

**Ainda há trabalho viável sem VM.** Aprovar um pacote não encerra essas etapas.
Os checkpoints anteriores estão preservados em
[arquivo histórico](RETOMADA-CHECKPOINTS-2026-10-17.md); suas antigas pendências
GTK/Poppler/pacote não descrevem a entrega atual.

## Ferramentas e ambiente

Windows local com Python3.13.15; último diagnóstico sem WSL/GTK/Flatpak.
Linux foi exercitado no CI Debian13 com GTK/Cairo/Poppler/CUPS e X11 virtual,
pelo código primeiro e Flatpak depois. Usar `/usr/bin/python3` para as extensões
nativas; Python do PATH pode ser incompatível.

Ferramentas confirmadas: REA6.5.0, Ghidra12.1.4, Temurin21.0.12.1 e Node24.22.0.
As rodadas novas são Ghidra direto `-noanalysis` com seed script REA, **não nova
observação MCP**. Caminhos: `A:\Programas\ghidra_12.1.4_PUBLIC`,
`A:\Programas\Eclipse Temurin JDK`, original em
`A:\Programas\Foxit PDF Reader\Foxit PDF Reader\FoxitPDFReader.exe`.
Hash de referência em `progresso/projeto.json`.

`scripts/analyze_foxit_headless.py --project-snapshot <projeto concluído>` copia
um projeto preservado para nova rodada; nunca modifica a origem. Manifestos
anteriores devem ser preservados. Originais/decompilações não entram no Git.
Não lançar Foxit no host normal; [preparação da contenção](COMO-CONTINUAR.md).

## Verificações

```bash
/usr/bin/python3 scripts/validate_functional_spec.py --check-render docs/contratos-funcionais.md
/usr/bin/python3 scripts/check_architecture.py
/usr/bin/python3 scripts/run_tests.py --output /tmp/linuxit-testes-novos.json
```

O último comando exige dependências Linux e tela para completar152 testes sem
skips. Fluxos manuais de CI: `no-vm-validation.yml` (fonte/corpus),
`linux-flatpak.yml` (fonte/payload/sandbox) e `delivery-audit.yml` (bundle
publicado reinstalado sem rebuild). Fontes/licenças, builder pareado e
`runtime-lib` devem ser preservados. Instruções: [instalação](instalacao.md).


Entrega0.1.5 publicada em `539bccb46fb3d5fddca4b70bef5a0c70aadce9a5`,
HEAD remoto/local e árvore limpa confirmados. A
[auditoria independente](../testes/resultados/0.1.5/audit/review.json)
reinstalou o mesmo bundle sem rebuild:85 arquivos app/2803 dependências/214 ELF/
149 arquivos de licença-créditos conferidos; controles7/7 e novo smoke5/5.
Suítes152/152 não foram repetidas nesta auditoria. O registro posterior é
verificado externamente para evitar autorreferência de hash Git.
