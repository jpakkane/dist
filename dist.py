#!/usr/bin/env python3

# Copyright 2016 The Meson development team

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse, sys, os, shutil
import subprocess, tarfile, zipfile
from collections import namedtuple

parser = argparse.ArgumentParser()

parser.add_argument('--name', default='emptyproject-0', dest='name',
                    help='Name to use in leading directory and package file names.')
parser.add_argument('--distfile', default=None, dest='distfile',
                    help='Distribution description file.')

def parse_distfile(dfname):
    Dist = namedtuple('Dist', ['copy', 'delete', 'run'])
    return Dist(['extra_file'], ['subdir/removeme.txt'], ['./packagingscript.py'])

def create_zip(zipfilename, packaging_dir):
    zf = zipfile.ZipFile(zipfilename, 'w', compression=zipfile.ZIP_DEFLATED,
                         allowZip64=True)
    zf.write(packaging_dir)
    for root, dirs, files in os.walk(packaging_dir):
        for d in dirs:
            dname = os.path.join(root, d)
            zf.write(dname, dname)
        for f in files:
            fname = os.path.join(root, f)
            zf.write(fname, fname)
    zf.close()

def create_dist(name, distfile):
    packaging_dir = name
    if os.path.exists(packaging_dir):
        print('Packaging dir %s already exists.' % packaging_dir)
        sys.exit(1)
    os.mkdir(packaging_dir)
    gitdir = os.path.join(packaging_dir, '.git')
    shutil.copytree('.git', gitdir)
    subprocess.check_call(['git', 'reset', '--hard'], cwd=packaging_dir)
    shutil.rmtree(gitdir)
    try:
        os.unlink(os.path.join(packaging_dir, '.gitignore'))
    except Exception:
        pass
    dist_info = parse_distfile(distfile)
    for c in dist_info.copy:
        ofname = os.path.join(packaging_dir, c)
        if os.path.isfile(c):
            shutil.copy2(c, ofname)
        else:
            shutil.copytree(c, ofname)
    for d in dist_info.delete:
        dfname = os.path.join(packaging_dir, d)
        if os.path.isfile(dfname):
            os.unlink(dfname)
        else:
            shutil.rmtree(dfname)
    for script in dist_info.run:
        subprocess.check_call([script, packaging_dir])
    tarfname = name + '.tar.xz'
    tf = tarfile.open(tarfname, 'w:xz')
    tf.add(packaging_dir, packaging_dir)
    tf.close()
    zipfilename = name + '.zip'
    create_zip(zipfilename, packaging_dir)
    # Create checksums here?
    shutil.rmtree(packaging_dir)

if __name__ == '__main__':
    options = parser.parse_args()
    if options.distfile is None:
        print('Must specify --distfile.')
        sys.exit(1)
    if not shutil.which('git'):
        print('Git not installed, can not create distribution without it.')
        sys.exit(1)
    if not os.path.exists('.git'):
        print('No .git directory in current directory, can not create distribution.')
        sys.exit(1)
    open('extra_file', 'w').close()
    create_dist(options.name, options.distfile)
    os.unlink('extra_file')
