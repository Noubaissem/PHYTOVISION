import Icon from './Icon';

const severiteBadge = {
  Elevee: "bg-red-50 text-danger border-danger/20",
  Moyenne: "bg-amber-50 text-warning border-warning/20",
  Faible: "bg-blue-50 text-info border-info/20",
  "-": "bg-primary/5 text-primary border-primary/20",
};

const actionBadge = {
  "Traitement curatif": "bg-red-50 text-danger border-danger/20",
  "Traitement preventif": "bg-amber-50 text-warning border-warning/20",
  "Elimination foyer": "bg-red-50 text-danger border-danger/20",
  Surveillance: "bg-blue-50 text-info border-info/20",
};

function SortHeader({ label, field, sortConfig, onSort }) {
  const active = sortConfig.field === field;
  const arrow = active && sortConfig.direction === "asc" ? "up" : "down";

  return (
    <button
      onClick={() => onSort(field)}
      className={`flex items-center gap-1 uppercase tracking-wide font-semibold whitespace-nowrap ${
        active ? "text-primary" : "text-sub hover:text-primary"
      }`}
    >
      {label}
      <span className="text-[10px]">{active ? (arrow === "up" ? "▲" : "▼") : "↕"}</span>
    </button>
  );
}

function HistoriqueTable({ data, onDetails, sortConfig, onSort }) {
  return (
    <div className="bg-card border border-border rounded-2xl overflow-hidden shadow-sm">
      <div className="overflow-x-auto">
        <table className="w-full text-xs">
          <thead>
            <tr className="bg-primary/5 border-b border-border">
              <th className="text-left px-4 py-3">
                <SortHeader label="#" field="id" sortConfig={sortConfig} onSort={onSort} />
              </th>
              <th className="text-left px-4 py-3">
                <SortHeader label="Date" field="date" sortConfig={sortConfig} onSort={onSort} />
              </th>
              <th className="text-left px-4 py-3">
                <SortHeader label="Maladie" field="maladie" sortConfig={sortConfig} onSort={onSort} />
              </th>
              <th className="text-left px-4 py-3">
                <SortHeader label="Severite" field="severite" sortConfig={sortConfig} onSort={onSort} />
              </th>
              <th className="text-left text-sub uppercase tracking-wide font-semibold px-4 py-3 whitespace-nowrap">Decision</th>
              <th className="text-left px-4 py-3">
                <SortHeader label="Confiance" field="confiance" sortConfig={sortConfig} onSort={onSort} />
              </th>
              <th className="text-left px-4 py-3">
                <SortHeader label="Zone" field="zone" sortConfig={sortConfig} onSort={onSort} />
              </th>
              <th className="text-left text-sub uppercase tracking-wide font-semibold px-4 py-3 whitespace-nowrap">NB vs CNN</th>
              <th className="px-4 py-3" />
            </tr>
          </thead>
          <tbody>
            {data.map((row) => {
              const disagreement = row.naiveBayes?.maladie && row.naiveBayes.maladie !== row.cnn?.maladie;

              return (
                <tr key={row.id} className="border-b border-border/60 hover:bg-primary/5 transition-colors">
                  <td className="px-4 py-3 text-sub">
                    {String(row.id).padStart(3, "0")}
                  </td>
                  <td className="px-4 py-3 text-ink whitespace-nowrap">{row.date}</td>
                  <td className="px-4 py-3">
                    <span className="bg-primary/5 text-primary border border-primary/20 px-2.5 py-1 rounded-full whitespace-nowrap">
                      {row.maladie}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <span className={`border px-2.5 py-1 rounded-full whitespace-nowrap ${severiteBadge[row.severite] || "bg-slate-50 text-sub border-border"}`}>
                      {row.severite}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <span className={`border px-2.5 py-1 rounded-full whitespace-nowrap ${actionBadge[row.action] || "bg-slate-50 text-sub border-border"}`}>
                      {row.modeleRetenu || "CNN"}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2">
                      <div className="w-14 h-1.5 bg-border rounded-full">
                        <div
                          className="h-full bg-primary rounded-full"
                          style={{ width: `${Number(row.confiance) || 0}%` }}
                        />
                      </div>
                      <span className="text-ink">{row.confiance}%</span>
                    </div>
                  </td>
                  <td className="px-4 py-3 text-sub whitespace-nowrap">{row.zone}</td>
                  <td className="px-4 py-3">
                    <span className={`border px-2.5 py-1 rounded-full whitespace-nowrap ${
                      disagreement
                        ? "bg-amber-50 text-warning border-warning/20"
                        : "bg-primary/5 text-primary border-primary/20"
                    }`}>
                      {disagreement ? "Desaccord" : "Accord"}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <button
                      onClick={() => onDetails(row)}
                      className="border border-border text-ink px-3 py-1.5 rounded-xl hover:border-primary/40 hover:text-primary transition-colors text-xs flex items-center gap-1.5"
                    >
                      <Icon name="file" className="w-3.5 h-3.5" />
                      Details
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default HistoriqueTable;
