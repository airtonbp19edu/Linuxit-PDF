# Retomada do Linuxit PDF

Fonte 0.1.7 em desenvolvimento: [criação PNG/JPEG](CRIACAO-IMAGENS.md).
17 testes portáveis e 12 regressões do worker passaram localmente; GTK/Linux e novo pacote aguardam execução.
O pacote publicado permanece 0.1.6, com auditoria independente confirmada.
20 subconjuntos e cinco propostas não significam implementação completa; VM,
paridade e demais pendências continuam abertas.


Atualizado em 2026-10-17T18:19:25-03:00. Fonte/Flatpak **0.1.6/devel**.
[Busca em anexos, modos e coleção](BUSCA-COLECOES.md):190/190 em cada suíte
fonte/payload/sandbox, zero falhas/erros/skips; smoke 5/5 e launcher 3/3.
32 métodos portáveis e seis GTK novos; capturas examinadas após corrigir o
sincronismo da fotografia, sem alterar o aplicativo. Campanha preservada 17/17.

[LinuxitPDF-0.1.6-x86_64.flatpak](../releases/LinuxitPDF-0.1.6-x86_64.flatpak),
35.601.808 bytes, SHA-256 `a71bca023a6bd2f671ffb7049a101a59ade185ef25bb5d3f8f0ddfeb7c399d05`.
[Revisão](../testes/resultados/0.1.6/validation-review.json) e [CI](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39069918299).
Publicação/auditoria independente devem ser consultadas nas últimas notas.

28 módulos/26 interfaces; 19 subconjuntos/seis propostas em 25 famílias.
Catálogo **248** (152 REA + 96 diretas),8 entradas novas/889 instruções/3.223 bytes
nesta continuação. Raw/projetos em `analysis-local/headless/no-vm-continuation-2026-10-17/`
e `no-vm-context-2026-10-17/`. RTTI confirmou CPDF_ImageRenderer e
CReflowViewerEx/IPDFViewer. Não repetir os oito alvos examinados.

Roteiro **43,33%**, paridade **0/25**; 37 critérios done/21 abertos em 14 etapas.
Ainda há trabalho sem VM: tipos/campos/fluxos, operações PDF e seis propostas.
Stemming, OCR, formatos adicionais, desktop real/portais/AT-SPI/impressão física
e serviços externos continuam pendentes; original depende de contenção offline.

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

- Estática03/05/07/08/09/11:15c9c90,15c5e00 e slots CPDF_ImageRenderer;
  tipos/ownership, campos desconhecidos da busca e contexto dos IDs7911/7913.
- Contratos12/lógica15/UI16: ampliar operações e as seis famílias propostas,
  mantendo19 subconjuntos parciais.28 módulos/26 interfaces documentados.
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

O último comando exige dependências Linux e tela para completar190 testes sem
skips. Fluxos manuais de CI: `no-vm-validation.yml` (fonte/corpus),
`linux-flatpak.yml` (fonte/payload/sandbox) e `delivery-audit.yml` (bundle
publicado reinstalado sem rebuild). Fontes/licenças, builder pareado e
`runtime-lib` devem ser preservados. Instruções: [instalação](instalacao.md).
