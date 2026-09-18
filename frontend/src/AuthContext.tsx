import { createContext, useContext, useState, type ReactNode } from 'react';
import { authApi } from './api';

interface User { id: string; email: string; first_name: string; last_name: string | null; role: string; }
interface AuthCtx { user: User | null; token: string | null; login: (email: string, password: string) => Promise<void>; logout: () => void; loading: boolean; }

const Ctx = createContext<AuthCtx>({} as AuthCtx);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(() => {
    try { return JSON.parse(localStorage.getItem('user') || 'null'); } catch { return null; }
  });
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'));
  const [loading, setLoading] = useState(false);

  const login = async (email: string, password: string) => {
    setLoading(true);
    try {
      const res = await authApi.login({ email, password });
      const { access_token, user: u } = res.data;
      localStorage.setItem('token', access_token);
      localStorage.setItem('user', JSON.stringify(u));
      setToken(access_token);
      setUser(u);
    } finally { setLoading(false); }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setToken(null);
    setUser(null);
  };

  return <Ctx.Provider value={{ user, token, login, logout, loading }}>{children}</Ctx.Provider>;
}

export const useAuth = () => useContext(Ctx);
