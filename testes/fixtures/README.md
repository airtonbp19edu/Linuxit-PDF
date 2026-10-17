# Fixture de busca

`busca-escopos.pdf` é gerado pelo código próprio de `tests/test_search_scopes.py`.
Contém duas páginas, marcador com destino, marcador sem destino local e uma nota
com assunto/conteúdo distintos. Não contém dados pessoais nem material do Foxit.

Consulta `alvo`, sem distinguir maiúsculas, na implementação Linuxit:

- somente texto: três ocorrências (duas com palavra inteira);
- somente marcadores: dois resultados, um sem destino local;
- somente comentários: um resultado;
- consulta `assunto`, somente comentários: um resultado no campo assunto.

Esses são valores esperados do contrato próprio. O mesmo arquivo será usado na
comparação com o Foxit quando houver ambiente Windows/x86 operacional.

## Fixture de anexos

`anexos-simples.pdf` é um PDF próprio sintético, gerado com o pypdf BSD já
incluído: uma página em branco e `nota-sintetica.txt` embutido no catálogo plano.
`anexos-simples.json` conserva texto, tamanho e SHA-256 do anexo e do PDF.
Os testes em `tests/test_pdf_attachments.py` geram também nomes perigosos,
duplicados, limites e recursos ainda não suportados em pastas temporárias.
Não há dados pessoais, recursos Foxit ou observação do original nesse corpus.
