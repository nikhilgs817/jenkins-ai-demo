# Jenkins AI Failure-Analysis Demo

Push this folder to your new GitHub repo, then point a Jenkins Pipeline job at it.

## Push to GitHub
```bash
cd ~/demo-app
git init && git add . && git commit -m "initial demo app"
git branch -M main
git remote add origin https://github.com/<YOUR_USER>/<YOUR_REPO>.git
git push -u origin main      # use a GitHub Personal Access Token as the password
```

## Break it for the demo (compile error)
In src/main/java/com/demo/HelloServlet.java change `println` to `printline`,
commit, push, and re-run the Jenkins job. The build fails at Stage 2 and the
local AI explains the cause + fix in the Jenkins console.
