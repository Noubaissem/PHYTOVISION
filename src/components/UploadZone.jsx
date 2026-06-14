import { useRef } from 'react';
import Icon from './Icon';

function UploadZone({ onFileSelect, preview }) {
  const fileInputRef = useRef();
  const cameraInputRef = useRef();

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) onFileSelect(file);
  };

  const handleChange = (e) => {
    const file = e.target.files[0];
    if (file) onFileSelect(file);
  };

  return (
    <div>
      <div
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
        onClick={() => fileInputRef.current.click()}
        className="border-2 border-dashed border-primary/25 bg-primary/5 rounded-2xl p-6 text-center cursor-pointer hover:border-primary/50 hover:bg-primary/10 transition-colors"
      >
        {preview ? (
          <img
            src={preview}
            alt="Feuille selectionnee"
            className="max-h-56 mx-auto rounded-2xl object-contain shadow-sm"
          />
        ) : (
          <div>
            <div className="w-12 h-12 bg-white border border-border rounded-2xl flex items-center justify-center mx-auto mb-3 text-primary shadow-sm">
              <Icon name="upload" className="w-6 h-6" />
            </div>
            <p className="text-ink font-semibold text-sm">
              Glisser une image ici
            </p>
            <p className="text-sub text-xs mt-1">
              JPG ou PNG, max 10 MB
            </p>
          </div>
        )}
      </div>

      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={handleChange}
      />

      <input
        ref={cameraInputRef}
        type="file"
        accept="image/*"
        capture="environment"
        className="hidden"
        onChange={handleChange}
      />

      <div className="grid grid-cols-2 gap-2 mt-3">
        <button
          onClick={() => fileInputRef.current.click()}
          className="bg-white border border-border text-ink text-xs py-2.5 rounded-xl hover:border-primary/40 hover:text-primary transition-colors flex items-center justify-center gap-2"
        >
          <Icon name="file" className="w-4 h-4" />
          Choisir fichier
        </button>
        <button
          onClick={() => cameraInputRef.current.click()}
          className="bg-white border border-border text-ink text-xs py-2.5 rounded-xl hover:border-primary/40 hover:text-primary transition-colors flex items-center justify-center gap-2"
        >
          <Icon name="camera" className="w-4 h-4" />
          Prendre photo
        </button>
      </div>
    </div>
  );
}

export default UploadZone;
