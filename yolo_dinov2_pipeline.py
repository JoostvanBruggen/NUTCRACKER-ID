# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2026 Joost van Bruggen — NUTCRACKER-ID
"""YOLO26n-seg foreground masks and matched full-image/cutout DINOv2 routes.

The model adapters are lazy and require explicit local source/weight paths. No
model or weight is fetched by this module. Synthetic tests inject both adapters.
"""
from __future__ import annotations
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Protocol
import subprocess
import argparse
import hashlib
import itertools
import json
import math
import numpy as np
from PIL import Image, ImageDraw

DINO_REVISION = "12592a9bdfea0a6e4ee4767cd5a8d3195c0e3509"
DINO_WEIGHT_SHA256 = "0b8b82f85de91b424aded121c7e1dcc2b7bc6d0adeea651bf73a13307fad8c73"
DINO_SIDE = 336
NEUTRAL_RGB = (124, 116, 104)
BIRD_CLASS_ID = 14  # COCO class 'bird'

@dataclass
class Detection:
    confidence: float
    mask: np.ndarray
    box_xyxy: tuple[float, float, float, float]

class Detector(Protocol):
    def detect(self, image: Image.Image) -> list[Detection]: ...
class Encoder(Protocol):
    def encode(self, image: Image.Image) -> np.ndarray: ...

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

class LocalYoloDetector:
    """Load the official YOLO26n-seg checkpoint only from a local file."""
    def __init__(self, weights: Path, confidence: float = 0.25):
        self.weights = weights.expanduser().resolve()
        if not self.weights.is_file():
            raise FileNotFoundError(f"Lokaal YOLO-gewicht ontbreekt: {self.weights}")
        self.confidence = confidence
        self._model = None
    def detect(self, image: Image.Image) -> list[Detection]:
        if self._model is None:
            from ultralytics import YOLO
            self._model = YOLO(str(self.weights))
        result = self._model.predict(source=np.asarray(image.convert("RGB")), classes=[BIRD_CLASS_ID],
                                     conf=self.confidence, retina_masks=True, verbose=False)[0]
        if result.boxes is None or result.masks is None:
            return []
        boxes = result.boxes.xyxy.cpu().numpy()
        confs = result.boxes.conf.cpu().numpy()
        masks = result.masks.data.cpu().numpy()
        found = []
        for box, confidence, mask in zip(boxes, confs, masks):
            resized = Image.fromarray((mask > 0.5).astype(np.uint8) * 255).resize(image.size, Image.Resampling.NEAREST)
            found.append(Detection(float(confidence), np.asarray(resized) > 0,
                                   tuple(float(v) for v in box)))
        return found

