# 📖 Glossary

Plain-English definitions of every term in the bootcamp. No jargon explaining jargon. When a word feels fuzzy, come here.

[↑ Back to README](README.md)  ·  [📚 Resources](RESOURCES.md)

> 💡 Each entry tells you *what it is* and *why you care*. Terms are grouped by world so related ideas sit together.

---

## 🖥️ Setup & general
- **Terminal / Shell** — A text window where you type commands instead of clicking. The shell (e.g. *Bash*) is the program that reads your commands.
- **WSL2 (Windows Subsystem for Linux)** — A way to run a real Linux system *inside* Windows. Lets you use Linux tools without leaving your PC.
- **Ubuntu** — A popular, beginner-friendly flavor (distribution) of Linux. The one we install in WSL2.
- **CLI (Command-Line Interface)** — Any tool you drive by typing commands. The opposite of a GUI (clicking).
- **Package manager** — A tool that installs/updates software for you (e.g. `apt` on Ubuntu, `npm` for Node).

## 🌐 Internet & networking
- **HTTP** — The language browsers and servers use to talk. A request goes out, a response comes back.
- **HTTPS** — HTTP with encryption (TLS), so nobody can read or tamper with the traffic. The padlock in your browser.
- **Request / Response** — You *ask* a server for something (request); it *answers* (response).
- **Status code** — A 3-digit number in a response. `200` = OK, `301` = moved, `404` = not found, `500` = server error.
- **DNS (Domain Name System)** — The internet's phone book. Turns a name like `example.com` into an IP address.
- **IP address** — A number that identifies a machine on a network, like a street address (e.g. `93.184.216.34`).
- **TCP** — The reliable delivery system underneath HTTP; makes sure data arrives in order and intact.
- **Port** — A numbered "door" on a machine. Web traffic uses `80` (HTTP) and `443` (HTTPS).
- **Client / Server** — The client asks (your browser, `curl`); the server answers (the API).
- **API** — A defined way for programs to talk to each other over the network. Your TaskFlow backend is one.
- **REST** — A common style for building APIs around resources (like "tasks") and HTTP verbs (GET/POST/PUT/DELETE).
- **JSON** — A simple text format for data, like `{"title": "Buy milk"}`. The lingua franca of APIs.
- **curl** — A command-line tool to make HTTP requests. Your microscope for APIs.

## 🐧 Linux
- **Filesystem** — How files are organized in folders (directories), starting from the root `/`.
- **Path** — The address of a file, e.g. `/home/you/projects/taskflow`. *Absolute* starts at `/`; *relative* starts where you are.
- **Permissions** — Rules for who can read/write/execute a file (`chmod`, `chown`). Critical on servers.
- **Process** — A running program. You can list (`ps`), monitor (`top`), and stop (`kill`) them.
- **Shell script** — A file of commands run in order. Automates repetitive work (e.g. backups).
- **sudo** — "Do this as the superuser (admin)." Needed for system-level changes. Use carefully.
- **Environment variable** — A named value available to programs (e.g. `PATH`, `PORT`). Config without code changes.

## 🌿 Git & GitHub
- **Git** — A tool that records snapshots (commits) of your code over time, so you can undo, branch, and collaborate.
- **Repository (repo)** — A project tracked by Git, including all its history.
- **Commit** — A saved snapshot with a message describing the change.
- **Branch** — A parallel line of work. Lets you build a feature without touching the main code.
- **Merge** — Combining one branch's changes into another.
- **Merge conflict** — When two changes touch the same lines and Git needs you to choose.
- **Remote** — A copy of the repo hosted elsewhere (e.g. on GitHub).
- **GitHub** — A website that hosts Git repos and adds collaboration (issues, pull requests).
- **Pull Request (PR)** — A proposal to merge your branch, with a place for review.

