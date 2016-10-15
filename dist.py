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

parser = argparse.ArgumentParser()

parser.add_argument('--name', default='emptyproject-0', dest='name',
                    help='Name to use in leading directory and package file names.')
parser.add_argument('--distfile', default=None, dest='distfile',
                    help='Distribution description file.')

def create_dist(name, distfile):
    packaging_dir = name
    if os.path.exists(packaging_dir):
        print('Packaging dir %s already exists.')
        sys.exit(1)
    os.mkdir(packaging_dir)
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
