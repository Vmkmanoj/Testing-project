import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './AuthContext';
import Layout from './components/Layout';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import EmployeesPage from './pages/EmployeesPage';
import TeamsPage from './pages/TeamsPage';
import ClientsPage from './pages/ClientsPage';
import LeaveTypesPage from './pages/LeaveTypesPage';
import LeaveBalancePage from './pages/LeaveBalancePage';
import LeaveRequestsPage from './pages/LeaveRequestsPage';
import OrgChartPage from './pages/OrgChartPage';
import PolicyPage from './pages/PolicyPage';

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { user } = useAuth();
  return user ? <>{children}</> : <Navigate to="/login" replace />;
}

function AppRoutes() {
  const { user } = useAuth();
  return (
    <Routes>
      <Route path="/login" element={user ? <Navigate to="/" replace /> : <LoginPage />} />
      <Route path="/*" element={
        <PrivateRoute>
          <Layout>
            <Routes>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/employees" element={<EmployeesPage />} />
              <Route path="/teams" element={<TeamsPage />} />
              <Route path="/clients" element={<ClientsPage />} />
              <Route path="/leave-types" element={<LeaveTypesPage />} />
              <Route path="/leave-balances" element={<LeaveBalancePage />} />
              <Route path="/leave-requests" element={<LeaveRequestsPage />} />
              <Route path="/org-chart" element={<OrgChartPage />} />

              {user?.role == "HR" ? (
                  <Route path="/policies" element={<PolicyPage />} />
              ) : (
                <></>
              )}
            </Routes>
          </Layout>
        </PrivateRoute>
      } />
    </Routes>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </AuthProvider>
  );
}
