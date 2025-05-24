const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Set view engine (if using templates)
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Routes
app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Catherine Vee </title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Arial', sans-serif; 
                line-height: 1.6; 
                color: #333;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                padding: 2rem;
            }
            header {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 2rem;
                margin-bottom: 2rem;
                text-align: center;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            }
            h1 { 
                color: #2c3e50; 
                margin-bottom: 0.5rem;
                font-size: 2.5rem;
            }
            .subtitle {
                color: #7f8c8d;
                font-size: 1.2rem;
                margin-bottom: 2rem;
            }
            nav {
                margin: 2rem 0;
            }
            nav a {
                display: inline-block;
                margin: 0 1rem;
                padding: 0.8rem 1.5rem;
                background: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 25px;
                transition: all 0.3s ease;
                font-weight: 500;
            }
            nav a:hover {
                background: #2980b9;
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(52, 152, 219, 0.4);
            }
            .content {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 2rem;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            }
            .intro {
                font-size: 1.1rem;
                color: #555;
                margin-bottom: 2rem;
            }
            .skills {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
                margin-top: 2rem;
            }
            .skill-card {
                background: #f8f9fa;
                padding: 1rem;
                border-radius: 10px;
                text-align: center;
                border-left: 4px solid #3498db;
            }
            @media (max-width: 768px) {
                .container { padding: 1rem; }
                h1 { font-size: 2rem; }
                nav a { 
                    display: block; 
                    margin: 0.5rem 0; 
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>Catherine Vee</h1>
                <p class="subtitle">Network Engineer</p>
                <nav>
                    <a href="/">Home</a>
                    <a href="/about">About</a>
                    <a href="/projects">Projects</a>
                    <a href="/contact">Contact</a>
                </nav>
            </header>
            
            <main class="content">
                <div class="intro">
                    <h2>Skills - Catherine Vee</h2>
                    <p> These are my skills!
                    </p>
                </div>
                
                <div class="skills">
                    <div class="skill-card">
                        <h3>Cloud</h3>
                        <p>AWS, Azure</p>
                    </div>
                    <div class="skill-card">
                        <h3>Network </h3>
                        <p>OSPF, IS-IS, BGP, IPv6</p>
                    </div>
                    <div class="skill-card">
                        <h3>Programming</h3>
                        <p>Bash, Python, Terraform, Kubernetes</p>
                    </div>
                    <div class="skill-card">
                        <h3>Tools</h3>
                        <p>AzureDevOps, GitHub Actions, infracost</p>
                    </div>
                </div>
            </main>
        </div>
    </body>
    </html>
  `);
});

app.get('/about', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>About - Catherine Vee</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Arial', sans-serif; 
                line-height: 1.6; 
                color: #333;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container { 
                max-width: 800px; 
                margin: 0 auto; 
                padding: 2rem;
            }
            .card {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 2rem;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                margin-bottom: 2rem;
            }
            h1 { color: #2c3e50; margin-bottom: 1rem; }
            h2 { color: #34495e; margin: 1.5rem 0 1rem 0; }
            p { margin-bottom: 1rem; color: #555; }
            .back-link {
                display: inline-block;
                margin-top: 2rem;
                padding: 0.8rem 1.5rem;
                background: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 25px;
                transition: all 0.3s ease;
            }
            .back-link:hover {
                background: #2980b9;
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <h1>About Me</h1>
                <p>I'm human!
                </p>
                
                <a href="/" class="back-link">← Back to Home</a>
            </div>
        </div>
    </body>
    </html>
  `);
});

