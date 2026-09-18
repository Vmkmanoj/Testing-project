import { useEffect, useState } from 'react';
import { clientApi } from '../api';
import { Plus, Trash2, Search, X } from 'lucide-react';

interface Client { id: string; name: string; email: string; phone: string; company_name: string; is_active: boolean; }

function ClientModal({ onClose, onSuccess }: { onClose: () => void; onSuccess: () => void }) {
  const [form, setForm] = useState({ name: '', email: '', phone: '', company_name: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const set = (k: string, v: string) => setForm(f => ({ ...f, [k]: v }));

  const submit = async (e: React.FormEvent) => {
    e.preventDefault(); setError(''); setLoading(true);
    try { await clientApi.create(form); onSuccess(); onClose(); }
    catch (err: any) { setError(err.response?.data?.detail || 'Failed.'); }
    finally { setLoading(false); }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <span className="modal-title">Add Client</span>
          <button className="btn btn-icon btn-outline" onClick={onClose}><X size={16} /></button>
        </div>
        <form onSubmit={submit}>
          <div className="modal-body">
            {error && <div className="alert alert-error">{error}</div>}
            <div className="form-group"><label className="form-label">Name</label><input className="form-input" value={form.name} onChange={e => set('name', e.target.value)} required /></div>
            <div className="form-group"><label className="form-label">Email</label><input className="form-input" type="email" value={form.email} onChange={e => set('email', e.target.value)} /></div>
            <div className="form-grid">
              <div className="form-group"><label className="form-label">Phone</label><input className="form-input" value={form.phone} onChange={e => set('phone', e.target.value)} /></div>
              <div className="form-group"><label className="form-label">Company</label><input className="form-input" value={form.company_name} onChange={e => set('company_name', e.target.value)} /></div>
            </div>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-outline" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn btn-primary" disabled={loading}>{loading ? <span className="spinner" /> : 'Add Client'}</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default function ClientsPage() {
  const [clients, setClients] = useState<Client[]>([]);
  const [filtered, setFiltered] = useState<Client[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  const load = async () => {
    setLoading(true);
    try { const r = await clientApi.getAll(); setClients(r.data.clients || []); }
    catch (_) {} finally { setLoading(false); }
  };
  useEffect(() => { load(); }, []);
  useEffect(() => { setFiltered(clients.filter(c => `${c.name} ${c.email} ${c.company_name}`.toLowerCase().includes(search.toLowerCase()))); }, [search, clients]);

  const handleDelete = async (id: string) => {
    if (!confirm('Delete this client?')) return;
    await clientApi.delete(id); load();
  };

  return (
    <div>
      <div className="page-header">
        <div><h2 className="page-title">Clients</h2><p className="page-subtitle">{clients.length} total clients</p></div>
        <div style={{ display: 'flex', gap: 12 }}>
          <div className="search-bar"><Search size={14} /><input placeholder="Search…" value={search} onChange={e => setSearch(e.target.value)} /></div>
          <button className="btn btn-primary" onClick={() => setShowModal(true)}><Plus size={16} /> Add Client</button>
        </div>
      </div>
      <div className="card">
        <div className="table-wrap">
          {loading ? <div className="loading-page"><span className="spinner" /></div> : (
            <table>
              <thead><tr><th>Name</th><th>Company</th><th>Email</th><th>Phone</th><th>Status</th><th>Actions</th></tr></thead>
              <tbody>
                {filtered.length === 0 ? <tr><td colSpan={6}><div className="empty-state"><p>No clients found.</p></div></td></tr>
                  : filtered.map(c => (
                    <tr key={c.id}>
                      <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{c.name}</td>
                      <td>{c.company_name || '—'}</td>
                      <td>{c.email || '—'}</td>
                      <td>{c.phone || '—'}</td>
                      <td><span className={`status-dot ${c.is_active ? 'dot-green' : 'dot-red'}`} />{c.is_active ? 'Active' : 'Inactive'}</td>
                      <td><button className="btn btn-sm btn-danger" onClick={() => handleDelete(c.id)}><Trash2 size={13} /></button></td>
                    </tr>
                  ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
      {showModal && <ClientModal onClose={() => setShowModal(false)} onSuccess={load} />}
    </div>
  );
}
