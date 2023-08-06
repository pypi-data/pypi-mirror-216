#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 6/26/2023 12:25 PM
# @Author  : zhangbc0315@outlook.com
# @File    : mol.py
# @Software: PyCharm

import os
import logging

from rdkit.Chem import AllChem


class Mol:

    def __init__(self, smiles: str, name: str):
        self.smiles = smiles
        self.name = name
        self.rdmol = AllChem.MolFromSmiles(smiles)
        AllChem.AddHs(self.rdmol)
        if self.rdmol is None:
            logging.warning(f"Failed to parse smiles: {smiles}")

    def optimize_mol(self):
        AllChem.EmbedMolecule(self.rdmol)
        AllChem.UFFOptimizeMolecule(self.rdmol)

    def get_positions(self):
        conf = self.rdmol.GetConformer()
        return conf.GetPositions()

    def get_gjf_block(self, chk_path: str):
        positions = self.get_positions()
        symbols = [atom.GetSymbol() for atom in self.rdmol.GetAtoms()]
        gjf_blocks = [f"%chk={chk_path}",
                      f"#p opt freq b3lyp/6-31g(d) geom=connectivity",
                      "",
                      "Title Card Required",
                      "",
                      "0 1"]
        for symbol, position in zip(symbols, positions):
            gjf_blocks.append(f"{symbol} {position[0]} {position[1]} {position[2]}")
        gjf_blocks.append("")
        return gjf_blocks

    def write_gjf(self, dp: str, gjf_name: str = None, chk_name: str = None):
        if gjf_name is None:
            gjf_name = f"{self.name}.gjf"
        if chk_name is None:
            chk_name = f"{self.name}.chk"
        gjf_path = os.path.join(dp, gjf_name)
        chk_path = os.path.join(dp, chk_name)
        gjf_block = self.get_gjf_block(chk_path)
        with open(gjf_path, "w") as f:
            f.write("\n".join(gjf_block))

    def calc_homo_lumo(self, temp_dp: str):
        if not os.path.exists(temp_dp):
            os.mkdir(temp_dp)
        self.write_gjf(temp_dp)


if __name__ == "__main__":
    pass
