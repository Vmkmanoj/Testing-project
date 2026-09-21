import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { leaveTypeApi } from '../api';
import { Plus, Trash2, Edit2, X } from 'lucide-react';

interface LeaveType { id: string; name: string; description: string; max_days_per_year: number; is_active: boolean; }

function LeaveTypeModal({ item, onClose, onSuccess }: { item?: LeaveType; onClose: () => void; onSuccess: () => void }) {
  const [form, setForm] = useState({ name: item?.name || '', description: item?.description || '', max_days_per_year: item?.max_days_per_year || 10 });
  const [error, setError] = useState('');
  const set = (k: string, v: any) => setForm(f => ({ ...f, [k]: v }));

  const mutation = useMutation({
    mutationFn: () => item ? leaveTypeApi.update(item.id, form) : leaveTypeApi.create(form),
    onSuccess: () => { onSuccess(); onClose(); },
    onError: (err: any) => setError(err.response?.data?.detail || 'Failed.'),
  });

  const submit = (e: React.FormEvent) => { e.preventDefault(); setError(''); mutation.mutate(); };

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
            <button type="submit" className="btn btn-primary" disabled={mutation.isPending}>{mutation.isPending ? <span className="spinner" /> : 'Save'}</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default function LeaveTypesPage() {
  const queryClient = useQueryClient();
  const [modal, setModal] = useState<{ open: boolean; item?: LeaveType }>({ open: false });

  const { data = [], isLoading } = useQuery({
    queryKey: ['leave-types'],
    queryFn: async () => {
      const r = await leaveTypeApi.getAll();
      return r.data as LeaveType[];
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => leaveTypeApi.delete(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['leave-types'] }),
  });

  const handleDelete = (id: string) => {
    if (!confirm('Delete this leave type?')) return;
    deleteMutation.mutate(id);
  };

  const invalidate = () => queryClient.invalidateQueries({ queryKey: ['leave-types'] });

  return (
    <div>
      <div className="page-header">
        <div><h2 className="page-title">Leave Types</h2><p className="page-subtitle">Manage available leave categories</p></div>
        <button className="btn btn-primary" onClick={() => setModal({ open: true })}><Plus size={16} /> Add Type</button>
      </div>
      <div className="card">
        <div className="table-wrap">
          {isLoading ? <div className="loading-page"><span className="spinner" /></div> : (
            <table>
              <thead><tr><th>Name</th><th>Description</th><th>Max Days/Year</th><th>Status</th><th>Actions</th></tr></thead>
              <tbody>
                {data.length === 0 ? <tr><td colSpan={5}><div className="empty-state"><p>No leave types yet.</p></div></td></tr>
                  : data.map(lt => (
                    <tr key={lt.id}>
                      <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{lt.name.replace(/_/g, ' ')}</td>
                      <td>{lt.description || '—'}</td>
                      <td><span className="badge badge-blue">{lt.max_days_per_year} days</span></td>
                      <td><span className={`badge ${lt.is_active ? 'badge-green' : 'badge-gray'}`}>{lt.is_active ? 'Active' : 'Inactive'}</span></td>
                      <td style={{ display: 'flex', gap: 6 }}>
                        <button className="btn btn-sm btn-outline" onClick={() => setModal({ open: true, item: lt })}><Edit2 size={13} /></button>
                        <button
                          className="btn btn-sm btn-danger"
                          onClick={() => handleDelete(lt.id)}
                          disabled={deleteMutation.isPending}
                        >
                          <Trash2 size={13} />
                        </button>
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
      {modal.open && <LeaveTypeModal item={modal.item} onClose={() => setModal({ open: false })} onSuccess={invalidate} />}
    </div>
  );
}
