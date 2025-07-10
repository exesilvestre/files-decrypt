import { useState } from 'react';
import JsonModal from '../jsonModal';
import './styles.css';
import { downloadFile, getFileJson } from '../../services/apiService';
import { DocumentListsProps } from './types';
import { DocumentAPIModel } from '../../pages/types';



const DocumentList = ({ documents }: DocumentListsProps) => {
  const [jsonData, setJsonData] = useState<object | null>(null);
  const flatDocuments = documents.flat();

  const grouped = flatDocuments.reduce((acc, doc) => {
      console.log('Processing document:', doc);
      const category = doc.category || 'Unknown';
      if (!acc[category]) {
          acc[category] = [];
      }
      acc[category].push(doc);
      return acc;
  }, {} as Record<string, DocumentAPIModel[]>);

  const handleViewJSON = async (guid: string) => {
    try {
      const data = await getFileJson(guid);
      setJsonData(data);
    } catch (err) {
      console.error('Error fetching file JSON:', err);
    }
  };

  const handleCloseModal = () => {
    setJsonData(null);
  };

  if (jsonData) {
    return (
      <div className="container">
        <JsonModal json={jsonData} onClose={handleCloseModal} />
      </div>
    );
  }
  console.log('Grouped documents:', grouped);
  return (
    <div className="container">
      {Object.entries(grouped).map(([category, files]) => (
        <div key={category} className="category">
          <h2>{category}</h2>
          <table className="docTable">
            <thead>
              <tr>
                <th>Filename</th>
                <th>GUID</th>
                <th>Extension</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {files.map((doc) => (
                <tr key={doc.guid}>
                  <td className="filename-cell" title={doc.filename}>
                    {doc.filename}
                  </td>
                  <td>{doc.guid}</td>
                  <td>{doc.metadata?.EXT || ''}</td>
                  <td className="actions">
                    <button onClick={() => downloadFile(doc.guid)}>Download</button>
                    <button onClick={() => handleViewJSON(doc.guid)}>View JSON</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  );
};

export default DocumentList;