import { useEffect, useState } from 'react';
import { employeeApi, authApi } from '../api';
import { Plus, Trash2, Search, X, Edit } from 'lucide-react';
import { useAuth } from '../AuthContext';

interface Employee { id: string; first_name: string; last_name: string | null; email: string; role: string; is_active: boolean; manager_id?: string | null; manager_name?: string | null; }

function RegisterModal({ onClose, onSuccess, managers }: { onClose: () => void; onSuccess: () => void; managers: Employee[] }) {
  const [form, setForm] = useState({ first_name: '', last_name: '', email: '', password: '', role: 'EMPLOYEE', manager_id: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const set = (k: string, v: string) => setForm(f => ({ ...f, [k]: v }));

  const submit = async (e: React.FormEvent) => {
    e.preventDefault(); setError(''); setLoading(true);
    try { await authApi.register(form); onSuccess(); onClose(); }
    catch (err: any) { setError(err.response?.data?.detail || 'Failed to register employee.'); }
    finally { setLoading(false); }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <span className="modal-title">Register Employee</span>
          <button className="btn btn-icon btn-outline" onClick={onClose}><X size={16} /></button>
        </div>
        <form onSubmit={submit}>
          <div className="modal-body">
            {error && <div className="alert alert-error">{error}</div>}
            <div className="form-grid">
              <div className="form-group"><label className="form-label">First Name</label><input className="form-input" value={form.first_name} onChange={e => set('first_name', e.target.value)} required /></div>
              <div className="form-group"><label className="form-label">Last Name</label><input className="form-input" value={form.last_name} onChange={e => set('last_name', e.target.value)} /></div>
            </div>
            <div className="form-group"><label className="form-label">Email</label><input className="form-input" type="email" value={form.email} onChange={e => set('email', e.target.value)} required /></div>
            <div className="form-group"><label className="form-label">Password</label><input className="form-input" type="password" value={form.password} onChange={e => set('password', e.target.value)} required /></div>
            <div className="form-grid">
              <div className="form-group">
                <label className="form-label">Role</label>
                <select className="form-select" value={form.role} onChange={e => set('role', e.target.value)}>
                  <option value="EMPLOYEE">Employee</option>
                  <option value="MANAGER">Manager</option>
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Manager</label>
                <select className="form-select" value={form.manager_id} onChange={e => set('manager_id', e.target.value)}>
                  <option value="">-- No Manager --</option>
                  {managers.map(m => (
                    <option key={m.id} value={m.id}>{m.first_name} {m.last_name || ''}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-outline" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn btn-primary" disabled={loading}>{loading ? <span className="spinner" /> : 'Register'}</button>
          </div>
        </form>
      </div>
    </div>
  );
}

function EditModal({ employee, managers, onClose, onSuccess }: { employee: Employee; managers: Employee[]; onClose: () => void; onSuccess: () => void }) {
  const [form, setForm] = useState({ first_name: employee.first_name, last_name: employee.last_name || '', is_active: employee.is_active, manager_id: employee.manager_id || '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const set = (k: string, v: any) => setForm(f => ({ ...f, [k]: v }));

  const submit = async (e: React.FormEvent) => {
    e.preventDefault(); setError(''); setLoading(true);
    try { await employeeApi.update(employee.id, form); onSuccess(); onClose(); }
    catch (err: any) { setError(err.response?.data?.detail || 'Failed to update employee.'); }
    finally { setLoading(false); }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <span className="modal-title">Edit Employee</span>
          <button className="btn btn-icon btn-outline" onClick={onClose}><X size={16} /></button>
        </div>
        <form onSubmit={submit}>
          <div className="modal-body">
            {error && <div className="alert alert-error">{error}</div>}
            <div className="form-grid">
              <div className="form-group"><label className="form-label">First Name</label><input className="form-input" value={form.first_name} onChange={e => set('first_name', e.target.value)} required /></div>
              <div className="form-group"><label className="form-label">Last Name</label><input className="form-input" value={form.last_name} onChange={e => set('last_name', e.target.value)} /></div>
            </div>
            <div className="form-group">
              <label className="form-label">Manager</label>
              <select className="form-select" value={form.manager_id} onChange={e => set('manager_id', e.target.value)}>
                <option value="">-- No Manager --</option>
                {managers.filter(m => m.id !== employee.id).map(m => (
                  <option key={m.id} value={m.id}>{m.first_name} {m.last_name || ''}</option>
                ))}
              </select>
            </div>
            <div className="form-group" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <input type="checkbox" checked={form.is_active} onChange={e => set('is_active', e.target.checked)} />
              <label className="form-label" style={{ marginBottom: 0 }}>Active</label>
            </div>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-outline" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn btn-primary" disabled={loading}>{loading ? <span className="spinner" /> : 'Save Changes'}</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default function EmployeesPage() {
  const { user } = useAuth();
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [managers, setManagers] = useState<Employee[]>([]);
  const [filtered, setFiltered] = useState<Employee[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingEmployee, setEditingEmployee] = useState<Employee | null>(null);
  const [deleting, setDeleting] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    try { 
      const [empRes, manRes] = await Promise.all([
        employeeApi.getAll(),
        employeeApi.getManagers()
      ]);
      setEmployees(empRes.data.employees || []); 
      setManagers(manRes.data.employees || []);
    }
    catch (_) {} finally { setLoading(false); }
  };
  useEffect(() => { load(); }, []);
  useEffect(() => { setFiltered(employees.filter(e => `${e.first_name} ${e.last_name} ${e.email}`.toLowerCase().includes(search.toLowerCase()))); }, [search, employees]);

  const handleDelete = async (id: string) => {
    if (!confirm('Delete this employee?')) return;
    setDeleting(id);
    try { await employeeApi.delete(id); load(); } catch (_) {} finally { setDeleting(null); }
  };

  const isHR = user?.role === 'HR';
  const canEdit = isHR;

  return (
    <div>
      <div className="page-header">
        <div>
          <h2 className="page-title">Employees</h2>
          <p className="page-subtitle">{employees.length} total employees</p>
        </div>
        <div style={{ display: 'flex', gap: 12 }}>
          <div className="search-bar">
            <Search size={14} />
            <input placeholder="Search employees…" value={search} onChange={e => setSearch(e.target.value)} />
          </div>
          {isHR && <button className="btn btn-primary" onClick={() => setShowModal(true)}><Plus size={16} /> Register</button>}
        </div>
      </div>

      <div className="card">
        <div className="table-wrap">
          {loading ? <div className="loading-page"><span className="spinner" /></div> : (
            <table>
              <thead>
                <tr><th>Name</th><th>Email</th><th>Role</th><th>Manager</th><th>Status</th>{isHR && <th>Actions</th>}</tr>
              </thead>
              <tbody>
                {filtered.length === 0 ? (
                  <tr><td colSpan={isHR ? 6 : 5}><div className="empty-state"><p>No employees found.</p></div></td></tr>
                ) : filtered.map(emp => (
                  <tr key={emp.id}>
                    <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{emp.first_name} {emp.last_name || ''}</td>
                    <td>{emp.email}</td>
                    <td><span className={`badge badge-${emp.role === 'HR' ? 'blue' : emp.role === 'MANAGER' ? 'green' : 'yellow'}`}>{emp.role}</span></td>
                    <td style={{ color: 'var(--text-secondary)' }}>{emp.manager_name || '-'}</td>
                    <td>
                      <span className={`status-dot ${emp.is_active ? 'dot-green' : 'dot-red'}`} />
                      {emp.is_active ? 'Active' : 'Inactive'}
                    </td>
                    {isHR && (
                      <td>
                        <div style={{ display: 'flex', gap: 8 }}>
                          <button className="btn btn-sm btn-outline" onClick={() => setEditingEmployee(emp)} title="Edit">
                            <Edit size={13} />
                          </button>
                          <button className="btn btn-sm btn-danger" onClick={() => handleDelete(emp.id)} disabled={deleting === emp.id} title="Delete">
                            {deleting === emp.id ? <span className="spinner" style={{ width: 12, height: 12 }} /> : <Trash2 size={13} />}
                          </button>
                        </div>
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {showModal && <RegisterModal managers={managers} onClose={() => setShowModal(false)} onSuccess={load} />}
      {editingEmployee && <EditModal employee={editingEmployee} managers={managers} onClose={() => setEditingEmployee(null)} onSuccess={load} />}
    </div>
  );
}
