# Retomada do Linuxit PDF

Fonte e Flatpak **0.1.12/devel**, com [TIFF multipágina](TIFF-MULTIPAGINA.md):
ordem por blocos de arquivo e páginas internas, orientação por página, RGB8 e
até 100 páginas totais. Encadeamento IFD limitado; sem SubIFDs recursivos ou
seleção individual de páginas TIFF. [OCR local](OCR-LOCAL.md) anterior
preservado, com limite próprio de 20 páginas, português/inglês e cópia rasterizada.

**380/380 testes próprios por ambiente**: fonte, payload e sandbox instalado,
sem falhas/erros/skips. Novos: 14 portáveis, dois GTK e uma integração Linux
TIFF→PDF→OCR. Um teste de recusa de TIFF foi adaptado/renomeado à nova regra;
362 IDs anteriores preservados e 18 novos IDs incluem essa substituição.
105 arquivos app e 11 relatórios CI conferidos; smoke 5/5 e launcher 3/3.
Publicação e auditoria desta entrega nas notas mais recentes. Testes próprios
não são paridade Foxit; relatórios e pacotes anteriores preservados.

Pastas sincronizadas: controles fora HOME negado/concedido passaram novamente.
Cliente real, portal/concessão persistente, AT-SPI e impressão física pendentes,
sem depender da VM Foxit. Demais formulários/anotações e famílias completas
continuam abertos. Editor de cópia/histórico e formatos anteriores preservados.

Arquitetura: 43 módulos/57 interfaces; catálogo: 323 (152 REA + 171 diretas), 23
subconjuntos/duas propostas em 25 famílias. Roteiro **43,93%**, 38 done/20 abertos;
paridade **0/25**, cobertura global desconhecida. Original não executado.
APIs de nuvem adiadas/IA excluída; não reiniciar análises preservadas.

VM: último diagnóstico histórico com NEM/Snail, Integridade da Memória ativa e
NAT então ativo; offline não validado. Usuário pediu continuar sem VM. Nenhuma
VM, rede ou proteção Windows alterada nesta rodada. Validar isolamento antes
de executar original; detalhes nas notas datadas anteriores.

Instruções permanentes e registros de marcos anteriores abaixo; a síntese acima
e as notas mais recentes definem o estado atual.

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

- Estática 03/05/07/08/09/11: alocação/tamanhos e chamadores dos arrays;
  15cd6e0/15cc9b0; atribuição do provedor ativo em dialog+1e48 e campos restantes
  de SearchOption; contexto0x138, serviços de imagem e ownership. As48 entradas
  desta continuação não devem ser repetidas. Tipos viewer/página/diálogo e
  stemming efetivo foram ligados; IDs7911/7913 ainda têm ambiguidade de comportamento.
- Contratos12/lógica15/UI16: ampliar operações e duas propostas, com nuvem adiada pelo usuário;
  23 subconjuntos parciais e 37 módulos/49 interfaces documentados.
- Runtime: desktop real, portais, AT-SPI, impressora física e serviços externos
  precisam de seus ambientes/equipamentos/contas. Isso é distinto da VM Foxit.
- VM10/11/18/19: observar original offline, D01–D20 eUI01–UI10, importar hashes/
  protocolos/evidências da campanha preservada e medir diferenças. Zero casos
  originais observados e50 cenários completos de aceitação ainda not_run.
- API01 encerrada por nova leitura: regras/rulesetsHTTP200 vazios e main
  protected=false após repositório público. Nenhuma configuração foi alterada.
  Ver REGRAS-REMOTAS-2026-10-18.md.

**Ainda há trabalho viável sem VM.** Aprovar um pacote não encerra essas etapas.
Os checkpoints anteriores estão preservados em
[arquivo histórico](RETOMADA-CHECKPOINTS-2026-10-17.md); suas antigas pendências
GTK/Poppler/pacote não descrevem a entrega atual.

## Ferramentas e ambiente

Atualização em 18/10/2026 às 01:21: VM Windows 10 x64 no VirtualBox 7.2.20
existe, com 8000 MB/duas vCPUs; o usuário relata lentidão. O log registra
Integridade da Memória ativa e backend NEM com mensagem Snail execution mode.
Não houve alteração de proteções nem execução do original por esta rodada.
NAT está ativo na configuração: contenção offline ainda precisa ser preparada
e validada. Diagnóstico e próximos passos nas notas de continuidade.

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
um projeto preservado para nova rodada; nunca modifica a origem. Selecionar
`--subject-sha256` para a DLL pinada; projetos e metadados exigem hash compatível. Manifestos
anteriores devem ser preservados. Originais/decompilações não entram no Git.
Não lançar Foxit no host normal; [preparação da contenção](COMO-CONTINUAR.md).

## Verificações

```bash
/usr/bin/python3 scripts/validate_functional_spec.py --check-render docs/contratos-funcionais.md
/usr/bin/python3 scripts/check_architecture.py
/usr/bin/python3 scripts/run_tests.py --output /tmp/linuxit-testes-novos.json
```

O último comando exige dependências Linux e tela para completar 290 testes sem
skips. Fluxos manuais de CI: `no-vm-validation.yml` (fonte/corpus),
`linux-flatpak.yml` (fonte/payload/sandbox) e `delivery-audit.yml` (bundle
publicado reinstalado sem rebuild). Fontes/licenças, builder pareado e
`runtime-lib` devem ser preservados. Instruções: [instalação](instalacao.md).
