# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2026 Joost van Bruggen — NUTCRACKER-ID
"""Synthetic-only tests for the optional YOLO/DINOv2 route."""
from pathlib import Path
import hashlib
import importlib.util
import tempfile
import unittest
from html.parser import HTMLParser
from urllib.parse import unquote
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("yolo_dinov2_pipeline",ROOT/"yolo_dinov2_pipeline.py")
PIPE=importlib.util.module_from_spec(spec);import sys;sys.modules[spec.name]=PIPE;spec.loader.exec_module(PIPE)

class FakeDetector:
    def detect(self,image):
        color=image.getpixel((0,0))[0]
        if color==20: return []
        if color==40:
            return [PIPE.Detection(.9,np.ones((image.height,image.width),bool),(0,0,image.width,image.height)) for _ in range(2)]
        if color==60:
            return [PIPE.Detection(.1,np.ones((image.height,image.width),bool),(0,0,image.width,image.height))]
        mask=np.zeros((image.height,image.width),bool);mask[4:20,5:21]=True
        return [PIPE.Detection(.95,mask,(5,4,21,20))]
class FakeEncoder:
    def encode(self,image):
        arr=np.asarray(image,dtype=np.float32)
        # Deterministic nonzero color/spatial summary, no ML model.
        v=np.array([arr[:,:,0].mean(),arr[:,:,1].mean(),arr[:,:,2].mean(),
                    arr[::2,::2,0].mean()+1],dtype=np.float32)
        return v/np.linalg.norm(v)

class ImageLinks(HTMLParser):
    def __init__(self):
        super().__init__(); self.sources=[]
    def handle_starttag(self,tag,attrs):
        if tag=="img": self.sources.append(dict(attrs)["src"])

class PipelineTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix=".synthetische-yolo-dino-test-",dir=ROOT)
        self.addCleanup(self.temp.cleanup);self.base=Path(self.temp.name)
        self.photos=self.base/"synthetisch";self.photos.mkdir()
        for n,c in [("fictief-a.png",80),("fictief-b.png",100),("fictief-geen-vogel.png",20),
                    ("fictief-meer-vogels.png",40),("fictief-lage-score.png",60)]:
            Image.new("RGB",(32,24),(c,c+5,c+10)).save(self.photos/n)
        self.hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in self.photos.iterdir()}
    def test_variable_count_masks_and_separate_routes(self):
        output=self.base/"uitvoer"
        result=PIPE.run(self.photos,output,FakeDetector(),FakeEncoder())
        self.assertEqual(result["image_count"],5);self.assertEqual(result["pair_count"],10)
        self.assertEqual(result["usable_mask_count"],2)
        self.assertIn("2 vogels gedetecteerd",next(x["status"] for x in result["records"] if x["name"]=="fictief-meer-vogels.png"))
        pair=next(p for p in result["pairs"] if "fictief-geen-vogel.png" in (p["a"],p["b"]))
        self.assertIsNone(pair["score_masked"])
        self.assertTrue((output/"rapport.html").is_file());self.assertTrue((output/"resultaten.json").is_file());self.assertTrue((output/"te_controleren.json").is_file())
        self.assertTrue(all((output/r[k]).is_file() for r in result["records"] for k in ("original","overlay") if r.get(k)))
        self.assertTrue(all((output/r["cutout"]).is_file() for r in result["records"] if r.get("cutout")))
        self.assertEqual(len(__import__("json").loads((output/"te_controleren.json").read_text(encoding="utf-8"))),3)
        links=ImageLinks();links.feed((output/"rapport.html").read_text(encoding="utf-8"));self.assertTrue(links.sources)
        self.assertTrue(all((output/unquote(src)).is_file() for src in links.sources))
        self.assertEqual(self.hashes,{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in self.photos.iterdir()})
    def test_reproducible_scores_and_no_overwrite(self):
        a=PIPE.run(self.photos,self.base/"out-a",FakeDetector(),FakeEncoder())
        b=PIPE.run(self.photos,self.base/"out-b",FakeDetector(),FakeEncoder())
        self.assertEqual(a["pairs"],b["pairs"])
        with self.assertRaises(FileExistsError):PIPE.run(self.photos,self.base/"out-a",FakeDetector(),FakeEncoder())
    def test_refuses_output_inside_input_and_bad_mask(self):
        with self.assertRaises(ValueError):PIPE.run(self.photos,self.photos/"out",FakeDetector(),FakeEncoder())
        bad=PIPE.Detection(.99,np.zeros((5,5),bool),(0,0,2,2))
        self.assertIsNone(PIPE.assess_mask([bad],(32,24))[0])
    def test_empty_input_and_local_weights_are_not_fetched(self):
        empty=self.base/"empty";empty.mkdir()
        result=PIPE.run(empty,self.base/"empty-out",FakeDetector(),FakeEncoder())
        self.assertEqual((result["image_count"],result["pair_count"]),(0,0))
        with self.assertRaises(FileNotFoundError):PIPE.LocalYoloDetector(self.base/"missing.pt")

if __name__=="__main__":unittest.main()


