import { useState } from 'react'
import './App.css'

interface Description {
  artist: string;
  genre: string;
  year: string;
  albumName: string;
  mood: string;
  genderOfArtist: string;
  language: string;
  region: string;
  featuredArtist: string;
}

interface AnalysisResult {
  song: string;
  artist: string;
  confidence: number;
}

function App() {
  const [selectedAnalyzers, setSelectedAnalyzers] = useState<string[]>([])
  const [lyrics, setLyrics] = useState('')
  const [audioFile, setAudioFile] = useState<File | null>(null)
  const [description, setDescription] = useState<Description>({
    artist: '',
    genre: '',
    year: '',
    albumName: '',
    mood: '',
    genderOfArtist: '',
    language: '',
    region: '',
    featuredArtist: ''
  })
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const selectAnalyzer = (analyzerName: string) => {
    setSelectedAnalyzers(currentAnalyzers => {
      if (currentAnalyzers.includes(analyzerName)) {
        return currentAnalyzers.filter(name => name !== analyzerName)
      } else {
        return [...currentAnalyzers, analyzerName]
      }
    })
  }

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setAudioFile(file)
    }
  }

  const updateDescription = (field: keyof Description, value: string) => {
    setDescription(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const handleSubmit = async () => {
    try {
      setIsLoading(true)
      setError(null)
      setResult(null)

      const requestData: any = {}
      
      if (selectedAnalyzers.includes('lyrics')) {
        requestData.lyrics_request = { lyrics }
      }
      
      if (selectedAnalyzers.includes('audio') && audioFile) {
        const formData = new FormData()
        formData.append('audio_file', audioFile)
      }
      
      if (selectedAnalyzers.includes('description')) {
        requestData.description_request = description
      }

      const response = await fetch('http://localhost:8000/analyze_song', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to analyze song')
      }

      const result = await response.json()
      setResult({
        song: result.song_name,
        artist: result.song_author,
        confidence: result.confidence_score
      })
    } catch (error) {
      setError(error instanceof Error ? error.message : 'An error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="container">
      <h1 className="title">SongSnap</h1>
      <p className="subtitle">Select analyzers and provide input</p>

      {/* Analyzer Selection */}
      <section className="section">
        <h2 className="section-title">Select Analyzers</h2>
        <button 
          className={`analyzer-button ${selectedAnalyzers.includes('lyrics') ? 'selected' : ''}`}
          onClick={() => selectAnalyzer('lyrics')}
        >
          Lyrics Analyzer
        </button>

        <button 
          className={`analyzer-button ${selectedAnalyzers.includes('audio') ? 'selected' : ''}`}
          onClick={() => selectAnalyzer('audio')}
        >
          Audio Analyzer
        </button>

        <button 
          className={`analyzer-button ${selectedAnalyzers.includes('description') ? 'selected' : ''}`}
          onClick={() => selectAnalyzer('description')}
        >
          Description Analyzer
        </button>
      </section>

      {/* Input Fields */}
      <section className="section">
        {selectedAnalyzers.includes('lyrics') && (
          <div className="input-section">
            <h2 className="section-title">Enter Lyrics</h2>
            <textarea
              className="text-area"
              value={lyrics}
              onChange={(e) => setLyrics(e.target.value)}
              placeholder="Paste your lyrics here..."
              rows={6}
            />
          </div>
        )}

        {selectedAnalyzers.includes('audio') && (
          <div className="input-section">
            <h2 className="section-title">Upload Audio</h2>
            <input
              type="file"
              accept="audio/mpeg"
              onChange={handleFileChange}
              className="file-input"
            />
            {audioFile && (
              <p className="file-name">
                Selected: {audioFile.name}
              </p>
            )}
          </div>
        )}

        {selectedAnalyzers.includes('description') && (
          <div className="input-section">
            <h2 className="section-title">Song Description</h2>
            {Object.entries(description).map(([field, value]) => (
              <input
                key={field}
                className="input"
                value={value}
                onChange={(e) => updateDescription(field as keyof Description, e.target.value)}
                placeholder={`Enter ${field.replace(/([A-Z])/g, ' $1').toLowerCase()}`}
              />
            ))}
          </div>
        )}
      </section>

      {/* Results Section */}
      {isLoading && <div className="loading">Analyzing...</div>}
      {error && <div className="error">{error}</div>}
      {result && (
        <div className="result-section">
          <h2 className="section-title">Analysis Result</h2>
          <div className="result-content">
            <p><strong>Song:</strong> {result.song}</p>
            <p><strong>Artist:</strong> {result.artist}</p>
            <p><strong>Confidence:</strong> {(result.confidence * 100).toFixed(2)}%</p>
          </div>
        </div>
      )}

      {/* Submit Button */}
      <button 
        className={`submit-button ${selectedAnalyzers.length === 0 ? 'disabled' : ''}`}
        onClick={handleSubmit}
        disabled={selectedAnalyzers.length === 0 || isLoading}
      >
        {isLoading ? 'Analyzing...' : 'Analyze Song'}
      </button>
    </div>
  )
}

export default App
