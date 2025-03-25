import React, { useState } from 'react';
import { View, Text, TouchableOpacity, ActivityIndicator, StyleSheet, Modal, Animated } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import * as DocumentPicker from 'expo-document-picker';

export default function AudioInput() {
  const router = useRouter();
  const { remainingMethods } = useLocalSearchParams(); // Get remaining methods
  const parsedMethods: string[] = remainingMethods ? JSON.parse(remainingMethods as string) : [];

   // State to store the inputted audio file
   const [audioFile, setAudioFile] = useState('');

   const routeMap = {
    LyricInput: "/screens/LyricInput",
    AudioInput: "/screens/AudioInput",
    DescriptionInput: "/screens/DescriptionInput",
  } as const;

  const handleSelectAudio = async () => {
    try {

      // Get audio file from user
      const file = await DocumentPicker.getDocumentAsync({
        type: 'audio/*',
      });

      // Ensure a file was selected and processes it
      if (!file.canceled && file.assets.length > 0) {
        setAudioFile(file.assets[0].uri);
      } 
    } catch (error) {
      console.error('Error picking audio file', error);
    }
  };

  const handleNext = () => {
    if (parsedMethods.length > 0) {
      const [nextMethod, ...Methods] = parsedMethods;
      const nextRoute = routeMap[nextMethod as keyof typeof routeMap];

      router.push({
        pathname: nextRoute,
        params: { remainingMethods: JSON.stringify(Methods) },
      });
    }    
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Search by Audio</Text>

      {/* Input button for audio file */}
      <TouchableOpacity style={styles.button} onPress={handleSelectAudio}>
        <Text style={styles.buttonText}>Pick an Audio File</Text>
      </TouchableOpacity>

      {/* Display selected file name */}
      {audioFile && <Text style={styles.fileName}>Selected file: {audioFile.split('/').pop()}</Text>}

      {/* Next Button */}
      <TouchableOpacity style={styles.button} onPress={handleNext}>
        <Text style={styles.buttonText}>Next</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'flex-start',
    alignItems: 'center',
    backgroundColor: '#fff',
    paddingTop: 200,
    paddingHorizontal: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 20,
    color: '#4A90E2',
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
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  fileName: {
    marginTop: 10,
    fontSize: 16,
    color: '#888',
  },
});