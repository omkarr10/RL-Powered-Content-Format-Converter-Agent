import React, { useState } from 'react';

const styles = {
  container: {
    maxWidth: 800,
    margin: '40px auto',
    padding: '30px',
    fontFamily: 'sans-serif',
    background: 'rgba(255, 255, 255, 0.15)',
    borderRadius: '16px',
    boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
    backdropFilter: 'blur(10px)',
    WebkitBackdropFilter: 'blur(10px)',
    border: '1px solid rgba(255, 255, 255, 0.18)',
    color: '#ffffff',
  },
  header: {
    textAlign: 'center',
    color: '#e0e0e0',
    marginBottom: '30px',
    textShadow: '0 1px 3px rgba(0,0,0,0.3)',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
  },
  formGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
  },
  select: {
  padding: '10px',
  borderRadius: '8px',
  border: '1px solid rgba(255, 255, 255, 0.3)',
  background: 'rgba(30, 60, 120, 0.8)',  
  color: '#fff',
  backdropFilter: 'blur(5px)',
  WebkitBackdropFilter: 'blur(5px)',
  outline: 'none',
  transition: 'background 0.3s ease',
},

  input: {
    padding: '10px',
    borderRadius: '8px',
    border: '1px solid rgba(255, 255, 255, 0.3)',
    background: 'rgba(255, 255, 255, 0.1)',
    color: '#fff',
    backdropFilter: 'blur(5px)',
    WebkitBackdropFilter: 'blur(5px)',
    outline: 'none',
    transition: 'background 0.3s ease',
  },
  textarea: {
    minHeight: '100px',
  },
  button: {
    padding: '12px 24px',
    backgroundColor: 'rgba(255, 255, 255, 0.25)',
    color: '#fff',
    border: '1px solid rgba(255, 255, 255, 0.4)',
    borderRadius: '12px',
    cursor: 'pointer',
    fontSize: '16px',
    fontWeight: '600',
    backdropFilter: 'blur(5px)',
    WebkitBackdropFilter: 'blur(5px)',
    boxShadow: '0 4px 30px rgba(255, 255, 255, 0.1)',
    transition: 'background-color 0.3s ease, color 0.3s ease',
  },
  buttonHover: {
    backgroundColor: 'rgba(255, 255, 255, 0.4)',
    color: '#222',
  },
  results: {
    marginTop: '30px',
    padding: '20px',
    background: 'rgba(255, 255, 255, 0.15)',
    borderRadius: '12px',
    border: '1px solid rgba(255, 255, 255, 0.3)',
    backdropFilter: 'blur(10px)',
    WebkitBackdropFilter: 'blur(10px)',
    color: '#fff',
  },
  metric: {
    display: 'flex',
    justifyContent: 'space-between',
    padding: '10px 0',
    borderBottom: '1px solid rgba(255, 255, 255, 0.2)',
  }
};

function App() {
  const [inputType, setInputType] = useState('text');
  const [outputType, setOutputType] = useState('audio');
  const [inputText, setInputText] = useState('');
  const [inputFile, setInputFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [btnHover, setBtnHover] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData();
    if (inputFile) formData.append('input_file', inputFile);
    if (inputText) formData.append('input_text', inputText);
    formData.append('input_type', inputType);
    formData.append('output_type', outputType);

    try {
      const res = await fetch('http://localhost:8000/convert-content', {
        method: 'POST',
        body: formData,
      });

      const contentType = res.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        const data = await res.json();
        setResponse(data);
      } else {
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = res.headers.get('content-disposition')?.split('filename=')[1] || 'converted-content';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        setResponse({
          converted_content: 'File downloaded successfully',
          metadata: { duration: 'See downloaded file', language: 'N/A' },
          clarity_score: 1.0,
          reward: 10.0,
          tags_metadata: { tags: ['converted', 'downloaded'], metadata: { length: blob.size } }
        });
      }
    } catch (err) {
      setResponse({ error: 'Request failed: ' + err.message });
    }
    setLoading(false);
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #1f1c2c, #928dab)',
      padding: '20px'
    }}>
      <div style={styles.container}>
        <div style={styles.header}>
          <h1>RL-Powered Content Format Converter</h1>
          <p>Convert between video, audio, and text with AI-powered quality optimization</p>
        </div>

        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.formGroup}>
            <h3>1. Select Conversion Type</h3>
            <div style={{ display: 'flex', gap: '20px' }}>
              <div style={styles.formGroup}>
                <label>Input Format:</label>
                <select
                  style={styles.select}
                  value={inputType}
                  onChange={e => setInputType(e.target.value)}
                >
                  <option value="text">Text</option>
                  <option value="audio">Audio</option>
                  <option value="video">Video</option>
                </select>
              </div>
              <div style={styles.formGroup}>
                <label>Output Format:</label>
                <select
                  style={styles.select}
                  value={outputType}
                  onChange={e => setOutputType(e.target.value)}
                >
                  <option value="audio">Audio</option>
                  <option value="text">Text</option>
                  <option value="video">Video (Summary)</option>
                </select>
              </div>
            </div>
          </div>

          <div style={styles.formGroup}>
            <h3>2. Upload Content</h3>
            {inputType === 'text' ? (
              <div style={styles.formGroup}>
                <label>Enter Text:</label>
                <textarea
                  style={{ ...styles.input, ...styles.textarea }}
                  value={inputText}
                  onChange={e => setInputText(e.target.value)}
                  placeholder="Enter the text you want to convert..."
                />
              </div>
            ) : (
              <div style={styles.formGroup}>
                <label>Upload {inputType.charAt(0).toUpperCase() + inputType.slice(1)} File:</label>
                <input
                  style={styles.input}
                  type="file"
                  accept={inputType + '/*'}
                  onChange={e => setInputFile(e.target.files[0])}
                />
              </div>
            )}
          </div>

          <button
            type="submit"
            style={{
              ...styles.button,
              ...(btnHover ? styles.buttonHover : {}),
              opacity: loading ? 0.7 : 1
            }}
            disabled={loading}
            onMouseEnter={() => setBtnHover(true)}
            onMouseLeave={() => setBtnHover(false)}
          >
            {loading ? 'Converting...' : 'Start Conversion'}
          </button>
        </form>

        {response && (
          <div style={styles.results}>
            <h3>Conversion Results</h3>

            {response.error ? (
              <div style={{ color: '#ff6b6b' }}>{response.error}</div>
            ) : (
              <>
                <div style={styles.metric}>
                  <strong>Converted Content:</strong>
                  <span>{response.converted_content || 'Processing...'}</span>
                </div>

                <div style={styles.metric}>
                  <strong>Clarity Score:</strong>
                  <span>{(response.clarity_score * 100).toFixed(1)}%</span>
                </div>

                <div style={styles.metric}>
                  <strong>Language:</strong>
                  <span>{response.metadata?.language?.toUpperCase()}</span>
                </div>

                <div style={styles.metric}>
                  <strong>Duration:</strong>
                  <span>{response.metadata?.duration}</span>
                </div>

                <div style={styles.metric}>
                  <strong>AI Feedback:</strong>
                  <span>Reward Score: {response.reward?.toFixed(2)}</span>
                </div>

                <div style={styles.metric}>
                  <strong>Tags:</strong>
                  <span>{response.tags_metadata?.tags?.join(', ')}</span>
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;