## ⚙️ Backend
- **Backend** — The server-side part of an app: logic, data, and APIs. (Frontend is what users see.)
- **Node.js** — A runtime that lets you run JavaScript outside the browser, e.g. on a server.
- **Express** — A small framework for building web servers and APIs in Node.
- **Route / Endpoint** — A URL + method your API responds to, e.g. `GET /tasks`.
- **CRUD** — Create, Read, Update, Delete — the four basic operations on data.
- **Database** — Organized, persistent storage for data (we use SQLite then PostgreSQL).
- **Middleware** — Code that runs between the request and your handler (e.g. logging, auth).

## 🐳 Docker
- **Container** — A lightweight, isolated box that runs your app with everything it needs. Same everywhere.
- **Image** — The blueprint a container is created from. Built from a `Dockerfile`.
- **Dockerfile** — A recipe describing how to build your image, step by step.
- **Volume** — Storage that lives outside a container, so data survives restarts.
- **Docker Compose** — A tool to run multiple containers together (e.g. app + database) from one file.
- **Registry** — A place to store and share images (e.g. Docker Hub, GitHub Container Registry).

## ☁️ AWS & cloud
- **Cloud** — Renting computers and services over the internet instead of owning hardware.
- **AWS** — Amazon Web Services, the largest cloud provider.
- **Region / Availability Zone** — Where your resources physically live (e.g. `us-east-1`).
- **EC2** — A virtual server you rent by the hour (or free, on the free tier).
- **Free tier** — AWS resources that cost nothing within set limits. We stay strictly inside it.
- **Security group** — A virtual firewall controlling traffic to/from your server.
- **SSH** — A secure way to log into a remote server's terminal.
- **IAM** — AWS's permission system: who can do what.
- **S3** — AWS's file/object storage service.
- **Billing alarm** — An alert that warns you if spending crosses a threshold (set it to $1!).

## 🔁 CI/CD
- **CI (Continuous Integration)** — Automatically building and testing your code on every change.
- **CD (Continuous Delivery/Deployment)** — Automatically shipping that code to a server.
- **Pipeline** — The automated sequence of steps (build → test → deploy).
- **GitHub Actions** — GitHub's built-in CI/CD that runs workflows from your repo.
- **Workflow** — A YAML file defining your pipeline's steps.
- **Secret** — A sensitive value (password, key) stored securely for the pipeline to use.

## 🏗️ Terraform & IaC
- **Infrastructure as Code (IaC)** — Defining servers, networks, etc. in text files instead of clicking.
- **Terraform** — A popular IaC tool that works across many clouds.
- **Provider** — A plugin that lets Terraform talk to a platform (e.g. the AWS provider).
- **Resource** — A single piece of infrastructure (e.g. an EC2 instance) declared in code.
- **State** — Terraform's record of what it has created, so it knows what to change.
- **plan / apply / destroy** — Preview changes / make them / tear them all down.

## ☸️ Kubernetes
- **Kubernetes (K8s)** — A system that runs and manages containers across many machines.
- **Cluster** — The set of machines Kubernetes manages.
- **Pod** — The smallest unit K8s runs: one (or a few) containers together.
- **Deployment** — A spec saying "keep N copies of this app running."
- **Service** — A stable network address for a set of pods.
- **Ingress** — Routes outside traffic to services (often with a domain + HTTPS).
- **Self-healing** — K8s restarts/replaces pods that die, automatically.
- **Autoscaling** — Adding/removing pods based on load.
- **ConfigMap / Secret** — Ways to give pods configuration and sensitive values.

## 🚀 Production
- **TLS / SSL certificate** — Proves your site's identity and enables HTTPS. Free via Let's Encrypt.
- **Health check** — A request the system uses to ask "are you alive/ready?"
- **Monitoring** — Watching metrics (CPU, errors, uptime) to know if things are healthy.
- **Logging** — Recording what your app did, for debugging and auditing.
- **Runbook** — A document telling you (or a teammate) how to operate and fix the system.

---

[↑ Back to README](README.md)  ·  [📚 Resources →](RESOURCES.md)  ·  [🚀 Start World 0 →](phases/phase-00-environment-setup/)