class LocalDinoV2Encoder:
    """Pinned DINOv2 ViT-B/14 adapter; uses only a local checkout and checkpoint."""
    def __init__(self, repo: Path, checkpoint: Path, device: str = "cpu"):
        self.repo = repo.expanduser().resolve()
        self.checkpoint = checkpoint.expanduser().resolve()
        if not self.repo.is_dir() or not (self.repo / "hubconf.py").is_file():
            raise FileNotFoundError("Lokale DINOv2-bronmap met hubconf.py ontbreekt.")
        revision = subprocess.run(["git", "-C", str(self.repo), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
        if revision != DINO_REVISION:
            raise ValueError(f"DINOv2-bronrevisie is {revision}, verwacht {DINO_REVISION}.")
        if not self.checkpoint.is_file():
            raise FileNotFoundError("Lokaal DINOv2-checkpoint ontbreekt.")
        if sha256(self.checkpoint) != DINO_WEIGHT_SHA256:
            raise ValueError("SHA-256 van het lokale DINOv2-checkpoint komt niet overeen met de vastgezette gewichten.")
        self.device = device
        self._model = None
        self._torch = None
    def _load(self):
        import torch
        self._torch = torch
        model = torch.hub.load(str(self.repo), "dinov2_vitb14", source="local", pretrained=False)
        state = torch.load(self.checkpoint, map_location="cpu", weights_only=True)
        if isinstance(state, dict) and "state_dict" in state:
            state = state["state_dict"]
        if not isinstance(state, dict):
            raise ValueError("DINOv2-checkpoint bevat geen state_dict.")
        model.load_state_dict(state, strict=True)
        self._model = model.to(self.device).eval()
    def encode(self, image: Image.Image) -> np.ndarray:
        if self._model is None:
            self._load()
        torch = self._torch
        rgb = image.convert("RGB")
        scale = min(DINO_SIDE / rgb.width, DINO_SIDE / rgb.height)
        size = (max(1, round(rgb.width * scale)), max(1, round(rgb.height * scale)))
        fitted = rgb.resize(size, Image.Resampling.BICUBIC)
        canvas = Image.new("RGB", (DINO_SIDE, DINO_SIDE), NEUTRAL_RGB)
        canvas.paste(fitted, ((DINO_SIDE-size[0])//2, (DINO_SIDE-size[1])//2))
        arr = np.asarray(canvas, dtype=np.float32).copy() / 255.0
        x = torch.from_numpy(arr).permute(2, 0, 1)
        mean = torch.tensor((.485,.456,.406)).reshape(3,1,1)
        std = torch.tensor((.229,.224,.225)).reshape(3,1,1)
        with torch.inference_mode():
            v = self._model(((x-mean)/std).unsqueeze(0).to(self.device)).squeeze(0)
            v = torch.nn.functional.normalize(v, dim=0)
        return v.detach().cpu().numpy().astype(np.float32)

def cosine(a: np.ndarray, b: np.ndarray) -> float:
    a, b = np.asarray(a, dtype=np.float64), np.asarray(b, dtype=np.float64)
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    if not denom or not math.isfinite(denom):
        raise ValueError("Ongeldige DINOv2-vector.")
    return float(np.clip(np.dot(a, b) / denom, -1.0, 1.0))

def assess_mask(detections: list[Detection], size: tuple[int, int]) -> tuple[Detection | None, str]:
    if not detections:
        return None, "Geen vogel gedetecteerd."
    if len(detections) != 1:
        return None, f"{len(detections)} vogels gedetecteerd; automatische uitsnede overgeslagen."
    d = detections[0]
    mask = np.asarray(d.mask, dtype=bool)
    if mask.shape != (size[1], size[0]):
        return None, "Masker heeft een onverwachte afmeting."
    ratio = float(mask.mean())
    if d.confidence < .25:
        return None, "Detectie onder de ingestelde vertrouwensgrens (0,25)."
    if ratio < .005 or ratio > .90:
        return None, f"Maskeroppervlak lijkt onbruikbaar ({ratio:.3%} van de foto)."
    if not mask.any():
        return None, "Leeg masker."
    return d, "Eén vogel; masker voldoet aan de automatische technische controle. Visuele controle blijft nodig."

def foreground(image: Image.Image, mask: np.ndarray) -> Image.Image:
    src = np.asarray(image.convert("RGB"))
    out = np.empty_like(src); out[:] = NEUTRAL_RGB
    out[np.asarray(mask, dtype=bool)] = src[np.asarray(mask, dtype=bool)]
    return Image.fromarray(out, "RGB")

def _safe_name(path: Path) -> str:
    return hashlib.sha256(path.name.encode("utf-8")).hexdigest()[:16]

def _html(report: Path, records: list[dict], pairs: list[dict], threshold: float) -> None:
    rows = []
    for r in records:
        imgs = "".join(f'<figure><img src="{escape(r[k])}" alt="{escape(label)}"><figcaption>{label}</figcaption></figure>'
                       for k,label in (("original","Origineel"),("overlay","Detectie"),("cutout","Neutrale achtergrond")) if r.get(k))
        rows.append(f'<article><h2>{escape(r["name"])}</h2><p>{escape(r["status"])}</p><div class="images">{imgs}</div></article>')
    pair_rows = "".join(f'<tr><td>{escape(p["a"])}</td><td>{escape(p["b"])}</td><td>{p["score_full"]:.4f}</td><td>{"—" if p["score_masked"] is None else f"{p["score_masked"]:.4f}"}</td></tr>' for p in pairs)
    page = ('<!doctype html><html lang="nl"><meta charset="utf-8"><title>NUTCRACKER-ID — YOLO/DINOv2</title>'
            '<style>body{font:16px system-ui;max-width:1100px;margin:2em auto;padding:0 1em} .images{display:flex;gap:1em;flex-wrap:wrap}figure{margin:0;width:30%}img{max-width:100%;max-height:260px}td,th{padding:.4em;border-bottom:1px solid #ccc}</style>'
            '<h1>YOLO26n-seg en DINOv2</h1><p>Cosine-overeenkomst is een technische score, geen identiteitskans. '
            'De maskercontrole is een heuristiek; inspecteer ieder masker. Meerdere vogels of onbruikbare maskers krijgen geen route-B-score.</p>'
            '<h2>Beelden en maskers</h2>'+''.join(rows)+f'<h2>Fotoparen (route A tegenover route B; grens {threshold:.2f})</h2>'
            '<table><thead><tr><th>Foto A</th><th>Foto B</th><th>Route A</th><th>Route B</th></tr></thead><tbody>'+pair_rows+'</tbody></table></html>')
    report.write_text(page, encoding="utf-8")

def run(input_dir: Path, output_dir: Path, detector: Detector, encoder: Encoder,
        threshold: float = .90) -> dict:
    src = input_dir.expanduser().resolve(); out = output_dir.expanduser().resolve()
    if not src.is_dir(): raise NotADirectoryError(src)
    if not 0.0 <= threshold <= 1.0: raise ValueError("Drempel moet tussen 0 en 1 liggen.")
    if out == src or src in out.parents:
        raise ValueError("Uitvoer mag niet in de invoermap staan.")
    if out.exists() and any(out.iterdir()):
        raise FileExistsError("Uitvoermap bestaat en is niet leeg; overschrijven is uitgeschakeld.")
    out.mkdir(parents=True, exist_ok=True)
    assets = out / "beelden"; assets.mkdir()
    paths = sorted(p for p in src.iterdir() if p.is_file() and p.suffix.lower() in {".jpg",".jpeg",".png",".webp",".bmp",".tif",".tiff"})
    records, vectors_a, vectors_b, needs_review = [], [], [], []
    for path in paths:
        key = _safe_name(path); original_file = assets / f"{key}_origineel.png"
        with Image.open(path) as opened: image = opened.convert("RGB")
        image.save(original_file, format="PNG")
        detections = detector.detect(image)
        chosen, status = assess_mask(detections, image.size)
        rec = {"name":path.name,"sha256":sha256(path),"width":image.width,"height":image.height,"detection_count":len(detections),"status":status,"original":f"beelden/{original_file.name}","overlay":None,"cutout":None}
        vectors_a.append(np.asarray(encoder.encode(image), dtype=np.float32))
        vectors_b.append(None)
        if detections:
            overlay = image.copy(); draw = ImageDraw.Draw(overlay, "RGBA")
            for d in detections:
                mask = np.asarray(d.mask, dtype=bool)
                if mask.shape == (image.height,image.width):
                    tint = np.zeros((image.height,image.width,4), dtype=np.uint8); tint[mask]=(0,160,90,95)
                    overlay=Image.alpha_composite(overlay.convert("RGBA"),Image.fromarray(tint)).convert("RGB")
                draw.rectangle(tuple(int(round(v)) for v in d.box_xyxy), outline=(255,80,30), width=3)
            overlay.save(assets/f"{key}_detectie.png"); rec["overlay"]=f"beelden/{key}_detectie.png"
        if chosen is not None:
            masked = foreground(image, chosen.mask); masked.save(assets/f"{key}_masker.png")
            rec["cutout"]=f"beelden/{key}_masker.png"
            vectors_b[-1]=np.asarray(encoder.encode(masked), dtype=np.float32)
        records.append(rec)
        if chosen is None: needs_review.append({"name":path.name,"status":status,"original":rec["original"]})
    pairs=[]
    for i,j in itertools.combinations(range(len(records)),2):
        a,b=records[i],records[j]
        sa=cosine(vectors_a[i],vectors_a[j])
        sb=cosine(vectors_b[i],vectors_b[j]) if vectors_b[i] is not None and vectors_b[j] is not None else None
        pairs.append({"a":a["name"],"b":b["name"],"score_full":sa,"score_masked":sb,
                      "route_a_above_threshold":sa>=threshold,
                      "route_b_above_threshold":None if sb is None else sb>=threshold})
    yolo_weights = getattr(detector, "weights", None)
    data={"project":"NUTCRACKER-ID","method":"YOLO26n-seg + pinned DINOv2 ViT-B/14","dino_code_revision":DINO_REVISION,
          "dino_weight_sha256":DINO_WEIGHT_SHA256,
          "yolo_weights_sha256":sha256(yolo_weights) if isinstance(yolo_weights, Path) and yolo_weights.is_file() else None,
          "dino_input_side":DINO_SIDE,"neutral_rgb":list(NEUTRAL_RGB),"threshold":threshold,
          "technical_scores_are_identity_probabilities":False,"image_count":len(records),"pair_count":len(pairs),
          "usable_mask_count":sum(r["cutout"] is not None for r in records),"records":records,"pairs":pairs}
    (out/"resultaten.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"te_controleren.json").write_text(json.dumps(needs_review,ensure_ascii=False,indent=2),encoding="utf-8")
    _html(out/"rapport.html",records,pairs,threshold)
    return data

def main() -> int:
    parser=argparse.ArgumentParser(description="Vergelijk volledige foto en YOLO-masker met dezelfde lokale DINOv2.")
    parser.add_argument("--photos",type=Path,required=True); parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--yolo-weights",type=Path,required=True); parser.add_argument("--dinov2-repo",type=Path,required=True)
    parser.add_argument("--dinov2-checkpoint",type=Path,required=True); parser.add_argument("--threshold",type=float,default=.90)
    args=parser.parse_args()
    report=run(args.photos,args.output,LocalYoloDetector(args.yolo_weights),LocalDinoV2Encoder(args.dinov2_repo,args.dinov2_checkpoint),args.threshold)
    print(f"Gereed: {report['image_count']} foto's, {report['pair_count']} paren, {report['usable_mask_count']} bruikbare maskers; rapport: {args.output/'rapport.html'}")
    return 0
if __name__=="__main__": raise SystemExit(main())



