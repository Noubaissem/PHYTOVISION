function Spinner({ size = "md", text = "" }) {
  const sizes = {
    sm: "w-4 h-4 border-2",
    md: "w-6 h-6 border-2",
    lg: "w-10 h-10 border-3",
  };

  return (
    <div className="flex flex-col items-center justify-center gap-3">
      <div
        className={`${sizes[size]} border-primary border-t-transparent
                    rounded-full animate-spin`}
      />
      {text && (
        <p className="text-xs text-sub animate-pulse">{text}</p>
      )}
    </div>
  );
}

export default Spinner;