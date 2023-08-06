# MIT License
#
# Copyright (c) 2023 Dechin Chen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import argparse
import uuid
from fold import get_hbonds, get_alpha, get_beta, get_residue_type
from hadder import AddHydrogen

parser = argparse.ArgumentParser()
parser.add_argument("-i", help="Set the input pdb file path.")
parser.add_argument("-o", help="Set the output txt file path.")
parser.add_argument("-oh", help="Write the hbonds into txt file.")
parser.add_argument("--simplified", help="Return the simplified information, default to be 0.", default='0')
parser.add_argument("--addh", help="Decide to rebuild hydrogen atoms or not, default to be 0.", default='0')

args = parser.parse_args()
pdb_name = args.i
save_txt_name = args.o
hbond_txt = args.oh
use_simplified = args.simplified
addh = args.addh

task_id = uuid.uuid1()
if not os.path.exists('/tmp/restraint-fold/'):
    os.mkdir('/tmp/restraint-fold/')
addh_pdb = '/tmp/restraint-fold/{}.pdb'.format(task_id)

if addh == '1':
    AddHydrogen(pdb_name, addh_pdb)
    print ('The new pdb file path is in: {}'.format(addh_pdb))
    pdb_name = addh_pdb

alphas = get_alpha(pdb_name, hbond_length=3.5)
betas = get_beta(pdb_name, hbond_length=4.0, alphas=alphas)

if save_txt_name is not None:
    if use_simplified == '0':
        with open(save_txt_name, 'w') as file:
            file.write('alpha:\n')
            file.write(' '.join(list(map(str,alphas))))
            file.write('\n')
            file.write('beta:\n')
            file.write(' '.join(list(map(str,betas))))
    else:
        with open(save_txt_name, 'w') as file:
            file.write('alpha:\n')
            for i in range(len(alphas)):
                if i == 0:
                    file.write(str(alphas[i]))
                    file.write('~')
                elif i == len(alphas)-1:
                    file.write(str(alphas[i]))
                    file.write('\n')
                elif alphas[i] != alphas[i-1]+1:
                    file.write(str(alphas[i-1]))
                    file.write('\n')
                    file.write(str(alphas[i]))
                    file.write('~')
                else:
                    continue
            file.write('\n')
            file.write('beta:\n')
            for i in range(len(betas)):
                if i == 0:
                    file.write(str(betas[i]))
                    file.write('~')
                elif i == len(betas)-1:
                    file.write(str(betas[i]))
                    file.write('\n')
                elif betas[i] != betas[i-1]+1:
                    file.write(str(betas[i-1]))
                    file.write('\n')
                    file.write(str(betas[i]))
                    file.write('~')
                else:
                    continue


if hbond_txt is not None:
    hbonds = get_hbonds(pdb_name, return_hbonds=True)
    with open(hbond_txt, 'w') as file:
        file.write('Hbonds:\n')
        file.write('{}\n'.format(hbonds.shape[0]))
        for bond in hbonds:
            file.write('{}\t{}\n'.format(bond[0], bond[1]))

