import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AnalyseView        from '../views/AnalyseView';
import HistoriqueView     from '../views/HistoriqueView';
import EpidemiologieView  from '../views/EpidemiologieView';

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/"              element={<AnalyseView />} />
        <Route path="/historique"    element={<HistoriqueView />} />
        <Route path="/epidemiologie" element={<EpidemiologieView />} />
      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;