# Brain Tumor MRI Dataviz

Projeto de visualizacao e organizacao de um dataset de ressonancias magneticas cerebrais, separado entre treino e teste para quatro classes: glioma, meningioma, ausencia de tumor e tumor pituitario.

## Visao Geral

- Total de imagens: 3.251.
- Volume aproximado das imagens: 88,3 MB.
- Dados brutos preservados em `data/raw/`.
- Inventario reproduzivel em `data/processed/image_inventory.csv`.
- Dashboard estatico em `reports/dashboard/index.html`, incluindo graficos exploratorios equivalentes aos do notebook.
- Notebook original preservado em `notebooks/Avaliacao.ipynb`.
- Referencia academica vinculada ao artigo publicado na Revista de Engenharia e Tecnologia.

## Resumo do Dataset

| Conjunto | Classe | Imagens | MB |
| --- | --- | ---: | ---: |
| Teste | Glioma | 87 | 2,49 |
| Teste | Meningioma | 115 | 2,68 |
| Teste | No tumor | 105 | 1,41 |
| Teste | Pituitary | 74 | 5,70 |
| Treino | Glioma | 826 | 19,42 |
| Treino | Meningioma | 822 | 19,33 |
| Treino | No tumor | 395 | 11,03 |
| Treino | Pituitary | 827 | 26,22 |

## Estrutura

```text
.
├── data/
│   ├── raw/                 # imagens originais extraidas do ZIP
│   ├── processed/           # metadados e dados agregados
│   └── DATA_DICTIONARY.md
├── notebooks/
│   └── Avaliacao.ipynb      # notebook original de avaliacao/modelagem
├── reports/
│   └── dashboard/           # painel estatico de dataviz
├── scripts/
│   └── build_metadata.py    # gera inventario, resumo e dados do dashboard
├── requirements.txt
└── README.md
```

## Como Regerar os Metadados

```bash
python scripts/build_metadata.py
```

## Como Abrir o Dashboard

Opcao simples:

```bash
python -m http.server 8000
```

Depois acesse:

```text
http://localhost:8000/reports/dashboard/
```

## Artigo Relacionado

O dashboard referencia o artigo **Convolutional Neural Network Model for Classification and Prediction of Brain Tumor Based on Magnetic Resonance Imaging**, de Gabriel Moraes de Oliveira e Elisangela Gisele do Carmo, publicado em 2025 na Revista de Engenharia e Tecnologia, Vol. 17 No. 1.

- Artigo: <https://revistas.uepg.br/index.php/ret/en/article/view/24630>
- PDF: <https://revistas.uepg.br/index.php/ret/en/article/view/24630/209209219515>

## Observacoes

Este repositorio organiza e visualiza o dataset. Ele nao substitui validacao medica, auditoria de vieses ou documentacao formal de origem/licenca dos dados.
