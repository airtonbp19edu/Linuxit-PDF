# O que a porcentagem do roteiro mede

**Ainda não há um percentual global confiável de recodificação.** O índice
43,93% foi calculado corretamente pelo modelo registrado, mas é inadequado
para representar o avanço incremental das funcionalidades. A apresentação
anterior dava destaque excessivo a esse número nas respostas sobre o projeto.

A revisão de 18/10/2026 examinou os 55 snapshots de `progresso/progresso.json`
até o commit `bc75bc4dd5b0d17c0626384a4e72e075158263bb`. Conferiu a aritmética
com frações exatas, definições/pesos e os manifestos das 14 versões registradas.
[Evidência estruturada](../testes/resultados/revisao-indicadores-2026-10-18/review.json).
Nenhuma suíte do aplicativo ou análise do original foi executada nesta revisão.

## Por que quase não saiu de 43%

A fórmula soma, em cada etapa:

`peso da etapa × soma dos pesos dos critérios done ÷ soma dos pesos de todos os critérios`

Critérios `partial`, `pending`, `blocked` e `unknown` contribuem com zero.
As duas principais frentes de desenvolvimento possuem critérios muito amplos:

| Etapa | Critério que continua parcial | Efeito na pontuação |
|---|---|---|
|15 — Lógica|Todas as demais famílias implementadas e testadas|OCR, TIFF, formulários e anotações não acrescentam pontos enquanto esse critério inteiro não fechar.|
|16 — Interface|Demais interações e integrações funcionais|Novos diálogos e operações não acrescentam pontos enquanto esse critério inteiro não fechar.|

Esses critérios concentram, respectivamente, 12/18 e 10/15 do peso interno
das etapas. Por isso, ambas continuam em 33,3% dos critérios ponderados, mesmo
após várias entregas. Esse valor não estima quanto da lógica ou da interface
está pronto.

Na história examinada, houve somente duas pontuações:

| Registro | Índice histórico | Motivo |
|---|---:|---|
|Primeiro registro, `0f08daa`|43,33%|37 critérios inteiramente concluídos.|
|A partir de `c403fa7`|43,93%|A consulta às regras remotas do GitHub passou de unknown a done; acréscimo de 0,60 ponto percentual.|

O total atual exato é `777937/17710 = 43,926425748…`, arredondado para 43,93%.
O aumento de 0,60 ponto não quantifica as funcionalidades implementadas nesse
intervalo. Pesos, definições e estados dos critérios foram preservados nesta revisão.

## Evidências de desenvolvimento que o índice não mostra

| Versão | Exemplo de entrega | Testes próprios registrados na fonte |
|---|---|---:|
|0.1.1|Base e marco inicial preservados|37|
|0.1.3|Correção e medição do painel lateral|114|
|0.1.6|Busca ampliada e coleções persistentes|190|
|0.1.9|Pastas sincronizadas locais|290|
|0.1.10|Editor de cópia, histórico e controles de formulário|333|
|0.1.11|OCR local em português/inglês|363|
|0.1.12|TIFF multipágina|380|
|0.1.13|Anotações adicionais e edição de comentário/autor|400|

Os números vêm dos manifestos de cada versão. A 0.1.13 tem 400/400 aprovados
em fonte, payload e sandbox, com 11 relatórios selados reconferidos por hash.
Isso documenta o desenvolvimento e a validação própria; não é porcentagem de
funcionalidades, cobertura de código ou teste diferencial. A população de testes
e o escopo mudam entre versões.

Existem subconjuntos próprios implementados em 23 das 25 famílias identificadas.
Isso não corresponde a 92% do aplicativo pronto: cada família contém quantidades
e complexidades diferentes de operações e continua parcial. O inventário global
do original permanece aberto. Nenhuma família teve paridade integral comprovada.

## Como apresentar o estado daqui em diante

- **Conclusão global da recodificação:** indeterminada; campo
  `implementation_completion_percent: null`.
- **Entregas próprias:** recursos concretos de cada versão, limites, evidências
  de implementação e validação e operações ainda pendentes.
- **Checklist original:** manter o índice histórico 43,93%, com esse rótulo,
  para preservar a série e os critérios. Não usá-lo como porcentagem do código.
- **Comparação com Foxit:** manter separada; depende da referência isolada e
  de comparações por operação. 0/25 famílias integralmente comprovadas não
  significa que nenhuma funcionalidade própria funcione.

Uma futura porcentagem operacional precisa de um catálogo delimitado de
operações, critérios verificáveis e pesos de complexidade explicitados antes
da medição. Dividir critérios amplos pode melhorar a sensibilidade, mas é uma
nova revisão de método: deve preservar o histórico e declarar o denominador.
Não há justificativa para substituir o indicador atual por um número estimado
apenas para fazê-lo subir.
