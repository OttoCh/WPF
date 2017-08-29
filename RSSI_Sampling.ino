//Program untuk melakukan pengambilan data RSSI di lapangan
//mengambil 5 sampel RSSI per AP
//Akses internet lewat WiFi Hotspot
//improvement, data di pack jadi satu char besar baru dikirim

#include <SPI.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ST7735.h>

const char* ssid = "Lambda";
const char* password = "langsung";
const char* broker_MQTT = "23.92.65.163";

const char* RSSI_AP1 = "otto/RSSI/AP1";
const char* RSSI_AP2 = "otto/RSSI/AP2";
const char* RSSI_AP3 = "otto/RSSI/AP3";
const char* RSSI_AP4 = "otto/RSSI/AP4";
const char* RSSI_AP5 = "otto/RSSI/AP5";
const char* RSSI_AP6 = "otto/RSSI/AP6";
const char* RSSI_AP7 = "otto/RSSI/AP7";
const char* RSSI_AP8 = "otto/RSSI/AP8";
const char* coor_X = "otto/coor/x"; //1 (+), 0 (-)
const char* coor_Y = "otto/coor/y";
const char* coor_X_change = "otto/coor/x_change";
const char* coor_Y_change = "otto/coor/y_change";
const char* reset = "otto/reset";
const char* ack = "otto/ACK";

const char* SSID_AP1 = "ESP-Test1";
const char* SSID_AP2 = "ESP-Test2";
const char* SSID_AP3 = "ESP-Test3";
const char* SSID_AP4 = "ESP-Test4";
const char* SSID_AP5 = "ESP-Test5";
const char* SSID_AP6 = "ESP-Test6";
const char* SSID_AP7 = "ESP-Test7";
const char* SSID_AP8 = "ESP-Test8";

int x = 0;
int y = 0;
boolean realMode = 0;
unsigned long uptime = 500;
unsigned long last = millis();
unsigned long last_call = millis();   //button
unsigned long debounce_time = 1000;

const int numButtons = 6;
const int buttonLowRange[] = {110,720,500,376,618,260};
const int buttonHighRange[] = {164,828,571,436,707,315};
const int totalAP = 8;
const int totalSample = 10;
int32_t all_RSSI[totalAP][totalSample];

#define TFT_CS 15
#define TFT_RST 4
#define TFT_DC 5
#define TFT_SCLK 14
#define TFT_MOSI 13

WiFiClient espClient;
PubSubClient client(espClient);
Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS, TFT_DC, TFT_MOSI, TFT_SCLK, TFT_RST);

