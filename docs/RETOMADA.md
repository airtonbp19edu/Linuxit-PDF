# Retomada do Linuxit PDF

Atualizado em 2026-10-17T18:40:30-03:00.
Fonte/Flatpak **0.1.7/devel**: [criação de PDF de PNG/JPEG](CRIACAO-IMAGENS.md),
com ordem ajustável, DPI, orientação EXIF, transparência branca e destino novo.
**212/212** em cada suíte fonte/payload/sandbox, zero falhas/erros/skips;
17 métodos novos do backend e cinco GTK. Campanha preservada 17/17,
smoke 5/5 e launcher 3/3. Capturas e hashes examinados.

30 módulos/29 interfaces; 20 subconjuntos/cinco propostas em 25 famílias.
Catálogo **250** (152 REA + 98 diretas); duas entradas novas de reflow/111 instruções/
467bytes nesta rodada, com RTTI IPDFViewerLayout/CReflowViewerLayout.
[Análise](REA-REFLOW.md). Original não executado; sem paridade diferencial.

37 critérios done/21 abertos em 14 etapas; roteiro **43,33%**, paridade **0/25**.
Ainda há trabalho sem VM. Publicação/auditoria são registradas nas notas;
aprovação do pacote não encerra os demais contratos ou etapas.

[LinuxitPDF-0.1.7-x86_64.flatpak](../releases/LinuxitPDF-0.1.7-x86_64.flatpak),
35614064 bytes; SHA-256 `093ee6c7ed6ab6a1c4974da836fedb3414e147dfa0554ddae9eac8ee575c9070`.
[Revisão](../testes/resultados/0.1.7/validation-review.json) e [CI](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39071324606).
Sete pacotes anteriores preservados. Próximos alvos exatos nas notas e análise;
não repetir as duas entradas ou os oito alvos anteriores já examinados.

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

- Estática03/05/07/08/09/11:1f21a80/1f21ac0 e slots CPDF_ImageRenderer/CReflowViewerLayout;
  tipos/ownership, campos desconhecidos da busca e contexto dos IDs7911/7913.
- Contratos12/lógica15/UI16: ampliar operações e as cinco famílias propostas,
  mantendo20 subconjuntos parciais.30 módulos/29 interfaces documentados.
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

O último comando exige dependências Linux e tela para completar212 testes sem
skips. Fluxos manuais de CI: `no-vm-validation.yml` (fonte/corpus),
`linux-flatpak.yml` (fonte/payload/sandbox) e `delivery-audit.yml` (bundle
publicado reinstalado sem rebuild). Fontes/licenças, builder pareado e
`runtime-lib` devem ser preservados. Instruções: [instalação](instalacao.md).
