import { 
  FlaskConical, 
  LayoutDashboard, 
  BotMessageSquare,
  BookOpenText,
  Microscope,
  ChartNoAxesCombined,
  ClipboardList,
  ListClock,
  PanelLeftClose,
  PanelLeftOpen,
  ListChevronsUpDown,
  ListChevronsDownUp 
} from "lucide-react" 

import "./Sidebar.css"

const Sidebar = () => {
  return (
    <div className="sidebar">
      <div className="title-container">
        <div className="title">
          <h2>Drug <FlaskConical/></h2>
          <h2>Discovery AI</h2>
          <h3>AI RAG Research Station</h3>
        </div>
        <div className="panel-open-close">
          <PanelLeftClose/>
        </div>
      </div>

      <div className="navigations-container">
        <div className="navigations">
          <ul>
            <span>
              <h4>MAIN CONSOLE</h4>
              <ListChevronsUpDown className="icon"/>
            </span>
            <li><LayoutDashboard/><p>Dashboard</p></li>
            <li><BotMessageSquare/><p>AI Assistant</p></li>
          </ul>

          <ul>
            <span>
              <h4>KNOWLEDGE RETRIEVAL</h4>
              <ListChevronsUpDown className="icon"/>
            </span>
            <li><BookOpenText/><p>Literature Retrieval</p></li>
            <li className="recents"><ListClock/><p>Recent Retrievals</p></li>
          </ul>

          <ul>
            <span>
              <h4>COMPOUND DISCOVERY</h4>
              <ListChevronsUpDown className="icon"/>
            </span>
            <li><Microscope/><p>Compound Analysis</p></li>
            <li className="recents"><ListClock/><p>Recent Compound Analysis</p></li>

            <li><ChartNoAxesCombined/><p>Similarity Analysis</p></li>
            <li className="recents"><ListClock/><p>Recent Similarity Analysis</p></li>
          </ul>
          
          <ul>
            <span>
              <h4>RESEARCH FINDINGS</h4>
              <ListChevronsUpDown className="icon"/>
            </span>
            <li><ClipboardList/><p>Research Reports</p></li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default Sidebar