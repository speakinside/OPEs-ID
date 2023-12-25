import dataclasses
import time
from pathlib import Path
from typing import Iterable

import requests
import tqdm
from rdkit import Chem


@dataclasses.dataclass(slots=True)
class PubChemFailure:
    formula: str
    http_code: int
    pubchem_code: str
    message: str


def pubchem_fetch_json_inchi(formula: str):
    try:
        req = requests.get(
            f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/formula/{formula}/JSON")
        req.raise_for_status()
        list_key = req.json()["Waiting"]["ListKey"]
        for i in range(1, 5):
            time.sleep(0.5*i)

            req = requests.get(
                f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/listkey/{list_key}/property/InChI/JSON")
            req.raise_for_status()

            if req.status_code == 200:
                break
        else:
            return PubChemFailure(
                formula, req.status_code, None, None)
    except requests.HTTPError as e:
        resp: requests.Response = e.response
        info = resp.json()['Fault']
        return PubChemFailure(
            formula, resp.status_code, info['Code'], info['Message'])

    return req.json()


def fetchFromFormulas(formulas: Iterable, sdf_path: str | Path, seperate_file: bool = False):
    failures = {}
    if isinstance(sdf_path, str):
        sdf_path = Path(sdf_path)

    if not seperate_file:
        sdf = Chem.SDWriter(sdf_path.with_suffix('.sdf').as_posix())
    else:
        sdf_path.mkdir(exist_ok=True)

    for formula in tqdm.tqdm(set(formulas)):
        if seperate_file:
            sfpath = sdf_path / f'{formula}.sdf'
            if sfpath.exists():
                print(f'Skip formula:{formula}')
                continue
        fetch = pubchem_fetch_json_inchi(formula)
        if isinstance(fetch, PubChemFailure):
            failures[formula] = fetch
            continue
        if seperate_file:
            sdf = Chem.SDWriter(sfpath.as_posix())

        for entry in fetch['PropertyTable']['Properties']:
            try:
                mol = Chem.MolFromInchi(entry["InChI"])
                mol.SetIntProp('CID', entry['CID'])
                sdf.write(mol)

            except Exception as e:
                print(f"Error on CID:{entry['CID']}")
                print(e)

        if seperate_file:
            sdf.close()

    if not seperate_file:
        sdf.close()

    return failures
