# Aceitação própria S12 executável

Os 50 planos de aceitação de `docs/especificacao-funcional.json` agora têm casos
executáveis. Cada caso segue o texto dado/ação/esperado da especificação, por uma
fronteira pública do aplicativo: o worker de linha de comando usado pela
interface, o módulo que a interface chama ou a própria janela GTK.

- `casos.py`: 36 casos sem tela.
- `casos_gtk.py`: 10 casos com a janela real (navegação, apresentação, seleção
  de resultados, área de transferência e régua). Precisam de `DISPLAY`.
- `fixtures/`: PDFs sintéticos próprios gerados por `gerar_fixtures.py`, sem
  material Foxit. `manifest.json` fixa tamanho e SHA-256; o executor recusa
  fixtures divergentes. `gerar_fixtures.py --check` confirma os bytes.

Fora desta execução: S12-23 (nuvem direta, adiada pelo usuário) e S12-25
(plataforma, proposta ainda sem contrato próprio implementado).

## Executar

```bash
dbus-run-session -- xvfb-run -a python3 scripts/run_acceptance.py run \
  --output testes/resultados/aceitacao/<data>/execucao.json
python3 scripts/run_acceptance.py apply --results testes/resultados/aceitacao/<data>/execucao.json
python3 scripts/validate_functional_spec.py --render docs/contratos-funcionais.md
```

`apply` só aceita execuções de uma revisão limpa. O validador confere cada
`execution_status` contra o arquivo de resultado (mesmo caso, estado, horário,
fronteira e revisão). Um teste unitário relacionado nunca conta como execução.

Um caso aprovado é resultado do contrato próprio naquela revisão. Não é
observação do Foxit, paridade nem aceitação da família inteira.
