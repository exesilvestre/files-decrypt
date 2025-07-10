import './styles.css';

interface Props {
  json: object | null;
  onClose: () => void;
}

const JsonModal = ({ json, onClose }: Props) => {
  if (!json) return null;

  return (
    <div className="modalOverlay" onClick={onClose}>
      <div className="modalContent" onClick={(e) => e.stopPropagation()}>
        <button className="closeButton" onClick={onClose}>Cerrar</button>
        <pre>{JSON.stringify(json, null, 2)}</pre>
      </div>
    </div>
  );
};

export default JsonModal;