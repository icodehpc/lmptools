from __future__ import annotations

from pydantic import BaseModel
import numpy as np
from typing import List
from .atom import Atom

class Polymer(BaseModel):
    atoms: List[Atom]

    @property
    def mass(self):
        return sum([atom.mass for atom in self.atoms])

    @property
    def com(self) -> List[float]:
        """
        Compute the center of mass of the chain using the unwrapped coordinates
        """
        # Assert that unwrapped coordinates are provided
        unwrapped = all([atom.unwrapped for atom in self.atoms])
        if not unwrapped:
            raise AssertionError(f"Polymer not unwrapped")

        xcm = np.mean([atom.xu for atom in self.atoms])
        ycm = np.mean([atom.yu for atom in self.atoms])
        zcm = np.mean([atom.zu for atom in self.atoms])
        return [xcm, ycm, zcm]

    @property
    def rg(self) -> float:
        """
        Radius of gyration of the polymer chain
        """
        unwrapped = all([atom.unwrapped for atom in self.atoms])
        if not unwrapped:
            raise AssertionError(f"Polymer not unwrapped")

        rcm = self.com
        masses = np.asarray([atom.mass for atom in self.atoms])
        x = np.asarray([atom.xu for atom in self.atoms])
        y = np.asarray([atom.yu for atom in self.atoms])
        z = np.asarray([atom.zu for atom in self.atoms])

        # (1/M)sum(m_i * (r_i,x - rcm,x)**2)
        rxx = np.dot(masses, (x - rcm[0])**2)/self.mass
        ryy = np.dot(masses, (y - rcm[1])**2)/self.mass
        rzz = np.dot(masses, (z - rcm[2])**2)/self.mass
        rxy = np.dot(masses, (x - rcm[0])*(y - rcm[1]))/self.mass
        rxz = np.dot(masses, (x - rcm[0])*(z - rcm[2]))/self.mass
        ryz = np.dot(masses, (y - rcm[1])*(z - rcm[2]))/self.mass

        # gyration tensor
        tensor = np.array([[rxx, rxy, rxz], [rxy, ryy, ryz], [rxz, ryz, rzz]])

        eigenvalues, _ = np.linalg.eig(tensor)
        #index = eigenvalues.argsort()[::-1]
        
        # return the principal eigenvalue
        return np.sqrt(np.sum(eigenvalues))

    def __len__(self):
        """
        compute the length of a single polymer
        """
        return len(self.atoms)
