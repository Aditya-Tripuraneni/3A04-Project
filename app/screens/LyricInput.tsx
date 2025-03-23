import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ActivityIndicator, Modal, Animated, Keyboard } from 'react-native';

export default function LyricInput() {
  const [lyrics, setLyrics] = useState('');
  const [loading, setLoading] = useState(false);
  const [songResult, setSongResult] = useState(''); 
  const [modalVisible, setModalVisible] = useState(false); 
  const fadeAnim = useState(new Animated.Value(0))[0]; 

  const handleSearch = async () => {
    Keyboard.dismiss();
    setLoading(true); // Show loading animation

    // Simulating the identification process (replace with actual backend call)
    setTimeout(() => {
      setLoading(false); 
      setSongResult('Hello by Adele');  // Placeholder result

      // Show the modal with animation
      setModalVisible(true);
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 500,
        useNativeDriver: true,
      }).start();

      // Clear lyrics input after search
      setLyrics('');
    }, 3000);  // Simulate 3 seconds loading time
  };

  // Close modal and reset fade animation
  const closeModal = () => {
    setModalVisible(false);
    fadeAnim.setValue(0);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Search by Lyrics</Text>

      {/* Input field for lyrics */}
      <TextInput
        style={styles.input}
        placeholder="Enter lyrics..."
        placeholderTextColor="#888"
        value={lyrics}
        onChangeText={(text) => setLyrics(text)}
      />

      {/* Search button */}
      <TouchableOpacity style={styles.button} onPress={handleSearch}>
        <Text style={styles.buttonText}>Search</Text>
      </TouchableOpacity>

      {/* Display loading spinner when searching */}
      {loading ? (
        <ActivityIndicator size="large" color="#3498DB" />
      ) : (
        <Text style={styles.result}>{songResult || 'No song identified yet.'}</Text>
      )}

      {/* Modal to display song result */}
      <Modal
        visible={modalVisible}
        animationType="fade"
        transparent={true}
        onRequestClose={closeModal}>
        <View style={styles.modalOverlay}>
          <Animated.View style={[styles.modalContainer, { opacity: fadeAnim }]}>
            <Text style={styles.modalTitle}>Song Identified!</Text>
            <Text style={styles.modalContent}>{songResult}</Text>

            <TouchableOpacity style={styles.closeButton} onPress={closeModal}>
              <Text style={styles.closeButtonText}>Close</Text>
            </TouchableOpacity>
          </Animated.View>
        </View>
      </Modal>
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
  result: {
    fontSize: 18,
    fontWeight: 'bold',
    marginTop: 20,
    color: '#4A90E2',
  },
  modalOverlay: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
  },
  modalContainer: {
    width: '80%',
    padding: 30,
    backgroundColor: '#fff',
    borderRadius: 10,
    alignItems: 'center',
  },
  modalTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    color: '#4A90E2',
  },
  modalContent: {
    fontSize: 20,
    fontWeight: 'normal',
    marginBottom: 30,
    color: '#3498DB',
  },
  closeButton: {
    backgroundColor: '#4A90E2',
    paddingVertical: 12,
    paddingHorizontal: 25,
    borderRadius: 10,
  },
  closeButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});