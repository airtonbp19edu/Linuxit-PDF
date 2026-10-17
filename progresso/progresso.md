# Progresso verificável

Progresso geral do roteiro: **43.33%**. Cada etapa usa o peso do pedido; dentro dela, atividades têm pesos estimados, registrados no JSON. Somente atividades com estado `done` e evidência existente contam. Isso mede entregas do roteiro, não equivalência do aplicativo.

Paridade Foxit verificada: **0/25 obrigações identificadas (0.00%)**. O inventário funcional permanece aberto. Testes próprios não contam como testes diferenciais.

Cobertura global de engenharia reversa: **não calculável** enquanto o universo de funções e seus pesos não estiver fechado. Medida parcial: quatro módulos com decompilação dirigida entre 141 PE inventariados (2,84%, peso unitário por módulo); 256 entradas distintas examinadas. 9.973 slots não constituem um denominador de funções únicas.

| Etapa | Peso | Fração verificada | Contribuição |
|---|---:|---:|---:|
| 01 — Diagnóstico e preparação | 3% | 80.0% | 2.40% |
| 02 — Identificação dos arquivos | 3% | 100.0% | 3.00% |
| 03 — Identificação tecnológica | 4% | 50.0% | 2.00% |
| 04 — Extração e desempacotamento | 5% | 100.0% | 5.00% |
| 05 — Mapeamento de dependências | 4% | 42.9% | 1.71% |
| 06 — Análise estática inicial | 5% | 100.0% | 5.00% |
| 07 — Catalogação das funções | 5% | 33.3% | 1.67% |
| 08 — Descompilação profunda | 10% | 13.0% | 1.30% |
| 09 — Reconstrução dos fluxos internos | 7% | 9.1% | 0.64% |
| 10 — Análise dinâmica | 6% | 0.0% | 0.00% |
| 11 — Engenharia reversa da interface | 4% | 25.0% | 1.00% |
| 12 — Especificação funcional | 4% | 12.5% | 0.50% |
| 13 — Projeto de arquitetura | 4% | 100.0% | 4.00% |
| 14 — Criação do projeto | 3% | 100.0% | 3.00% |
| 15 — Reconstrução da lógica principal | 9% | 33.3% | 3.00% |
| 16 — Interface e integrações | 7% | 33.3% | 2.33% |
| 17 — Compilação intermediária | 2% | 100.0% | 2.00% |
| 18 — Testes comparativos | 7% | 10.0% | 0.70% |
| 19 — Correção de incompatibilidades | 4% | 14.3% | 0.57% |
| 20 — Geração dos pacotes | 3% | 100.0% | 3.00% |
| 21 — Auditoria e entrega final | 1% | 50.0% | 0.50% |

A sincronização é medida separadamente em `sincronizacao-git.json`. O hash registrado é sempre de um commit remoto previamente confirmado; um arquivo não pode conter o hash do próprio commit. Consulte também a árvore/HEAD remotos e o estado de trabalho atual.

Este relatório não encerra as 21 etapas. Atividades bloqueadas e parciais contribuem com zero até serem verificadas. Mudanças de critérios/pesos devem ser explicadas no histórico, preservando a comparabilidade.
