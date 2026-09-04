import csv
from pathlib import Path

from models.biomedical_entities import SideEffectEntity

class SIDERService:
    def __init__(
        self,
        file_path: str
    ):
        self.file_path = Path(file_path)
    
    
    def get_side_effects(
        self,
        pubchem_cids: list[str]
    ) -> list[SideEffectEntity]:
        
        sider_ids = {
            f"CID{int(pubchem_cid):09d}"
            for pubchem_cid in pubchem_cids
        }
        
        print(sider_ids)
        
        side_effects = []
        seen_meddra_ids = set()
        
        with self.file_path.open(
            "r",
            encoding="utf-8"
        ) as file:
            
            reader = csv.reader(
                file, delimiter="\t"
            )
            
            for row in reader:
                if (len(row) < 6 or 
                    row[1] not in sider_ids or 
                    row[3] != "PT" or
                    row[4] in seen_meddra_ids
                ):
                    continue

                seen_meddra_ids.add(row[4])
                
                side_effects.append(
                    SideEffectEntity(
                        meddra_id = row[4],
                        side_effect_name = row[5],
                        meddra_level = row[3]
                    )
                )
                
        return side_effects

    
PROJECT_ROOT = Path(__file__).resolve().parents[3]
SIDER_FILE = (
    PROJECT_ROOT / "data" / "sider" / "meddra_all_se.tsv"
)
    
sider_service = SIDERService(SIDER_FILE)
                
                
        