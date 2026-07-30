import importlib.util, json
from pathlib import Path
MODULE=Path(__file__).parents[1]/'tools/asset-mapping/scan_robrowser_assets.py'
spec=importlib.util.spec_from_file_location('scanner',MODULE); scanner=importlib.util.module_from_spec(spec); spec.loader.exec_module(scanner)

def test_normalize_and_logical_id_are_deterministic():
    p=r'Data\\Texture\\유저인터페이스\\btn_ok.BMP'
    assert scanner.normalize_path(p)=='data/texture/유저인터페이스/btn_ok.bmp'
    assert scanner.logical_id(p)=='ui.texture.btn.ok.bmp'

def test_scan_extracts_consumers_and_rathena_domains(tmp_path):
    (tmp_path/'src').mkdir(); (tmp_path/'src/a.js').write_text('load("data/sprite/monster/poring.spr")',encoding='utf-8'); (tmp_path/'src/b.js').write_text('x="data/sprite/monster/poring.spr"',encoding='utf-8')
    result=scanner.scan(tmp_path)
    assert result['summary']['filesScanned']==2
    assert result['summary']['uniqueAssets']==1
    asset=result['assets'][0]
    assert asset['referenceCount']==2
    assert asset['category']=='Entity'
    assert 'monster' in asset['rathenaDomains']

def test_scan_reports_logical_id_collisions(tmp_path):
    (tmp_path/'a.js').write_text('"data/ui/a-b.png" "data/ui/a_b.png"',encoding='utf-8')
    result=scanner.scan(tmp_path)
    assert result['summary']['logicalIdCollisions']==1

def test_mapping_rules_json_is_valid():
    rules=Path(__file__).parents[1]/'tools/asset-mapping/mapping_rules.json'
    data=json.loads(rules.read_text(encoding='utf-8'))
    assert data['version']==1 and 'rathena_domains' in data
