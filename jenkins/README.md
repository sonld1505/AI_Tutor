# Jenkins — Phase 1 setup

Jenkins LTS runs on the factory EC2 as a systemd service, bound to **127.0.0.1:8080**
(`/etc/systemd/system/jenkins.service.d/override.conf`). It is not exposed publicly.
The `jenkins` user is in the `docker` group.

## 1. Open the UI through an SSH tunnel

```bash
ssh -i <your-key>.pem -L 8080:127.0.0.1:8080 ubuntu@<ec2-host>
# then browse http://localhost:8080
```

Unlock with the initial password (on EC2):

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Choose **Install suggested plugins** (includes Pipeline, Git, GitHub Branch Source,
Timestamper — all required by `Jenkinsfile`), then create the admin user.

## 2. GitHub credential

Store it in **Manage Jenkins → Credentials**, never in Git:

- a GitHub fine-grained token (repo `AI_Tutor`: Contents read, Commit statuses write,
  Pull requests read), as *Username with password* or *GitHub App*.

## 3. Pipeline job

**New Item → Multibranch Pipeline** (`branch 'develop'` / `branch 'main'` conditions in
`Jenkinsfile` only work in multibranch jobs):

- Branch source: GitHub, repo `sonld1505/AI_Tutor`, the credential above.
- Build configuration: by `Jenkinsfile`.
- Discover branches + pull requests from origin.

## 4. GitHub webhook / status checks

Inbound webhooks need Jenkins reachable from GitHub. While Jenkins is localhost-only,
use periodic branch scanning in the multibranch job instead. Exposing Jenkins
(reverse proxy + TLS + security group restricted to GitHub hook IPs) is a separate,
reviewed DevOps change.

Once builds report status, mark the Jenkins check as **required** in the
`main`/`develop` branch protection rules.

## Expected state today

Every pipeline run currently **fails at Build** — no application project exists yet and
all gates fail closed (NO UNIT TEST PASS = NO DEPLOY). That is the correct result.
