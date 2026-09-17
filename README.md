<div align="center">

<h1>Coderr Backend</h1>

<p>
  REST API for a service marketplace platform,<br>
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
  <strong>Coderr</strong> is a service marketplace where customers can
  discover business profiles and offers, place orders and leave reviews.
</p>

<p>
  Business users can publish service offers and manage incoming orders,
  while customers can purchase offer packages and review businesses.
</p>

<p>
  This repository contains my backend implementation created as part of the
  <strong>Developer Akademie Backend curriculum</strong>.
</p>

<blockquote>
  The frontend was provided by Developer Akademie.
  My main responsibility in this project is the Django REST API and backend logic.
</blockquote>

<h2>Features</h2>

<ul>
  <li>Customer and business user registration</li>
  <li>Django REST Framework token authentication</li>
  <li>User profile management</li>
  <li>Separate customer and business profile listings</li>
  <li>Offer creation with Basic, Standard and Premium packages</li>
  <li>Offer filtering, searching and ordering</li>
  <li>Customer order creation</li>
  <li>Business order status management</li>
  <li>Customer reviews and ratings</li>
  <li>Marketplace statistics</li>
  <li>Django Admin integration</li>
  <li>Demo accounts for frontend guest login</li>
  <li>100% measured test coverage</li>
</ul>

<h2>Tech Stack</h2>

<p>
  <strong>Python</strong> •
  <strong>Django</strong> •
  <strong>Django REST Framework</strong> •
  SQLite •
  Token Authentication •
  django-filter •
  django-cors-headers •
  python-dotenv •
  Pillow •
  Coverage.py
</p>

<h2>API Overview</h2>

<h3>Authentication</h3>

<table>
  <tr>
    <th>Method</th>
    <th>Endpoint</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>POST</td>
    <td><code>/api/registration/</code></td>
    <td>Register a customer or business user</td>
  </tr>
  <tr>
    <td>POST</td>
    <td><code>/api/login/</code></td>
    <td>Authenticate and receive a token</td>
  </tr>
</table>

<h3>Profiles</h3>

<table>
  <tr>
    <th>Method</th>
    <th>Endpoint</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>GET / PATCH</td>
    <td><code>/api/profile/{user_id}/</code></td>
    <td>Retrieve or update a profile</td>
  </tr>
  <tr>
    <td>GET</td>
    <td><code>/api/profiles/business/</code></td>
    <td>List business profiles</td>
  </tr>
  <tr>
    <td>GET</td>
    <td><code>/api/profiles/customer/</code></td>
    <td>List customer profiles</td>
  </tr>
</table>

<h3>Offers</h3>

<table>
  <tr>
    <th>Method</th>
    <th>Endpoint</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>GET / POST</td>
    <td><code>/api/offers/</code></td>
    <td>List offers or create a new offer</td>
  </tr>
  <tr>
    <td>GET / PATCH / DELETE</td>
    <td><code>/api/offers/{offer_id}/</code></td>
    <td>Retrieve or manage an offer</td>
  </tr>
  <tr>
    <td>GET</td>
    <td><code>/api/offerdetails/{detail_id}/</code></td>
    <td>Retrieve an offer package</td>
  </tr>
</table>

<h3>Orders</h3>

<table>
  <tr>
    <th>Method</th>
    <th>Endpoint</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>GET / POST</td>
    <td><code>/api/orders/</code></td>
    <td>List or create orders</td>
  </tr>
  <tr>
    <td>PATCH / DELETE</td>
    <td><code>/api/orders/{order_id}/</code></td>
    <td>Update or delete an order</td>
  </tr>
  <tr>
    <td>GET</td>
    <td><code>/api/order-count/{business_user_id}/</code></td>
    <td>Get active order count</td>
  </tr>
  <tr>
    <td>GET</td>
    <td><code>/api/completed-order-count/{business_user_id}/</code></td>
    <td>Get completed order count</td>
  </tr>
</table>

<h3>Reviews</h3>

<table>
  <tr>
    <th>Method</th>
    <th>Endpoint</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>GET / POST</td>
    <td><code>/api/reviews/</code></td>
    <td>List or create reviews</td>
  </tr>
  <tr>
    <td>PATCH / DELETE</td>
    <td><code>/api/reviews/{review_id}/</code></td>
    <td>Update or delete a review</td>
  </tr>
</table>

<h3>Marketplace Information</h3>

<table>
  <tr>
    <th>Method</th>
    <th>Endpoint</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>GET</td>
    <td><code>/api/base-info/</code></td>
    <td>Retrieve marketplace statistics</td>
  </tr>
</table>

<h2>Authentication</h2>

<p>
  Protected endpoints use Django REST Framework Token Authentication.
</p>

<p>
  After registration or login, the API returns an authentication token.
  Send it with protected requests using:
</p>

<pre><code>Authorization: Token &lt;your-token&gt;</code></pre>

<p>
  Permissions depend on the endpoint and distinguish between customers,
  business users, object owners, authenticated users and administrators.
