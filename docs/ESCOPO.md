# Escopo autorizado do Linuxit PDF

O objetivo é uma implementação independente das funcionalidades PDF aprovadas,
com Linux prioritário, Flatpak nos marcos de entrega e Windows posteriormente.
A referência é o Foxit Reader 2025.2.0.33046 x86, identificado em
[projeto.json](../progresso/projeto.json). A base própria MIT e a licença BSD
do pypdf permanecem preservadas. UPDF continua fora do escopo.

## Exclusão de IA — decisão do usuário em 17/10/2026

O usuário declarou não ter interesse na IA integrada e autorizou deixá-la de
fora. O **assistente de IA do Foxit e recursos generativos** estão excluídos
das próximas análises, da implementação e dos critérios de paridade. Isso
inclui chat e resumo, tradução ou explicação de documentos por IA.

O módulo `plugins/AiAssistant.fpi` e rótulos do assistente já constavam do
inventário geral de arquivos/importações/controles. Essa presença foi
incidental: as últimas rodadas trataram de busca, impressão, interface e
arquitetura, sem investigação dirigida desse plugin nem implementação de IA.
Os inventários históricos são preservados para manter a proveniência.

A decisão estruturada está em `scope_exclusions` de
[projeto.json](../progresso/projeto.json), com data/hora, origem do pedido e
efeitos. Os contratos, a arquitetura e o registro de pendências apontam para
essa decisão. Não programar alvos, cenários ou entregas específicos de IA.

As **25 famílias já identificadas** não incluíam uma obrigação dedicada de IA;
nenhuma linha foi removida da matriz para elevar percentuais. Busca literal,
índice, stemming, acessibilidade, formulários e colaboração sem IA continuam
nos escopos já registrados. Novas funcionalidades descobertas devem ser
classificadas conforme esta exclusão antes de criar uma obrigação.

Pesos e critérios das 21 etapas permanecem inalterados. Progresso geral
43,33%, catálogo histórico 209 e paridade comprovada 0/25 permanecem iguais.
O inventário funcional autorizado ainda está aberto; a exclusão não fecha
a fase A nem resolve as pendências da VM.


Em 2026-10-17T19:20:19-03:00, o usuário decidiu: **“Deixar nuvem para depois”**.
A integração de nuvem fica adiada; a família permanece no inventário das 25,
sem alteração dos pesos ou critérios. Prioridade atual: operações PDF locais.


Em 2026-10-17T20:51:10-03:00, o usuário autorizou o [fluxo de pastas sincronizadas](PASTAS-SINCRONIZADAS.md).
O Linuxit trabalha com arquivos locais; o cliente externo gerencia a nuvem.
APIs de provedor, login, upload e colaboração remota continuam adiados.
Nenhuma família foi removida ou peso alterado.


Em 2026-10-20T12:41-03:00, a pedido do usuário ("fechar logo esse ciclo"), a família Nuvem/colaboração
passou a ser atendida pelo fluxo de pastas sincronizadas decidido em 17/10/2026: o contrato
deixou de ser proposta e os casos S12-23 verificam esse fluxo (etapa E28). Login em provedor,
transferência por API e colaboração remota continuam adiados; pesos e critérios não mudaram.


Em 2026-10-20T21:18-03:00, o usuário decidiu deixar a **renderização 3D** (U3D/PRC/glTF, girar,
vistas, árvore de peças, medidas) para uma atualização futura. Fica no inventário como pendente
adiada (operação `layers-media/3d`); hoje há imagem de apresentação e extração do modelo. Tudo o
que foi levantado está em [ESTUDO-3D-U3D-PRC.md](ESTUDO-3D-U3D-PRC.md). Pesos e critérios não mudaram.
