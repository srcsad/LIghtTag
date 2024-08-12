
#include <Adafruit_GFX.h>
#include <Adafruit_NeoMatrix.h>
#include <Adafruit_NeoPixel.h>
#ifndef PSTR
 #define PSTR // Make Arduino Due happy
#endif

#define PIN 6
#include<SoftwareSerial.h>

SoftwareSerial softSerial1(2,3);
char arr [16]; // 定义一个字符数组
int num [4]; // 定义一个整数数组
Adafruit_NeoMatrix matrix = Adafruit_NeoMatrix(32,8, PIN,
  NEO_MATRIX_TOP     + NEO_MATRIX_LEFT +
  NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG,
  NEO_GRB            + NEO_KHZ800);

const uint16_t colors[] = {
  matrix.Color(255, 0, 0), matrix.Color(0, 255, 0), matrix.Color(0, 0, 255) };
int i=5;
int j=1;
int x    = matrix.width();
int y    = matrix.height();
int pass = 0;
struct MessageValue {
  String message;
  String value;
};
struct MessageValue getMessage(String inputtedStr) {
  struct MessageValue result;

  char charArr[50];
  inputtedStr.toCharArray(charArr, 50);
  char* ptr = strtok(charArr, "||");
  result.message = String(ptr);
  ptr = strtok(NULL, "||");

  if (ptr == NULL) {
    result.value = String("");
    return result;
  }

  result.value = String(ptr);

  return result;
}

// Declare MessageValue struct's instance
struct MessageValue receivedData;

void setup() {
  Serial.begin(9600);
  softSerial1.begin(9600);
  matrix.begin();
  matrix.setTextWrap(false);
  matrix.setTextColor(colors[0]);
}
void loop() {
 String inString="";
  if(Serial.available()>0){

  while(Serial.available()>0){
    inString += char(Serial.read()); // 读取一个字符
    delay(10);
}
strcpy (arr, inString.c_str());
  int num [4];
  char *p = strtok (arr, ","); // 分割第一个子字符串
  int i = 0; // 定义一个索引变量
  while (p != NULL) { // 循环直到没有子字符串
  num [i] = atoi (p); // 将子字符串转换为整数并存储在数组中
  i++; // 增加索引
  p = strtok (NULL, ","); // 分割下一个子字符串
}

matrix.fillScreen(0); // 清空矩阵
for(; j < 3; j++){
  for(; i < 50; i+=2){
          matrix.setBrightness(i);
          matrix.drawRect(num[0],num[1],num[2],num[3],matrix.Color(197, 127, 51));
          matrix.show();
          delay(10);
   
      }
  for(; i > 10; i-=2){
          matrix.setBrightness(i);
          matrix.drawRect(num[0],num[1],num[2],num[3],matrix.Color(197, 127, 51));
          matrix.show();
          delay(10);
      }
  }
matrix.fillScreen(0);
matrix.show();
softSerial1.println("1");
}
if(softSerial1.available() > 0){
  while (softSerial1.available() > 0) {
    // From ProtoPie Connect 1.9.0, We can use '\0' as delimiter in Arduino Serial
    String receivedString = softSerial1.readStringUntil('\0'); 
  
    receivedData = getMessage(receivedString);}

    if (receivedData.message.equals("yes")){
      softSerial1.println(receivedData.value.toInt());
      delay(100);
      }
    if (receivedData.message.equals("no")){
      softSerial1.println(receivedData.value.toInt());
      delay(100);
      }  
      if(receivedData.message.equals("yes")){
        Serial.println("1");
        delay(100);
        }
      if(receivedData.message.equals("no")){
        Serial.println("0");
        delay(100);
        }
  }
 // 更新矩阵显示
}