</p>

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
  Create a <code>.env</code> file in the project root.
</p>

<p>Generate a Django secret key:</p>

<pre><code>python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"</code></pre>

<p>Add the generated value to your local <code>.env</code>:</p>

<pre><code>SECRET_KEY=your-generated-secret-key</code></pre>

<blockquote>
  <strong>Important:</strong>
  Never commit the real <code>.env</code> file or your
  <code>SECRET_KEY</code>.
</blockquote>

<h3>5. Prepare the database</h3>

<pre><code>python manage.py migrate</code></pre>

<p>
  The local SQLite database is excluded from version control.
</p>

<h3>6. Create demo users</h3>

<pre><code>python manage.py seed_demo_data</code></pre>

<p>
  The command can safely be executed multiple times.
</p>

<h3>7. Start the development server</h3>

<pre><code>python manage.py runserver</code></pre>

<p>Backend:</p>

<pre><code>http://127.0.0.1:8000/</code></pre>

<h2>Demo Accounts</h2>

<table>
  <tr>
    <th>Role</th>
    <th>Username</th>
    <th>Password</th>
  </tr>
  <tr>
    <td>Customer</td>
    <td><code>andrey</code></td>
    <td><code>asdasd</code></td>
  </tr>
  <tr>
    <td>Business</td>
    <td><code>kevin</code></td>
    <td><code>asdasd24</code></td>
  </tr>
</table>

<p>
  These accounts are intended for the frontend guest login.
</p>

<h2>Frontend</h2>

<p>
  My frontend fork used for local integration is available here:
</p>

<p>
  <a href="https://github.com/JuliaKeller13/Coderr_frontend">
    github.com/JuliaKeller13/Coderr_frontend
  </a>
</p>

<p>
  The original frontend project was provided by Developer Akademie:
</p>

<p>
  <a href="https://github.com/Developer-Akademie-Backendkurs/project.Coderr">
    github.com/Developer-Akademie-Backendkurs/project.Coderr
  </a>
</p>

<p>
  During local development the frontend communicates with:
</p>

<pre><code>http://127.0.0.1:8000/api/</code></pre>

<h2>Media Files</h2>

<p>
  Uploaded profile pictures and offer images are stored in the local
  <code>media/</code> directory during development.
</p>

<p>
  The directory is excluded from version control.
  With <code>DEBUG=True</code>, Django serves these files through the
  development server.
</p>

<h2>Testing & Coverage</h2>

<p>
  The project uses separate test settings with a faster password hasher.
</p>

<p>Run the complete test suite:</p>

<pre><code>python manage.py test --settings=coderr.settings_test</code></pre>

<p>
  For repeated local test runs, Django can keep the test database:
</p>

<pre><code>python manage.py test --keepdb --settings=coderr.settings_test</code></pre>

<p>Run the complete suite with coverage:</p>

<pre><code>python -m coverage erase
python -m coverage run manage.py test --settings=coderr.settings_test
python -m coverage report -m</code></pre>

<div align="center">

<img
  src="https://img.shields.io/badge/Test%20Coverage-100%25-success"
  alt="100 percent test coverage"
/>

</div>

<h2>Django Admin</h2>

<p>Create an administrator account:</p>

<pre><code>python manage.py createsuperuser</code></pre>

<p>Start the development server and open:</p>

<pre><code>http://127.0.0.1:8000/admin/</code></pre>

<p>
  Profiles, offers, offer details, orders and reviews are available through
  the Django Admin interface.
</p>

<h2>Project Structure</h2>

<pre>
coderr_backend/
├── coderr/
│   ├── settings.py
│   ├── settings_test.py
│   └── urls.py
├── core/
│   ├── api/
│   └── tests/
├── offers/
│   ├── api/
│   └── tests/
├── orders/
│   ├── api/
│   └── tests/
├── reviews/
│   ├── api/
│   └── tests/
├── users/
│   ├── api/
│   ├── management/
│   └── tests/
├── manage.py
├── requirements.txt
└── README.md
</pre>

<p>
  API-related serializers, views, URLs, permissions, filters and pagination
  are kept inside the corresponding application's <code>api/</code> package.
</p>

<h2>Project Context</h2>

<p>
  Coderr was implemented as a learning project within the
  <strong>Developer Akademie Backend curriculum</strong>.
</p>

<p>
  The frontend was supplied as the client application.
  My main task was to design and implement the Django REST API according to
  the provided backend requirements.
</p>

<p>
  The project focuses on Django architecture, REST APIs, relational models,
  serializers, permissions, authentication, validation, filtering,
  automated testing and clean code principles.
</p>

<hr>

<div align="center">

<h3>Julia Keller</h3>

<p>
  <a href="https://github.com/JuliaKeller13">GitHub</a>
  &nbsp;•&nbsp;
  <a href="https://github.com/JuliaKeller13/Coderr_frontend">Frontend</a>
</p>

<p>
  Developed as part of the software development curriculum at
  <strong>Developer Akademie</strong>.
</p>

</div>