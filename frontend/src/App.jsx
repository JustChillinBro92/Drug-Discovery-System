import { Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar/Navbar";
import Sidebar from "./components/Sidebar/Sidebar";
import Sessionbar from "./components/Sessionbar/Sessionbar";
import Footer from "./components/Footer/Footer";

import Home from "./pages/Home/Home";
import Assistant from "./pages/Assisstant/Assistant";
import CompoundAnalysis from "./pages/Compound Analysis/CompoundAnalysis";
import SimilarityAnalysis from "./pages/Similarity Analysis/SimilarityAnalysis";
import LiteratureRetrieval from "./pages/Literature Retrieval/LiteratureRetrieval";

import RecentCompunds from "./pages/Recents/Recent Compounds/RecentCompunds";
import RecentSimilarity from "./pages/Recents/Recent Similarity/RecentSimilarity";
import RecentLiterature from "./pages/Recents/Recent Literature/RecentLiterature";

import "./index.css";

const App = () => {
  return (
    <>
      <div className="page">
        <div className="app">
          <Sidebar/>
          <div className="app-content">
            <Navbar />
            <div className="page-content">
              <Routes>
                <Route path="/" element={<Home/>}/>
                <Route path="/assistant" element={<Assistant/>}/>
                <Route path="/compound-analysis" element={<CompoundAnalysis/>}/>
                <Route path="/similrity-analysis" element={<SimilarityAnalysis/>}/>
                <Route path="/similarity-analysis" element={<SimilarityAnalysis/>}/>
                <Route path="/literature-retrieval" element={<LiteratureRetrieval/>}/>
                <Route path="/recent-compounds" element={<RecentCompunds/>}/>
                <Route path="/recent-similarity" element={<RecentSimilarity/>}/>
                <Route path="/recent-literature" element={<RecentLiterature/>}/>
              </Routes>
            </div>
          </div> 
          <Sessionbar/>
        </div>
        <Footer/>
      </div>
    </>
  )
}

export default App