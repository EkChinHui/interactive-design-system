import { useState } from 'react';
import './Modal.css';

interface EditSystemModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  fileName: string;
  systemName: string;
}

export default function EditSystemModal({
  isOpen,
  onClose,
  onSuccess,
  fileName,
  systemName
}: EditSystemModalProps) {
  const [comment, setComment] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:3001/api/edit-design-system', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ fileName, comment }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to edit design system');
      }

      // Reset form
      setComment('');
      setIsLoading(false);

      // Call success callback
      onSuccess();
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Edit {systemName}</h2>
          <button className="modal-close" onClick={onClose} aria-label="Close modal">
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-group">
            <label htmlFor="edit-comment">What would you like to change?</label>
            <textarea
              id="edit-comment"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="Describe the changes you want to make..."
              rows={6}
              required
              disabled={isLoading}
            />
            <small className="form-hint">
              Example: "Make the primary color more vibrant", "Add rounded corners to all buttons", "Increase font sizes"
            </small>
          </div>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <div className="modal-actions">
            <button
              type="button"
              onClick={onClose}
              className="btn-secondary"
              disabled={isLoading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn-primary"
              disabled={isLoading}
            >
              {isLoading ? 'Updating...' : 'Update Design System'}
            </button>
          </div>
        </form>

        {isLoading && (
          <div className="loading-overlay">
            <div className="spinner"></div>
            <p>Updating your design system... This may take a minute.</p>
          </div>
        )}
      </div>
    </div>
  );
}
