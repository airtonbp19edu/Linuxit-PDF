# Etapa 16 — integração do painel Anexos

Retomada posterior: [geometria corrigida e pacote 0.1.3](ETAPA-16-LAYOUT.md),
114/114 por ambiente e capturas examinadas; o histórico abaixo foi preservado.

Atualização posterior deste checkpoint: a [etapa 20](ETAPA-20.md) validou
fonte e Flatpak 0.1.2 em Linux, com 104/104 testes em cada ambiente
fonte/payload/sandbox e cinco casos GTK do painel. O relato abaixo
preserva os resultados e limites da rodada original.

Em **17/10/2026**, o backend da etapa 15 foi ligado ao código da interface GTK.
Há um painel **Anexos** na barra lateral e em **Exibir → Anexos**, com listagem,
**Atualizar** e **Salvar selecionado…**. Esta entrega é de código-fonte em
desenvolvimento após o Flatpak 0.1.1. A IA continua [fora do escopo](ESCOPO.md).

## Fluxo implementado no código

A listagem é iniciada ao abrir o painel, evitando analisar anexos de todo PDF
que o leitor abre. O usuário escolhe uma entrada e uma pasta existente.
Cancelar o seletor não inicia gravação. Arquivos existentes permanecem
intactos; o painel pede outra pasta em caso de conflito. Nomes que o backend
recusa podem ser vistos, com o motivo; o botão de salvar fica desativado para
essas entradas. O conteúdo não é aberto/executado automaticamente.

O [controlador portável](../app/attachment_tasks.py) publica estado para os
widgets e chama o worker em subprocesso com UTF-8 explícito. Gerações de
documento/lista e um token capturado antes do diálogo impedem usar seleção
obsoleta. Callbacks antigos não substituem o novo documento. O painel permite
somente uma extração por vez; botões são reabilitados ao terminar ou falhar.
As mensagens do worker aparecem em linguagem de usuário, sem traceback.

Uma extração já confirmada pode concluir após trocar de documento. O resultado
antigo não altera o status do novo. Fechar a janela invalida tarefas pendentes
e callbacks; um subprocesso já iniciado não tem interrupção imediata garantida.
Os limites e casos ainda não suportados do [backend](ETAPA-15.md) continuam:
catálogo plano, sem portfólios, /Kids, senha não vazia ou anexos só de anotações.

Os nomes são rótulos de texto, sem interpretar markup, e caracteres de controle
são substituídos na apresentação. A lista conserva seus índices próprios,
incluindo nomes duplicados. A navegação por teclado dentro dela não é tomada
pelos atalhos de página da janela.

## O que foi verificado

**14/14 testes portáveis do controlador passaram**. Usam callbacks adiados
controlados para provocar corridas e o worker real com PDFs sintéticos para
listar, salvar e gerar conflito. Cobrem carga sob demanda, resultado/erro
obsoleto, seleção inválida após atualizar, cancelamento, bloqueio de nomes,
estado ocupado, troca de documento, fechamento antes de iniciar, confirmação
inválida e mensagens de erro.

Uma primeira rodada teve 13 sucessos e uma falha: caracteres acentuados no
stderr do worker estavam sendo decodificados incorretamente no Windows.
O subprocesso passou a usar `-X utf8`; a rodada corrigida passou integralmente.
Os dois relatórios foram preservados:

- [Primeira rodada](../testes/resultados/etapa-16-controlador-tests-2026-10-17.json).
- [Rodada corrigida](../testes/resultados/etapa-16-controlador-tests-fixed-2026-10-17.json).

## Validação visual ainda pendente

**Nenhum teste GTK foi aprovado nesta rodada.** Os quatro casos de
[test_attachment_panel_gtk.py](../tests/test_attachment_panel_gtk.py) foram
descobertos e marcados `skipped`, pois esta máquina não oferece GTK/tela X11 ou
Wayland. `wsl --list --quiet` reconfirmou que o WSL não está instalado.
O controlador com runner de testes não valida widgets, layout ou dispatch GTK.

O [relatório de disponibilidade](../testes/resultados/etapa-16-gtk-disponibilidade-2026-10-17.json)
conserva **0 aprovados, 4 skips**. São casos de salvar/conflito, cancelar pasta,
trocar documento durante diálogo e selecionar nome inválido. Não houve GUI,
suíte completa Linux, renderização visual do novo painel ou Flatpak novo.

O [resumo técnico do marco](../testes/resultados/etapa-16-painel-anexos-2026-10-17.json)
registra hashes da fonte e verificações estruturais, com essa limitação explícita.

No Linux com dependências e tela disponíveis, executar com nomes de saída novos:

```bash
/usr/bin/python3 scripts/run_tests.py --pattern test_attachment_panel_gtk.py --output testes/resultados/painel-gtk-proxima-rodada.json
/usr/bin/python3 scripts/run_tests.py --output testes/resultados/source-proxima-rodada.json
```

O teste portável pode ser repetido no ambiente atual sem VM:

```powershell
python scripts/run_tests.py --pattern test_attachment_tasks.py --temp-dir analysis-local/test-temp-proxima --output testes/resultados/controlador-proxima-rodada.json
```

## Estado de continuidade

O critério abrangente da etapa 16 passa de `pending` a **`partial`**, apoiado
no controlador testado e no código conectado à janela, sem declarar os widgets
validados. Os critérios/pesos e a revisão permanecem iguais. Etapa 16 com
**33,3% verificados**, roteiro **43,33%**, catálogo original **209** e paridade
**0/25**. Arquitetura atual: 21 módulos, 15 referências de interfaces e nove
fechamentos locais sem gi/Cairo; as 25 famílias mantêm 15 subconjuntos/10 propostas.

Próximo passo: executar esses quatro testes e a suíte real GTK/Linux, corrigir
o que for encontrado e inspecionar o painel. Isso exige runtime Linux adequado,
sem depender da VM Windows para o Foxit. A comparação com o original segue
separada no [registro de pendências](../progresso/pendencias-analises.md).
