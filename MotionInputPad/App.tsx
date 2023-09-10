import * as React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import Gestures from './Gestures';
import InputGestures from './InputGesture';
import {Alert, View, Text, Button, TouchableOpacity, SafeAreaView, StyleSheet} from "react-native";
  
const HomePage = ({navigation}) => {
    return (
      <View style={styles.container}>
        <Button title="Set gestures" onPress={()=>{navigation.navigate("Input")}}/>
        <Button title="Open Apps" onPress={()=>{navigation.navigate("Gestures")}}/>
      </View>
    );
  };



function App(): JSX.Element {

  const Stack = createNativeStackNavigator();
  return (
    <NavigationContainer>
        <Stack.Navigator initialRouteName="Home">
            <Stack.Screen name = "Home" component={HomePage} />
            <Stack.Screen name = "Input" component={InputGestures} />
            <Stack.Screen name = "Gestures" component={Gestures} />
        </Stack.Navigator>
    </NavigationContainer>
  );

}



const styles = StyleSheet.create({
    container: {
      flex: 1,
      alignItems: "center",
      justifyContent: "space-around",
      flexDirection:"row",
    }
  });


export default App;
