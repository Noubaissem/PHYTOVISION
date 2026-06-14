import Icon from './Icon';

function StatisticCard({ label, value, sub, color = "text-ink", icon = "chart" }) {
  return (
    <div className="bg-card border border-border rounded-2xl p-4 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="text-xs text-sub uppercase tracking-wide mb-1">
            {label}
          </p>
          <p className={`text-2xl font-semibold ${color} truncate`}>
            {value}
          </p>
          {sub && (
            <p className="text-xs text-sub mt-1">{sub}</p>
          )}
        </div>
        <span className="w-10 h-10 rounded-2xl bg-primary/10 text-primary flex items-center justify-center shrink-0">
          <Icon name={icon} className="w-5 h-5" />
        </span>
      </div>
    </div>
  );
}

export default StatisticCard;
