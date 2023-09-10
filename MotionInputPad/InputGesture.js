import React, { Component } from 'react';
import {   
    Shape,
    Surface,
    Path,
} from "@react-native-community/art";


import {
  StyleSheet,
  View,
  PanResponder,
  Dimensions
} from 'react-native';

import axios from 'axios';
import {treat_map} from "./utility"

const deviceWidth = Dimensions.get('window').width;
const deviceHeight = Dimensions.get('window').height;
 
const baseURL = 'http://127.0.0.1:8081/input';

const headers = {
    "Content-Type": "application/json",
  };

export default class InputGestures extends Component {
  constructor(props){
    super(props);
    
    this.lastClick = null;
    this.click = null;
    this.mousePosition = null;
    this.lastMousePostion = null;
    this.arrUsedPoint = [];
    this.allPoints = [];
    this.nowR = 5;
    this.showPoints = null;
    this.interval = 300;
    this.status = true;
    this.count = 0;
    // this.state = {points: 0};
    
    

    this._panResponder = PanResponder.create({
        onStartShouldSetPanResponder: this.onStartShouldSetPanResponder.bind(this),
        onMoveShouldSetPanResponder: this.onMoveShouldSetPanResponder.bind(this),
        onPanResponderGrant: this.onPanResponderGrant.bind(this),
        onPanResponderMove: this.onPanResponderMove.bind(this),
        onPanResponderRelease: this.onPanResponderRelease.bind(this),
        onPanResponderTerminate: this.onPanResponderTerminate.bind(this),
      });
  }


  setUpdate(){
    this.setState({});
  }

  onStartShouldSetPanResponder(e, g){
    return true;
  }

  onMoveShouldSetPanResponder(e, g){
    return true;
  }


  onPanResponderGrant(e, g){
    this.lastClick = this.click
    this.click = new Date()
    
    if (this.lastClick && (this.click - this.lastClick < this.interval)){
        // this.status = !this.status;
        this.Out()
    }

    if (!this.status){
        return
    }

    if (g.numberActiveTouches == 1){
        this.mousePosition = {
          x: e.nativeEvent.locationX,
          y: e.nativeEvent.locationY
        };
        this.ResetDrawPoint();
        this.AddUsePoint(this.mousePosition);
      }

  }

  onPanResponderMove(e, g){
    // console.log(this.arrUsedPoint.length)
    if (this.arrUsedPoint.length > 200){
        this.Out()
    }
    if (g.numberActiveTouches == 1 && this.status){
      this.mousePosition = {
        x: e.nativeEvent.locationX,
        y: e.nativeEvent.locationY
      };
      this.AddUsePoint(this.mousePosition);
    }

  }

  onPanResponderRelease(e, g){
    // console.log(this.arrUsedPoint)
    // console.log(this.showPoints)
    
    if (this.status){
        this.endPanResponder(e, g);
    }

    if (this.arrUsedPoint.length > 5){
        // console.log(this.arrUsedPoint)
        
        // var output = JSON.stringify(treat_map(this.arrUsedPoint))
        var output = treat_map(this.arrUsedPoint)
        
        if (output){
            console.log("send list")
            sendres = {"list": output, "count": this.count}
            axios.post(baseURL, sendres).then((res) => {
                console.log(res)
            }).catch((error) => {
                console.log(error)
            });
        }
    }

    this.count += 1;
    if (this.count > 8){
        setTimeout(() => {
            this.Out();
        }, 500);
        
    }
  }

  onPanResponderTerminate(e, g){
    // this.endPanResponder(e, g);
  }

  endPanResponder(e, g){
    setTimeout(() => {
        this.showPoints = null;
        this.setUpdate();
    }, 800);
    
  }

  ResetDrawPoint(){
    this.arrUsedPoint = [];
    this.nowR = 5;
    this.showPoints = null;
  }

  AddUsePoint(pos){
    this.lastMousePostion = this.mousePosition;
    this.AddSinglePoint(pos); 
    this.setUpdate();
  }

  AddSinglePoint(pos){
    this.arrUsedPoint.push(pos);
    d = new Path();
    for(var i=0;i<this.arrUsedPoint.length;i++){
      var p = this.arrUsedPoint[i];
      if (i==0){
        d.moveTo(p.x, p.y);
      }else{
        d.lineTo(p.x, p.y);
      }
    }
    this.showPoints = d;
  }

  Out(){
    // console.log("double click")
    CancelURL = baseURL + "/cancel";
    sendres = {"clean": true}
    axios.post(CancelURL, sendres).then((res) => {
        console.log(res)
    }).catch((error) => {
        console.log(error)
    });
    
    this.props.navigation.navigate("Home");
  }


  render() {
    return (
      <View style={styles.container} {...this._panResponder.panHandlers}>
        <Surface ref={'lineView'} width={deviceWidth} height={deviceHeight} >
            <Shape d={this.showPoints} stroke={'rgb(0,0,255)'} strokeWidth={this.nowR} />
        </Surface>
      </View>
    );
  }
}


const styles = StyleSheet.create({
    container: {
      flex: 1,
      alignItems: "center",
      justifyContent: "center"
    }
  });
