import { useEffect, useState } from 'react';
import { projectApi, teamApi, employeeApi, clientApi } from '../api';
import { useAuth } from '../AuthContext';
import {  Users, X, FolderOpen, UserPlus } from 'lucide-react';

interface Team { id: string; name: string; description: string; project_id: string; member_count: number; }
interface Project { id: string; name: string; description: string; status: string; client_id: string; }
interface Client { id: string; name: string; }
interface Employee { id: string; first_name: string; last_name: string | null; email: string; role: string; }

function CreateProjectModal({ clients, onClose, onSuccess }: { clients: Client[]; onClose: () => void; onSuccess: () => void }) {
  const [form, setForm] = useState({ name: '', description: '', client_id: clients[0]?.id || '', status: 'PLANNING' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const set = (k: string, v: string) => setForm(f => ({ ...f, [k]: v }));

  const submit = async (e: React.FormEvent) => {
    e.preventDefault(); setError(''); setLoading(true);
    try { await projectApi.create(form); onSuccess(); onClose(); }
    catch (err: any) { setError(err.response?.data?.detail || 'Failed to create project.'); }
    finally { setLoading(false); }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <span className="modal-title">Create Project</span>
          <button className="btn btn-icon btn-outline" onClick={onClose}><X size={16} /></button>
        </div>
        <form onSubmit={submit}>
          <div className="modal-body">
            {error && <div className="alert alert-error">{error}</div>}
            <div className="form-group"><label className="form-label">Project Name</label><input className="form-input" value={form.name} onChange={e => set('name', e.target.value)} required /></div>
            <div className="form-group"><label className="form-label">Description</label><input className="form-input" value={form.description} onChange={e => set('description', e.target.value)} /></div>
            <div className="form-group">
              <label className="form-label">Client</label>
              <select className="form-select" value={form.client_id} onChange={e => set('client_id', e.target.value)}>
                {clients.length === 0
                  ? <option value="">No clients — ask HR to add one</option>
                  : clients.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
              </select>
            </div>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-outline" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn btn-primary" disabled={loading || clients.length === 0}>{loading ? <span className="spinner" /> : 'Create'}</button>
          </div>
        </form>
      </div>
    </div>
  );
}

function CreateTeamModal({ projects, onClose, onSuccess }: { projects: Project[]; onClose: () => void; onSuccess: () => void }) {
  const [form, setForm] = useState({ name: '', description: '', project_id: projects[0]?.id || '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const set = (k: string, v: string) => setForm(f => ({ ...f, [k]: v }));

  const submit = async (e: React.FormEvent) => {
    e.preventDefault(); setError(''); setLoading(true);
    try { await projectApi.createTeam(form); onSuccess(); onClose(); }
    catch (err: any) { setError(err.response?.data?.detail || 'Failed.'); }
    finally { setLoading(false); }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <span className="modal-title">Create Team</span>
          <button className="btn btn-icon btn-outline" onClick={onClose}><X size={16} /></button>
        </div>
        <form onSubmit={submit}>
          <div className="modal-body">
            {error && <div className="alert alert-error">{error}</div>}
            <div className="form-group"><label className="form-label">Team Name</label><input className="form-input" value={form.name} onChange={e => set('name', e.target.value)} required /></div>
            <div className="form-group"><label className="form-label">Description</label><input className="form-input" value={form.description} onChange={e => set('description', e.target.value)} /></div>
            <div className="form-group">
              <label className="form-label">Project</label>
              <select className="form-select" value={form.project_id} onChange={e => set('project_id', e.target.value)}>
                {projects.length === 0
                  ? <option value="">No projects yet — create one first</option>
                  : projects.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
              </select>
            </div>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-outline" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn btn-primary" disabled={loading || projects.length === 0}>{loading ? <span className="spinner" /> : 'Create Team'}</button>
          </div>
        </form>
      </div>
    </div>
  );
}

function AssignMemberModal({ teams, employees, onClose, onSuccess }: { teams: Team[]; employees: Employee[]; onClose: () => void; onSuccess: () => void }) {
  const [form, setForm] = useState({ team_id: teams[0]?.id || '', user_id: employees[0]?.id || '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const set = (k: string, v: string) => setForm(f => ({ ...f, [k]: v }));

  const submit = async (e: React.FormEvent) => {
    e.preventDefault(); setError(''); setSuccess(''); setLoading(true);
    try { await teamApi.assign(form); setSuccess('Employee assigned successfully!'); onSuccess(); }
    catch (err: any) { setError(err.response?.data?.detail || 'Failed to assign.'); }
    finally { setLoading(false); }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <span className="modal-title">Assign Employee to Team</span>
          <button className="btn btn-icon btn-outline" onClick={onClose}><X size={16} /></button>
        </div>
        <form onSubmit={submit}>
          <div className="modal-body">
            {error && <div className="alert alert-error">{error}</div>}
            {success && <div className="alert alert-success">{success}</div>}
            <div className="form-group">
              <label className="form-label">Team</label>
              <select className="form-select" value={form.team_id} onChange={e => set('team_id', e.target.value)}>
                {teams.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Employee</label>
              <select className="form-select" value={form.user_id} onChange={e => set('user_id', e.target.value)}>
                {employees.map(emp => (
                  <option key={emp.id} value={emp.id}>
                    {emp.first_name} {emp.last_name || ''} ({emp.role})
                  </option>
                ))}
              </select>
            </div>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-outline" onClick={onClose}>Close</button>
            <button type="submit" className="btn btn-primary" disabled={loading}>{loading ? <span className="spinner" /> : 'Assign'}</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default function TeamsPage() {
  const { user } = useAuth();
  const [teams, setTeams] = useState<Team[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [clients, setClients] = useState<Client[]>([]);
  const [loading, setLoading] = useState(true);
  const [dataReady, setDataReady] = useState(false);
  const [modal, setModal] = useState<'project' | 'team' | 'assign' | null>(null);
  const isManager = user?.role === 'MANAGER';

  const load = async () => {
    setLoading(true);
    try {
      const [teamsRes, projRes, empRes, cliRes] = await Promise.allSettled([
        teamApi.getAll(),
        projectApi.getAll(),
        employeeApi.getAll(),
        clientApi.getAll(),
      ]);
      if (teamsRes.status === 'fulfilled') setTeams(teamsRes.value.data.teams || []);
      if (projRes.status === 'fulfilled') setProjects(projRes.value.data.projects || []);
      if (empRes.status === 'fulfilled') setEmployees(empRes.value.data.employees || []);
      if (cliRes.status === 'fulfilled') setClients(cliRes.value.data.clients || []);
    } catch (_) {}
    setLoading(false);
    setDataReady(true);
  };

  useEffect(() => { load(); }, []);

  const openModal = (type: 'project' | 'team' | 'assign') => {
    if (!dataReady) return;
    setModal(type);
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h2 className="page-title">Teams</h2>
          <p className="page-subtitle">{teams.length} team(s) across {projects.length} project(s)</p>
        </div>
        {isManager && (
          <div style={{ display: 'flex', gap: 10 }}>
            <button className="btn btn-outline" onClick={() => openModal('project')} disabled={!dataReady}>
              <FolderOpen size={15} /> New Project
            </button>
            <button className="btn btn-outline" onClick={() => openModal('team')} disabled={!dataReady || projects.length === 0}>
              <Users size={15} /> New Team
            </button>
            <button className="btn btn-primary" onClick={() => openModal('assign')} disabled={!dataReady || teams.length === 0}>
              <UserPlus size={15} /> Assign Employee
            </button>
          </div>
        )}
      </div>

      {/* Projects Section */}
      {projects.length > 0 && (
        <div style={{ marginBottom: 28 }}>
          <h3 style={{ fontSize: 14, fontWeight: 600, color: 'var(--text-muted)', marginBottom: 12, textTransform: 'uppercase', letterSpacing: '0.06em' }}>Projects</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: 14 }}>
            {projects.map(p => (
              <div key={p.id} className="card" style={{ padding: 20 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 12 }}>
                  <div style={{ fontWeight: 700, fontSize: 15 }}>{p.name}</div>
                  <span className={`badge ${p.status === 'PLANNING' ? 'badge-yellow' : p.status === 'ACTIVE' ? 'badge-green' : 'badge-gray'}`}>{p.status}</span>
                </div>
                <div style={{ fontSize: 13, color: 'var(--text-muted)' }}>{p.description || 'No description'}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Teams Section */}
      <div>
        <h3 style={{ fontSize: 14, fontWeight: 600, color: 'var(--text-muted)', marginBottom: 12, textTransform: 'uppercase', letterSpacing: '0.06em' }}>Teams</h3>
        {loading ? <div className="loading-page"><span className="spinner" /></div> : teams.length === 0 ? (
          <div className="card"><div className="card-body">
            <div className="empty-state">
              <Users style={{ width: 48, height: 48 }} />
              <p>{isManager ? 'No teams yet. Create a project first, then add a team.' : 'No teams have been created yet.'}</p>
            </div>
          </div></div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 14 }}>
            {teams.map(t => (
              <div key={t.id} className="card" style={{ padding: 20 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
                  <div style={{ fontWeight: 700, fontSize: 15 }}>{t.name}</div>
                  <div className="stat-icon indigo" style={{ width: 32, height: 32 }}><Users size={15} /></div>
                </div>
                <div style={{ fontSize: 13, color: 'var(--text-muted)', marginBottom: 14 }}>{t.description || 'No description'}</div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span className="badge badge-blue">{t.member_count} member{t.member_count !== 1 ? 's' : ''}</span>
                  {isManager && (
                    <button className="btn btn-sm btn-outline" onClick={() => openModal('assign')} style={{ fontSize: 11 }}>
                      <UserPlus size={12} /> Assign
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Modals */}
      {modal === 'project' && <CreateProjectModal clients={clients} onClose={() => setModal(null)} onSuccess={load} />}
      {modal === 'team' && <CreateTeamModal projects={projects} onClose={() => setModal(null)} onSuccess={load} />}
      {modal === 'assign' && <AssignMemberModal teams={teams} employees={employees} onClose={() => setModal(null)} onSuccess={load} />}
    </div>
  );
}

