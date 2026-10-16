# Arquitetura da implementação independente

Linuxit 0.1.0 parte da base própria MIT Print&View 3.4.0/Winux, conforme
`proveniencia-base.json`. Não se apresenta esse reaproveitamento como nova
engenharia reversa do Foxit. O original serve de referência para contratos
específicos; pseudocódigo, DLLs e templates Foxit não entram na aplicação.

- `app/main.py`: interface GTK, navegação e publicação de resultados na geração correspondente.
- `app/search_engine.py`: extração/busca por página; cache limitado e cancelamento.
- `app/pdf_panels.py`: modelo portável de marcadores, comentários e camadas.
- `app/rendering.py`: Poppler para imagem/texto e coordenadas; processos canceláveis.
- `app/imposition.py`: composição PDF e geometria, compartilhada com a preparação da saída.
- `app/print_window.py`, `worker_cli.py`: opções, prévia e preparação assíncrona.
- `app/cups_backend.py`, `windows_print.py`: fronteiras específicas do sistema.
- `app/appearance.py`, `presentation.py`, `page_cache.py`: preferências, apresentação e memória de imagens.

A pesquisa avançada deve expor somente opções implementadas. Escopo por página,
marcadores e comentários usa uma requisição imutável e resultados tipados por
origem. Cancelamento e limite de resultados valem para todos os escopos.
Stemming, proximidade, busca em anexos e índice de coleção permanecem pendentes.

As fases A e B podem avançar por contrato; isso não encerra a análise das demais
famílias. Paridade exige observação do original e teste diferencial, além dos
testes internos. O pacote usa ID próprio e branch Flatpak `devel` até os critérios
de validação serem atendidos.
