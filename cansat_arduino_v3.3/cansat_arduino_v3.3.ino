#include <Adafruit_MPL3115A2.h>

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <SPI.h>
#include <RH_RF95.h>

#define BNO055_SAMPLERATE_DELAY_MS (100)

#define RFM95_CS 4
#define RFM95_RST 2
#define RFM95_INT 3

#define RF95_FREQ 915.0
 
// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);

Adafruit_MPL3115A2 baro = Adafruit_MPL3115A2();
Adafruit_BNO055 bno = Adafruit_BNO055(55);

int16_t packetnum = 0;  // packet counter, we increment per xmission

#define servopin 5
#define pulse 1500

void displaySensorDetails(void)
{
  sensor_t sensor;
  bno.getSensor(&sensor);
  Serial.println("------------------------------------");
  Serial.print  ("Sensor:       "); Serial.println(sensor.name);
  Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
  Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
  Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println(" xxx");
  Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println(" xxx");
  Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println(" xxx");
  Serial.println("------------------------------------");
  Serial.println("");
  delay(500);
}

void displaySensorStatus(void)
{
  /* Get the system status values (mostly for debugging purposes) */
  uint8_t system_status, self_test_results, system_error;
  system_status = self_test_results = system_error = 0;
  bno.getSystemStatus(&system_status, &self_test_results, &system_error);

  /* Display the results in the Serial Monitor */
  Serial.println("");
  Serial.print("System Status: 0x");
  Serial.println(system_status, HEX);
  Serial.print("Self Test:     0x");
  Serial.println(self_test_results, HEX);
  Serial.print("System Error:  0x");
  Serial.println(system_error, HEX);
  Serial.println("");
  delay(500);
}

void displayCalStatus(void)
{
  /* Get the four calibration values (0..3) */
  /* Any sensor data reporting 0 should be ignored, */
  /* 3 means 'fully calibrated" */
  uint8_t system, gyro, accel, mag;
  system = gyro = accel = mag = 0;
  bno.getCalibration(&system, &gyro, &accel, &mag);

  /* The data should be ignored until the system calibration is > 0 */
  Serial.print("\t");
  if (!system)
  {
    Serial.print("! ");
  }

  /* Display the individual values */
  Serial.print("Sys:");
  Serial.print(system, DEC);
  Serial.print(" G:");
  Serial.print(gyro, DEC);
  Serial.print(" A:");
  Serial.print(accel, DEC);
  Serial.print(" M:");
  Serial.print(mag, DEC);
}

void Blink(byte PIN, byte DELAY_MS, byte loops) {
  for (byte i=0; i<loops; i++)  {
    digitalWrite(PIN,HIGH);
    delay(DELAY_MS);
    digitalWrite(PIN,LOW);
    delay(DELAY_MS);
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println("Adafruit_MPL3115A2 test!");
  Serial.println("Orientation Sensor Test"); Serial.println("");

  pinMode(8, OUTPUT);
  pinMode(servopin, OUTPUT);

  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }

  delay(1000);

  /* Display some basic information on this sensor */
  displaySensorDetails();

  /* Optional: Display current status */
  displaySensorStatus();

  bno.setExtCrystalUse(true);

  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);

  Serial.println("Arduino LoRa RX Test!");

  // manual reset
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);
 
  while (!rf95.init()) {
    Serial.println("LoRa radio init failed");
    while (1);
  }
  Serial.println("LoRa radio init OK!");

  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM (for low power module)
  // No encryption
  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("setFrequency failed");
    while (1);
  }
  Serial.print("Set Freq to: "); Serial.println(RF95_FREQ);

  rf95.setTxPower(23, false);

  Serial.print("RFM69 radio @");  Serial.print((int)RF95_FREQ);  Serial.println(" MHz");
}

void servo() {
  for (int i = 0; i <= 20; i++) {
    digitalWrite(servopin, HIGH);
    delayMicroseconds(pulse);
    digitalWrite(servopin, LOW);
    delay(20);
  }
}

void rotate() {
  for (int i = 0; i <= 20; i++) {
    digitalWrite(servopin, HIGH);
    delayMicroseconds(2500);
    digitalWrite(servopin, LOW);
    delay(20);
  }
}

void loop(void)
{
  if (! baro.begin()) {
    Serial.println("Couldnt find sensor");
    return;
  }
  /*
  if (rf69.available()) {
    // Should be a message for us now
    Serial.println("available");
    uint8_t buf[RH_RF69_MAX_MESSAGE_LEN];
    uint8_t len = sizeof(buf);
    Serial.println(char(buf));
    Serial.println((char*)buf);
    if (!len) return;
    buf[len] = 0;
    char *ans;
    ans = strstr((char *)buf, "&");
    Serial.println(ans);
    if (strstr((char *)buf, "$")) {
      // Send a reply!
      Serial.println("Sent a reply");
    }
   
  }
  */


  if (rf95.available()) {
    // Should be a message for us now   
    uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
    uint8_t len = sizeof(buf);
    if (rf95.recv(buf, &len)) {
      if (!len) return;
      buf[len] = 0;
      Serial.print("Received [");
      Serial.print(len);
      Serial.print("]: ");
      Serial.println((char*)buf);
      Serial.print("RSSI: ");
      Serial.println(rf95.lastRssi(), DEC);

      if (strstr((char *)buf, "21332")) {
        Serial.println("TEST Recieved");
        servo();     
      }
      else if (strstr((char *)buf, "29797")) {
        Serial.println("rotate Recieved");
        rotate();     
      }
    } else {
      Serial.println("Receive failed");
    }
  }
  
  /* Get a new sensor event */
  sensors_event_t event;
  bno.getEvent(&event);

  /* Display the floating point data */
  Serial.print("X: ");
  Serial.print(event.orientation.x);
  Serial.print("\tY: ");
  Serial.print(event.orientation.y);
  Serial.print("\tZ: ");
  Serial.println(event.orientation.z);
  /* Optional: Display calibration status */
  //displayCalStatus();
  /* Wait the specified delay before requesting nex data */
  //delay(BNO055_SAMPLERATE_DELAY_MS);
  
  float altm = baro.getAltitude();
  Serial.print(altm); Serial.println(" meters");

  float tempC = baro.getTemperature();
  Serial.print(tempC); Serial.println("*C");

  String myString = "";

  myString = String(event.orientation.x) + ',' + String(event.orientation.y) + ',' + String(event.orientation.z) + ',' + String(altm) + ',' + String(tempC);
  //Serial.print(myString);
  char radiopacket[4];
  //radiopacket[0] = char(event.orientation.x)
  
  //char radiopacket[4];
  
  //delay(25);
  myString.toCharArray(radiopacket, 255);
  //itoa(packetnum++, radiopacket+13, 10);
  Serial.print("Sending "); Serial.println(radiopacket);
  rf95.send((uint8_t *)radiopacket, strlen(radiopacket));
  rf95.waitPacketSent();
  //delay(100);
  
  // Send a message!
  
}
