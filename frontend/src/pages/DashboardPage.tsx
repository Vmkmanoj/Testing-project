import { useRef } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { useAuth } from '../AuthContext';
import { employeeApi, clientApi, leaveRequestApi, agentApi } from '../api';
import { Users, Building2, CalendarClock, UserCheck, UploadCloud, Loader } from 'lucide-react';

export default function DashboardPage() {
  const { user } = useAuth();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const isHR = user?.role === 'HR';
  const isManager = user?.role === 'MANAGER';

  const { data: statsData, isLoading } = useQuery({
    queryKey: ['dashboard-stats', user?.role],
    queryFn: async () => {
      const results = await Promise.allSettled([
        isHR ? employeeApi.getAll() : Promise.resolve(null),
        isHR ? clientApi.getAll() : Promise.resolve(null),
        isHR ? leaveRequestApi.getAll() : leaveRequestApi.getMy(),
      ]);
      const empData = results[0].status === 'fulfilled' ? results[0].value?.data : null;
      const cliData = results[1].status === 'fulfilled' ? results[1].value?.data : null;
      const leaveData = results[2].status === 'fulfilled' ? results[2].value?.data : null;
      const actualLeaveData = Array.isArray(leaveData) ? leaveData : leaveData?.items || [];
      const pendingLeaves = actualLeaveData.filter((r: any) => r.status === 'PENDING').length;
      return {
        employees: empData?.total || empData?.employees?.length || 0,
        clients: cliData?.total || cliData?.clients?.length || 0,
        pendingLeaves,
      };
    },
    enabled: !!user,
  });

  const stats = statsData ?? { employees: 0, clients: 0, pendingLeaves: 0 };

  const uploadMutation = useMutation({
    mutationFn: (file: File) => agentApi.uploadPdf(file),
    onSuccess: () => {
      alert('Document uploaded successfully!');
      if (fileInputRef.current) fileInputRef.current.value = '';
    },
    onError: () => {
      alert('Failed to upload document.');
      if (fileInputRef.current) fileInputRef.current.value = '';
    },
  });

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    uploadMutation.mutate(file);
  };

  return (
    <div>
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 className="page-title">Welcome back, {user?.first_name} 👋</h2>
          <p className="page-subtitle">Here's what's happening today</p>
        </div>
        {isHR && (
          <div>
            <input
              type="file"
              accept=".pdf"
              ref={fileInputRef}
              style={{ display: 'none' }}
              onChange={handleFileUpload}
            />
            <button
              className="btn btn-primary"
              style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '10px 16px', fontWeight: 600, boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
              onClick={() => fileInputRef.current?.click()}
              disabled={uploadMutation.isPending}
            >
              {uploadMutation.isPending ? <Loader style={{ animation: 'spin 1s linear infinite' }} size={18} /> : <UploadCloud size={18} />}
              {uploadMutation.isPending ? 'Uploading...' : 'Upload Policy'}
            </button>
          </div>
        )}
      </div>

      {isLoading ? (
        <div className="loading-page"><span className="spinner" /></div>
      ) : (
        <div className="stats-grid">
          {isHR && (
            <>
              <div className="stat-card indigo">
                <div className="stat-icon indigo"><Users size={20} /></div>
                <div className="stat-value">{stats.employees}</div>
                <div className="stat-label">Total Employees</div>
              </div>
              <div className="stat-card emerald">
                <div className="stat-icon emerald"><Building2 size={20} /></div>
                <div className="stat-value">{stats.clients}</div>
                <div className="stat-label">Total Clients</div>
              </div>
            </>
          )}
          <div className="stat-card amber">
            <div className="stat-icon amber"><CalendarClock size={20} /></div>
            <div className="stat-value">{stats.pendingLeaves}</div>
            <div className="stat-label">{isHR || isManager ? 'Pending Leave Requests' : 'My Pending Requests'}</div>
          </div>
          <div className="stat-card rose">
            <div className="stat-icon rose"><UserCheck size={20} /></div>
            <div className="stat-value" style={{ textTransform: 'capitalize', fontSize: 18 }}>{user?.role}</div>
            <div className="stat-label">Your Role</div>
          </div>
        </div>
      )}

      <div className="card">
        <div className="card-header">
          <span className="card-title">Quick Actions</span>
        </div>
        <div className="card-body" style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
          {isHR && <a href="/employees" className="btn btn-outline">👥 Manage Employees</a>}
          {isHR && <a href="/clients" className="btn btn-outline">🏢 Manage Clients</a>}
          {isHR && <a href="/leave-types" className="btn btn-outline">📋 Leave Types</a>}
          {(isHR || isManager) && <a href="/leave-requests" className="btn btn-outline">✅ Review Leaves</a>}
          {!isHR && <a href="/leave-requests" className="btn btn-primary">📝 Apply for Leave</a>}
          {!isHR && <a href="/leave-balances" className="btn btn-outline">📊 My Balance</a>}
        </div>
      </div>
    </div>
  );
}
