import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  StyleSheet,
  ActivityIndicator,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import * as DocumentPicker from 'expo-document-picker';

// Interface for the description fields
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

// Interface for the analysis result
interface AnalysisResult {
  song: string;
  artist: string;
  confidence: number;
}

export default function TabOneScreen() {
  // State to manage selected analyzers (lyrics, audio, description)
  const [selectedAnalyzers, setSelectedAnalyzers] = useState<string[]>([]);
  const [lyrics, setLyrics] = useState(''); // State for lyrics input
  const [audioFile, setAudioFile] = useState<string | null>(null); // State for base64-encoded audio file
  const [audioFileName, setAudioFileName] = useState<string | null>(null); // State for audio file name
  const [description, setDescription] = useState<Description>({
    artist: '',
    genre: '',
    year: '',
    albumName: '',
    mood: '',
    genderOfArtist: '',
    language: '',
    region: '',
    featuredArtist: '',
  });
  const [result, setResult] = useState<AnalysisResult | null>(null); // State for analysis result
  const [error, setError] = useState<string | null>(null); // State for error messages
  const [isLoading, setIsLoading] = useState(false); // State for loading indicator

  // Function to determine the correct API URL
  const getApiUrl = () => {
    // Replace with your backend URL
    return 'https://song-snap-3a04-4c786329b520.herokuapp.com';
  };

  // Function to toggle analyzers (lyrics, audio, description)
  const selectAnalyzer = (analyzerName: string) => {
    setSelectedAnalyzers(currentAnalyzers => {
      if (currentAnalyzers.includes(analyzerName)) {
        // Remove analyzer if already selected
        return currentAnalyzers.filter(name => name !== analyzerName);
      } else {
        // Add analyzer to the list
        return [...currentAnalyzers, analyzerName];
      }
    });
  };

  // Function to update description fields dynamically
  const updateDescription = (field: keyof Description, value: string) => {
    setDescription(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  // Function to pick an audio file and convert it to base64
  const pickAudioFile = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: 'audio/*', // Restrict to audio files
      });

      if (result.canceled) {
        return; // Exit if no file is selected
      }

      const fileUri = result.assets[0].uri;
      const fileName = result.assets[0].name; // Get the file name
      setAudioFileName(fileName); // Update state with the file name

      // Fetch the file and convert it to base64
      const response = await fetch(fileUri);
      const blob = await response.blob();
      const reader = new FileReader();

      reader.onloadend = () => {
        const base64data = reader.result?.toString().split(',')[1]; // Extract base64 string
        setAudioFile(base64data || ''); // Update state with base64-encoded audio
      };

      reader.readAsDataURL(blob); // Encode the file as base64

    } catch (err) {
      console.error('Audio file selection error:', err);
      setError('Failed to select audio file.');
    }
  };

  // Function to handle form submission and send data to the backend
  const handleSubmit = async () => {
    try {
      setIsLoading(true); // Show loading indicator
      setError(null); // Clear previous errors
      setResult(null); // Clear previous results

      const requestData: any = {}; // Object to hold request payload

      // Add lyrics data if selected
      if (selectedAnalyzers.includes('lyrics')) {
        requestData.lyrics_request = {
          lyrics: lyrics,
        };
      }

      // Add description data if selected
      if (selectedAnalyzers.includes('description')) {
        requestData.description_request = {
          artist: description.artist,
          genre: description.genre,
          year: description.year,
          albumName: description.albumName,
          mood: description.mood,
          genderOfArtist: description.genderOfArtist,
          language: description.language,
          region: description.region,
          featuredArtist: description.featuredArtist,
        };
      }

      // Add audio data if selected
      if (selectedAnalyzers.includes('audio') && audioFile) {
        requestData.audio_request = {
          audio_file: audioFile, // Send base64-encoded audio
        };
      }

      const API_URL = getApiUrl();
      console.log('Starting request...');
      console.log('URL:', `${API_URL}/analyze_song`);
      console.log('Request data:', JSON.stringify(requestData, null, 2));

      // Make the POST request to the backend
      const response = await fetch(`${API_URL}/analyze_song`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify(requestData),
      });

      console.log('Response received. Status:', response.status);
      const responseText = await response.text();
      console.log('Raw response:', responseText);

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}: ${responseText}`);
      }

      // Parse and display the result
      const result = JSON.parse(responseText);
      setResult({
        song: result.song_name,
        artist: result.song_author,
        confidence: result.confidence_score,
      });
    } catch (error) {
      console.error('Detailed error:', error);
      if (error instanceof Error) {
        if (error.message.includes('Cannot connect to server')) {
          setError('Cannot connect to the server. Please check if:\n1. The backend is running\n2. Your phone and computer are on the same WiFi network\n3. The IP address is correct');
        } else {
          setError(`Error: ${error.message}`);
        }
      } else {
        setError('An unexpected error occurred');
      }
    } finally {
      setIsLoading(false); // Hide loading indicator
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <Text style={styles.title}>SongSnap</Text>
        <Text style={styles.subtitle}>Select analyzers and provide input</Text>

        {/* Analyzer Selection */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Select Analyzers</Text>
          <TouchableOpacity
            style={[
              styles.analyzerButton,
              selectedAnalyzers.includes('lyrics') && styles.selectedButton,
            ]}
            onPress={() => selectAnalyzer('lyrics')}
          >
            <Text style={styles.buttonText}>Lyrics Analyzer</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[
              styles.analyzerButton,
              selectedAnalyzers.includes('audio') && styles.selectedButton,
            ]}
            onPress={() => selectAnalyzer('audio')}
          >
            <Text style={styles.buttonText}>Audio Analyzer</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[
              styles.analyzerButton,
              selectedAnalyzers.includes('description') && styles.selectedButton,
            ]}
            onPress={() => selectAnalyzer('description')}
          >
            <Text style={styles.buttonText}>Description Analyzer</Text>
          </TouchableOpacity>
        </View>

        {/* Input Fields */}
        <View style={styles.section}>
          {selectedAnalyzers.includes('lyrics') && (
            <View style={styles.inputSection}>
              <Text style={styles.sectionTitle}>Enter Lyrics</Text>
              <TextInput
                style={styles.textArea}
                multiline
                numberOfLines={6}
                value={lyrics}
                onChangeText={setLyrics}
                placeholder="Paste your lyrics here..."
                placeholderTextColor="#888"
              />
            </View>
          )}

          {selectedAnalyzers.includes('audio') && (
            <View style={styles.inputSection}>
              <Text style={styles.sectionTitle}>Input Audio File</Text>
              <TouchableOpacity style={styles.button} onPress={pickAudioFile}>
                <Text style={styles.buttonText}>Pick an Audio File</Text>
              </TouchableOpacity>

              {audioFileName && <Text style={styles.fileName}>Selected file: {audioFileName}</Text>}
            </View>
          )}

          {selectedAnalyzers.includes('description') && (
            <View style={styles.inputSection}>
              <Text style={styles.sectionTitle}>Song Description</Text>
              {Object.entries(description).map(([field, value]) => (
                <TextInput
                  key={field}
                  style={styles.input}
                  value={value}
                  onChangeText={(text) => updateDescription(field as keyof Description, text)}
                  placeholder={`Enter ${field.replace(/([A-Z])/g, ' $1').toLowerCase()}`}
                  placeholderTextColor="#888"
                />
              ))}
            </View>
          )}
        </View>

        {/* Results Section */}
        {isLoading && (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#3498DB" />
            <Text style={styles.loadingText}>Analyzing...</Text>
          </View>
        )}
        {error && (
          <View style={styles.errorContainer}>
            <Text style={styles.errorText}>{error}</Text>
          </View>
        )}
        {result && (
          <View style={styles.resultSection}>
            <Text style={styles.sectionTitle}>Analysis Result</Text>
            <View style={styles.resultContent}>
              <Text style={styles.resultText}>
                <Text style={styles.resultLabel}>Song:</Text> {result.song}
              </Text>
              <Text style={styles.resultText}>
                <Text style={styles.resultLabel}>Artist:</Text> {result.artist}
              </Text>
              <Text style={styles.resultText}>
                <Text style={styles.resultLabel}>Confidence:</Text>{' '}
                {(result.confidence * 100).toFixed(2)}%
              </Text>
            </View>
          </View>
        )}

        {/* Submit Button */}
        <TouchableOpacity
          style={[
            styles.submitButton,
            (selectedAnalyzers.length === 0 || isLoading) && styles.disabledButton,
          ]}
          onPress={handleSubmit}
          disabled={selectedAnalyzers.length === 0 || isLoading}
        >
          <Text style={styles.buttonText}>
            {isLoading ? 'Analyzing...' : 'Analyze Song'}
          </Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F0F2F5',
  },
  scrollContent: {
    padding: 20,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#2C3E50',
    textAlign: 'center',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#7F8C8D',
    textAlign: 'center',
    marginBottom: 24,
  },
  section: {
    backgroundColor: 'white',
    borderRadius: 10,
    padding: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#2C3E50',
    marginBottom: 16,
  },
  analyzerButton: {
    backgroundColor: '#3498DB',
    padding: 16,
    borderRadius: 8,
    marginBottom: 8,
  },
  selectedButton: {
    backgroundColor: '#2980B9',
  },
  inputSection: {
    marginBottom: 16,
  },
  input: {
    borderWidth: 1,
    borderColor: '#BDC3C7',
    borderRadius: 6,
    padding: 12,
    marginBottom: 12,
    fontSize: 16,
  },
  textArea: {
    borderWidth: 1,
    borderColor: '#BDC3C7',
    borderRadius: 6,
    padding: 12,
    height: 150,
    textAlignVertical: 'top',
    fontSize: 16,
  },
  submitButton: {
    backgroundColor: '#E74C3C',
    padding: 16,
    borderRadius: 8,
    marginTop: 16,
  },
  disabledButton: {
    backgroundColor: '#BDC3C7',
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
    textAlign: 'center',
  },
  loadingContainer: {
    alignItems: 'center',
    padding: 16,
  },
  loadingText: {
    color: '#3498DB',
    fontSize: 16,
    fontWeight: '600',
    marginTop: 8,
  },
  errorContainer: {
    backgroundColor: '#FDE8E8',
    padding: 16,
    borderRadius: 8,
    marginVertical: 16,
  },
  errorText: {
    color: '#C53030',
    textAlign: 'center',
  },
  resultSection: {
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 10,
    marginVertical: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  resultContent: {
    gap: 8,
  },
  resultText: {
    fontSize: 16,
  },
  resultLabel: {
    fontWeight: '600',
    color: '#2C3E50',
  },
  button: {
    backgroundColor: '#4A90E2',
    paddingVertical: 15,
    paddingHorizontal: 40,
    borderRadius: 10,
    marginVertical: 10,
    width: '80%',
    alignItems: 'center',
  },
  fileName: {
    marginTop: 10,
    fontSize: 16,
    color: '#888',
  },
});
