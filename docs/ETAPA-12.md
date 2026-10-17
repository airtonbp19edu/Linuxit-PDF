# Etapa 12 — especificação funcional com lacunas explícitas

Este relatório conserva o marco inicial de 14 subconjuntos/11 propostas.
A [continuação na etapa 15](ETAPA-15.md) implementou o backend de anexos planos;
o registro estruturado atual tem 15 subconjuntos/10 propostas. A especificação
de referência e a fase A continuam abertas.

Em **17/10/2026**, os contratos das 25 famílias identificadas foram organizados
em [JSON estruturado](especificacao-funcional.json) e no
[registro legível](contratos-funcionais.md). Há **50 cenários de aceitação
planejados**, um nominal e um excepcional por família. São uma base de
especificação; não encerram os casos necessários de cada família.

O trabalho pode avançar sem a VM: entradas, saídas, restrições, efeitos,
erros, fontes, testes existentes e lacunas ficam rastreáveis para a
implementação incremental. A validação do comportamento Foxit e a consolidação
completa da fase A continuam dependentes das análises/observações pendentes.

## O que foi formalizado

- **14 famílias com algum subconjunto atual**: abertura/renderização, navegação,
  apresentação, três fontes de busca, seleção, impressão, imposição, painéis
  de marcadores/anotações/camadas, distância simples e aparência. Um painel
  somente leitura não é edição/persistência; nomes de camadas não são mídia/3D.
- **11 famílias somente como propostas futuras**: busca em anexos, índice de
  coleção, modos linguísticos avançados, formulários, anexos/portfólios,
  assinaturas, proteção completa, acessibilidade, nuvem, conversão e integrações
  completas de plataforma. A existência de adaptadores parciais ou de uma
  tentativa de senha vazia não encerra essas famílias.
- Cada registro identifica o estado da implementação segundo a matriz atual,
  comportamento próprio ou proposto, cenários, efeitos e lacunas da referência.
  Os valores esperados/observados no Foxit ficam `null`, sem inventar resultados.
- Índices internos de página usam base zero; páginas nos relatórios de
  observação usam base um. Reaproveitamento MIT permanece distinto da
  recuperação do original. Inventário global e denominador de paridade seguem
  abertos; a versão publicada continua 0.1.1 `devel`.

O detalhamento conserva limites encontrados no código: consulta de até 256
caracteres; limite padrão de 5.000 hits; destino ausente sem página/retângulo
inventados; busca de assunto/conteúdo sem autor; N-up em 1/2/4/6/9/16; distinção
entre frente/verso manual e duplex; distância simples em centímetros e modos
de aparência system/light/dark. Esses limites são do contrato próprio atual,
sem atribuir equivalência ao Foxit.

Para funcionalidades não implementadas, cada cenário descreve uma proposta
testável e os documentos de laboratório ainda necessários. Nenhum envio remoto,
uso de certificado pessoal, atualização, associação de arquivos ou impressão
física é autorizado/executado apenas por constar na especificação. Operações
externas continuam requerendo sua tarefa específica.

## Verificação do material

`scripts/validate_functional_spec.py` cruza os 25 IDs com a matriz, verifica
referências ao código/evidências, resolve nomes de testes por AST sem carregar
GTK, confere IDs dos planos D/UI e rejeita mistura entre proposta, execução e
paridade. O Markdown é derivado do JSON para evitar duas especificações
divergentes.

```powershell
python scripts/validate_functional_spec.py --check-render docs/contratos-funcionais.md
```

Para atualizar o registro depois de editar o JSON:

```powershell
python scripts/validate_functional_spec.py --render docs/contratos-funcionais.md
```

Foram conferidas 19 referências distintas a testes e 25 fontes locais. Dez
verificações portáveis de subcondições do código passaram: metadados, destinos
de marcadores, campos de comentários, tamanho de consulta, consulta vazia e
cancelada previamente, palavra Unicode, identidade alterada, ordem de livreto,
N-up fracionário e PDF vazio. Elas não executam os 50 planos completos nem a
suíte GTK. O relatório da rodada está em
[etapa-12-especificacao-2026-10-17.json](../testes/resultados/etapa-12-especificacao-2026-10-17.json).

## O que permanece pendente

O critério de detalhamento da etapa 12 passa de `pending` a **`partial`**:
há registro para as 25 famílias, mas propostas, subfunções não implementadas,
fixtures ausentes e comportamento original desconhecido impedem fechar a
especificação de referência. A consolidação da fase A continua `pending`.
Critérios e pesos não mudaram: **etapa 12 com 12,5% verificados**, progresso
geral **43,33%**, catálogo **209 entradas** e paridade **0/25 famílias**.

Próximo passo: especializar o corpus e transformar os cenários em casos
executáveis por família. Primeiro comparar abertura, busca, navegação e prévia
com a mesma fixture no original, quando a VM estiver pronta. Para famílias
futuras, localizar o fluxo correspondente e confirmar disponibilidade Reader
antes de adotar uma proposta como contrato recuperado. A ambiguidade dos IDs
7911/7913, campos incompletos de busca e geometria de impressão continua aberta.
