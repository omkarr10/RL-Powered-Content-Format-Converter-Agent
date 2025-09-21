# RL-Powered Content Format Converter Agent

A sophisticated content format conversion system powered by Reinforcement Learning (RL) algorithms. This project provides intelligent content transformation capabilities with adaptive learning to optimize conversion quality and performance.

## 🚀 Features

- **Multi-Format Support**: Convert between various content formats including:
  - Video to Audio extraction
  - Audio to Text transcription (using Whisper STT)
  - Text to Speech synthesis (using gTTS/Tortoise-TTS)
  - Intelligent format optimization

- **RL-Powered Optimization**: 
  - Adaptive learning from conversion quality metrics
  - Dynamic parameter adjustment based on content characteristics
  - Performance optimization through reinforcement learning

- **RESTful API**: Fast and efficient FastAPI backend with comprehensive endpoints
- **React Frontend**: Modern, responsive user interface for easy file uploads and conversions
- **Cloud-Ready**: Configured for deployment on Render with optimized build processes

## 🏗️ Architecture

```
├── backend/                 # FastAPI Backend
│   ├── agent/              # RL Agent and conversion logic
│   │   ├── converter.py    # Main conversion orchestrator
│   │   ├── rl_agent.py     # Reinforcement Learning agent
│   │   ├── utils.py        # Utility functions
│   │   └── models/         # AI Models
│   │       ├── whisper_stt.py  # Speech-to-Text
│   │       └── tts.py      # Text-to-Speech
│   ├── routes/             # API endpoints
│   ├── logs/               # Conversion logs and metrics
│   └── temp/               # Temporary file storage
├── frontend/               # React Frontend
│   ├── src/                # React source code
│   └── public/             # Static assets
└── env/                    # Python virtual environment
```

## 🔧 Prerequisites

- Python 3.9+
- Node.js 16+
- FFmpeg (for video/audio processing)
- Git

## 📦 Installation

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/omkarr10/RL-Powered-Content-Format-Converter-Agent.git
   cd RL-Powered-Content-Format-Converter-Agent
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv env
   # Windows
   env\Scripts\activate
   # Linux/Mac
   source env/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   cd backend
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Create necessary directories**
   ```bash
   mkdir logs temp
   ```

### Frontend Setup

1. **Install Node.js dependencies**
   ```bash
   cd frontend
   npm install
   ```

## 🚀 Running the Application

### Development Mode

1. **Start the Backend**
   ```bash
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Start the Frontend**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the Application**
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Frontend: http://localhost:1234 (or port shown in terminal)

### Production Deployment

#### Docker Deployment

1. **Build the Docker image:**
   ```bash
   docker build -t rl-converter .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 rl-converter
   ```

3. **Access the service:**
   - API: http://localhost:8000
   - Health check: http://localhost:8000/health

#### Render.com Deployment

The project is configured for deployment on Render.com with the included `render.yaml` configuration.

1. **Connect your GitHub repository to Render**
2. **Create a new Web Service**
3. **Use the Dockerfile for deployment**
4. **Set environment variables if needed**

#### Team Integration

For integration with Ashmit's backend:

1. **Schema Alignment**: Outputs are already aligned with the expected schema
2. **API Endpoint**: Use `POST /convert-content` for conversions
3. **Metadata**: All responses include comprehensive metadata
4. **Feedback Loop**: Use `POST /feedback` for user feedback collection

**Integration Example:**
```python
import requests

