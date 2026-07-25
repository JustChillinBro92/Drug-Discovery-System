import re


class SynonymCleaner:
    def clean(
        self,
        synonyms: list[str]
    ) -> list[str]:

        cleaned = []

        for synonym in synonyms:

            if not synonym:
                continue


            synonym = synonym.strip()


            # Remove very short values
            if len(synonym) < 3:
                continue


            # Remove ChEMBL IDs
            if synonym.upper().startswith(
                "CHEMBL"
            ):
                continue


            # Remove CAS numbers
            if re.match(
                r"^\d{2,7}-\d{2}-\d$",
                synonym
            ):
                continue


            # Avoid duplicates
            if synonym not in cleaned:
                cleaned.append(
                    synonym
                )


        return cleaned



synonym_cleaner = SynonymCleaner()