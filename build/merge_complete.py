from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
HANDBOOK = PROJECT_ROOT / 'handbook'

order = []
order.append(('README.md', PROJECT_ROOT / 'README.md'))
order.append(('INDEX.md', PROJECT_ROOT / 'INDEX.md'))

for layer in ['l1-theory', 'l2-context', 'l3-protocol', 'l4-framework',
              'l5-pattern', 'l6-observability', 'l7-production-security',
              'l8-case-studies']:
    layer_dir = HANDBOOK / layer
    for f in sorted(layer_dir.glob('*.md')):
        order.append((f.name, f))

for app in ['appendix-a-react-template', 'appendix-b-multi-agent-skeleton',
            'appendix-c-framework-matrix', 'appendix-d-glossary',
            'quiz-l1-l3', 'quiz-l4-l5', 'quiz-l6-l8']:
    order.append((f'{app}.md', HANDBOOK / 'appendices' / f'{app}.md'))

print(f'总文件数: {len(order)}')

with open('handbook/COMPLETE.md', 'w', encoding='utf-8') as out:
    for i, (name, path) in enumerate(order, 1):
        if not path.exists():
            print(f'MISSING: {path}')
            continue
        rel = path.relative_to(PROJECT_ROOT)
        out.write(f'\n{"="*80}\n')
        out.write(f'## [{i:02d}] {rel}\n')
        out.write(f'{"="*80}\n\n')
        out.write(path.read_text(encoding='utf-8'))

import os
size_kb = os.path.getsize('handbook/COMPLETE.md') / 1024
print(f'生成: handbook/COMPLETE.md ({size_kb:.1f} KB)')