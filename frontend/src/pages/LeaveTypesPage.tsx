import { useEffect, useState } from 'react';
import { leaveTypeApi } from '../api';
import { Plus, Trash2, Edit2, X } from 'lucide-react';

interface LeaveType { id: string; name: string; description: string; max_days_per_year: number; is_active: boolean; }

function LeaveTypeModal({ item, onClose, onSuccess }: { item?: LeaveType; onClose: () => void; onSuccess: () => void }) {
  const [form, setForm] = useState({ name: item?.name || '', description: item?.description || '', max_days_per_year: item?.max_days_per_year || 10 });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const set = (k: string, v: any) => setForm(f => ({ ...f, [k]: v }));

  const submit = async (e: React.FormEvent) => {
    e.preventDefault(); setError(''); setLoading(true);
    try {
      if (item) await leaveTypeApi.update(item.id, form);
      else await leaveTypeApi.create(form);
      onSuccess(); onClose();
    } catch (err: any) { setError(err.response?.data?.detail || 'Failed.'); }
    finally { setLoading(false); }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <span className="modal-title">{item ? 'Edit' : 'Add'} Leave Type</span>
          <button className="btn btn-icon btn-outline" onClick={onClose}><X size={16} /></button>
        </div>
        <form onSubmit={submit}>
          <div className="modal-body">
            {error && <div className="alert alert-error">{error}</div>}
            <div className="form-group"><label className="form-label">Name</label><input className="form-input" value={form.name} onChange={e => set('name', e.target.value)} required /></div>
            <div className="form-group"><label className="form-label">Description</label><input className="form-input" value={form.description} onChange={e => set('description', e.target.value)} /></div>
            <div className="form-group"><label className="form-label">Max Days / Year</label><input className="form-input" type="number" value={form.max_days_per_year} onChange={e => set('max_days_per_year', +e.target.value)} min={1} required /></div>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-outline" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn btn-primary" disabled={loading}>{loading ? <span className="spinner" /> : 'Save'}</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default function LeaveTypesPage() {
  const [leaveTypes, setLeaveTypes] = useState<LeaveType[]>([]);
  const [loading, setLoading] = useState(true);
  const [modal, setModal] = useState<{ open: boolean; item?: LeaveType }>({ open: false });

  const load = async () => {
    setLoading(true);
    try { const r = await leaveTypeApi.getAll(); setLeaveTypes(r.data); }
    catch (_) {} finally { setLoading(false); }
  };
  useEffect(() => { load(); }, []);

  const handleDelete = async (id: string) => {
    if (!confirm('Delete this leave type?')) return;
    await leaveTypeApi.delete(id); load();
  };

  return (
    <div>
      <div className="page-header">
        <div><h2 className="page-title">Leave Types</h2><p className="page-subtitle">Manage available leave categories</p></div>
        <button className="btn btn-primary" onClick={() => setModal({ open: true })}><Plus size={16} /> Add Type</button>
      </div>
      <div className="card">
        <div className="table-wrap">
          {loading ? <div className="loading-page"><span className="spinner" /></div> : (
            <table>
              <thead><tr><th>Name</th><th>Description</th><th>Max Days/Year</th><th>Status</th><th>Actions</th></tr></thead>
              <tbody>
                {leaveTypes.length === 0 ? <tr><td colSpan={5}><div className="empty-state"><p>No leave types yet.</p></div></td></tr>
                  : leaveTypes.map(lt => (
                    <tr key={lt.id}>
                      <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{lt.name.replace(/_/g, ' ')}</td>
                      <td>{lt.description || '—'}</td>
                      <td><span className="badge badge-blue">{lt.max_days_per_year} days</span></td>
                      <td><span className={`badge ${lt.is_active ? 'badge-green' : 'badge-gray'}`}>{lt.is_active ? 'Active' : 'Inactive'}</span></td>
                      <td style={{ display: 'flex', gap: 6 }}>
                        <button className="btn btn-sm btn-outline" onClick={() => setModal({ open: true, item: lt })}><Edit2 size={13} /></button>
                        <button className="btn btn-sm btn-danger" onClick={() => handleDelete(lt.id)}><Trash2 size={13} /></button>
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
      {modal.open && <LeaveTypeModal item={modal.item} onClose={() => setModal({ open: false })} onSuccess={load} />}
    </div>
  );
}
