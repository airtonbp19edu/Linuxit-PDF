# Retomada do Linuxit PDF

Fonte e Flatpak **0.1.9/devel**, com [pastas sincronizadas locais](PASTAS-SINCRONIZADAS.md).
Pasta preferida, últimas pastas, atalhos para abrir/salvar e cópias novas completas,
sem sobrescrita. Alterações externas exigem reabrir; o envio cabe ao cliente externo.
**290/290 testes próprios** por ambiente: fonte, payload e sandbox instalado,
sem falhas, erros ou skips; 15 métodos portáveis e oito GTK novos.
Dois controles fora de HOME passaram: acesso negado sem concessão e permitido
com concessão específica. Cliente real, portal e persistência da concessão em
um desktop permanecem pendentes; esses testes não precisam da VM Foxit.

[Continuação estática de 18/10/2026](REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md): 16 entradas novas,
823 instruções/2.831 bytes conferidos; enum de busca, RTTI e geometria refinados.
Fonte/pacote preservados; as suítes completas não foram repetidas nesta rodada.

Arquitetura: 37 módulos/49 interfaces. Catálogo: 275 entradas (152 REA + 123 diretas).
São 23 subconjuntos e duas propostas em 25 famílias. Roteiro: **43,33%**,
37 critérios `done` e 21 abertos; paridade: **0/25**. Original não executado.
APIs remotas de nuvem continuam adiadas. Publicação confirmada no GitHub;
auditoria independente do mesmo pacote aprovada (sete controles + cinco smoke).
Evidências nas notas datadas; o restante do projeto continua parcial.

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

- Estática 03/05/07/08/09/11: helpers 15cb590/15cb720/15cbb70/15cb8a0/15cb130,
  tipo do receptor this+98 e slot+20, escritores/pré-condições dos arrays.
  Busca: provedor+58 e offsets 3/5/6/7/0xc/0x10; offset+14 tem enum parcial
  reconhecido. Impressão: contexto0x138, 1b57340/1b5a420 e BackgroundDrawer.
  Contextos dos IDs7911/7913 seguem abertos. Não repetir os três lotes de18/10.
- Contratos12/lógica15/UI16: ampliar operações e duas propostas, com nuvem adiada pelo usuário;
  23 subconjuntos parciais e 37 módulos/49 interfaces documentados.
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

O último comando exige dependências Linux e tela para completar 290 testes sem
skips. Fluxos manuais de CI: `no-vm-validation.yml` (fonte/corpus),
`linux-flatpak.yml` (fonte/payload/sandbox) e `delivery-audit.yml` (bundle
publicado reinstalado sem rebuild). Fontes/licenças, builder pareado e
`runtime-lib` devem ser preservados. Instruções: [instalação](instalacao.md).
