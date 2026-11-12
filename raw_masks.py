from config import credential
from pathlib import Path
import os,json,time,zipfile,io
import requests

def segment_raw(video, folder, prompt='person', status=print):
    from replicate_jobs import submit_prediction, wait_prediction
    folder = Path(folder)
    headers = {'Authorization': 'Bearer ' + credential('REPLICATE_API_TOKEN')}
    prediction_path = folder / 'sam-raw-request.json'
    if not prediction_path.exists():
        with open(video, 'rb') as source:
            response = requests.post('https://api.replicate.com/v1/files', headers=headers, files={'content': source}, timeout=(10, 120))
        response.raise_for_status()
        url = response.json()['urls']['get']
        submit_prediction(prediction_path, headers, {
            'version': '408f82fc20c300aac5d61d2e34ddb34cd0181e810e9f609d250aed14d5f81269',
            'input': {'video': url, 'prompt': prompt, 'mask_only': True, 'return_zip': True},
        })
    j = wait_prediction(prediction_path, headers, status)
    r=requests.get(j['output'],timeout=180);r.raise_for_status();(folder/'sam-masks.zip').write_bytes(r.content)
    out=folder/'raw-masks';out.mkdir(exist_ok=True)
    for stale in out.glob('mask_*.png'):stale.unlink()
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        for name in z.namelist():
            base=Path(name).name
            if base.startswith('mask_') and base.endswith('.png'):(out/base).write_bytes(z.read(name))
    return out

def clean_border_fragments(folder):
    """Remove tiny, narrow disconnected edge fragments; preserve large edge subjects."""
    import numpy as np
    from PIL import Image
    from scipy.ndimage import label
    folder=Path(folder);output=folder.parent/'clean-masks';output.mkdir(exist_ok=True)
    for stale in output.glob('mask_*.png'):stale.unlink()
    report=[]
    for p in sorted(folder.glob('mask_*.png')):
        a=np.asarray(Image.open(p).convert('L'))>127;labels,_=label(a);h,w=a.shape;removed=0
        for ident in (set(labels[:,0])|set(labels[:,-1]))-{0}:
            y,x=np.where(labels==ident)
            if len(x)<h*w*.03 and x.max()-x.min()+1<=max(6,int(w*.05)):
                a[labels==ident]=False;removed+=len(x)
        Image.fromarray(a.astype(np.uint8)*255).save(output/p.name)
        report.append({'frame':p.stem,'removed_border_pixels':removed,'mask_pixels':int(a.sum()),'left_right_edge_pixels':int(a[:,0].sum()+a[:,-1].sum())})
    (folder.parent/'mask-cleanup-report.json').write_text(json.dumps(report,indent=2))
    return output


def merge_repair_masks(base, repaired, output):
    """Retain either segmentation's coverage and fill enclosed subject holes."""
    import numpy as np
    from PIL import Image
    from scipy.ndimage import binary_fill_holes
    base, repaired, output = Path(base), Path(repaired), Path(output)
    first, second = sorted(base.glob("mask_*.png")), sorted(repaired.glob("mask_*.png"))
    if not first or [p.name for p in first] != [p.name for p in second]:
        raise ValueError("Frame alignment: repair masks differ")
    output.mkdir(exist_ok=True)
    for original, repair in zip(first, second):
        a = np.asarray(Image.open(original).convert("L")) > 127
        b = np.asarray(Image.open(repair).convert("L")) > 127
        if a.shape != b.shape:
            raise ValueError("Frame alignment: repair dimensions differ")
        combined = binary_fill_holes(a | b)
        Image.fromarray(combined.astype(np.uint8) * 255).save(output / original.name)
    return output
