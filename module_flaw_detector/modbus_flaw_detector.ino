#include <SoftwareSerial.h>
#include <HardwareSerial.h>
#include "src/ModbusMaster.h"




#define TX_PIN PA9
#define RX_PIN PA10

#define RELAY_PIN PB3

#define PIN_RED_LED PB11
#define PIN_GREEN_LED PB10


SoftwareSerial mySerial(RX_PIN, TX_PIN);

void setup() {
  mySerial.begin(9600);

  pinMode(PIN_RED_LED, OUTPUT);
  pinMode(PIN_GREEN_LED, OUTPUT);

  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);

  digitalWrite(PIN_RED_LED, HIGH);
  digitalWrite(PIN_GREEN_LED, LOW);
}


void loop() {
  if (mySerial.available() > 0) {
    String signalstr = mySerial.readString();
    signalstr.trim();

    if (signalstr == "red") {
      digitalWrite(PIN_RED_LED, HIGH);
      digitalWrite(PIN_GREEN_LED, LOW);
      digitalWrite(RELAY_PIN, LOW);
      mySerial.println("ONLINE: " + String(signalstr));
    }
    else if (signalstr == "green"){
      digitalWrite(PIN_RED_LED, LOW);
      digitalWrite(PIN_GREEN_LED, HIGH);
      digitalWrite(RELAY_PIN, HIGH);
      mySerial.println("ONLINE: " + String(signalstr));
    }
    else{
      mySerial.println(String("UNKNOWN COMMAND: ") + String(signalstr));
    }
  }
}
