import { useEffect, useState } from "react";

export type GithubSession = {
  is_authenticated: boolean;
  username?: string;
  email?: string;
  github_login?: string;
  avatar_url?: string;
  can_comment_on_gists?: boolean;
  csrf_token: string;
};

const anonymousSession: GithubSession = {
  is_authenticated: false,
  csrf_token: "",
};

export function useGithubSession(apiUrl: string) {
  const [session, setSession] = useState<GithubSession>(anonymousSession);
  const [isLoading, setIsLoading] = useState(true);

  async function refreshSession() {
    const response = await fetch(`${apiUrl}/api/auth/github/session/`, {
      credentials: "include",
    });
    const payload: GithubSession = await response.json();
    setSession(payload);
    setIsLoading(false);
    return payload;
  }

  useEffect(() => {
    refreshSession().catch(() => {
      setIsLoading(false);
    });
  }, [apiUrl]);

  async function logout() {
    const currentSession = session.csrf_token ? session : await refreshSession();
    const response = await fetch(`${apiUrl}/api/auth/logout/`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": currentSession.csrf_token,
      },
      body: JSON.stringify({}),
    });
    const payload: GithubSession = await response.json();
    setSession(payload);
  }

  function login(nextUrl?: string, intent?: "comment") {
    const next = nextUrl || `${location.pathname}${location.search}${location.hash}`;
    const intentQuery = intent ? `&intent=${encodeURIComponent(intent)}` : "";
    location.assign(
      `${apiUrl}/api/auth/github/login/?next=${encodeURIComponent(next)}${intentQuery}`,
    );
  }

  return {
    session,
    isLoading,
    refreshSession,
    login,
    logout,
  };
}
