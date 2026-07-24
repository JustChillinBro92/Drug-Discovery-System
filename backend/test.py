from services.sources.chembl_service import chembl_service
from services.normalizers.compound_normalizer import compound_normalizer


# result = chembl_service.search_compound("Aspirin")


# print("SEARCH RESULT")
# print(result)


# molecule = chembl_service.get_molecule(
#     "CHEMBL25"
# )


# print("\nMOLECULE DETAILS")
# print(molecule)


compound = compound_normalizer.normalize("Aspirin")

print(compound)
print()
print("Name:", compound.canonical_name)
print("ChEMBL ID:", compound.chembl_id)
print("SMILES:", compound.smiles)
print("Formula:", compound.molecular_formula)