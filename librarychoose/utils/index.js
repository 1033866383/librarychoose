export const groupArray = function (array, subGroupLength) {
    let index = 0;
    let newArray = [];
    while(index < array.length) {
        newArray.push(array.slice(index, index += subGroupLength));
    }
    return newArray;
}
export const ColorUI = {
  Blue: '#0081ff',
  Cyan: '#1cbbb4',
  Yellow: '#fbbd08',
  Olive: '#8dc63f',
  Orange: '#f37b1d',
  Purple: '#6739b6',
  Brown: '#a5673f',
  Red: '#e54d42'
}
export const analysisColor = ['#1cbbb4','#8dc63f','#f37b1d','#a5673f']
