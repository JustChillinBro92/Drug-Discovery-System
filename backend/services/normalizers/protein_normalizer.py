from models.biomedical_entities import ProteinEntity


class ProteinNormalizer:
    def normalize(
        self,
        data: dict,
        organism: str | None = None
    ) -> ProteinEntity:

        protein_description = data.get(
            "proteinDescription",
            {}
        )

        protein_name = (
            protein_description
            .get("recommendedName", {})
            .get("fullName", {})
            .get("value")
        )


        # Gene symbol

        gene_symbol = None

        genes = data.get(
            "genes",
            []
        )

        if genes:

            gene_symbol = (
                genes[0]
                .get("geneName", {})
                .get("value")
            )


        # Comments

        function = None
        subcellular_location = None
        pathways = []


        for comment in data.get(
            "comments",
            []
        ):
            comment_type = comment.get(
                "commentType"
            )


            if comment_type == "FUNCTION":
                texts = comment.get(
                    "texts",
                    []
                )

                if texts:
                    function = texts[0].get(
                        "value"
                    )


            elif comment_type == "PATHWAY":
                texts = comment.get(
                    "texts",
                    []
                )

                pathways.extend(
                    text.get("value")
                    for text in texts
                    if text.get("value")
                )


            elif comment_type == "SUBCELLULAR LOCATION":
                locations = []

                for item in comment.get(
                    "subcellularLocations",
                    []
                ):

                    location = item.get(
                        "location",
                        {}
                    )

                    value = location.get(
                        "value"
                    )

                    if value:
                        locations.append(value)


                if locations:
                    subcellular_location = ", ".join(
                        dict.fromkeys(locations)
                    )


        # Sequence

        sequence_data = data.get(
            "sequence",
            {}
        )

        sequence = sequence_data.get(
            "value"
        )

        sequence_length = sequence_data.get(
            "length"
        )


        return ProteinEntity(
            uniprot_id=data.get(
                "primaryAccession"
            ),
            protein_name=protein_name,
            gene_symbol=gene_symbol,
            organism=organism,
            function=function,
            subcellular_location=(
                subcellular_location
            ),
            pathways=list(
                dict.fromkeys(pathways)
            ),
            sequence=sequence,
            sequence_length=sequence_length
        )
        
        
protein_normalizer = ProteinNormalizer()