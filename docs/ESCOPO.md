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
