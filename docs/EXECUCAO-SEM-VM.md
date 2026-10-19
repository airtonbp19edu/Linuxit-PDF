# Execução abrangente sem VM — 19/10/2026

Pedido: completar todo trabalho que não exige executar o Foxit na VM. O estado
por pacote está em `progresso/execucao-sem-vm.json`. Nuvem direta23 permanece
adiada e IA generativa excluída. Nenhum comando é enviado à VM suspensa.

Baseline preservado:0.1.15/d0a6213,490 testes próprios por ambiente. Fonte0.1.16
em desenvolvimento; novo código ainda não tem aprovação Linux/pacote até seus
relatórios serem examinados. Critérios/pesos/paridade integral intactos.

## S01 — seleção por caractere e cursor

Ferramenta Caracteres, separada da seleção por região existente. Usa offsets e
caixas reais PopplerGLib, sem dividir igualmente a largura de palavras. Arrasto
em qualquer direção, seleção parcial, cursor, setas visuais, Shift para ampliar,
Home/End e Ctrl+A/C. Combinações, ZWJ, modificadores de tom e pares regionais são
agrupados para evitar cortes internos nesses casos. Não é implementação integral
de todas as regras Unicode de grafemas nem correção universal da ordem de um PDF.
Conserva a ordem Unicode entregue pelo extrator; não inverte strings RTL.

Até100000caracteres por página; divergência entre caixas e texto é recusada.
Worker isolado/cancelável, sessão autenticada com lease e permissão de cópia.
Cache e callbacks vinculados à sessão/página/rotação. Seis portáveis passaram;
dois testes Linux/GTK preparados, incluindo largura variável real e CropBox/rotação.
Novo typelib PopplerGLib e biblioteca pareada integram a receita de build.

Referência: [PopplerPage/get_text_layout](https://poppler.freedesktop.org/api/glib/poppler-Poppler-Page.html).
Esse contrato próprio não é observação Foxit nem aceitação de toda a família.

## Fila

S02 eventos/cálculos; S03 anotações; S04 sessão autenticada em edição/impressão;
S05 anexos/índice/idiomas; S06 confiança/tempo; S07 voz/medidas; S08 camadas/mídia/3D;
S09 preferências/conversão/OCR; S10 integrações/plataforma; S11 contratos/aceitação
e estática; S12 suíteLinux/entrega/auditoria. Cada pacote registra o que foi
implementado/testado e o que depende de recursos/contratos ainda indisponíveis.
Não substituir validação física ou do original por testes sintéticos.
