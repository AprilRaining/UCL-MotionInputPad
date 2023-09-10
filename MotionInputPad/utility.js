import {
    Dimensions
  } from 'react-native';

const deviceWidth = Dimensions.get('window').width;
const deviceHeight = Dimensions.get('window').height;


export function treat_map(flist){
    if (flist.length < 5){
        return false;
    }
    
    var scope = {leftlevel:100000, upperlevel: 100000, rightlevel: 0, lowerlevel: 0}

    for (var i in flist){
        var tem = flist[i]
        scope.leftlevel = scope.leftlevel > tem["x"] ? tem["x"] : scope.leftlevel;
        scope.upperlevel = scope.upperlevel > tem["y"] ? tem["y"] : scope.upperlevel;
        scope.rightlevel = scope.rightlevel < tem["x"] ? tem["x"] : scope.rightlevel;
        scope.lowerlevel = scope.lowerlevel < tem["y"] ? tem["y"] : scope.lowerlevel;
        console.log(i, flist[i]);
    }

    var width = scope.rightlevel - scope.leftlevel;
    var height = scope.lowerlevel - scope.upperlevel;

    console.log(scope);
    console.log(width, height);
    
    if (width/deviceWidth < 0.2 && height/deviceHeight < 0.2){
        return false;
    }

    var max_w_h = Math.max(height, width);
    var output = [[], []];



    for (var i in flist){
        output[0].push((flist[i]["x"] - (scope.leftlevel + width/2 - max_w_h/2))/(max_w_h+20));
        output[1].push((flist[i]["y"] - (scope.upperlevel + height/2 - max_w_h/2))/(max_w_h+20));
    }

    console.log(output);
    return output;
} 



