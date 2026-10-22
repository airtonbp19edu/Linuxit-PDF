# A4 — contratos individuais do inventário conhecido

A A4 detalha as **116 operações conhecidas nas 25 famílias**, preservando o
inventário provisório e as lacunas do original. O registro fonte está em
[contratos-operacoes-v1.json](contratos-operacoes-v1.json), ligado à
[especificação funcional](especificacao-funcional.json). Sua versão legível
integra [contratos-funcionais.md](contratos-funcionais.md), em cada família.

Cada operação possui entradas, saídas, restrições, ao menos um erro específico,
efeitos, fronteira de cancelamento, planos relacionados e fontes com símbolo
Python resolvível por AST. Os 116 registros foram redigidos individualmente;
não são a repetição de um contrato genérico para cada ID. Os limites incluem
as distinções entre seleção e ativação de marcador, cancelamento anterior ou
posterior à publicação, submissão à fila e papel impresso, assinatura de uma
revisão e confiança, marca de redação e aplicação, XFA híbrido e render dinâmico,
texto de anexos e conversão visual, concessão de portal e acesso irrestrito.

## Evidência e limites

O campo `current_bounded_source` descreve o código próprio revisado, dentro dos
limites de cada operação. `pending_environment_or_reference` descreve requisito
dependente do ambiente ou da referência; `deferred_by_user` conserva o adiamento.
Nenhum desses estados é paridade. Os campos `foxit_expected`/`foxit_observed`
ficam nulos e `new_execution_status` fica `not_run`: revisar o contrato não é
executar a operação, o plano S12 ou o original.

As âncoras registram arquivo/símbolo/linhas e SHA-256 do trecho **na revisão do
contrato**. Linhas e hashes não são declarados atuais após toda alteração futura
do código. O validador resolve os símbolos atuais por AST sem importar GTK;
uma mudança de semântica exige revisão humana do texto, além desse controle.
Planos S12 vinculados pertencem à família e podem exercitar só parte da operação.
Não são 116 novas aceitações nem comprovação de todos os estados descritos.

## Como conferir e regenerar

```powershell
python scripts/validate_functional_spec.py --check-render docs/contratos-funcionais.md
python -m unittest discover -s tests -p test_operation_contracts.py -v
```

Depois de alterar o registro ou a especificação:

```powershell
python scripts/validate_functional_spec.py --render docs/contratos-funcionais.md
```

O validador exige igualdade exata de IDs com o inventário, sem faltantes ou
duplicados; vínculo correto às famílias; erros e cancelamento preenchidos;
símbolos locais existentes; referências S12 válidas; e separação explícita
entre proposta, código e observação. Os oito controles do validador incluem
mutações negativas para evitar aprovação por mera existência de arquivo.
O [comprovante desta revisão](../testes/resultados/a4-2026-10-22/review.json)
registra 116 operações, 25 famílias e 95 símbolos de fontes conferidos, além
dos oito testes do validador. As 81 aceitações preservadas continuam vinculadas
a suas próprias revisões; não foram reexecutadas pela A4.

## A4 e o critério amplo da etapa 12

O detalhamento escrito do **inventário conhecido** está completo nesta revisão.
O critério amplo da especificação de referência e a consolidação da fase A
continuam parciais: o universo Foxit permanece aberto, contratos completos do
original não foram observados e há implementações limitadas/adiadas. A decisão
B3 de adotar o inventário fixo como denominador ainda cabe ao usuário. Por isso,
esta entrega não muda pesos, índice do checklist, percentual de recodificação
ou aprovação de qualquer família.

A6 evolui funções próprias em paralelo. Foram incluídas extensões explícitas
nos contratos existentes para JavaScript QuickJS opt-in, cópia XFA de fluxo
próprio, DSS/OCSP e preparação/conclusão offline de carimbo, redação vetorial
conservadora e edição recuperada. As fronteiras de teste/runtime dessas
extensões pertencem aos relatórios A6. Preservar a distinção entre comandos
anteriores e novos; não promover o subconjunto a recurso universal.

A revisão independente da redação vetorial encontrou e corrigiu texto com
contorno largo que escapava da caixa calculada e thumbnails privados que
continuavam referenciados. O perfil passou a recusar `Tr=1/2`, validar finitude
de transformações compostas e remover `/Thumb`/`PieceInfo`/`SeparationInfo` da
página tratada. Três casos adversariais novos e seis existentes passaram.
