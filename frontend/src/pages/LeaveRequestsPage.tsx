import { useEffect, useState } from 'react';
import { leaveRequestApi, leaveTypeApi } from '../api';
import { useAuth } from '../AuthContext';
import { Plus, Check, X, CalendarDays } from 'lucide-react';

interface LR { id: string; user_id: string; leave_type_id: string; start_date: string; end_date: string; total_days: number; reason: string; status: string; }
interface LT { id: string; name: string; }

function ApplyModal({ leaveTypes, onClose, onSuccess }: { leaveTypes: LT[]; onClose: () => void; onSuccess: () => void }) {
  const [form, setForm] = useState({ leave_type_id: leaveTypes[0]?.id || '', start_date: '', end_date: '', total_days: 1, reason: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const set = (k: string, v: any) => setForm(f => ({ ...f, [k]: v }));

  const submit = async (e: React.FormEvent) => {
    e.preventDefault(); setError(''); setLoading(true);
    try { await leaveRequestApi.create(form); onSuccess(); onClose(); }
    catch (err: any) { setError(err.response?.data?.detail || 'Failed to apply for leave.'); }
    finally { setLoading(false); }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <span className="modal-title">Apply for Leave</span>
          <button className="btn btn-icon btn-outline" onClick={onClose}><X size={16} /></button>
        </div>
        <form onSubmit={submit}>
          <div className="modal-body">
            {error && <div className="alert alert-error">{error}</div>}
            <div className="form-group">
              <label className="form-label">Leave Type</label>
              <select className="form-select" value={form.leave_type_id} onChange={e => set('leave_type_id', e.target.value)}>
                {leaveTypes.map(lt => <option key={lt.id} value={lt.id}>{lt.name.replace(/_/g, ' ')}</option>)}
              </select>
            </div>
            <div className="form-grid">
              <div className="form-group"><label className="form-label">Start Date</label><input className="form-input" type="date" value={form.start_date} onChange={e => set('start_date', e.target.value)} required /></div>
              <div className="form-group"><label className="form-label">End Date</label><input className="form-input" type="date" value={form.end_date} onChange={e => set('end_date', e.target.value)} required /></div>
            </div>
            <div className="form-group"><label className="form-label">Total Days</label><input className="form-input" type="number" value={form.total_days} onChange={e => set('total_days', +e.target.value)} min={1} required /></div>
            <div className="form-group"><label className="form-label">Reason (optional)</label><input className="form-input" value={form.reason} onChange={e => set('reason', e.target.value)} placeholder="Brief reason…" /></div>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-outline" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn btn-primary" disabled={loading}>{loading ? <span className="spinner" /> : 'Submit'}</button>
          </div>
        </form>
      </div>
    </div>
  );
}

function ActionModal({ request, onClose, onSuccess }: { request: LR; onClose: () => void; onSuccess: () => void }) {
  const [action, setAction] = useState<'APPROVED' | 'REJECTED'>('APPROVED');
  const [comment, setComment] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const submit = async (e: React.FormEvent) => {
    e.preventDefault(); setError(''); setLoading(true);
    try { await leaveRequestApi.action(request.id, { action, comment }); onSuccess(); onClose(); }
    catch (err: any) { setError(err.response?.data?.detail || 'Failed.'); }
    finally { setLoading(false); }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <span className="modal-title">Review Leave Request</span>
          <button className="btn btn-icon btn-outline" onClick={onClose}><X size={16} /></button>
        </div>
        <form onSubmit={submit}>
          <div className="modal-body">
            {error && <div className="alert alert-error">{error}</div>}
            <div style={{ background: 'rgba(15,23,42,0.4)', borderRadius: 10, padding: 16, marginBottom: 16 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)', fontSize: 13 }}>Duration</span>
                <span style={{ fontWeight: 600 }}>{request.total_days} day(s)</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 8 }}>
                <span style={{ color: 'var(--text-muted)', fontSize: 13 }}>Dates</span>
                <span style={{ fontSize: 13 }}>{request.start_date} → {request.end_date}</span>
              </div>
              {request.reason && <div style={{ marginTop: 8, fontSize: 13, color: 'var(--text-secondary)' }}>"{request.reason}"</div>}
            </div>
            <div className="form-group">
              <label className="form-label">Decision</label>
              <div style={{ display: 'flex', gap: 10 }}>
                {(['APPROVED', 'REJECTED'] as const).map(a => (
                  <button key={a} type="button" onClick={() => setAction(a)}
                    className={`btn ${action === a ? (a === 'APPROVED' ? 'btn-primary' : 'btn-danger') : 'btn-outline'}`}
                    style={{ flex: 1, justifyContent: 'center' }}>
                    {a === 'APPROVED' ? <Check size={14} /> : <X size={14} />} {a}
                  </button>
                ))}
              </div>
            </div>
            <div className="form-group"><label className="form-label">Comment (optional)</label><input className="form-input" value={comment} onChange={e => setComment(e.target.value)} placeholder="Add a comment…" /></div>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-outline" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn btn-primary" disabled={loading}>{loading ? <span className="spinner" /> : 'Confirm'}</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default function LeaveRequestsPage() {
  const { user } = useAuth();
  const [requests, setRequests] = useState<LR[]>([]);
  const [leaveTypes, setLeaveTypes] = useState<LT[]>([]);
  const [loading, setLoading] = useState(true);
  const [showApply, setShowApply] = useState(false);
  const [actionItem, setActionItem] = useState<LR | null>(null);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const limit = 10;

  const isHR = user?.role === 'HR';
  const isManager = user?.role === 'MANAGER';
  const canApprove = isHR || isManager;

  const load = async () => {
    setLoading(true);
    try {
      const [reqRes, ltRes] = await Promise.all([
        canApprove ? leaveRequestApi.getAll(page, limit) : leaveRequestApi.getMy(page, limit),
        leaveTypeApi.getAll(),
      ]);
      setRequests(reqRes.data.items);
      setTotal(reqRes.data.total);
      setLeaveTypes(ltRes.data);
    } catch (_) {} finally { setLoading(false); }
  };
  useEffect(() => { load(); }, [page]);

  const statusBadge = (s: string) =>
    s === 'APPROVED' ? 'badge-green' : s === 'REJECTED' ? 'badge-red' : 'badge-yellow';

  return (
    <div>
      <div className="page-header">
        <div><h2 className="page-title">Leave Requests</h2><p className="page-subtitle">{canApprove ? 'All leave requests' : 'Your requests'}</p></div>
        {!canApprove && <button className="btn btn-primary" onClick={() => setShowApply(true)}><Plus size={16} /> Apply for Leave</button>}
      </div>
      <div className="card">
        <div className="table-wrap">
          {loading ? <div className="loading-page"><span className="spinner" /></div> : (
            <table>
              <thead><tr><th>Employee</th><th>Dates</th><th>Days</th><th>Reason</th><th>Status</th>{canApprove && <th>Action</th>}</tr></thead>
              <tbody>
                {requests.length === 0 ? <tr><td colSpan={canApprove ? 6 : 5}><div className="empty-state"><CalendarDays style={{ width: 48, height: 48 }} /><p>No leave requests found.</p></div></td></tr>
                  : requests.map(r => (
                    <tr key={r.id}>
                      <td style={{ fontWeight: 600, fontSize: 12, color: 'var(--text-muted)', fontFamily: 'monospace' }}>{r.user_id.slice(0, 8)}…</td>
                      <td style={{ fontSize: 13 }}>{r.start_date} → {r.end_date}</td>
                      <td><span className="badge badge-blue">{r.total_days}d</span></td>
                      <td style={{ maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{r.reason || '—'}</td>
                      <td><span className={`badge ${statusBadge(r.status)}`}>{r.status}</span></td>
                      {canApprove && (
                        <td>
                          {r.status === 'PENDING'
                            ? <button className="btn btn-sm btn-outline" onClick={() => setActionItem(r)}>Review</button>
                            : <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>Done</span>}
                        </td>
                      )}
                    </tr>
                  ))}
              </tbody>
            </table>
          )}
        </div>
        {!loading && total > 0 && (
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px', borderTop: '1px solid var(--border)' }}>
            <span style={{ fontSize: 13, color: 'var(--text-muted)' }}>
              Showing {Math.min((page - 1) * limit + 1, total)} to {Math.min(page * limit, total)} of {total} entries
            </span>
            <div style={{ display: 'flex', gap: 8 }}>
              <button 
                className="btn btn-outline btn-sm" 
                disabled={page === 1} 
                onClick={() => setPage(p => p - 1)}
              >
                Previous
              </button>
              <button 
                className="btn btn-outline btn-sm" 
                disabled={page * limit >= total} 
                onClick={() => setPage(p => p + 1)}
              >
                Next
              </button>
            </div>
          </div>
        )}
      </div>
      {showApply && <ApplyModal leaveTypes={leaveTypes} onClose={() => setShowApply(false)} onSuccess={load} />}
      {actionItem && <ActionModal request={actionItem} onClose={() => setActionItem(null)} onSuccess={load} />}
    </div>
  );
}