app.get('/projects', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Projects - Your Name</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Arial', sans-serif; 
                line-height: 1.6; 
                color: #333;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container { 
                max-width: 1000px; 
                margin: 0 auto; 
                padding: 2rem;
            }
            .card {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 2rem;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                margin-bottom: 2rem;
            }
            h1 { color: #2c3e50; margin-bottom: 2rem; text-align: center; }
            .projects-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 2rem;
                margin-bottom: 2rem;
            }
            .project {
                background: #f8f9fa;
                padding: 1.5rem;
                border-radius: 10px;
                border-left: 4px solid #3498db;
            }
            .project h3 {
                color: #2c3e50;
                margin-bottom: 0.5rem;
            }
            .project p {
                color: #666;
                margin-bottom: 1rem;
            }
            .tech-stack {
                display: flex;
                flex-wrap: wrap;
                gap: 0.5rem;
                margin-top: 1rem;
            }
            .tech-tag {
                background: #3498db;
                color: white;
                padding: 0.2rem 0.8rem;
                border-radius: 15px;
                font-size: 0.8rem;
            }
            .back-link {
                display: inline-block;
                padding: 0.8rem 1.5rem;
                background: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 25px;
                transition: all 0.3s ease;
            }
            .back-link:hover {
                background: #2980b9;
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <h1>Projects</h1>
                <div class="projects-grid">
                    <div class="project">
                        <h3>Terraform</h3>
                        <p>Cloud Resource Management</p>
                        <div class="tech-stack">
                            <span class="tech-tag">Multi-subscription directories</span>
                            <span class="tech-tag">Node.js client sites</span>
                            <span class="tech-tag">Multi-region</span>
                        </div>
                    </div>
                    
                    <div class="project">
                        <h3>Python</h3>
                        <p>Cloud and Network Automation</p>
                        <div class="tech-stack">
                            <span class="tech-tag">Netmiko</span>
                            <span class="tech-tag">Nornir</span>
                            <span class="tech-tag">Ansible</span>
                            <span class="tech-tag">Powershell SDK</span>
                        </div>
                    </div>
                    
                    <div class="project">
                        <h3>Kubernetes</h3>
                        <p>A respo.</p>
                        <div class="tech-stack">
                            <span class="tech-tag">eksctl</span>
                            <span class="tech-tag">Docker</span>
                            <span class="tech-tag">AKS</span>
                            <span class="tech-tag">K3s</span>
                        </div>
                    </div>
                    
                    <div class="project">
                        <h3>Internetworking</h3>
                        <p>Connecting Devices</p>
                        <div class="tech-stack">
                            <span class="tech-tag">IPv6 + IPv4</span>
                            <span class="tech-tag">BGP</span>
                            <span class="tech-tag">MPLS</span>
                            <span class="tech-tag">IS-IS</span>
                        </div>
                    </div>
                </div>
                
                <a href="/" class="back-link">← Back to Home</a>
            </div>
        </div>
    </body>
    </html>
  `);
});

app.get('/contact', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Contact - Catherine Vee</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Arial', sans-serif; 
                line-height: 1.6; 
                color: #333;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container { 
                max-width: 600px; 
                margin: 0 auto; 
                padding: 2rem;
            }
            .card {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 2rem;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            }
            h1 { color: #2c3e50; margin-bottom: 2rem; text-align: center; }
            .contact-info {
                text-align: center;
                margin-bottom: 2rem;
            }
            .contact-info p {
                margin: 1rem 0;
                color: #555;
            }
            .contact-links {
                display: flex;
                justify-content: center;
                gap: 1rem;
                flex-wrap: wrap;
                margin: 2rem 0;
            }
            .contact-link {
                display: inline-block;
                padding: 0.8rem 1.5rem;
                background: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 25px;
                transition: all 0.3s ease;
            }
            .contact-link:hover {
                background: #2980b9;
                transform: translateY(-2px);
            }
            .back-link {
                display: inline-block;
                margin-top: 2rem;
                padding: 0.8rem 1.5rem;
                background: #95a5a6;
                color: white;
                text-decoration: none;
                border-radius: 25px;
                transition: all 0.3s ease;
            }
            .back-link:hover {
                background: #7f8c8d;
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <h1>Get In Touch</h1>
                <div class="contact-info">
                    <p> I might respond!</p>
                    <p><strong>Email:</strong> catherine.vee@outlook.com</p>
                    <p><strong>Location:</strong> United States </p>
                </div>
                
                <div class="contact-links">
                    <a href="mailto:catherine.vee@outlook.com" class="contact-link">Send Email</a>
                    <a href="https://linkedin.com/in/catherinevee" class="contact-link" target="_blank">LinkedIn</a>
                    <a href="https://github.com/catherinevee" class="contact-link" target="_blank">GitHub</a>
                </div>
                
                <div style="text-align: center; margin-top: 2rem; color: #666;">
                    <p>Let's build something amazing together :)</p>
                </div>
                
                <div style="text-align: center;">
                    <a href="/" class="back-link">← Back to Home</a>
                </div>
            </div>
        </div>
    </body>
    </html>
  `);
});

// Handle form submissions
app.post('/contact', (req, res) => {
  const { name, email, message } = req.body;
  console.log('Contact form submission:', { name, email, message });
  res.redirect('/contact?success=true');
});

// 404 handler
app.use((req, res) => {
  res.status(404).send(`
    <h1>404 - Page Not Found</h1>
    <p>The page you're looking for doesn't exist.</p>
    <a href="/">Go back home</a>
  `);
});

// Error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something went wrong!');
});

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});

module.exports = app;