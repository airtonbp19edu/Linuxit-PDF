# Etapa 21 — auditoria incremental da entrega

Iniciada em 17/10/2026 após a entrega 0.1.2/devel. O aplicativo e o bundle
publicado serão preservados. Esta etapa não encerra a reconstrução: continuam
abertos os contratos, a implementação de várias famílias, a observação do
original na VM offline e validações de desktop/integração/impressão física.

[`scripts/audit_delivery.py`](../scripts/audit_delivery.py) verifica a identidade
do bundle e das três entregas, os sete relatórios selados do CI, a igualdade
entre fonte atual/snapshot/commit testado, populações e contagens de testes,
licenças MIT/BSD, inventário de dependências e registro de critérios abertos.
Atividades históricas `done` recebem conferência estrutural de links; não se
repete toda a engenharia reversa nem se converte arquivo existente em nova
prova de comportamento.

O modo `--installed-root` confere o deployment informado pelo próprio Flatpak,
o commit OSTree e o runtime registrados, todos os bytes de dependências e da
aplicação, os ELF realmente presentes e os avisos de cada pacote. O fluxo manual
[delivery-audit.yml](../.github/workflows/delivery-audit.yml) instala o **bundle já
publicado**, sem reconstrução, em usuário/runner Linux efêmero, e executa um novo
smoke GTK no sandbox. Nenhum original Foxit é transferido ou executado.

Sete controles sintéticos de recusa passaram localmente, incluindo dependência
alterada, licença ausente, ELF não catalogado, duplicidade, caminho externo e
skip em relatório. A auditoria local passou. Resultado instalado/Linux ainda
pendente neste checkpoint; os relatórios finais serão incorporados após exame.
Os 104 testes por ambiente da etapa 20 são evidência histórica preservada;
a nova suíte de controles do auditor é uma execução parcial separada.

Os critérios/pesos da etapa 21 permanecem: auditoria histórica `done`, encerramento
de obrigações `pending`, sincronização histórica `done`. A fração de 50% e o
roteiro 43,33% não aumentam pela criação deste verificador. Paridade 0/25 e
cobertura global desconhecida. O recorte de cabeçalho lateral continua pendente.
