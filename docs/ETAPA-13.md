# Etapa 13 — revisão do projeto de arquitetura

O marco abaixo tinha 19 módulos/11 interfaces. A [etapa 15](ETAPA-15.md)
acrescentou o backend de anexos; a [etapa 16](ETAPA-16.md) ligou o painel no
código. O inventário atual tem 21 módulos/15 interfaces, sem alterar os critérios
de projeto já verificados.

Em **17/10/2026**, a arquitetura foi revisada para a versão **0.1.1**, seguindo
os contratos detalhados da etapa 12. Os dois critérios da etapa 13 já estavam
`done` no roteiro; esta rodada amplia sua rastreabilidade sem aumentar o
percentual nem declarar implementação completa.

## Entrega desta rodada

- [Arquitetura revisada](arquitetura.md), com responsabilidades, comunicação
  entre módulos, concorrência, limites e extensões futuras.
- [Inventário estruturado](arquitetura-componentes.json): 19 módulos próprios,
  11 referências de interfaces e vínculo com as 25 famílias da especificação.
- [Registro de pendências](../progresso/pendencias-analises.md) e
  [fonte estruturada](../progresso/pendencias-analises.json): os 21 critérios
  ainda abertos em 14 etapas, com causa e próximo passo.
- [Verificador estrutural](../scripts/check_architecture.py) e
  [resultado examinado](../testes/resultados/etapa-13-arquitetura-2026-10-17.json).

A revisão explicita o ciclo adiado `rendering`/`search_engine`, as chamadas
diretas/dicionários entre UI e serviços e o cancelamento que não interrompe
uniformemente todos os trabalhos. Marcas/legendas de mosaico usam Cairo;
na ausência dele esse ramo retorna sem desenhá-las. A validação de livreto
portável não cobre essa capacidade. Esses pontos ficaram registrados sem
alterar comportamento da aplicação nesta rodada.

As extensões futuras permanecem propostas: seus módulos não foram criados e
seus contratos não viraram funcionalidades por constarem da arquitetura.
O trabalho de edição, integrações e engenharia reversa das demais famílias
segue nos respectivos critérios abertos.

## Verificações

```powershell
python scripts/check_architecture.py
python scripts/validate_functional_spec.py --check-render docs/contratos-funcionais.md
```

O verificador lê AST, confere módulos e símbolos existentes, verifica os sete
fechamentos locais sem import de `gi`/Cairo e cruza famílias com a etapa 12.
Também exige que o registro de pendências inclua exatamente os critérios
abertos do progresso, conservando nomes/estados e causas não confirmadas nulas.
Não importa GTK nem executa Foxit ou operações de impressão.

O relatório com hashes dos módulos registra a fonte examinada. A suíte GTK no
Linux e o Flatpak não foram executados novamente. Catálogo 209, versão 0.1.1,
progresso geral **43,33%**, etapa 13 **100% dos dois critérios de projeto** e
paridade **0/25** permanecem preservados. Pesos e critérios não mudaram.

## Continuidade com VM e limites de análise

Etapas 10, 11, 12, 18 e 19 têm pendências diretas de observação/comparação do
original; a auditoria final da 21 depende também desses resultados. Etapas
11/12 têm, além disso, trabalho estático, corpus e especificação que avançam
sem VM. As análises 03/05/07/08/09 e a implementação 15/16 também têm tarefas
próprias; a VM não encerra essas lacunas por si só.

Os relatórios examinados comprovam timeouts de autoanálise de 1.801,7 segundos
e 600 segundos. Não comprovam esgotamento de tokens. O registro mantém esse
motivo desconhecido (`null`) e trata interrupção futura de contexto/tokens
como risco de continuidade, com checkpoint após cada lote de alvos. Os chats
perdidos não foram usados para inventar a causa de análises parciais.

Próximo passo independente da VM: especializar fixtures e converter os casos
próprios da etapa 12 em verificações executáveis; validar o ramo Cairo do
mosaico em Linux. Para engenharia reversa, retomar os alvos exatos da etapa
11 e de impressão, preservando rodadas e assinaturas provisórias. Na VM,
validar o ambiente offline antes de observar D01–D20 e UI01–UI10.
