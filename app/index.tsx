import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { useRouter } from 'expo-router';

export default function HomeScreen() {
  const router = useRouter();
  
  // State to track selected search methods
  const [selectedMethods, setSelectedMethods] = useState<string[]>([]);

  // Handle method selection
  const toggleMethod = (method: string) => {
    setSelectedMethods((prevMethods) => {
      if (prevMethods.includes(method)) {
        return prevMethods.filter((item) => item !== method); // Deselect method by removing from array if already selected
      }
      return [...prevMethods, method]; // Select method by adding to array if not already selected
    });
  };

  // Handle navigation to first selected method's input screen
  const handleNext = () => {
    if (selectedMethods.length === 0) {
      alert("Please select at least one search method.");
      return;
    }
  
    const [firstMethod, ...remainingMethods] = selectedMethods;
  
    // Map search methods to their respective screens
    const routeMap = {
      LyricInput: "/screens/LyricInput",
      AudioInput: "/screens/AudioInput",
      DescriptionInput: "/screens/DescriptionInput",
    } as const;
  
    const nextRoute = routeMap[firstMethod as keyof typeof routeMap];
  
    // Navigate to first selected method's screen, passing remaining methods as params
    router.push({
      pathname: nextRoute,
      params: { remainingMethods: JSON.stringify(remainingMethods) },
    });
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>SongSnap</Text>
      <Text style={styles.subtitle}>Find your favourite songs instantly</Text>

      {/* Selection buttons for search methods */}
      <View style={styles.buttonContainer}>
        <TouchableOpacity
          style={[styles.button, selectedMethods.includes('LyricInput') ? styles.selected : styles.lyricsButton]}
          onPress={() => toggleMethod('LyricInput')}
        >
          <Text style={styles.buttonText}>Search by Lyrics</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.button, selectedMethods.includes('AudioInput') ? styles.selected : styles.audioButton]}
          onPress={() => toggleMethod('AudioInput')}
        >
          <Text style={styles.buttonText}>Search by Audio</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.button, selectedMethods.includes('DescriptionInput') ? styles.selected : styles.descriptionButton]}
          onPress={() => toggleMethod('DescriptionInput')}
        >
          <Text style={styles.buttonText}>Search by Description</Text>
        </TouchableOpacity>
      </View>

      {/* Next button to next screen */}
      <TouchableOpacity style={styles.nextButton} onPress={handleNext}>
        <Text style={styles.buttonText}>Next</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F0F2F5',
    paddingHorizontal: 20,
  },
  title: {
    fontSize: 42,
    fontWeight: 'bold',
    color: '#2C3E50',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 18,
    color: '#7F8C8D',
    marginBottom: 30,
    textAlign: 'center',
    maxWidth: '80%',
  },
  buttonContainer: {
    width: '100%',
    alignItems: 'center',
  },
  button: {
    paddingVertical: 16,
    paddingHorizontal: 40,
    borderRadius: 30,
    marginVertical: 10,
    width: '80%',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 3,
  },
  lyricsButton: {
    backgroundColor: '#E74C3C',
  },
  audioButton: {
    backgroundColor: '#3498DB',
  },
  descriptionButton: {
    backgroundColor: '#2ECC71',
  },
  selected: {
    backgroundColor: '#95a5a6',
  },
  nextButton: {
    paddingVertical: 16,
    paddingHorizontal: 40,
    backgroundColor: '#8E44AD',
    borderRadius: 30,
    marginTop: 30,
    width: '80%',
    alignItems: 'center',
  },
  buttonText: {
    color: '#FFF',
    fontSize: 20,
    fontWeight: '600',
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
});
