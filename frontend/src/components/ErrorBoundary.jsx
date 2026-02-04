import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught:', error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '300px',
          padding: '40px',
          textAlign: 'center',
          gap: '16px',
        }}>
          <AlertTriangle size={48} style={{ color: 'var(--warning, #f59e0b)' }} />
          <h2 style={{ margin: 0, fontSize: '20px', fontWeight: 600 }}>
            Algo deu errado
          </h2>
          <p style={{ color: 'var(--text-muted, #94a3b8)', maxWidth: '400px', lineHeight: 1.5 }}>
            Ocorreu um erro inesperado nesta seção. Tente recarregar a página.
          </p>
          <button
            className="btn btn-primary"
            onClick={this.handleReset}
            style={{ marginTop: '8px' }}
          >
            <RefreshCw size={16} />
            Tentar Novamente
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
