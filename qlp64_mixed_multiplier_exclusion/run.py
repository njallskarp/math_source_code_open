"""Rebuild the complete mixed cover and compare every row fiber independently."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import shlex
import subprocess
import time
import audit
import search
import structural

ROOT = Path(__file__).resolve().parent


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True)+'\n')


def encode(row, bound):
    word = 0
    for v in row:
        assert -bound <= v <= bound
        word = word*(2*bound+1)+v+bound
    assert word < 2**64
    return word


def prepare_oracles(work, parents, d):
    """Include every distinct row of every parent, including empty row fibers."""
    bound = 64//(2*d)
    for kind in ('axis', 'symmetric'):
        cap = search.target(d)[0]//2 if kind == 'axis' else search.target(d)[0]
        rows = sorted({q[0] for q in parents} if kind == 'axis'
                      else {r for q in parents for r in q[1:]})
        with (work/f'{kind}-input{d}.txt').open('w') as stream:
            stream.write(f'{d} {len(rows)} {bound} {cap}\n')
            for p in rows:
                children = (search.mixed_lifts(p, bound, cap) if kind == 'axis'
                            else search.symmetric_lifts(p, sum(p), bound, cap))
                codes = sorted(encode(r, bound) for r in children)
                assert len(set(codes)) == len(children)
                stream.write(' '.join(map(str, p))+' '+str(len(codes))+'\n')
                stream.write(' '.join(map(str, codes))+'\n')


def compile_sources(work, cxx, extra_flags):
    flags = [cxx, '-std=c++20', '-O3', '-Wall', '-Wextra', '-Wpedantic',
             '-Wshadow', '-Werror']
    if platform.system() == 'Darwin':
        sdk = subprocess.check_output(['xcrun', '--show-sdk-path'], text=True).strip()
        flags += ['-isysroot', sdk, '-isystem', str(Path(sdk)/'usr/include/c++/v1')]
    flags += shlex.split(extra_flags)
    commands = []
    for kind in ('axis', 'symmetric'):
        command = [*flags, str(ROOT/f'{kind}_oracle.cpp'), '-o', str(work/f'{kind}_oracle')]
        subprocess.run(command, check=True)
        commands.append(command)
    return commands


def main():
    if not __debug__:
        raise RuntimeError('Run Python without -O: assertions are proof checks.')
    parser = argparse.ArgumentParser()
    parser.add_argument('--workdir', type=Path, required=True)
    parser.add_argument('--cxx', default='c++')
    parser.add_argument('--cxxflags', default='')
    args = parser.parse_args()
    work = args.workdir.resolve()
    if work == ROOT or ROOT in work.parents:
        raise RuntimeError('Choose a work directory outside the source package.')
    work.mkdir(parents=True, exist_ok=True)
    # Prevent a stale successful receipt surviving a failed rerun.
    (work/'verified.json').unlink(missing_ok=True)
    expected = json.loads((ROOT/'expected.json').read_text())
    started = time.monotonic()
    commands = compile_sources(work, args.cxx, args.cxxflags)
    result = dict(audit=audit.run(), structural=structural.run())
    assert result['audit'] == expected['audit']
    assert result['structural'] == expected['structural']
    rows = search.root_rows()
    qs = sorted(set(search.match(*rows, search.target(4))))
    levels = [dict(length=4, states=len(qs), sha256=search.digest(qs),
                   root_row_counts=list(map(len, rows)))]
    (work/'cover4.json').write_text(json.dumps(qs, separators=(',', ':'))+'\n')
    stage_seconds = []
    for d in (8, 16, 32):
        tick = time.monotonic()
        assert qs, 'Unexpected earlier empty stage; inspect changed input/source.'
        parents = qs
        qs, counters = search.extend(parents)
        levels.append(dict(length=d, states=len(qs), sha256=search.digest(qs), **counters))
        (work/f'cover{d}.json').write_text(json.dumps(qs, separators=(',', ':'))+'\n')
        prepare_oracles(work, parents, d)
        stage_seconds.append(dict(length=d, seconds=time.monotonic()-tick))
        print(json.dumps(levels[-1]), flush=True)
    result['levels'] = levels
    assert levels == expected['levels'] and not qs
    oracle_seconds = []
    for kind in ('axis', 'symmetric'):
        outputs = []
        for d in (8, 16, 32):
            tick = time.monotonic()
            with (work/f'{kind}-oracle{d}.log').open('w') as log:
                completed = subprocess.run([str(work/f'{kind}_oracle'),
                    str(work/f'{kind}-input{d}.txt')], check=True, text=True,
                    stdout=subprocess.PIPE, stderr=log)
            outputs.append(json.loads(completed.stdout))
            oracle_seconds.append(dict(kind=kind, length=d, seconds=time.monotonic()-tick))
        result[kind+'_oracle'] = outputs
        assert outputs == expected[kind+'_oracle']
    assert result == expected
    write_json(work/'result.json', result)
    write_json(work/'execution.json', dict(commands=commands,
        python=platform.python_version(), platform=platform.platform(),
        compiler=subprocess.check_output([args.cxx, '--version'], text=True).splitlines()[0],
        source_sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(ROOT.iterdir()) if p.suffix in ('.py', '.cpp')},
        stage_seconds=stage_seconds, oracle_seconds=oracle_seconds,
        total_seconds=time.monotonic()-started))
    final = dict(verified=True, mixed_multipliers=[31, 63], final_compressed_states=0,
                 final_sha256=levels[-1]['sha256'],
                 ordinary_exclusion_dependency_replayed=False,
                 affine_corollary_conditional_on_ordinary_exclusion=True)
    write_json(work/'verified.json', final)
    print(json.dumps(final, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
