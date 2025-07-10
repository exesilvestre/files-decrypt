// src/pages/FileUploadPage.tsx
import { useState } from 'react';
import FileUploader from '../components/fileuploader';
import DocumentList from '../components/DocumentsList';
import { DocumentAPIModel } from './types';


const FileUploadPage = () => {
  const [documents, setDocuments] = useState<DocumentAPIModel[]>([]);

  const handleUploadComplete = (newDocs: DocumentAPIModel[]) => {
    setDocuments((prev) => [...prev, ...newDocs]);
  };

  return (
    <div>
      <FileUploader onUploadComplete={handleUploadComplete} />
      <DocumentList documents={documents} />
    </div>
  );
};

export default FileUploadPage;
