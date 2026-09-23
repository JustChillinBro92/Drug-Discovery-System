**BACKEND**:
------------
1. Add a ranking system to the synonyms in compound_normalizer.py

2. Disable rdkit's internal logger in rdkit_service.py

3. Text chunker needs semantic chunking and maybe work on full paper text

4. Define an update literature retrieval(by id) method in literature resolver

5. LLM needs to go through the literature retrievals and decide the best retrieval to fetch / update with further literatures (by id)

6. Add tool calls for individual protein, side effects, disease (By Name)

7. Add methods for multiple compound(separated by ',') analysis

8. Add support for protein, side effect, diseases related to compound through chatbot. E.g: Can paracetamol treat body pain?, Is drowzyness a probable cause of paracetamol?, Does cox-1 interact with aspirin?
Notes:
------
-> Probably compound keywords will be needed
-> or normalize compound name using ai
-> Utilize the graph for answers


**FRONTEND**
------------
1. Lazy loading proteins, side effects, diseases under compound in application state (backend support needed)

2. Add loading, success, error states for operations (api calls)