# Aceitação própria S12 executável

Os 59 planos de aceitação de `docs/especificacao-funcional.json` têm casos
executáveis. Cada caso segue o texto dado/ação/esperado da especificação, por uma
fronteira pública do aplicativo: o worker de linha de comando usado pela
interface, o módulo que a interface chama ou a própria janela GTK.

- `casos.py`: 44 casos sem tela.
- `casos_gtk.py`: 13 casos com a janela real (navegação, apresentação, seleção
  de resultados, área de transferência, régua, diálogo de campos XFA e pasta
  sincronizada).
  Precisam de `DISPLAY`.
- `casos_portal.py`: 2 casos S12-25 com o portal real do desktop
  (`xdg-desktop-portal-gtk`), conduzidos por `xdotool`. Precisam de `DISPLAY`.
- `fixtures/`: PDFs sintéticos próprios gerados por `gerar_fixtures.py`, sem
  material Foxit. `manifest.json` fixa tamanho e SHA-256; o executor recusa
  fixtures divergentes. `gerar_fixtures.py --check` confirma os bytes.

Os casos S12-23 (nuvem) verificam o fluxo de pasta sincronizada escolhido pelo usuário;
login, transferência por API e colaboração remota continuam adiados e não têm casos.

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
