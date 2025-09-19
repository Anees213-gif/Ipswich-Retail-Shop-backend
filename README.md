# Ipswich Retail - Modern E-commerce Platform

A production-ready e-commerce platform built with Django REST Framework and React, featuring comprehensive admin management, modern UI/UX, and robust API architecture.

## 🚀 Features

### Storefront
- **Product Catalog**: Advanced filtering, search, and pagination
- **Product Details**: Image galleries, specifications, and related products
- **Shopping Cart**: Persistent cart with guest and user support
- **Checkout Process**: Complete order flow with validation
- **Responsive Design**: Mobile-first with dark/light mode support

### Admin Dashboard
- **Product Management**: Full CRUD with image upload and bulk operations
- **Order Management**: Status tracking, filtering, and bulk updates
- **Customer Management**: Customer profiles and order history
- **Analytics Dashboard**: KPIs, charts, and business metrics
- **User Authentication**: Secure admin login and session management

### API & Backend
- **RESTful API**: Comprehensive API with OpenAPI documentation
- **Authentication**: Session-based and token authentication
- **Data Validation**: Robust input validation and error handling
- **Pagination**: Efficient pagination with metadata
- **Health Monitoring**: Health checks and metrics endpoints

## 🛠 Tech Stack

### Backend
- **Django 4.2** - Web framework
- **Django REST Framework** - API framework
- **PostgreSQL** - Primary database
- **Redis** - Caching and session storage
- **Celery** - Background task processing
- **Gunicorn** - WSGI server
- **Docker** - Containerization

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling framework
- **shadcn/ui** - Component library
- **Zustand** - State management
- **React Hook Form** - Form handling
- **Zod** - Schema validation

### DevOps & Tools
- **Docker Compose** - Development environment
- **GitHub Actions** - CI/CD pipeline
- **pytest** - Testing framework
- **ESLint/Prettier** - Code quality
- **Black/isort** - Python formatting
- **Prometheus** - Metrics collection

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Shop
   ```

2. **Start with Docker Compose**
   ```bash
   make dev
   # or manually:
   docker-compose up --build -d
   docker-compose exec backend python manage.py migrate
   docker-compose exec backend python manage.py seed_demo
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api/
   - Admin Panel: http://localhost:8000/admin/
   - API Documentation: http://localhost:8000/api/docs/
   - Health Check: http://localhost:8000/api/health/
   - Metrics: http://localhost:8000/api/metrics/

### Local Development

1. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py seed_demo
   python manage.py runserver
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 📁 Project Structure

```
Shop/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Route components
│   │   ├── store/          # Zustand state management
│   │   ├── lib/            # Utilities and API client
│   │   └── types/          # TypeScript definitions
│   ├── Dockerfile
│   └── package.json
├── backend/                 # Django backend
│   ├── apps/
│   │   ├── core/           # Core functionality
│   │   ├── products/       # Product management
│   │   ├── orders/         # Order processing
│   │   └── customers/      # Customer management
│   ├── ipswich_retail/     # Django project settings
│   ├── Dockerfile
│   └── requirements.txt
└── docker-compose.yml      # Full stack orchestration
```

## 🛒 Features

### Frontend Features
- **Modern UI**: Professional design with dark/light mode
- **Product Catalog**: Advanced filtering, search, and pagination
- **Shopping Cart**: Persistent cart with localStorage
- **Checkout Process**: Complete form validation
- **Admin Panel**: Full CRUD operations for products, orders, customers
- **Responsive Design**: Mobile-first approach
- **Accessibility**: WCAG 2.1 AA compliant

### Backend Features
- **RESTful API**: Django REST Framework
- **Admin Interface**: Django admin with custom configurations
- **Database Models**: Products, Orders, Customers, Categories
- **Authentication**: Session and token-based auth
- **File Uploads**: Image handling for products
- **Caching**: Redis integration
- **Background Tasks**: Celery for async processing

## 🧪 Testing

### Backend Testing
```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Run specific test
docker-compose exec backend python manage.py test apps.core.tests.HealthCheckAPITest
```

### Frontend Testing
```bash
# Run tests
cd frontend && npm run test

# Run linting
cd frontend && npm run lint
```

### Test Coverage
- **Backend**: Minimum 70% coverage required
- **Frontend**: Component and integration tests
- **API**: End-to-end API testing
- **CI/CD**: Automated testing on every commit

## 🔧 Development Commands

