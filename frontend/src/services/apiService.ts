import { DocumentAPIModel } from '../pages/types';
// Base URL de la API
const API_BASE_URL = 'http://localhost:8000'

export const uploadFile = async (file: File): Promise<DocumentAPIModel> => {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${API_BASE_URL}/uploadfile/`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    throw new Error('Upload failed');
  }

  const data: DocumentAPIModel = await res.json();
  return data;
};

export const downloadFile = (guid: string): void => {
  const url = `${API_BASE_URL}/downloadFile/${guid}`;

  fetch(url)
    .then(response => {
      if (!response.ok) {
        if (response.status === 404) alert('File not found (404)');
        else if (response.status === 400) alert('Bad request');
        else alert(`Download error: ${response.statusText}`);
        throw new Error('Download failed');
      }
      const filename = response.headers.get('X-Filename') || `file-${guid}`;
      return response.blob().then(blob => ({ blob, filename }));
    })
    .then(({ blob, filename }) => {
      const downloadUrl = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = downloadUrl;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(downloadUrl);
    })
    .catch(error => {
      console.error('Unexpected error while downloading the file', error);
      alert('Unexpected error while downloading the file');
    });
};

export const getFileJson = async (guid: string) => {
  const res = await fetch(`${API_BASE_URL}/file/${guid}`);
  if (!res.ok) throw new Error('Error al obtener JSON');
  return await res.json();
};