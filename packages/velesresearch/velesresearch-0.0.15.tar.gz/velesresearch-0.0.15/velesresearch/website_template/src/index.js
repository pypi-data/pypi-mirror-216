import { createRoot } from "react-dom/client";
import SurveyComponent from "./SurveyComponent";
import Footer from "./FooterComponent";

const container = document.getElementById("root");
const root = createRoot(container);
root.render(<SurveyComponent />);
