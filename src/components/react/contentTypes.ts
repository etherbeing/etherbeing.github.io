export type Project = {
  github_id: string;
  name: string;
  html_url: string | null;
  description: string | null;
  created_at: string | null;
  pushed_at: string | null;
  updated_at?: string | null;
  language: string | null;
  languages: string[];
  stargazers_count?: number;
  watchers_count?: number;
};

export type BlogEntry = {
  id?: string;
  gist_id: string;
  html_url: string | null;
  image_url?: string;
  description: string | null;
  created_at: string | null;
  updated_at?: string | null;
  content?: string;
};
