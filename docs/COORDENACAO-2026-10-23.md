# Coordenação e retomadas de 23/10/2026

O usuário pediu trabalho simultâneo do Claude e do Codex, continuidade autônoma
das tarefas elegíveis e uso da VM, respeitando os controles já registrados.
A divisão completa está em [DIVISAO-TAREFAS](DIVISAO-TAREFAS-2026-10-23.md).
O ajuste posterior desse documento prevalece sobre a tabela inicial histórica.

| Responsável | Frente vigente |
|---|---|
| Codex | S1, S3/C1, S2, S4 e operação exclusiva da VM/E30 |
| Claude | Instalador Windows/E34; correções medidas no app, testes e aceitação; kitE23; propostaB3; revisão do candidato0.1.19 |

Codex criou a automação **retomar-linuxit-pdf-s-05-30**, ativa, para uma retomada
às **05:30 de23/10/2026, America/Sao_Paulo**, neste mesmo chat. A programação
foi confirmada pelo aplicativo. O prompt foi ajustado à divisão aceita e manda
reler os registros antes de agir, evitando execução concorrente na VM.

Claude confirmou em `CHAT-CLAUDE.txt` que agendou a própria retomada às05:10.
Codex não controla nem verificou diretamente a agenda do Claude: essa informação
é a confirmação recebida do outro agente. A retomada do Codex é local e depende
de o computador e o aplicativo estarem disponíveis no horário.

## Comunicação e exclusividade

- Claude escreve somente `CHAT-CLAUDE.txt`; Codex escreve somente
  `CHAT-CODEX.txt`. Cada um lê o arquivo do outro. `CHAT-IA.txt` é histórico.
- O formato anterior perdeu linhas por gravações concorrentes do arquivo
  inteiro. Não reconstruir esse histórico por suposição nem apagar mensagens.
- Codex envia sinais no ramo `codex/vm-status` enquanto opera a VM. Nesta
  rodada os sinais foram publicados por avanço normal, sem force push e sem
  alterar a main ou o índice de trabalho.
- Antes de retomar a VM, conferir se Claude assumiu a operação pelo protocolo
  de transferência. Um sinal antigo não autoriza dois operadores simultâneos.
- Divergência medida deve conter caso, resultado Foxit, resultado Linuxit e
  caminho das evidências para Claude corrigir. Decisão de comportamento que
  ainda não tenha autorização permanece para o usuário.
- Manter os segundos do relógio e a resposta da interface sob observação.
  Se parar, suspender entradas, salvar última ação confirmada e avisar; não
  reiniciar automaticamente. Contenção offline continua obrigatória.

## Limites que continuam vigentes

Não publicar releases, decidirB3, alterar critérios/pesos ou executar o Foxit
fora da contenção por inferência deste pedido. IA permanece excluída; nuvem
direta e3D permanecem adiados. Coautoria dos novos commits do Codex segue a
[escolha confirmada](COAUTORIA-CODEX-2026-10-23.md): Airtonautor e trailerCodex.

O checkpoint técnico fica em [RETOMADA](RETOMADA.md), nos
[avisos](AVISOS-E-STATUS.md) e nas notas de continuidade, com horário real.
Agendar a retomada e preparar mapas não encerra S1/S2/S3/S4 ou E30.
