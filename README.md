<div align="center">

<img
  src="https://raw.githubusercontent.com/JuliaKeller13/Coderr_frontend/main/assets/logo/logo_coderr.svg"
  alt="Coderr Logo"
  width="180"
/>

<h1>Coderr Backend</h1>

<p>
  REST API for a service marketplace,<br>
  built with Django and Django REST Framework.
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-6.1.1-092E20?logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/DRF-3.18.1-A30000" alt="Django REST Framework">
  <img src="https://img.shields.io/badge/Coverage-100%25-success" alt="Coverage">
</p>

<p>
  <a href="https://github.com/JuliaKeller13/Coderr_frontend">
    <strong>Frontend Repository</strong>
  </a>
  &nbsp;•&nbsp;
  <a href="https://github.com/Developer-Akademie-Backendkurs/project.Coderr">
    Developer Akademie Project
  </a>
</p>

</div>

<hr>

<h2>About</h2>

<p>
  <strong>Coderr</strong> is a service marketplace where customers can browse
  offers, place orders and review business users.
</p>

<p>
  This repository contains my backend implementation created as part of the
  <strong>Developer Akademie Backend curriculum</strong>.
</p>

<p>
  Business users can create service offers and manage incoming orders.
  The REST API provides authentication, profiles, offers, orders, reviews
  and marketplace statistics.
</p>

<blockquote>
  The frontend was originally provided by Developer Akademie.
  I forked and adapted it for integration with this backend.
</blockquote>

<h2>API Overview</h2>

<table>
  <tr>
    <th>Method</th>
    <th>Endpoint</th>
    <th>Resource</th>
  </tr>
  <tr>
    <td>POST</td>
    <td><code>/api/registration/</code></td>
    <td>Registration</td>
  </tr>
  <tr>
    <td>POST</td>
    <td><code>/api/login/</code></td>
    <td>Login</td>
  </tr>
  <tr>
    <td>GET / PATCH</td>
    <td><code>/api/profile/{user_id}/</code></td>
    <td>Profile</td>
  </tr>
  <tr>
    <td>GET / POST</td>
    <td><code>/api/offers/</code></td>
    <td>Offers</td>
  </tr>
  <tr>
    <td>GET / PATCH / DELETE</td>
    <td><code>/api/offers/{offer_id}/</code></td>
    <td>Offer detail</td>
  </tr>
  <tr>
    <td>GET / POST</td>
    <td><code>/api/orders/</code></td>
    <td>Orders</td>
  </tr>
  <tr>
    <td>GET / POST</td>
    <td><code>/api/reviews/</code></td>
    <td>Reviews</td>
  </tr>
  <tr>
    <td>GET</td>
    <td><code>/api/base-info/</code></td>
    <td>Marketplace statistics</td>
  </tr>
</table>

<h2>Authentication</h2>

<p>
  Protected endpoints use Django REST Framework Token Authentication.
</p>

<pre><code>Authorization: Token &lt;your-token&gt;</code></pre>

<h2>Setup</h2>

<h3>1. Clone the repository</h3>

<pre><code>git clone https://github.com/JuliaKeller13/coderr_backend.git
cd coderr_backend</code></pre>

<h3>2. Create and activate a virtual environment</h3>

<h4>Windows PowerShell</h4>

<pre><code>python -m venv .venv
.\.venv\Scripts\Activate.ps1</code></pre>

<h4>macOS / Linux</h4>

<pre><code>python3 -m venv .venv
source .venv/bin/activate</code></pre>

<h3>3. Install dependencies</h3>

<pre><code>python -m pip install -r requirements.txt</code></pre>

<h3>4. Configure the environment</h3>

<p>
  Create a local <code>.env</code> file in the project root:
</p>

<pre><code>SECRET_KEY=your-generated-secret-key</code></pre>

<blockquote>
  <strong>Important:</strong>
  Never commit the real <code>.env</code> file or a real
  <code>SECRET_KEY</code>.
</blockquote>

<h3>5. Prepare the database</h3>

<pre><code>python manage.py migrate</code></pre>

<h3>6. Create a superuser</h3>

<p>
  Create an administrator account for access to the Django Admin interface:
</p>

<pre><code>python manage.py createsuperuser</code></pre>

<p>
  Follow the prompts to choose your own username, email address and password.
  Superuser credentials are created locally and are not stored in this repository.
</p>

<h3>7. Start the server</h3>

<pre><code>python manage.py runserver</code></pre>

<p>Backend:</p>

<pre><code>http://127.0.0.1:8000/</code></pre>

<p>Django Admin:</p>

<pre><code>http://127.0.0.1:8000/admin/</code></pre>

<h2>Frontend</h2>

<p>
  My adapted frontend fork is available here:
</p>

<p>
  <a href="https://github.com/JuliaKeller13/Coderr_frontend">
    github.com/JuliaKeller13/Coderr_frontend
  </a>
</p>

<p>
  For local development it connects to:
</p>

<pre><code>http://127.0.0.1:8000/api/</code></pre>

<p>
  The original frontend was provided by Developer Akademie:
</p>

<p>
  <a href="https://github.com/Developer-Akademie-Backendkurs/project.Coderr">
    github.com/Developer-Akademie-Backendkurs/project.Coderr
  </a>
</p>

<h2>Testing</h2>

<p>Run all tests:</p>

<pre><code>python manage.py test --settings=core.settings_test</code></pre>

<p>Run coverage:</p>

<pre><code>python -m coverage erase
python -m coverage run manage.py test --settings=core.settings_test
python -m coverage report -m</code></pre>

<div align="center">

<img
  src="https://img.shields.io/badge/Application%20Coverage-100%25-success"
  alt="100 percent application coverage"
/>

</div>

<h2>Project Structure</h2>

<pre>
coderr_backend/
├── base_info_app/
│   ├── api/
│   └── tests/
├── users_app/
│   ├── api/
│   └── tests/
├── offers_app/
│   ├── api/
│   └── tests/
├── orders_app/
│   ├── api/
│   └── tests/
├── reviews_app/
│   ├── api/
│   └── tests/
├── core/
├── manage.py
└── requirements.txt
</pre>

<h2>Project Context</h2>

<p>
  Coderr was implemented as a learning project within the
  <strong>Developer Akademie Backend curriculum</strong>.
</p>

<p>
  The frontend was provided as the client application.
  My main task was to design and implement the Django REST API according
  to the project's backend requirements.
</p>

<h2>License</h2>

<p>
  Components provided by Developer Akademie, including the original
  Coderr frontend and associated assets, are subject to the
  <strong>Developer Akademie Learning License (Non-commercial)</strong>.
  See <a href="./LICENSE.md">LICENSE.md</a> for details.
</p>

<p>
  This repository is published for non-commercial learning and portfolio use.
</p>

<hr>

<div align="center">

<img
  src="https://raw.githubusercontent.com/JuliaKeller13/Coderr_frontend/main/assets/logo/logo_coderr.svg"
  alt="Coderr Logo"
  width="90"
/>

<h3>Julia Keller</h3>

<p>
  <a href="https://github.com/JuliaKeller13">GitHub</a>
  &nbsp;•&nbsp;
  <a href="https://github.com/JuliaKeller13/Coderr_frontend">Frontend</a>
</p>

<p>
  Developed as part of the Developer Akademie GmbH advanced training program.
</p>

</div>
