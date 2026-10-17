# Reflow — sincronização examinada estaticamente

Rodada reflow-locks-2026-10-17, sem executar o original. Entrada fixada pelo
SHA-256 90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6.
Ghidra 12.1.4, Temurin 21, script de sementes REA e perfil direto -noanalysis;
não é uma nova resposta do MCP REA. PE/IAT conferidos com pefile e Capstone 5.0.6.

| Entrada x86 | Bytes | Resultado examinado |
|---|---:|---|
|0x1f21a80|35|Guarda nula e salto a 0x1f22620; chamada IAT 0x531cb70 → KERNEL32!EnterCriticalSection|
|0x1f21ac0|35|Guarda nula e salto a 0x1f22650; chamada IAT 0x531cb74 → KERNEL32!LeaveCriticalSection|

São duas entradas únicas adicionais, 70 bytes e 32 instruções nas funções de
entrada, com endereços/cobertura de bytes conferidos. Helpers examinados para
resolver imports não são somados como novas funções únicas. O catálogo passa
a 252 entradas (152 REA + 100 diretas exclusivas); denominador global desconhecido.

A hipótese anterior sobre o par chamado em torno de campos de reflow +0x8c e
contexto +0xb8 recebe apoio estático de sincronização Win32. Isso não prova a
tipagem completa, ownership ou ciclo de vida de todos os layouts/renderers.
Não equivale a observar concorrência/UI original nem autoriza promoção de paridade.

Metadados: [sementes](windows-evidence/foxit-rea/reflow-locks-2026-10-17-seeds.tsv),
[rodada](windows-evidence/foxit-rea/headless-cross-checks-reflow-locks-2026-10-17.json),
[instruções](../testes/resultados/reflow-locks-2026-10-17/machine-checks.json),
[imports](../testes/resultados/reflow-locks-2026-10-17/import-joins.json).
Projeto e respostas integrais preservados fora do Git em
analysis-local/headless/reflow-locks-2026-10-17/. Não repetir estas duas entradas.
Próximos alvos: slots layout/renderer, tipos/ownership, campos da busca
3/5/6/7/12/16/20 e ambiguidade contextual dos IDs 7911/7913.