```bash
# Development
make dev          # Start development environment
make dev-up       # Start Docker services
make dev-down     # Stop Docker services

# Database
make migrate      # Run migrations
make seed         # Load demo data

# Testing
make test         # Run tests
make test-coverage # Run tests with coverage
make lint         # Run linting

# Code Quality
make format       # Format code
make clean        # Clean up

# Monitoring
make health       # Check service health
make logs         # View logs
```

## 📚 API Documentation

### Public Endpoints
- `GET /api/` - API root with endpoint information
- `GET /api/health/` - Health check endpoint
- `GET /api/metrics/` - Prometheus metrics
- `GET /api/categories/` - List all categories
- `GET /api/products/` - List products with filtering and pagination
- `GET /api/products/{slug}/` - Get product details
- `POST /api/orders/` - Create new order

### Admin Endpoints
- `GET /api/admin/products/` - List all products (admin)
- `POST /api/admin/products/` - Create new product
- `PUT /api/admin/products/{id}/` - Update product
- `DELETE /api/admin/products/{id}/` - Delete product
- `GET /api/admin/orders/` - List all orders
- `PUT /api/admin/orders/{id}/` - Update order status

### API Features
- **Pagination**: Standardized pagination with metadata
- **Filtering**: Advanced filtering by category, brand, price, rating
- **Search**: Full-text search across products
- **Sorting**: Multiple sorting options
- **Rate Limiting**: API rate limiting for protection
- **CORS**: Configurable CORS settings

## 🐳 Docker Services

- **frontend**: React development server
- **backend**: Django application
- **db**: PostgreSQL database
- **redis**: Redis cache and message broker
- **celery**: Background task worker
- **celery-beat**: Task scheduler

## 🔐 Environment Variables

Copy `backend/env.example` to `backend/.env` and configure:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_HOST=db
DB_NAME=ipswich_retail
DB_USER=postgres
DB_PASSWORD=postgres
```

## 🚀 Deployment

### Free-Tier Platforms

#### Render
```bash
# Deploy backend
# 1. Connect GitHub repository
# 2. Set environment variables
# 3. Deploy automatically on push

# Environment variables:
DJANGO_SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgresql://...
CORS_ALLOWED_ORIGINS=https://your-frontend-url.onrender.com
```

#### Railway
```bash
# Deploy with Railway CLI
railway login
railway init
railway up
```

#### PythonAnywhere
```bash
# Manual deployment
# 1. Upload code
# 2. Configure WSGI file
# 3. Set environment variables
# 4. Run migrations
```

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up SSL/HTTPS
- [ ] Configure production database
- [ ] Set up monitoring and logging
- [ ] Configure email settings
- [ ] Set up backup strategy

## 📊 Monitoring & Observability

### Health Checks
- **Endpoint**: `/api/health/`
- **Checks**: Database connection, system resources
- **Response**: JSON with status and system info

### Metrics
- **Endpoint**: `/api/metrics/`
- **Format**: Prometheus metrics
- **Metrics**: Application metrics, system metrics

### Logging
- **Format**: Structured JSON logging
- **Levels**: DEBUG, INFO, WARNING, ERROR
- **Correlation**: Request ID tracking

## 📝 License

This project is licensed under the MIT License.

## 🔒 Security

### Authentication
- Session-based authentication for admin
- Token authentication for API
- CSRF protection enabled
- Secure password validation

### API Security
- Rate limiting on write operations
- CORS configuration
- Input validation and sanitization
- SQL injection protection

### Production Security
- HTTPS enforcement
- Secure headers
- Environment variable management
- Regular security updates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`make test`)
5. Run linting (`make lint`)
6. Commit your changes (`git commit -m 'Add some amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript for all frontend code
- Write tests for new features
- Update documentation
- Follow conventional commit messages

## 🆘 Support

- **Documentation**: Check the `docs/` directory
- **Issues**: Open an issue on GitHub
- **API Docs**: http://localhost:8000/api/docs/
- **Health Check**: http://localhost:8000/api/health/

## 🎯 Roadmap

- [ ] Payment integration (Stripe, PayPal)
- [ ] Advanced analytics dashboard
- [ ] Mobile app support
- [ ] Multi-language support
- [ ] Advanced inventory management
- [ ] Customer reviews and ratings
- [ ] Wishlist functionality
- [ ] Advanced search with Elasticsearch
- [ ] Real-time notifications
- [ ] Advanced reporting
