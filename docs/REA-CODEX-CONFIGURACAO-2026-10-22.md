# REA no Codex — configuração e capacidades

Conferido em 2026/10/22 às 00:43 (America/Sao_Paulo, UTC-03:00).

## Resultado confirmado

- REA **6.7.0** registrado em `C:\Users\Airtonbp19\.codex\config.toml`, usando o Node24.22.0 já instalado e o launcher local do pacote. Não depende de baixar pacote a cada início.
- Configuração anterior preservada em `config.toml.rea.backup`, hash conferido. Todas as configurações não relacionadas ao REA permaneceram semanticamente iguais.
- Skill `reverse-engineer-anything` versão42 instalada em `C:\Users\Airtonbp19\.agents\skills\reverse-engineer-anything`. Somente Codex configurado; outros clientes não foram alterados.
- `rea doctor --client codex --provider ghidra --json`: saudável; registro `aligned`; Ghidra12.1.4/JDK21.0.12.1 aprovados.
- Cliente MCP temporário iniciou **o comando exato registrado**, negociou protocolo2025-11-25, recebeu servidorREA6.7.0, listou207 ferramentas e chamou `binary_session` com sucesso. Sem binário aberto, sem execução do original e sem acessar a VM. O processo temporário próprio foi encerrado ao terminar.

**Reinicie o Codex para carregar o servidor no chat.** A conexão foi testada com cliente independente; o catálogo deste chat ainda não inclui REA. Não repetir setup apenas porque uma sessão já aberta ainda não recebeu as ferramentas. Ver [documentação oficial de MCP no Codex](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).

Recibo publicável: [codex-registration-2026-10-22.json](../testes/resultados/e21-rea-pc/codex-registration-2026-10-22.json). Respostas completas e hashes ficam em `analysis-local/rea-instalacao/`, ignorado pelo Git. A configuração privada não foi copiada para o repositório.

## O que podemos fazer com o provedor disponível

Depois de abrir um alvo admitido e concluir a análise estática do Ghidra:

1. Inventariar funções, segmentos, símbolos e strings de executáveis e DLLs nativos compatíveis.
2. Ler assembly, instruções, bytes e pseudocódigo de funções. Pseudocódigo é uma interpretação do decompilador, não recuperação literal do código-fonte original.
3. Buscar strings e padrões de bytes; seguir referências cruzadas e identificar chamadores/callees e alvos de chamadas resolvidos.
4. Examinar tipos e estruturas reconhecidos pelo analisador, endereços e correspondência com offsets no arquivo; registrar campos não resolvidos como hipóteses.
5. Produzir evidências rastreáveis para especificar e comparar a implementação própria. O servidor também oferece inventário de pacotes/artefatos, análise estática JavaScript/Electron e metadados/membros.NET sem executar o alvo, dentro dos respectivos limites.

Para o Linuxit PDF, isso permite continuar os alvos estáticos de busca, impressão e reflow já registrados, sem rodar o Foxit e sem VM. Retomar os resultados preservados; este setup não refez análise nem avançou os critérios de reconstrução. O próximo alvo depende da fila vigente.

## Limites confirmados

- As207 ferramentas do catálogo incluem recursos de outras plataformas e provedores. Não declarar todas disponíveis. IDA, JADX, Kuna, Hopper e outras dependências opcionais não foram instaladas nesta configuração.
- No Windows, o perfil GhidraP0 admite alvos PE nativos compatíveis e exige caminhos locais NTFS e controles de admissão. Não presumir suporte de um caminho sincronizado ou a um alvo específico só porque `doctor` passou.
- Nesse perfil, **anotar/renomear funções e modificar o banco Ghidra não estão disponíveis**. Podemos registrar interpretações e nomes propostos nas notas próprias.
- Operações nativas só respondem depois da análise automática completa. O teste atual verificou conexão e disponibilidade declarada, não desempenho nem conclusão da análise de um executável grande.
- Testes dinâmicos e comparação visual continuam sujeitos à contenção e às autorizações da VM. REA não substitui a VM, não reconstrói automaticamente todo o aplicativo e não comprova paridade sozinho.

## Depois de reiniciar

Verificar se `binary_session` aparece entre as ferramentas e conferir identidade6.7.0. Se o registro continuar alinhado e as ferramentas não aparecerem, ler o erro de inicialização do cliente; não reinstalar repetidamente. Pelo terminal, `rea` já funciona com os caminhos configurados.
