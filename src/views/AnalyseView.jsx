import { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';
import StatisticCard from '../components/StatisticCard';
import UploadZone from '../components/UploadZone';
import ResultCards from '../components/ResultCards';
import Spinner from '../components/Spinner';
import Icon from '../components/Icon';
import AnalyseController from '../controllers/AnalyseController';
import DashboardController from '../controllers/DashboardController';

const CAMEROON_REGIONS = [
  'Adamaoua',
  'Centre',
  'Est',
  'Extreme-Nord',
  'Littoral',
  'Nord',
  'Nord-Ouest',
  'Ouest',
  'Sud',
  'Sud-Ouest',
];

function AnalyseView() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [zone, setZone] = useState('Centre');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    DashboardController.load(setStats, () => {});
  }, []);

  const handleFileSelect = (selectedFile) => {
    setFile(selectedFile);
    setPreview(URL.createObjectURL(selectedFile));
    setResult(null);
  };

  const handleAnalyse = () => {
    if (!file) return;
    AnalyseController.analyser(file, zone, setResult, setLoading, setError);
  };

  return (
    <div className="flex min-h-screen bg-bg">
      <Sidebar />

      <main className="flex-1 flex flex-col min-w-0">
        <header className="bg-card/95 border-b border-border px-6 py-4 flex items-center justify-between shadow-sm">
          <div>
            <h1 className="text-xl font-semibold text-ink">
              Tableau de bord Analyse
            </h1>
            <p className="text-sm text-sub mt-1">IRAD Cameroun - Diagnostic du mais</p>
          </div>
          <span className="bg-primary/10 text-primary border border-primary/20 text-xs px-3 py-1.5 rounded-full font-semibold flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-primary" />
            Systeme actif
          </span>
        </header>

        <div className="flex-1 p-5 lg:p-6 flex flex-col gap-5">
          <section className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
            <StatisticCard
              label="Total analyses"
              value={stats?.totalAnalyses ?? "-"}
              sub="+12 cette semaine"
              icon="chart"
            />
            <StatisticCard
              label="Maladies detectees"
              value={stats?.totalMaladies ?? "-"}
              sub="79% des analyses"
              color="text-danger"
              icon="shield"
            />
            <StatisticCard
              label="Feuilles saines"
              value={stats?.totalSaines ?? "-"}
              sub="21% des analyses"
              color="text-primary"
              icon="leaf"
            />
            <StatisticCard
              label="Maladie dominante"
              value={stats?.maladieDominante ?? "-"}
              sub="47 cas detectes"
              color="text-warning"
              icon="alert"
            />
          </section>

          <section className="grid grid-cols-1 xl:grid-cols-2 gap-5">
            <div className="bg-card border border-border rounded-2xl p-5 shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-base font-semibold text-ink">Importer une feuille</h2>
                  <p className="text-xs text-sub mt-1">Ajoutez une image claire pour comparer Naif Bayes et CNN.</p>
                </div>
                <span className="w-10 h-10 rounded-2xl bg-primary/10 text-primary flex items-center justify-center">
                  <Icon name="upload" className="w-5 h-5" />
                </span>
              </div>

              <UploadZone onFileSelect={handleFileSelect} preview={preview} />

              <div className="mt-4">
                <label className="text-xs font-semibold text-sub mb-2 block">Region du Cameroun</label>
                <select
                  value={zone}
                  onChange={(e) => setZone(e.target.value)}
                  className="w-full bg-white border border-border text-ink text-sm rounded-2xl px-4 py-3 outline-none focus:border-primary/50"
                >
                  {CAMEROON_REGIONS.map((region) => (
                    <option key={region} value={region}>{region}</option>
                  ))}
                </select>
              </div>

              <button
                onClick={handleAnalyse}
                disabled={!file || loading}
                className="w-full mt-4 bg-primary text-white font-semibold text-sm py-3 rounded-2xl hover:bg-green-700 disabled:opacity-40 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2 shadow-sm shadow-primary/20"
              >
                {loading ? (
                  <>
                    <Spinner size="sm" />
                    <span>Analyse en cours...</span>
                  </>
                ) : (
                  <>
                    <Icon name="activity" className="w-4 h-4" />
                    Lancer l'analyse
                  </>
                )}
              </button>

              {error && (
                <p className="text-danger text-xs mt-3 text-center">{error}</p>
              )}
            </div>

            <div className="bg-card border border-border rounded-2xl p-5 shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-base font-semibold text-ink">Comparaison des modeles</h2>
                  <p className="text-xs text-sub mt-1">Baseline Naif Bayes, modele CNN et decision finale IRAD.</p>
                </div>
                <span className="w-10 h-10 rounded-2xl bg-primary/10 text-primary flex items-center justify-center">
                  <Icon name="shield" className="w-5 h-5" />
                </span>
              </div>

              {result ? (
                <ResultCards result={result} />
              ) : (
                <div className="flex flex-col items-center justify-center min-h-64 text-sub text-sm bg-primary/5 border border-primary/10 rounded-2xl">
                  <span className="w-14 h-14 rounded-2xl bg-white border border-border flex items-center justify-center text-primary mb-3 shadow-sm">
                    <Icon name="leaf" className="w-7 h-7" />
                  </span>
                  <p className="text-ink font-semibold">Aucune analyse en cours</p>
                  <p className="text-xs mt-1">Importez une image pour commencer.</p>
                </div>
              )}
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}

export default AnalyseView;
