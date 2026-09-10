"""Compile the reviewer implementation; keep the executable outside the repo."""
from pathlib import Path
import platform
import subprocess
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: python3 build.py OUTPUT_EXECUTABLE')
output = Path(sys.argv[1]).resolve()
output.parent.mkdir(parents=True, exist_ok=True)
flags = ['-std=c++20', '-O3', '-Wall', '-Wextra', '-Wpedantic', '-Wshadow', '-Werror']
if platform.system() == 'Darwin':
    sdk = subprocess.check_output(['xcrun', '--show-sdk-path'], text=True).strip()
    flags += ['-isysroot', sdk, '-isystem', str(Path(sdk)/'usr/include/c++/v1')]
subprocess.run(['c++', *flags, str(Path(__file__).with_name('full_lag_check.cpp')),
                '-o', str(output)], check=True)
