import { useLocation, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import { LayoutDashboard, Users, Building2, UsersRound, CalendarDays, FileText, BarChart3, LogOut } from 'lucide-react';
import { type ReactNode } from 'react';
import ChatWidget from './ChatWidget';

interface NavItem { label: string; path: string; icon: ReactNode; roles?: string[]; }

const navItems: NavItem[] = [
    { label: 'Dashboard', path: '/', icon: <LayoutDashboard size={18} /> },
    { label: 'Employees', path: '/employees', icon: <Users size={18} /> },
    { label: 'Org Chart', path: '/org-chart', icon: <UsersRound size={18} /> },
    { label: 'Teams', path: '/teams', icon: <UsersRound size={18} />, roles: ['MANAGER'] },
    { label: 'Clients', path: '/clients', icon: <Building2 size={18} />, roles: ['HR'] },
    { label: 'Leave Types', path: '/leave-types', icon: <FileText size={18} />, roles: ['HR'] },
    { label: 'Leave Requests', path: '/leave-requests', icon: <CalendarDays size={18} /> },
    { label: 'My Balance', path: '/leave-balances', icon: <BarChart3 size={18} />, roles: ['EMPLOYEE', 'MANAGER'] },
    { label: 'Policies', path: '/policies', icon: <FileText size={18} /> },
];

export default function Layout({ children }: { children: ReactNode }) {
    const { user, logout } = useAuth();
    const location = useLocation();
    const navigate = useNavigate();

    const handleLogout = () => { logout(); navigate('/login'); };

    const visibleItems = navItems.filter(item => !item.roles || (user && item.roles.includes(user.role)));
    const initials = user ? `${user.first_name[0]}${user.last_name?.[0] || ''}`.toUpperCase() : '?';

    const topbarTitles: Record<string, { title: string; subtitle: string }> = {
        '/': { title: 'Dashboard', subtitle: 'Overview of your workspace' },
        '/employees': { title: 'Employees', subtitle: 'Manage your team members' },
        '/org-chart': { title: 'Org Chart', subtitle: 'Company hierarchy' },
        '/teams': { title: 'Teams', subtitle: 'Create and manage project teams' },
        '/clients': { title: 'Clients', subtitle: 'Manage client accounts' },
        '/leave-types': { title: 'Leave Types', subtitle: 'Configure leave categories' },
        '/leave-requests': { title: 'Leave Requests', subtitle: 'View and manage requests' },
        '/leave-balances': { title: 'Leave Balance', subtitle: 'Your leave entitlements' },
        '/policies': { title: 'Company Policies', subtitle: 'View and manage policy documents' },
    };
    const current = topbarTitles[location.pathname] || { title: 'EMS', subtitle: '' };

    return (
        <div className="app-layout">
            {/* Sidebar */}
            <aside className="sidebar">
                <div className="sidebar-logo">
                    <div className="logo-icon">E</div>
                    <div>
                        <div className="logo-text">EMS Pulse</div>
                        <div className="logo-sub">Management System</div>
                    </div>
                </div>

                <nav className="sidebar-nav">
                    <div className="nav-section-label">Navigation</div>
                    {visibleItems.map(item => (
                        <Link
                            key={item.path}
                            to={item.path}
                            className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
                        >


                            {item.icon}
                            {item.label}
                        </Link>
                    ))}
                </nav>

                <div className="sidebar-footer">
                    <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '10px 4px', marginBottom: 8 }}>
                        <div className="user-avatar" style={{ width: 34, height: 34, fontSize: 12 }}>{initials}</div>
                        <div style={{ flex: 1, minWidth: 0 }}>
                            <div style={{ fontSize: 13, fontWeight: 600, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                                {user?.first_name} {user?.last_name || ''}
                            </div>
                            <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>{user?.email}</div>
                        </div>
                    </div>
                    <button className="nav-item" onClick={handleLogout} style={{ color: 'var(--rose)', width: '100%' }}>
                        <LogOut size={16} /> Sign out
                    </button>
                </div>
            </aside>

            {/* Main */}
            <main className="main-content">
                <div className="topbar">
                    <div>
                        <div className="topbar-title">{current.title}</div>
                        <div className="topbar-subtitle">{current.subtitle}</div>
                    </div>
                    <div className="topbar-right">
                        <span className={`role-badge role-${user?.role}`}>{user?.role}</span>
                        <div className="user-avatar">{initials}</div>
                    </div>
                </div>

                <div className="page-content">{children}</div>
            </main>

            <ChatWidget />
        </div>
    );
}