def convert_for_team(input_type, output_type, content):
    """Convert content for team integration."""
    response = requests.post(
        "https://your-deployed-service.com/convert-content",
        data={
            "input_type": input_type,
            "output_type": output_type,
            "input_text": content
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        return {
            "transcript": result.get("transcript"),
            "generated_audio": result.get("generated_audio"),
            "metadata": result.get("metadata"),
            "feedback": result.get("feedback")
        }
    return None
```

## 📚 API Endpoints

### POST `/convert-content`

Convert content between different formats with RL-powered optimization.

**Parameters:**
- `input_file` (file, optional): File to convert
- `input_text` (string, optional): Text content to convert
- `input_type` (string, required): Source format (`video`, `audio`, `text`)
- `output_type` (string, required): Target format (`audio`, `video`, `text`)

**Example Requests:**

```bash
# Text to Audio
curl -X POST "http://localhost:8000/convert-content" \
  -F "input_type=text" \
  -F "output_type=audio" \
  -F "input_text=Hello world"

# Audio to Text
curl -X POST "http://localhost:8000/convert-content" \
  -F "input_file=@sample.wav" \
  -F "input_type=audio" \
  -F "output_type=text"

# Video to Text (Complete Pipeline)
curl -X POST "http://localhost:8000/convert-content" \
  -F "input_file=@video.mp4" \
  -F "input_type=video" \
  -F "output_type=text"
```

**Response Schema (Aligned with Team Backend):**
```json
{
  "converted_content": "temp/extracted_audio.wav",
  "metadata": {
    "duration": 12.3,
    "clarity_score": 0.9,
    "language": "en",
    "method_used": "whisper-base",
    "content_type": "video",
    "output_type": "audio",
    "file_size": 1024000,
    "quality_metrics": {
      "clarity": 0.9,
      "confidence": 0.85
    }
  },
  "transcript": "Hello world transcription...",
  "generated_audio": "temp/generated_audio.mp3",
  "generated_video": null,
  "feedback": {
    "clarity_score": 0.9,
    "reward": 9.0,
    "user_rating": null,
    "improvement_suggestions": []
  },
  "rl": {
    "state": {"content_type": "video", "length": 1024000, "quality": 0.5},
    "action": "video2audio",
    "exploration_epsilon": 0.1,
    "learning_rate": 0.1
  }
}
```

### GET `/health`

Health check endpoint for container orchestration.

**Response:**
```json
{
  "status": "healthy",
  "service": "rl-converter"
}
```

### POST `/feedback`

Submit feedback for conversion quality (for RL learning).

**Parameters:**
- `conversion_id` (string): ID of the conversion
- `user_rating` (float): User rating (1-10)
- `feedback_text` (string, optional): Additional feedback

**Example:**
```bash
curl -X POST "http://localhost:8000/feedback" \
  -H "Content-Type: application/json" \
  -d '{"conversion_id": "123", "user_rating": 8.5, "feedback_text": "Good quality"}'
```

## 🤖 RL Agent Features

The Reinforcement Learning agent continuously learns from conversion operations to:

- **Optimize Quality**: Adjust parameters based on output quality metrics
- **Improve Performance**: Learn efficient conversion pathways
- **Adapt to Content**: Customize processing based on content characteristics
- **Resource Management**: Optimize computational resource usage

## 🛠️ Technology Stack

### Backend
- **FastAPI**: High-performance web framework
- **OpenAI Whisper**: State-of-the-art speech recognition
- **gTTS/Tortoise-TTS**: Text-to-speech synthesis
- **FFmpeg-Python**: Video/audio processing
- **NumPy**: Numerical computations
- **Transformers**: AI model integration

### Frontend
- **React 18**: Modern JavaScript framework
- **Parcel**: Zero-configuration build tool
- **Responsive Design**: Mobile-friendly interface

### AI/ML
- **Reinforcement Learning**: Custom RL agent for optimization
- **Speech Processing**: Whisper STT integration
- **Natural Language Processing**: Tokenizers and transformers

## 📁 File Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── agent/
│   ├── converter.py       # Main conversion logic
│   ├── rl_agent.py        # RL optimization engine
│   ├── utils.py           # Helper functions
│   └── models/            # AI model implementations
├── routes/
│   └── convert.py         # API route handlers
└── logs/                  # Application logs

frontend/
├── package.json           # Node.js dependencies
├── src/
│   ├── App.jsx           # Main React component
│   ├── index.js          # Application entry point
│   └── config.js         # Frontend configuration
└── public/
    └── index.html        # HTML template
```

## 🔍 Features in Detail

### Content Conversion Pipeline
1. **Input Processing**: File upload and validation
2. **Format Detection**: Automatic content type recognition
3. **RL Decision Making**: Optimal conversion strategy selection
4. **Processing**: AI-powered format transformation
5. **Quality Assessment**: Output quality evaluation
6. **Learning Update**: RL agent parameter adjustment

### Supported Conversions
- **Video → Audio**: Extract audio tracks from video files
- **Audio → Text**: Transcribe speech using Whisper STT
- **Text → Speech**: Generate natural speech from text
- **Quality Enhancement**: AI-powered optimization

## 🚨 Troubleshooting

### Common Issues

1. **Rust Compiler Error**
   ```bash
   pip install --only-binary=all -r requirements.txt
   ```

2. **Missing Logs Directory**
   ```bash
   mkdir backend/logs
   ```

3. **Port Already in Use**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8001
   ```

4. **FFmpeg Not Found**
   - Install FFmpeg and ensure it's in your system PATH

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI Whisper for speech recognition capabilities
- FastAPI for the excellent web framework
- Render.com for deployment infrastructure
- The open-source community for various libraries and tools

## 📞 Support

For support, email [your-email] or create an issue in the GitHub repository.

---

**Made with ❤️ by [omkarr10](https://github.com/omkarr10)**
