//wifi
#include <WiFi.h>
const char* ssid = "ITEK 2nd"; //Morten - iPhone
const char* password = "Four_Sprints_F21v"; //TestTest12
WiFiClient espClient;

//mqtt
#include <PubSubClient.h>
const char* mqtt_server = "10.120.0.211"; //172.20.10.6
const char* inTopic = "move_input";
PubSubClient client(espClient);

//camera
#include "esp_camera.h"
#define CAMERA_MODEL_WROVER_KIT
#include "camera_pins.h"
void startCameraServer();

//motor
int const LED12 = 12;
int const LED13 = 13;
int const LED2 = 2;
int const LED15 = 15;

char ackLeft = ' ';
char ackRigh = ' ';

//I2C
#include <Wire.h>
TwoWire I2CBME = TwoWire(0);
int const I2C_SDA = 33;
int const I2C_SCL = 32;

//dust sensor
byte dust_byte[30];
char buf1[6];
char buf2[6];
char buf10[6];
int dust_index = 0;
int dust_data[3];

//air sensor library
#include <DFRobot_SGP40.h>
#define dust_sensor 14
DFRobot_SGP40 air_sensor;
char buf[8];
boolean toggle;

//tof sensor
#include <VL53L0X.h>
VL53L0X sensor;
//#define HIGH_ACCURACY
//#define LONG_RANGE
#define HIGH_SPEED

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  randomSeed(micros());
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  if((char)payload[0] == 'A') {
    toggle = !toggle;
    return;
  }

  if((char)payload[1] == 'F') {
    digitalWrite(15,LOW);
    digitalWrite(2,HIGH);
    Serial.print("left forward, ");
    ackLeft = 'F';
  } else if((char)payload[1] == 'B') {
    digitalWrite(15,HIGH); //2 high
    digitalWrite(2,LOW); //15 high
    Serial.print("left backward,");
    ackLeft = 'B';
  } else { //payload == Z
    digitalWrite(15, LOW);
    digitalWrite(2, LOW);
    Serial.print("left stop, ");
    ackLeft = 'Z';
  }

  if((char)payload[0] == 'F') {
    digitalWrite(13,HIGH);
    digitalWrite(12,LOW);
    Serial.println("right forward");
    ackRigh = 'F';
  } else if((char)payload[0] == 'B') {
    digitalWrite(13,LOW);
    digitalWrite(12,HIGH);
    Serial.println("right backward");
    ackRigh = 'B';
  } else { //payload == Z
    digitalWrite(13,LOW);
    digitalWrite(12,LOW);
    Serial.println("right stop");
    ackRigh = 'Z';
  }
    char ackMove[2];
    ackMove[0] = ackLeft;
    ackMove[1] = ackRigh;
    client.publish("robocar/debug",ackMove);
}

