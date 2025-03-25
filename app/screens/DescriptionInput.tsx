import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ScrollView } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';

export default function DescriptionInput() {
  const router = useRouter();
  const { remainingMethods } = useLocalSearchParams();
  const parsedMethods: string[] = remainingMethods ? JSON.parse(remainingMethods as string) : [];

  // State to store input values for each description field
  const [description, setDescription] = useState({
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

  // State to track expanded input field
  const [expandedField, setExpandedField] = useState<string | null>(null);

   // Handle expansion and collapsing of a specific input field
  const toggleFieldExpansion = (field: string) => {
    setExpandedField(expandedField === field ? null : field);
  }

  const routeMap = {
    LyricInput: "/screens/LyricInput",
    AudioInput: "/screens/AudioInput",
    DescriptionInput: "/screens/DescriptionInput",
  } as const;

  // Handle text entered into input fields
  const handleDescriptionInput = (field: keyof typeof description, value: string) => {
    setDescription({ ...description, [field]: value });
  }

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

  const formatCollapsibleLabel = (key: string) => {
    return key.replace(/([A-Z])/g, ' $1').replace(/^\w/, c => c.toUpperCase());
  }

  const formatPlaceholderLabel = (key: string) => {
    return key.replace(/([A-Z])/g, ' $1').toLowerCase();
  }

  return (
    <ScrollView contentContainerStyle={styles.contentContainer} style={styles.container}>
      <Text style={styles.title}>Search by Description</Text>

      {/* Render each description field as input */}
      {Object.keys(description).map((key) => (
        <View key={key} style={styles.inputContainer}>
          <TouchableOpacity onPress={() => toggleFieldExpansion(key)} style={styles.fieldToggle}>
            <Text style={styles.label}>{formatCollapsibleLabel(key)}:</Text>
          </TouchableOpacity>

          {/* Render input field if it is expanded */}
          {expandedField === key && (
            <TextInput
              style={styles.input}
              placeholder={`Enter ${formatPlaceholderLabel(key)}...`}
              placeholderTextColor="#888"
              value={description[key as keyof typeof description]}
              onChangeText={(text) => handleDescriptionInput(key as keyof typeof description, text)}
            />
          )}
        </View>
      ))}

      <TouchableOpacity style={styles.button} onPress={handleNext}>
        <Text style={styles.buttonText}>Next</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    paddingHorizontal: 20,
  },
  contentContainer: {
    flexGrow: 1,
    paddingVertical: 20, 
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 20,
    color: '#4A90E2',
    textAlign: 'center',
  },
  inputContainer: {
    width: '100%',
    marginBottom: 15,
  },
  label: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 5,
    color: '#4A90E2',
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
    padding: 10,
    fontSize: 16,
    width: '100%',
  },
  button: {
    backgroundColor: '#4A90E2',
    paddingVertical: 15,
    paddingHorizontal: 40,
    borderRadius: 10,
    marginVertical: 10,
    width: '80%',
    alignSelf: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  fieldToggle: {
    backgroundColor: '#f0f0f0',
    padding: 10,
    borderRadius: 5,
    marginBottom: 5,
    width: '100%',
  },
});
