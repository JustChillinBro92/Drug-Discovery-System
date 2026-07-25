import json

from services.sources.chembl_service import chembl_service
from services.normalizers.compound_normalizer import compound_normalizer
from services.analyzers.rdkit_service import rdkit_service
from services.analyzers.fingerprint_service import fingerprint_service
from services.analyzers.similarity_service import similarity_service

# result = chembl_service.search_compound("Aspirin")


# print("SEARCH RESULT")
# print(result)


# molecule = chembl_service.get_molecule(
#     "CHEMBL25"
# )


# print("\nMOLECULE DETAILS")
# print(molecule)


compound1 = compound_normalizer.normalize("Aspirin")
compound2 = compound_normalizer.normalize("Ibuprofen")


print(
    json.dumps(
        compound1.model_dump(),
        indent=4
    )
)

print()

print(
    json.dumps(
        compound2.model_dump(),
        indent=4
    )
)

print()

# print("Name:", compound1.canonical_name)
# print("ChEMBL ID:", compound1.chembl_id)
# print("SMILES:", compound1.smiles)
# print("Formula:", compound1.molecular_formula)


# print(rdkit_service.validate_compound(compound1))

# properties = rdkit_service.analyze_properties(compound1)

# print(
#     json.dumps(
#         properties.model_dump(),
#         indent=4
#     )
# )

fingerprint1 = fingerprint_service.generate_morgan_fingerprint(compound1)
fingerprint2 = fingerprint_service.generate_morgan_fingerprint(compound2)

# print(fingerprint1)

# print("Algorithm:", fingerprint1.algorithm)

# print("Radius:", fingerprint1.radius)

# print("Bits:", fingerprint1.n_bits)

# print(
#     "Fingerprint length:",
#     len(fingerprint1.fingerprint)
# )

# print(
#     "Number of active bits:",
#     sum(fingerprint1.fingerprint)
# )

similarity = similarity_service.calculate_similarity(
    fingerprint1,
    fingerprint2,
    compound2.canonical_name
)

print(
    json.dumps(
        similarity.model_dump(),
        indent=4
    )
)

