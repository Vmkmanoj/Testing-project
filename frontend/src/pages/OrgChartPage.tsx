import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { employeeApi } from '../api';
import { Users, User as UserIcon, ChevronDown, ChevronRight } from 'lucide-react';

interface Employee {
  id: string;
  first_name: string;
  last_name: string | null;
  email: string;
  role: string;
  is_active: boolean;
  manager_id: string | null;
  manager_name: string | null;
}

function OrgNode({ employee, employees }: { employee: Employee, employees: Employee[] }) {
  const [expanded, setExpanded] = useState(true);
  const subordinates = employees.filter(e => e.manager_id === employee.id);

  return (
    <div style={{ marginLeft: 24, marginTop: 12 }}>
      <div
        style={{
          display: 'flex', alignItems: 'center', gap: 12, padding: '12px 20px',
          background: 'var(--surface)', border: '1px solid var(--border)',
          borderRadius: 8, cursor: subordinates.length > 0 ? 'pointer' : 'default',
          width: 'fit-content', minWidth: 280,
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
        }}
        onClick={() => setExpanded(!expanded)}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', width: 24, height: 24 }}>
          {subordinates.length > 0 ? (
            expanded ? <ChevronDown size={18} color="var(--text-secondary)" /> : <ChevronRight size={18} color="var(--text-secondary)" />
          ) : (
            <UserIcon size={18} color="var(--text-muted)" />
          )}
        </div>
        <div style={{ flex: 1 }}>
          <div style={{ fontWeight: 600, fontSize: 15, color: 'var(--text-primary)' }}>{employee.first_name} {employee.last_name || ''}</div>
          <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 2 }}>{employee.role}</div>
        </div>
        {subordinates.length > 0 && (
          <span className={`badge badge-${employee.role === 'MANAGER' || employee.role === 'HR' ? 'green' : 'blue'}`}>
            {subordinates.length} direct report{subordinates.length !== 1 ? 's' : ''}
          </span>
        )}
      </div>

      {expanded && subordinates.length > 0 && (
        <div style={{ borderLeft: '2px solid var(--border)', marginLeft: 12, paddingLeft: 12, paddingTop: 8 }}>
          {subordinates.map(sub => (
            <OrgNode key={sub.id} employee={sub} employees={employees} />
          ))}
        </div>
      )}
    </div>
  );
}

export default function OrgChartPage() {
  const { data: employees = [], isLoading } = useQuery({
    queryKey: ['org-chart'],
    queryFn: async () => {
      const res = await employeeApi.getAll();
      return (res.data.employees || []) as Employee[];
    },
  });

  const employeeIds = new Set(employees.map(e => e.id));
  const topLevel = employees.filter(e => !e.manager_id || !employeeIds.has(e.manager_id));

  return (
    <div>
      <div className="page-header">
        <div>
          <h2 className="page-title">Organization Chart</h2>
          <p className="page-subtitle">View company hierarchy and reporting lines</p>
        </div>
      </div>

      <div className="card">
        <div style={{ padding: 32, overflowX: 'auto', minHeight: 400 }}>
          {isLoading ? (
            <div className="loading-page"><span className="spinner" /></div>
          ) : employees.length === 0 ? (
            <div className="empty-state"><Users size={48} /><p>No employees found.</p></div>
          ) : topLevel.length === 0 ? (
            <div className="empty-state"><p>No hierarchy found. Assign managers to view the chart.</p></div>
          ) : (
            <div style={{ marginLeft: -24 }}>
              {topLevel.map(emp => (
                <OrgNode key={emp.id} employee={emp} employees={employees} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
