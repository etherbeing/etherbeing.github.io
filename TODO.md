# Roadmap
1. - [x] Integrate the frontend with the auth mechanism on the backend only authenticated users can access the dashboard
2. - [ ] Make only users with the scope 'superuser' to access the dashboard, this scope should only be managed locally and no user can register itself as such
3. - [ ] Integrate the frontend and the backend by using the OpenApi.json endpoint, this mean we are going to search for endpoints tagged in an specific way and auto generate forms for it based on other metadata on the dashboard (like a django admin but better)
4. - [ ] Render the data set by the admin user into the frontend
5. - [ ] Make sure the admin user can create new entries for the blog, and the entries are displayed in the frontend
6. - [ ] The admin user should be able to see the comments and moderate them from the admin site, post can be CRUDed
7. - [ ] Integrate with Google ReCaptcha to avoid bots to post data
8. - [ ] Implement the contact form so users can contact us, this should be protected by recaptcha
9. - [ ] Protect the comment endpoint with recaptcha as well as the login, and register endpoints
10. - [ ] So far we should be able to use our site completely so now let's put it on production and let's go to the hardened steps
11. - [ ] Using keycloak implement oauth integration for local oauth.
12. - [ ] Using google, facebook, x and github implement the oauth social auths.
13. - [ ] Implement the SSO features for signing in with our devices
14. - [ ] Implement a channel for live updates on websocket for live updates on comments on post
15. - [ ] Implement a channel for live updates on websocket for live updates on blogs
16. - [ ] Using PWA implement live notifications on new blog entries and RSS feeds
17. - [ ] Allow users to quickly add blog posts to favorites so he can watch again its favorite posts, this should allow the user to filter posts based on preferences
18. - [ ] Implement JWT token refresh and expiration
19. - [ ] Implement in site payments and donation through PayPal and cryptocurrencies.
20. - [ ] Implement stats on the admin dashboard to measure, user flow, revenues and more
21. - [ ] Implement a task manager for queueing the jobs obtained through the site
22. - [ ] Implement in page chat for assistance
23. - [ ] Integrate with `Eve: EGO Neural Network` (Our own neural network)
24. - [ ] Design how to make courses created by us more accessible to everyone
25. - [ ] Implement a Watchdog for services deployed to clients
26. - [ ] Implement a live collaboration tool where we integrate with the next applications and having the PWA of the admin dashboard we could reply, enqueue in the task manager and more the issues assigned there:
    1. - [ ] Github
    2. - [ ] Gitlab
27. - [-] Coming soon...