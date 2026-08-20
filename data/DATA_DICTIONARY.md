# Dicionario de Dados

Este projeto organiza imagens de ressonancia magnetica cerebral em quatro classes.

## Pastas

| Caminho | Descricao |
| --- | --- |
| `data/raw/Training/` | Imagens originais do conjunto de treino. |
| `data/raw/Testing/` | Imagens originais do conjunto de teste. |
| `data/processed/image_inventory.csv` | Inventario com uma linha por imagem. |
| `data/processed/class_summary.csv` | Resumo agregado por conjunto e classe. |

## Classes

| Pasta original | Classe padronizada |
| --- | --- |
| `glioma_tumor` | Glioma |
| `meningioma_tumor` | Meningioma |
| `no_tumor` | No tumor |
| `pituitary_tumor` | Pituitary |

## Campos do inventario

| Campo | Descricao |
| --- | --- |
| `split` | Conjunto padronizado: `train` ou `test`. |
| `label` | Nome legivel da classe. |
| `label_raw` | Nome original da pasta da classe. |
| `file_name` | Nome do arquivo de imagem. |
| `relative_path` | Caminho relativo no projeto. |
| `size_bytes` | Tamanho do arquivo em bytes. |
| `width` | Largura da imagem em pixels. |
| `height` | Altura da imagem em pixels. |
