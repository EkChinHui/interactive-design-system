import { useState } from 'react';
import './Modal.css';

interface CreateSystemModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (fileName: string, path: string) => void;
}

export default function CreateSystemModal({ isOpen, onClose, onSuccess }: CreateSystemModalProps) {
  const [name, setName] = useState('');
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:3001/api/generate-design-system', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, prompt }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to generate design system');
      }

      // Reset form
      setName('');
      setPrompt('');
      setIsLoading(false);

      // Call success callback
      onSuccess(data.fileName, data.path);
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
          <h2>Create New Design System</h2>
          <button className="modal-close" onClick={onClose} aria-label="Close modal">
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-group">
            <label htmlFor="system-name">System Name</label>
            <input
              id="system-name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g., Cyberpunk, Retro, Brutalist"
              required
              disabled={isLoading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="system-prompt">Design Description</label>
            <textarea
              id="system-prompt"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe the design system you want to create. Be specific about colors, typography, spacing, and overall aesthetic..."
              rows={6}
              required
              disabled={isLoading}
            />
            <small className="form-hint">
              Example: "A cyberpunk-inspired design system with neon colors, dark backgrounds, and futuristic fonts"
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
              {isLoading ? 'Generating...' : 'Generate Design System'}
            </button>
          </div>
        </form>

        {isLoading && (
          <div className="loading-overlay">
            <div className="spinner"></div>
            <p>Generating your design system... This may take a minute.</p>
          </div>
        )}
      </div>
    </div>
  );
}
