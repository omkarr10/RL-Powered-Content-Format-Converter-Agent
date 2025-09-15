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

The project is configured for deployment on Render.com with the included `render.yaml` configuration.

## 📚 API Endpoints

### POST `/convert-content`

Convert content between different formats.

**Parameters:**
- `input_file` (file, optional): File to convert
- `input_text` (string, optional): Text content to convert
- `input_type` (string, required): Source format (video, audio, text)
- `output_type` (string, required): Target format (audio, text, speech)

**Example Request:**
```bash
curl -X POST "http://localhost:8000/convert-content" \
  -F "input_file=@sample.mp4" \
  -F "input_type=video" \
  -F "output_type=audio"
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
