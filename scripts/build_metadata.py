from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DASHBOARD_ASSETS_DIR = PROJECT_ROOT / "reports" / "dashboard" / "assets"

LABELS = {
    "glioma_tumor": "Glioma",
    "meningioma_tumor": "Meningioma",
    "no_tumor": "No tumor",
    "pituitary_tumor": "Pituitary",
}

SPLITS = {
    "Training": "train",
    "Testing": "test",
}


def jpeg_size(path: Path) -> tuple[int | None, int | None]:
    """Read JPEG dimensions without loading the full image into memory."""
    with path.open("rb") as file:
        data = file.read(2)
        if data != b"\xff\xd8":
            return None, None

        while True:
            marker_start = file.read(1)
            if not marker_start:
                return None, None
            if marker_start != b"\xff":
                continue

            marker = file.read(1)
            while marker == b"\xff":
                marker = file.read(1)

            if marker in {b"\xc0", b"\xc1", b"\xc2", b"\xc3", b"\xc5", b"\xc6", b"\xc7", b"\xc9", b"\xca", b"\xcb", b"\xcd", b"\xce", b"\xcf"}:
                file.read(3)
                height = int.from_bytes(file.read(2), "big")
                width = int.from_bytes(file.read(2), "big")
                return width, height

            if marker in {b"\xd8", b"\xd9"}:
                continue

            segment_length_bytes = file.read(2)
            if len(segment_length_bytes) != 2:
                return None, None
            segment_length = int.from_bytes(segment_length_bytes, "big")
            file.seek(segment_length - 2, 1)


def normalize_path(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def collect_inventory() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for original_split, split in SPLITS.items():
        split_dir = RAW_DIR / original_split
        for label_dir in sorted(split_dir.iterdir()):
            if not label_dir.is_dir():
                continue
            label_raw = label_dir.name
            label = LABELS.get(label_raw, label_raw.replace("_", " ").title())
            for image_path in sorted(label_dir.glob("*.jpg")):
                width, height = jpeg_size(image_path)
                records.append(
                    {
                        "split": split,
                        "label": label,
                        "label_raw": label_raw,
                        "file_name": image_path.name,
                        "relative_path": normalize_path(image_path),
                        "size_bytes": image_path.stat().st_size,
                        "width": width,
                        "height": height,
                    }
                )
    return records


def build_summary(records: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], dict[str, object]] = {}
    for record in records:
        key = (str(record["split"]), str(record["label"]))
        if key not in grouped:
            grouped[key] = {
                "split": record["split"],
                "label": record["label"],
                "image_count": 0,
                "total_size_mb": 0.0,
            }
        grouped[key]["image_count"] = int(grouped[key]["image_count"]) + 1
        grouped[key]["total_size_mb"] = float(grouped[key]["total_size_mb"]) + int(record["size_bytes"]) / (1024 * 1024)

    return [
        {
            "split": item["split"],
            "label": item["label"],
            "image_count": item["image_count"],
            "total_size_mb": round(float(item["total_size_mb"]), 2),
        }
        for item in sorted(grouped.values(), key=lambda row: (str(row["split"]), str(row["label"])))
    ]


def build_dashboard_data(records: list[dict[str, object]], summary: list[dict[str, object]]) -> dict[str, object]:
    labels = sorted({str(record["label"]) for record in records})
    splits = ["train", "test"]

    counts = {split: {label: 0 for label in labels} for split in splits}
    sizes = {split: {label: 0 for label in labels} for split in splits}
    samples: dict[str, list[dict[str, object]]] = defaultdict(list)
    notebook_sample_grid: list[dict[str, object]] = []
    notebook_comparison: dict[str, dict[str, object]] = {}

    for record in records:
        split = str(record["split"])
        label = str(record["label"])
        counts[split][label] += 1
        sizes[split][label] += int(record["size_bytes"])
        key = f"{split}:{label}"
        if len(samples[key]) < 8:
            samples[key].append(
                {
                    "label": label,
                    "split": split,
                    "file_name": record["file_name"],
                    "path": "../../" + str(record["relative_path"]),
                    "width": record["width"],
                    "height": record["height"],
                }
            )
        if split == "train" and len(notebook_sample_grid) < 25:
            notebook_sample_grid.append(
                {
                    "label": label,
                    "split": split,
                    "file_name": record["file_name"],
                    "path": "../../" + str(record["relative_path"]),
                    "width": record["width"],
                    "height": record["height"],
                }
            )
        if split not in notebook_comparison:
            notebook_comparison[split] = {
                "label": label,
                "split": split,
                "file_name": record["file_name"],
                "path": "../../" + str(record["relative_path"]),
                "width": record["width"],
                "height": record["height"],
            }

    total_size_mb = round(sum(int(record["size_bytes"]) for record in records) / (1024 * 1024), 2)
    return {
        "title": "Brain Tumor MRI Dataviz",
        "generated_from": "data/raw",
        "total_images": len(records),
        "total_size_mb": total_size_mb,
        "labels": labels,
        "splits": splits,
        "counts": counts,
        "sizes_mb": {
            split: {label: round(size / (1024 * 1024), 2) for label, size in split_sizes.items()}
            for split, split_sizes in sizes.items()
        },
        "summary": summary,
        "samples": dict(samples),
        "notebook_views": {
            "sample_grid": notebook_sample_grid,
            "comparison": notebook_comparison,
        },
        "article": {
            "title": "Convolutional Neural Network Model for Classification and Prediction of Brain Tumor Based on Magnetic Resonance Imaging",
            "authors": ["Gabriel Moraes de Oliveira", "Elisangela Gisele do Carmo"],
            "journal": "Revista de Engenharia e Tecnologia",
            "issue": "Vol. 17 No. 1 (2025): Publicacao Continua",
            "published": "2025-02-21",
            "section": "Artigos",
            "license": "Creative Commons Atribuicao 4.0 Internacional",
            "keywords": [
                "Computer Vision",
                "Convolutional Neural Network",
                "Deep Learning",
                "Magnetic Resonance Imaging",
            ],
            "url": "https://revistas.uepg.br/index.php/ret/en/article/view/24630",
            "pdf_url": "https://revistas.uepg.br/index.php/ret/en/article/view/24630/209209219515",
            "summary": "O artigo apresenta uma abordagem experimental com rede neural convolucional de cinco camadas, desenvolvida no Google Colab com Keras e TensorFlow, para classificacao de tumores cerebrais em imagens de ressonancia magnetica.",
        },
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    DASHBOARD_ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    records = collect_inventory()
    summary = build_summary(records)
    dashboard_data = build_dashboard_data(records, summary)

    write_csv(PROCESSED_DIR / "image_inventory.csv", records)
    write_csv(PROCESSED_DIR / "class_summary.csv", summary)

    (PROCESSED_DIR / "dashboard_data.json").write_text(
        json.dumps(dashboard_data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (DASHBOARD_ASSETS_DIR / "dashboard-data.js").write_text(
        "window.DASHBOARD_DATA = "
        + json.dumps(dashboard_data, indent=2, ensure_ascii=False)
        + ";\n",
        encoding="utf-8",
    )

    print(f"Inventory: {len(records)} images")
    print(f"Summary rows: {len(summary)}")
    print(f"Dashboard data: {PROCESSED_DIR / 'dashboard_data.json'}")


if __name__ == "__main__":
    main()
