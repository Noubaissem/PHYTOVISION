import Icon from './Icon';

function SearchBar({ value, onChange, placeholder }) {
  return (
    <div className="flex items-center gap-2 bg-card border border-border rounded-2xl px-4 py-2.5 flex-1 shadow-sm focus-within:border-primary/50 focus-within:ring-4 focus-within:ring-primary/10 transition-all">
      <Icon name="search" className="w-4 h-4 text-sub" />
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder || "Rechercher..."}
        className="bg-transparent outline-none text-ink text-sm placeholder-sub flex-1"
      />
    </div>
  );
}

export default SearchBar;
