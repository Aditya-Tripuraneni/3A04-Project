import { Stack } from "expo-router";

export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen
        name="index"
        options={{ headerShown: false}}
      />
      <Stack.Screen
        name="screens/LyricInput"
        options={{ headerTitle: "Lyrics Search", headerBackTitle: "Back" }}
      />
      <Stack.Screen
        name="screens/AudioInput"
        options={{ headerTitle: "Audio Search", headerBackTitle: "Back" }}
      />
      <Stack.Screen
        name="screens/DescriptionInput"
        options={{ headerTitle: "Description Search", headerBackTitle: "Back" }}
      />
    </Stack>
  );
}