void setup_WiFi() {
  delay(10);
  tft.print("\nConnecting to: \n");
  tft.print(ssid);
  Serial.print("Connecting to: ");
  Serial.println(ssid);
  WiFi.begin(ssid,password);
  while(WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  tft.setTextColor(ST7735_GREEN);
  tft.print("\nWIFI CONNECTED\n");
  Serial.println("CONNECTED");
  tft.setTextColor(ST7735_WHITE);
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.println("got msg");
  //Merubah byte >> char >> int
  char buf = (char)payload[0];
  int receivedPayload = buf-'0';
  //
  String receivedTopic;
  for(int i=0; i<strlen(topic); i++) {
    receivedTopic+=topic[i];
  }
   if(receivedTopic==ack) {
    Serial.println("ACK");
    tft.setTextColor(ST7735_GREEN);
    tft.print("ACK\n");
    tft.setTextColor(ST7735_WHITE);
   }
   else if(receivedTopic==coor_X || receivedTopic==coor_Y) {
    if(receivedTopic==coor_X) {
      x = receivedPayload;
      Serial.print("current x: ");
      Serial.println(x);
    }
    else if(receivedTopic==coor_Y) {
      y = receivedPayload;
      Serial.print("current y: ");
      Serial.println(y);
    }
    tft.print("\nChange coordinate ");
    tft.print(x);
    tft.print(" ");
    tft.print(y);
   }
}

void get_RSSI() {
  byte available_networks = WiFi.scanNetworks();
  for(int i=0; i<totalSample; i++) {  
    for(int network=0; network < available_networks; network++) { 
      if(WiFi.SSID(network)== SSID_AP1) {
        all_RSSI[0][i] = abs(WiFi.RSSI(network));
      }
      else if(WiFi.SSID(network)== SSID_AP2){
        all_RSSI[1][i] = abs(WiFi.RSSI(network));
        }
      else if(WiFi.SSID(network)== SSID_AP3){
        all_RSSI[2][i] = abs(WiFi.RSSI(network));
        }
      else if(WiFi.SSID(network)== SSID_AP4){
        all_RSSI[3][i] = abs(WiFi.RSSI(network));
        }
      else if(WiFi.SSID(network)== SSID_AP5){
        all_RSSI[4][i] = abs(WiFi.RSSI(network));
        }
      else if(WiFi.SSID(network)== SSID_AP6){
        all_RSSI[5][i] = abs(WiFi.RSSI(network));
        }
      else if(WiFi.SSID(network)== SSID_AP7){
        all_RSSI[6][i] = abs(WiFi.RSSI(network));
        }
      else if(WiFi.SSID(network)== SSID_AP8){
        all_RSSI[7][i] = abs(WiFi.RSSI(network));
        }        
    }
    //tunggu 1 detik sebelum ambil data berikutnya
    delay(1000);
  }
  return;
}

void clear_RSSI() {
  for(int j=0; j<totalAP;j++) {
    for(int i=0; i<totalSample;i++) {
      all_RSSI[j][i] = 0;
    }
  }
  return;
}

void publish_RSSI() {
  const char* topic_pub;
  int err = 0;
  for(int j=0; j<totalAP;j++) {
    if(j==0) {
      topic_pub = RSSI_AP1;
    }
    else if(j==1) {
      topic_pub = RSSI_AP2;
    }
    else if(j==2) {
      topic_pub = RSSI_AP3;
    }
    else if(j==3) {
      topic_pub = RSSI_AP4;
    }
    else if(j==4) {
      topic_pub = RSSI_AP5;
    }
    else if(j==5) {
      topic_pub = RSSI_AP6;
    }
    else if(j==6) {
      topic_pub = RSSI_AP7;
    }
    else if(j==7) {
      topic_pub = RSSI_AP8;
    }
	//make check if this array is actually empty thing
	int totalzero = 0;
	bool doUpload = true;
	for(int i=0; i<totalSample; i++) {
		if(all_RSSI[j][i]==0) {
			totalzero += 1;
		}
	}
	if(totalzero == totalSample) {
		doUpload = false;
	}
      	if(doUpload) {
		char msg[100];
	      	for(int i=0; i<totalSample; i++) {
			char buf[10];
			sprintf(buf, "%d\t", all_RSSI[j][i]);
			strcat(msg, buf);
	      	}
	      	if(!client.publish(topic_pub, msg)) {
			err += 1;
			tft.setTextColor(ST7735_RED);
			tft.print(j);
			tft.print(" Fail to upload\n");
			printf("%d %d fail to upload\n", j);
	      }
	}
  }
  if(err==0) {
    tft.setTextColor(ST7735_GREEN);
    tft.print("all success");
    tft.setTextColor(ST7735_WHITE);
  }
  tft.setTextColor(ST7735_GREEN);
  tft.print("\nDONE!");
  tft.setTextColor(ST7735_WHITE);
  return;
}

void Change_coor(int coor, int plus) {
  int pub_coor;
  const char* pub_topic;
  if(coor) {
    //change X coordinate
    if(plus) {
      pub_coor = 1;
    }
    else {
      pub_coor = 0;
    }
    pub_topic = coor_X_change;
  }
  else{
    //change Y coordinate
    if(plus) {
      pub_coor = 1;
    }
    else {
      pub_coor = 0;
    }
    pub_topic = coor_Y_change;
  }
  char msg[10];
  sprintf(msg, "%d", pub_coor);
  if(client.publish(pub_topic, msg, true)) {
    if(coor) {
      if(plus) x+=1;
      else x-=1;
    }
    else {
      if(plus) y+=1;
      else y-=1;
    }
    delay(1000);
    printf("Change coordinate to %d %d", x,y);
  }
  else {
    tft.setTextColor(ST7735_RED);
    tft.print("\nFail to publish coordinate");
    tft.setTextColor(ST7735_WHITE);
  }
}


void read_button() {
  int numButtons = 6;
  int button[] = {1,2,3,4,5,6};
  int buttonLowRange[] = {127, 175, 315, 510, 930};
  int buttonHighRange[] = {135, 179, 326, 520, 934};
 
}

void Write_RSSI() {
  tft.fillScreen(ST7735_BLACK);
  tft.setCursor(0,0);
  tft.setTextColor(ST7735_WHITE);
  for(int j=0; j<totalAP; j++) {
    tft.print("AP");
    tft.print(j+1);
    tft.print(" ");
    tft.print(x);
    tft.print(" ");
    tft.print(y);
    tft.print(" | ");
    for(int i=0; i<totalSample; i++) {
      tft.print(all_RSSI[j][i]);
      tft.print(" ");
    }
    tft.print("\n");
  }
}

void sampling_routine() {
  get_RSSI();
  Write_RSSI();
  publish_RSSI();
  clear_RSSI();
}

void reconnect() {
  while(!client.connected()) {
    if(client.connect("RSSI")) {
      client.subscribe(ack);
      client.subscribe(coor_X);
      client.subscribe(coor_Y);
      Serial.println("Connected");
      tft.setTextColor(ST7735_GREEN);
      tft.print("\nBROKER CONNECTED\n");
      tft.setTextColor(ST7735_WHITE);
    }
  }
}

void clean_screen() {
  tft.fillScreen(ST7735_BLACK);
  tft.setCursor(0,0);
}

void realtimeRSSI() {
  realMode = !realMode;
  while(realMode == 1) {
    get_RSSI();
    Write_RSSI();
    clear_RSSI();
    checkButton();
  }
  return;
}

void checkButton() {
  int reading = analogRead(A0);
  int tmpButtonState = 0;
  unsigned long now = millis();
  if(reading>100 && now-last_call > debounce_time) {
    tft.print("\t");
    Serial.println(reading);
    last_call = millis();
    //ada yang menekan
    for(int i=0; i< numButtons; i++) {
      if(reading>=buttonLowRange[i] && reading<=buttonHighRange[i]) {
        tmpButtonState = i+1;
        break;
      }
    }
    switch(tmpButtonState) {
      case 1:
        //minus X
        Change_coor(1,0);
        break;
      case 2:
        //PLUS X
        Change_coor(1,1);
        break;
      case 3:
        //MINUS Y
        Change_coor(0,0);
        break;
      case 4:
        //PLUS Y
        Change_coor(0,1);
        break;
      case 5:
        //RESET
        //Serial.println("5");
        //clean_screen();
        realtimeRSSI();
        break;
      case 6:
        //Sampling
        //Serial.println("6");
        sampling_routine();
        break;
    }
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("Starting");
  tft.initR(INITR_BLACKTAB);
  tft.fillScreen(ST7735_BLACK);
  tft.setTextColor(ST7735_WHITE);
  tft.setTextSize(1);
  tft.setCursor(0,0);
  tft.setRotation(1);
  tft.print("Starting");
  setup_WiFi();
  tft.print("Connecting to MQTT Broker \n");
  tft.print(broker_MQTT);
  Serial.print("Connecting to MQTT Broker ");
  Serial.println(broker_MQTT);
  client.setServer(broker_MQTT, 1883);
  client.setCallback(callback);
  reconnect();
  delay(1000);
  tft.setTextColor(ST7735_GREEN);
  tft.print("\nREADY");
  tft.setTextColor(ST7735_WHITE);
  pinMode(A0, INPUT);
  //test1();
}

void loop() {
  // put your main code here, to run repeatedly:
  if(WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi disconnect");
    setup_WiFi();
  }
  if(!client.connected()) {
    Serial.println("Broker disconnect");
    reconnect();
  }
  client.loop();
  //selalu cek button kalau ada perintah
  checkButton();
  delay(100);
}
