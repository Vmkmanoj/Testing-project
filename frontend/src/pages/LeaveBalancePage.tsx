import { useQuery } from '@tanstack/react-query';
import { leaveBalanceApi } from '../api';
import { BarChart3 } from 'lucide-react';

interface Balance { id: string; leave_type_id: string; year: number; total_days: number; used_days: number; leave_type_name: string }

export default function LeaveBalancePage() {
  const { data: balances = [], isLoading } = useQuery({
    queryKey: ['leave-balance'],
    queryFn: async () => {
      const r = await leaveBalanceApi.getMy();
      return r.data as Balance[];
    },
  });

  return (
    <div>
      <div className="page-header">
        <div><h2 className="page-title">My Leave Balance</h2><p className="page-subtitle">Current year leave entitlements</p></div>
      </div>

      {isLoading ? <div className="loading-page"><span className="spinner" /></div> : balances.length === 0 ? (
        <div className="card"><div className="card-body"><div className="empty-state"><BarChart3 /><p>No leave balances found. Contact HR to set up your leave entitlements.</p></div></div></div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 16 }}>
          {balances.map(b => {
            const used = b.used_days;
            const total = b.total_days;
            const pct = total > 0 ? (used / total) * 100 : 0;
            const remaining = total - used;
            return (
              <div key={b.id} className="card" style={{ padding: 24 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
                  <div>
                    <div style={{ fontWeight: 700, fontSize: 16, color: 'var(--text-primary)' }}>{b.year}</div>
                    <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>Leave Type : {b.leave_type_name}</div>
                  </div>
                  <div className="stat-icon indigo"><BarChart3 size={18} /></div>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                  <span style={{ fontSize: 13, color: 'var(--text-muted)' }}>Used</span>
                  <span style={{ fontSize: 13, fontWeight: 600 }}>{used} / {total} days</span>
                </div>
                <div style={{ background: 'rgba(15,23,42,0.5)', borderRadius: 8, height: 8, overflow: 'hidden', marginBottom: 12 }}>
                  <div style={{ height: '100%', width: `${pct}%`, background: pct > 80 ? 'var(--rose)' : pct > 50 ? 'var(--amber)' : 'var(--primary)', borderRadius: 8, transition: 'width 0.4s ease' }} />
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span className={`badge ${remaining <= 0 ? 'badge-red' : remaining <= 3 ? 'badge-yellow' : 'badge-green'}`}>{remaining} days remaining</span>
                  <span className="badge badge-gray">{Math.round(pct)}% used</span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
