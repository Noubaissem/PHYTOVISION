import { useMemo, useEffect, useState } from 'react';
import Sidebar from '../components/Sidebar';
import SearchBar from '../components/SearchBar';
import HistoriqueTable from '../components/HistoriqueTable';
import DiagnosticModal from '../components/DiagnosticModal';
import Spinner from '../components/Spinner';
import EmptyState from '../components/EmptyState';
import Icon from '../components/Icon';
import HistoriqueController from '../controllers/HistoriqueController';

const PAGE_SIZE_OPTIONS = [5, 10, 25];

function uniqueValues(data, field) {
  return ["Tous", ...Array.from(new Set(data.map(item => item[field]).filter(Boolean)))];
}

function csvValue(value) {
  const clean = String(value ?? "").replace(/"/g, '""');
  return `"${clean}"`;
}

function HistoriqueView() {
  const [data, setData] = useState([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selected, setSelected] = useState(null);
  const [healthFilter, setHealthFilter] = useState("Toutes");
  const [severityFilter, setSeverityFilter] = useState("Tous");
  const [zoneFilter, setZoneFilter] = useState("Tous");
  const [modelFilter, setModelFilter] = useState("Tous");
  const [confidenceFilter, setConfidenceFilter] = useState("Tous");
  const [sortConfig, setSortConfig] = useState({ field: "date", direction: "desc" });
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);

  useEffect(() => {
    HistoriqueController.load(setData, setLoading, setError);
  }, []);

  useEffect(() => {
    setPage(1);
  }, [query, healthFilter, severityFilter, zoneFilter, modelFilter, confidenceFilter, pageSize]);

  const summary = useMemo(() => {
    const total = data.length;
    const sick = data.filter(d => d.maladie !== "Sain").length;
    const healthy = data.filter(d => d.maladie === "Sain").length;
    const disagreements = data.filter(d => d.naiveBayes?.maladie && d.naiveBayes.maladie !== d.cnn?.maladie).length;
    const avgConfidence = total
      ? Math.round(data.reduce((sum, d) => sum + (Number(d.confiance) || 0), 0) / total)
      : 0;

    return [
      { label: "Analyses", count: total, sub: `${avgConfidence}% confiance moy.`, icon: "history", color: "text-ink" },
      { label: "Maladies", count: sick, sub: `${healthy} feuilles saines`, icon: "shield", color: "text-danger" },
      { label: "Desaccords NB/CNN", count: disagreements, sub: "preuves des limites NB", icon: "alert", color: "text-warning" },
      { label: "Decisions CNN", count: data.filter(d => d.modeleRetenu === "CNN").length, sub: "modele final IRAD", icon: "check", color: "text-primary" },
    ];
  }, [data]);

  const filtered = useMemo(() => {
    return HistoriqueController
      .filter(data, query)
      .filter(d => {
        if (healthFilter === "Maladies" && d.maladie === "Sain") return false;
        if (healthFilter === "Saines" && d.maladie !== "Sain") return false;
        if (severityFilter !== "Tous" && d.severite !== severityFilter) return false;
        if (zoneFilter !== "Tous" && d.zone !== zoneFilter) return false;
        if (modelFilter !== "Tous" && d.modeleRetenu !== modelFilter) return false;
        if (confidenceFilter === "Haute" && Number(d.confiance) < 85) return false;
        if (confidenceFilter === "Faible" && Number(d.confiance) >= 85) return false;
        return true;
      });
  }, [data, query, healthFilter, severityFilter, zoneFilter, modelFilter, confidenceFilter]);

  const sorted = useMemo(() => {
    const severityRank = { Elevee: 3, Moyenne: 2, Faible: 1, "-": 0 };

    return [...filtered].sort((a, b) => {
      const { field, direction } = sortConfig;
      const factor = direction === "asc" ? 1 : -1;
      let left = a[field];
      let right = b[field];

      if (field === "date") {
        left = new Date(left).getTime();
        right = new Date(right).getTime();
      } else if (field === "severite") {
        left = severityRank[left] ?? 0;
        right = severityRank[right] ?? 0;
      } else if (field === "confiance" || field === "id") {
        left = Number(left) || 0;
        right = Number(right) || 0;
      } else {
        left = String(left || "").toLowerCase();
        right = String(right || "").toLowerCase();
      }

      if (left > right) return factor;
      if (left < right) return -factor;
      return 0;
    });
  }, [filtered, sortConfig]);

  const totalPages = Math.max(1, Math.ceil(sorted.length / pageSize));
  const currentPage = Math.min(page, totalPages);
  const paginated = sorted.slice((currentPage - 1) * pageSize, currentPage * pageSize);

  const handleSort = (field) => {
    setSortConfig(current => ({
      field,
      direction: current.field === field && current.direction === "asc" ? "desc" : "asc"
    }));
  };

  const resetFilters = () => {
    setQuery("");
    setHealthFilter("Toutes");
    setSeverityFilter("Tous");
    setZoneFilter("Tous");
    setModelFilter("Tous");
    setConfidenceFilter("Tous");
  };

  const handleExport = () => {
    const headers = [
      "Date", "Maladie finale", "Severite", "Action", "Confiance finale", "Zone",
      "Modele retenu", "Prediction NB", "Confiance NB", "Prediction CNN",
      "Confiance CNN", "F1 CNN", "Cluster", "Intervention"
    ];
    const rows = sorted.map(d => [
      d.date,
      d.maladie,
      d.severite,
      d.action,
      d.confiance,
      d.zone,
      d.modeleRetenu,
      d.naiveBayes?.maladie,
      d.naiveBayes?.confiance,
      d.cnn?.maladie,
      d.cnn?.confiance,
      d.cnn?.f1Score,
      d.clustering?.cluster,
      d.clustering?.intervention
    ].map(csvValue).join(","));

    const blob = new Blob([[headers.map(csvValue).join(","), ...rows].join("\n")], {
      type: "text/csv;charset=utf-8;"
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "phytovision_diagnostics_filtres.csv";
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex min-h-screen bg-bg">
      <Sidebar />

      {selected && (
        <DiagnosticModal
          diagnostic={selected}
          onClose={() => setSelected(null)}
        />
      )}

      <main className="flex-1 flex flex-col min-w-0">
        <header className="bg-card/95 border-b border-border px-6 py-4 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 shadow-sm">
          <div>
            <h1 className="text-xl font-semibold text-ink">Historique des diagnostics</h1>
            <p className="text-sm text-sub mt-1">{filtered.length} resultats affiches sur {data.length} analyses</p>
          </div>
          <button
            onClick={handleExport}
            disabled={sorted.length === 0}
            className="bg-primary text-white text-xs px-4 py-2.5 rounded-xl hover:bg-green-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors flex items-center gap-2 shadow-sm shadow-primary/20"
          >
            <Icon name="download" className="w-4 h-4" />
            Exporter CSV filtre
          </button>
        </header>

        <div className="flex-1 p-5 lg:p-6 flex flex-col gap-5">
          {error && (
            <div className="border border-warning/25 bg-amber-50 text-warning rounded-2xl px-4 py-3 text-xs">
              {error}
            </div>
          )}

          <section className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
            {summary.map(s => (
              <div key={s.label} className="bg-card border border-border rounded-2xl p-4 flex items-center gap-3 shadow-sm">
                <span className="w-10 h-10 rounded-2xl bg-primary/10 text-primary flex items-center justify-center">
                  <Icon name={s.icon} className="w-5 h-5" />
                </span>
                <div>
                  <p className="text-xs text-sub">{s.label}</p>
                  <p className={`text-lg font-semibold ${s.color}`}>{s.count}</p>
                  <p className="text-xs text-sub mt-0.5">{s.sub}</p>
                </div>
              </div>
            ))}
          </section>

          <section className="bg-card border border-border rounded-2xl p-4 shadow-sm flex flex-col gap-3">
            <div className="flex flex-col xl:flex-row gap-3 xl:items-center">
              <SearchBar
                value={query}
                onChange={setQuery}
                placeholder="Rechercher par maladie, zone, action..."
              />
              <div className="flex flex-wrap gap-2">
                {["Toutes", "Maladies", "Saines"].map(f => (
                  <button
                    key={f}
                    onClick={() => setHealthFilter(f)}
                    className={`text-xs px-4 py-2.5 rounded-xl border transition-colors whitespace-nowrap ${
                      healthFilter === f
                        ? "bg-primary text-white border-primary shadow-sm shadow-primary/20"
                        : "bg-card border-border text-sub hover:border-primary/40 hover:text-primary"
                    }`}
                  >
                    {f}
                  </button>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-5 gap-2">
              <select value={severityFilter} onChange={(e) => setSeverityFilter(e.target.value)} className="bg-white border border-border text-ink text-xs rounded-xl px-3 py-2.5 outline-none focus:border-primary/50">
                {uniqueValues(data, "severite").map(value => <option key={value}>{value}</option>)}
              </select>
              <select value={zoneFilter} onChange={(e) => setZoneFilter(e.target.value)} className="bg-white border border-border text-ink text-xs rounded-xl px-3 py-2.5 outline-none focus:border-primary/50">
                {uniqueValues(data, "zone").map(value => <option key={value}>{value}</option>)}
              </select>
              <select value={modelFilter} onChange={(e) => setModelFilter(e.target.value)} className="bg-white border border-border text-ink text-xs rounded-xl px-3 py-2.5 outline-none focus:border-primary/50">
                {uniqueValues(data, "modeleRetenu").map(value => <option key={value}>{value}</option>)}
              </select>
              <select value={confidenceFilter} onChange={(e) => setConfidenceFilter(e.target.value)} className="bg-white border border-border text-ink text-xs rounded-xl px-3 py-2.5 outline-none focus:border-primary/50">
                {["Tous", "Haute", "Faible"].map(value => <option key={value}>{value}</option>)}
              </select>
              <button
                onClick={resetFilters}
                className="bg-white border border-border text-sub text-xs px-3 py-2.5 rounded-xl hover:border-primary/40 hover:text-primary transition-colors"
              >
                Reinitialiser
              </button>
            </div>
          </section>

          {loading ? (
            <div className="flex-1 flex items-center justify-center py-20">
              <Spinner size="lg" text="Chargement des diagnostics..." />
            </div>
          ) : sorted.length === 0 ? (
            <EmptyState
              icon="history"
              title="Aucun diagnostic trouve"
              subtitle="Aucun resultat ne correspond a votre recherche. Essayez un autre filtre."
              action="Reinitialiser la recherche"
              onAction={resetFilters}
            />
          ) : (
            <>
              <HistoriqueTable
                data={paginated}
                onDetails={(row) => setSelected(row)}
                sortConfig={sortConfig}
                onSort={handleSort}
              />

              <div className="bg-card border border-border rounded-2xl px-4 py-3 flex flex-col md:flex-row md:items-center md:justify-between gap-3 shadow-sm">
                <p className="text-xs text-sub">
                  Page {currentPage} sur {totalPages} - {sorted.length} resultats
                </p>
                <div className="flex items-center gap-2">
                  <select
                    value={pageSize}
                    onChange={(e) => setPageSize(Number(e.target.value))}
                    className="bg-white border border-border text-ink text-xs rounded-xl px-3 py-2 outline-none focus:border-primary/50"
                  >
                    {PAGE_SIZE_OPTIONS.map(size => (
                      <option key={size} value={size}>{size} / page</option>
                    ))}
                  </select>
                  <button
                    onClick={() => setPage(p => Math.max(1, p - 1))}
                    disabled={currentPage === 1}
                    className="bg-white border border-border text-ink text-xs px-3 py-2 rounded-xl hover:border-primary/40 disabled:opacity-40 disabled:cursor-not-allowed"
                  >
                    Precedent
                  </button>
                  <button
                    onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                    disabled={currentPage === totalPages}
                    className="bg-white border border-border text-ink text-xs px-3 py-2 rounded-xl hover:border-primary/40 disabled:opacity-40 disabled:cursor-not-allowed"
                  >
                    Suivant
                  </button>
                </div>
              </div>
            </>
          )}
        </div>
      </main>
    </div>
  );
}

export default HistoriqueView;
