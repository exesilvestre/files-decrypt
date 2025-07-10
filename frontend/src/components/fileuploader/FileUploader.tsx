import { useState } from 'react';
import './styles.css';
import { uploadFile } from '../../services/apiService';
import { DocumentAPIModel } from '../../pages/types';

interface Props {
  onUploadComplete: (docs: DocumentAPIModel[]) => void;
}

const FileUploader = ({ onUploadComplete }: Props) => {
  const [dragging, setDragging] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragging(false);

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      setSelectedFile(files[0]);
      setFileName(files[0].name);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      setSelectedFile(files[0]);
      setFileName(files[0].name);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    try {
      const data = await uploadFile(selectedFile);
      onUploadComplete([data]);
      setSelectedFile(null);
      setFileName(null);
    } catch (error) {
      console.error('Upload error', error);
    }
  };

  const handleRemove = () => {
    setSelectedFile(null);
    setFileName(null);
  };

  return (
    <div className="container">
      <div
        className={`dropzone ${dragging ? 'dragging' : ''}`}
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
      >
        <input
          type="file"
          id="fileInput"
          onChange={handleFileChange}
          className="input"
        />
        <label htmlFor="fileInput" className="label">
          {fileName ? (
            <div className="fileDisplay">
              <span className="fileName">{fileName}</span>
            </div>
          ) : (
            <>
              <strong>Drag & drop</strong> your file here or{' '}
              <span className="browse">browse</span>
            </>
          )}
        </label>
      </div>

      {selectedFile && (
        <div className="buttonGroup">
            <button className="removeButton" onClick={handleRemove}>
            Eliminar
            </button>
            <button className="uploadButton" onClick={handleUpload}>
            Enviar
            </button>
        </div>
        )}

    </div>
  );
};

export default FileUploader;