void reconnect() { 
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe(inTopic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void dust_sensor_loop() {
  if(Serial2.available()) {
    if(Serial2.read() == 0x42 && Serial2.read() == 0x4D) {
      //Serial.println("header done");
      for(int i = 0; i < 14; i++) {
         if(Serial2.available()) {
           //if(i%2 == 0) {
             //Serial.print("HIGH ");
           //} else {
             //Serial.print("LOW ");
           //}
           dust_byte[dust_index] =  Serial2.read();
           //Serial.println(dust_byte[dust_index]);
           dust_index++;
         }
      }
      
/*      for(int i = 14; i < 30; i++) { //flush the no-data bytes[
        if(Serial2.available()) {
          Serial2.read();
        }
      }*/
    }
  for(int i = 0; i < 3; i++) {
    dust_data[i] = (dust_byte[2+i*2]<<4) + dust_byte[2+1+(i*2)];
  }
  sprintf(buf1,"%03i",dust_data[0]);
  sprintf(buf2,"%03i",dust_data[1]);
  sprintf(buf10,"%03i",dust_data[2]);

  client.publish("robocar/dust_output/pm1",buf1);
  client.publish("robocar/dust_output/pm2.5",buf2);
  client.publish("robocar/dust_output/pm10",buf10);

  dust_index = 0;
  }
}

void setup() { 
  //serial
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  
  //wifi
  setup_wifi();
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  //mqtt
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  //camera
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  // if PSRAM IC present, init with UXGA resolution and higher JPEG quality
  //                      for larger pre-allocated frame buffer.
  if (psramFound()) {
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }
    
  #if defined(CAMERA_MODEL_ESP_EYE)
    pinMode(13, INPUT_PULLUP);
    pinMode(14, INPUT_PULLUP);
  #endif
    
  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  sensor_t* s = esp_camera_sensor_get();
  // initial sensors are flipped vertically and colors are a bit saturated
  if (s->id.PID == OV3660_PID) {
    s->set_vflip(s, 1); // flip it back
    s->set_brightness(s, 1); // up the brightness just a bit
    s->set_saturation(s, -2); // lower the saturation
  }
  // drop down frame size for higher initial frame rate
  s->set_framesize(s, FRAMESIZE_QVGA);

  #if defined(CAMERA_MODEL_M5STACK_WIDE) || defined(CAMERA_MODEL_M5STACK_ESP32CAM)
    s->set_vflip(s, 1);
    s->set_hmirror(s, 1);
  #endif
  
  startCameraServer();
  
  Serial.print("Camera Ready! Use 'http://");
  Serial.print(WiFi.localIP());
  Serial.println("' to connect");
  
  //motors
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(15, OUTPUT);
  //pinMode(32, OUTPUT);
  //pinMode(33, OUTPUT);

  //sensors
  I2CBME.begin(I2C_SDA, I2C_SCL);//last param is clock freq

  //dust sensor
  Serial2.begin(9600,SERIAL_8N1,dust_sensor,-1);
  
  //air sensor
  air_sensor.begin(10000);
  toggle = false;
  
  //tof sensor
  sensor.setBus(&I2CBME);
  sensor.setTimeout(500);
  while(!sensor.init()) {
    Serial.println("Failed to detect and initialize sensor!");
  }

  #if defined LONG_RANGE
    // lower the return signal rate limit (default is 0.25 MCPS)
    sensor.setSignalRateLimit(0.1);
    // increase laser pulse periods (defaults are 14 and 10 PCLKs)
    sensor.setVcselPulsePeriod(VL53L0X::VcselPeriodPreRange, 18);
    sensor.setVcselPulsePeriod(VL53L0X::VcselPeriodFinalRange, 14);
  #endif
  
  #if defined HIGH_SPEED
    // reduce timing budget to 20 ms (default is about 33 ms)
    sensor.setMeasurementTimingBudget(20000);
  #elif defined HIGH_ACCURACY
    // increase timing budget to 200 ms
    sensor.setMeasurementTimingBudget(200000);
  #endif*/
  
}

void loop() {
  // MQTT reconnect if disconncted
  unsigned long now = millis();
  if (!client.connected()) {
    reconnect();
  }
  
  Serial.println(millis() - now);
  now = millis();
  
  // MQTT callback
  client.loop();

  Serial.println(millis() - now);
  now = millis();
  
  // Publish reading from air sensor (SGP40)
  if(toggle) {
    sprintf(buf, "%03i", air_sensor.getVoclndex());
    client.publish("robocar/air_output", buf);
  }

  Serial.println(millis() - now);
  now = millis();
  
  // Publish reading from dust sensor (SM-UART-04L)
  dust_sensor_loop();

  Serial.println(millis() - now);
  now = millis();

  // Publish reading from TOF sensor (VL53L0X)
  sprintf(buf, "%04i", sensor.readRangeSingleMillimeters());
  if (sensor.timeoutOccurred()) { Serial.print(" TIMEOUT"); } else {
    client.publish("robocar/tof_output", buf);
  }

  Serial.println(millis() - now);
}
