import { useEffect, useState, useRef } from 'react';
import { agentApi } from '../api';
import { useAuth } from '../AuthContext';
import { FileText, Trash2, Upload, File as FileIcon, Search, Loader2 } from 'lucide-react';

interface Policy {
  id: string;
  title: string;
  file_name: string;
  created_at: string;
}

export default function PolicyPage() {
  const [policies, setPolicies] = useState<Policy[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [search, setSearch] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { user } = useAuth();
  
  const isHR = user?.role === 'HR' || user?.role === 'ADMIN'; // Ensure proper permission checks

  const fetchPolicies = async () => {
    try {
      const res = await agentApi.getPolicies();
      setPolicies(res.data);
    } catch (error) {
      console.error('Failed to fetch policies', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPolicies();
  }, []);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    try {
      await agentApi.uploadPdf(file);
      await fetchPolicies();
    } catch (error) {
      console.error('Failed to upload document', error);
      alert('Failed to upload document.');
    } finally {
      setUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this policy document?')) return;
    
    try {
      await agentApi.deletePolicy(id);
      setPolicies(policies.filter(p => p.id !== id));
    } catch (error) {
      console.error('Failed to delete document', error);
      alert('Failed to delete document.');
    }
  };

  const filteredPolicies = policies.filter(p => 
    p.title.toLowerCase().includes(search.toLowerCase()) || 
    p.file_name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="page-container fade-in">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <div>
          <h2>Company Policies</h2>
          <p className="text-muted">View and manage company policy documents.</p>
        </div>
        {isHR && (
          <div>
            <input
              type="file"
              ref={fileInputRef}
              style={{ display: 'none' }}
              accept="application/pdf"
              onChange={handleFileUpload}
            />
            <button 
              className="btn btn-primary" 
              onClick={() => fileInputRef.current?.click()}
              disabled={uploading}
              style={{ display: 'flex', alignItems: 'center', gap: '8px' }}
            >
              {uploading ? <Loader2 size={16} className="spin" /> : <Upload size={16} />}
              {uploading ? 'Uploading...' : 'Upload Policy'}
            </button>
          </div>
        )}
      </div>

      <div className="card" style={{ marginBottom: '24px' }}>
        <div style={{ padding: '16px', borderBottom: '1px solid var(--border-color)', display: 'flex', gap: '12px', alignItems: 'center' }}>
          <Search size={18} style={{ color: 'var(--text-muted)' }} />
          <input 
            type="text" 
            placeholder="Search policies..." 
            className="form-input" 
            style={{ border: 'none', background: 'transparent', padding: 0, width: '100%', outline: 'none' }}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        
        {loading ? (
          <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
            <Loader2 size={24} className="spin" style={{ margin: '0 auto', marginBottom: '8px' }} />
            Loading policies...
          </div>
        ) : filteredPolicies.length === 0 ? (
          <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
            <FileText size={48} style={{ margin: '0 auto', marginBottom: '16px', opacity: 0.2 }} />
            <p>No policy documents found.</p>
          </div>
        ) : (
          <div className="table-responsive">
            <table className="table">
              <thead>
                <tr>
                  <th>Document Name</th>
                  <th>Date Added</th>
                  {isHR && <th style={{ textAlign: 'right' }}>Actions</th>}
                </tr>
              </thead>
              <tbody>
                {filteredPolicies.map(policy => (
                  <tr key={policy.id}>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                        <div style={{ 
                          width: '40px', height: '40px', borderRadius: '8px', 
                          background: 'rgba(59, 130, 246, 0.1)', color: 'var(--primary)',
                          display: 'flex', alignItems: 'center', justifyContent: 'center'
                        }}>
                          <FileIcon size={20} />
                        </div>
                        <div>
                          <div style={{ fontWeight: 500 }}>{policy.title}</div>
                          <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{policy.file_name}</div>
                        </div>
                      </div>
                    </td>
                    <td>
                      {new Date(policy.created_at).toLocaleDateString()}
                    </td>
                    {isHR && (
                      <td style={{ textAlign: 'right' }}>
                        <button 
                          className="btn-icon" 
                          style={{ color: 'var(--rose)' }}
                          onClick={() => handleDelete(policy.id)}
                          title="Delete Document"
                        >
                          <Trash2 size={18} />
                        </button>
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
