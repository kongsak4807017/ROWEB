from pathlib import Path
import re
import shutil
import subprocess

HTML=Path(__file__).parents[1]/'apps/admin-studio/mockup/unified-workbench.html'

def test_unified_workbench_contains_all_modules():
    text=HTML.read_text(encoding='utf-8')
    for view in ['scanner','assets','mapping','releases','command','players','economy','security','audit']:
        assert f'id="{view}"' in text
        assert f'data-view="{view}"' in text

def test_workbench_preserves_safe_mockup_boundary():
    text=HTML.read_text(encoding='utf-8')
    assert 'SIMULATED DATA' in text
    assert 'dry-run' in text.lower()
    assert 'WebSocket(' not in text
    assert 'fetch(' not in text
    assert 'SELECT ' not in text
    assert 'atcommand' not in text.lower()

def test_workbench_has_real_local_mapping_functions():
    text=HTML.read_text(encoding='utf-8')
    for function in ['function scan(','function norm(','function lid(','function domains(','function manifest(']:
        assert function in text
    assert 'webkitdirectory' in text
    assert 'mappingJson' in text

def test_embedded_javascript_has_valid_syntax(tmp_path):
    if not shutil.which('node'):
        return
    text=HTML.read_text(encoding='utf-8')
    scripts=re.findall(r'<script>(.*?)</script>',text,re.S)
    assert scripts
    js=tmp_path/'workbench.js'; js.write_text(scripts[-1],encoding='utf-8')
    subprocess.run(['node','--check',str(js)],check=True,capture_output=True,text=True)
