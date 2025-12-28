# 🌀 Pixflow

A modern social media platform built with FastAPI and Streamlit, featuring image and video sharing, user authentication, and a beautiful dark-themed interface.

![Pixflow Demo](https://via.placeholder.com/800x400/1e293b/ffffff?text=Pixflow+Social+Media+Platform)

## ✨ Features

- **🔐 User Authentication**: Secure JWT-based authentication with FastAPI-Users
- **📸 Media Upload**: Support for images and videos with automatic optimization via ImageKit
- **🗑️ Post Management**: Delete your own posts
- **🎨 Beautiful UI**: Dark-themed, responsive interface with smooth animations
- **👤 User Profiles**: User avatars and email-based identification
- **📝 Caption Support**: Add captions to your posts with overlay display


## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM with async support
- **SQLite** - Lightweight database
- **ImageKit** - Image and video optimization service
- **JWT Authentication** - Secure token-based auth

### Frontend
- **Streamlit** - Python-based web application framework
- **Custom CSS** - Beautiful dark theme with gradients and animations

### Database Models
- **User**: Email, password, timestamps
- **Post**: User association, media URL, caption, file type, creation date

## 🚀 Quick Start

### Prerequisites
- Python 3.14+
- pip or uv package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd pixflow
   ```

2. **Install dependencies**
   ```bash
   pip install -e .
   # or
   uv sync
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   JWT_SECRET=your-super-secret-jwt-key-here
   IMAGEKIT_PUBLIC_KEY=your-imagekit-public-key
   IMAGEKIT_PRIVATE_KEY=your-imagekit-private-key
   IMAGEKIT_URL_ENDPOINT=https://ik.imagekit.io/your_imagekit_id
   ```

4. **Initialize the database**
   ```bash
   python main.py
   ```
   The database will be created automatically on first run.

### Running the Application

1. **Start the backend server**
   ```bash
   python main.py
   ```
   The FastAPI server will be available at `http://localhost:8000`

2. **Launch the frontend**
   ```bash
   streamlit run frontend.py
   ```
   The Streamlit app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
pixflow/
├── app/
│   ├── __init__.py
│   ├── app.py          # FastAPI application and routes
│   ├── db.py           # Database models and configuration
│   ├── schema.py       # Pydantic schemas
│   ├── users.py        # User authentication setup
│   └── images.py       # ImageKit configuration
├── frontend.py         # Streamlit frontend application
├── main.py            # Application entry point
├── pyproject.toml     # Project configuration and dependencies
├── .gitignore        # Git ignore rules
└── README.md         # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `JWT_SECRET` | Secret key for JWT token signing | Yes |
| `IMAGEKIT_PUBLIC_KEY` | ImageKit public key for uploads | Yes |
| `IMAGEKIT_PRIVATE_KEY` | ImageKit private key for uploads | Yes |
| `IMAGEKIT_URL_ENDPOINT` | ImageKit URL endpoint | Yes |

### Supported File Types

- **Images**: PNG, JPG, JPEG
- **Videos**: MP4, AVI, MOV, MKV, WEBM

## 📡 API Endpoints

### Authentication (`/auth`)
- `POST /auth/jwt/login` - User login
- `POST /auth/register` - User registration
- `POST /auth/reset-password` - Password reset
- `GET /auth/verify` - Email verification

### User Management (`/users`)
- `GET /users/me` - Get current user info
- `PUT /users/me` - Update user profile

### Posts
- `POST /upload` - Upload new post 
- `GET /feed` - Get all posts feed
- `DELETE /posts/{post_id}` - Delete own post

## 🎨 UI Features

### Dark Theme
- Modern gradient backgrounds
- Glass-morphism effects
- Smooth hover animations
- Responsive card layouts

### Interactive Elements
- File upload with drag & drop
- Live post deletion with highlighting
- Caption overlay toggle

## 🧪 Testing

The application includes basic functionality testing:

```bash
# Run the application and test manually:
1. Register a new account
2. Upload an image/video with caption
3. View the post in the feed
4. Test deletion functionality
```

## 🔒 Security Features

- **JWT Token Authentication**: Secure user sessions
- **Input Validation**: Pydantic schema validation
- **File Type Restrictions**: Controlled upload types
- **User Authorization**: Post ownership validation

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

