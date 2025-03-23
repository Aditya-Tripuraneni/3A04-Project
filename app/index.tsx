import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { useRouter } from 'expo-router';

export default function HomeScreen() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <Text style={styles.title}>SongSnap</Text>
      <Text style={styles.subtitle}>Find your favourite songs instantly</Text>

      {/* Handles navigation to different input screens*/} 
      <View style={styles.buttonContainer}>
        <TouchableOpacity style={[styles.button, styles.lyricsButton]} onPress={() => router.push('/screens/LyricInput')}>
          <Text style={styles.buttonText}>Search by Lyrics</Text>
        </TouchableOpacity>

        <TouchableOpacity style={[styles.button, styles.audioButton]} onPress={() => router.push('/screens/AudioInput')}>
          <Text style={styles.buttonText}>Search by Audio</Text>
        </TouchableOpacity>

        <TouchableOpacity style={[styles.button, styles.descriptionButton]} onPress={() => router.push('/screens/DescriptionInput')}>
          <Text style={styles.buttonText}>Search by Description</Text>
        </TouchableOpacity>
      </View>
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
  buttonText: {
    color: '#FFF',
    fontSize: 20,
    fontWeight: '600',
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
});
