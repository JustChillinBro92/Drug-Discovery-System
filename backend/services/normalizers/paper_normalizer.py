from models.paper_entity import PaperEntity

from services.sources.europepmc_service import europepmc_service


class PaperNormalizer:
    def normalize(
        self, 
        query: str,
        page_size: int = 10
    ) -> list[PaperEntity]:
        
        # 1. Search up the papers using Europe PMC service
        
        response = europepmc_service.search_service(
            query=query,
            page_size=page_size
        )
        
        # 2. Extract the result from response
        
        results = (
            response
            .get("resultList", {})
            .get("result", [])
        )
        
        # 3. Extract necessary data and populate papers list with paper entities
        
        papers = []
        
        for result in results:
            # Extract author name from author list
            
            author_list = (
                result
                .get("authorList", {})
                .get("author", [])
            )
            
            authors = [
               author_data.get("fullName")
               for author_data in author_list
               if author_data.get("fullName")
            ]
            
            # Extract journal title, publication date, type
            
            journal = (
                result
                .get("journalInfo", {})
                .get("journal", {})
                .get("title")
            )
            
            publication_date = (
                result
                .get("journalInfo", {})
                .get("printPublicationDate")
            )
            
            publication_types = (
                result
                .get("pubTypeList", {})
                .get("pubType", [])
            )
            
            
            # Extract keywords and mesh terms
            
            keywords = (
                result
                .get("keywordList", {})
                .get("keyword", [])
            )

            mesh_terms = [
                mesh.get("descriptorName")
                for mesh in (
                    result
                    .get("meshHeadingList", {})
                    .get("meshHeading", [])
                )
                if mesh.get("descriptorName")
            ]
            
            
            # Create paper entity
            
            paper = PaperEntity(
                pmid = result.get("pmid"),
                pmcid = result.get("pmcid"),
                doi = result.get("doi"),
                title = result.get("title", ""),
                abstract = result.get("abstractText"),
                authors = authors,
                journal = journal,
                publication_year = result.get("pubYear"),
                publication_date = publication_date,
                publication_types = publication_types,
                keywords = keywords,
                mesh_terms = mesh_terms,
                source = result.get("source", "Europe PMC"),
                open_access = result.get("isOpenAccess") == "Y",
                in_pmc = result.get("inPMC") == "Y",
                cited_by_count = result.get("citedByCount", 0),
                url = (
                    f"https://europepmc.org/article/"
                    f"{result.get('source')}/"
                    f"{result.get('id')}"                    
                )
            )
            
            papers.append(paper)
            
        return papers
    

paper_normalizer = PaperNormalizer()
            
        