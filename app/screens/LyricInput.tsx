import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Keyboard, TouchableWithoutFeedback } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';

export default function LyricInput() {
  const router = useRouter();
  const { remainingMethods } = useLocalSearchParams(); // Get remaining methods
  const parsedMethods: string[] = remainingMethods ? JSON.parse(remainingMethods as string) : [];

  // State to store the entered lyrics
  const [lyrics, setLyrics] = useState('');

  const routeMap = {
    LyricInput: "/screens/LyricInput",
    AudioInput: "/screens/AudioInput",
    DescriptionInput: "/screens/DescriptionInput",
  } as const;

  // Handle navigation to next screen
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
    <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
      <View style={styles.container}>
        <Text style={styles.title}>Search by Lyrics</Text>
        
        {/* Input field for lyrics */}
        <TextInput 
          style={styles.input} 
          placeholder="Enter lyrics..." 
          placeholderTextColor="#888"
          value={lyrics}
          onChangeText={setLyrics}
        />
        
        {/* Next button */}
        <TouchableOpacity style={styles.button} onPress={handleNext}>
          <Text style={styles.buttonText}>Next</Text>
        </TouchableOpacity>
      </View>
    </TouchableWithoutFeedback>
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
  input: {
    height: 50,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 10,
    width: '100%',
    paddingHorizontal: 15,
    marginBottom: 20,
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
});