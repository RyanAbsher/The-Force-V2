#include <ctype.h>

#define bit2400Delay 416
#define halfBit2400Delay 208

#define SHOW_SIGNAL_0 6
#define SHOW_SIGNAL_1 7
#define SHOW_SIGNAL_2 8
#define SHOW_SIGNAL_3 9
#define SHOW_SIGNAL_4 10

byte tx = 2;
byte SWval;

int signalInput = 0;
int showRunning = 0;
int cleared = 0;

void setup()
{
  pinMode(SHOW_SIGNAL_0, INPUT);
  pinMode(SHOW_SIGNAL_1, INPUT);
  pinMode(SHOW_SIGNAL_2, INPUT);
  pinMode(SHOW_SIGNAL_3, INPUT);
  pinMode(SHOW_SIGNAL_4, INPUT);
  
  Serial.begin(9600);
  pinMode(tx, OUTPUT);
  digitalWrite(tx, HIGH);
  delay(2);
}

void loop()
{
  for(int i = 0; i <= 100; i++)
  {

    if(Serial.available())
    {
      int character  = Serial.parseInt();
      Serial.read();
      
      SWprint(0x11); // Initialize
      
      SWprint(0x00); // Address
      
      SWprint(0x00); // Mode Setting
      
      SWprint(0); // Digit 0 (Leave 0)
      SWprint(0); // Digit 1 (Leave 0)
      SWprint(0); // Digit 2
      SWprint(character); // Digit 3
      SWprint(character+1); // Digit 4
      SWprint(character+2); // Digit 6
      
      SWprint(0x00); // Misc Settings
    }
  };

}

void SWprint(int data)
{
  byte mask;
  //startbit
  digitalWrite(tx,LOW);
  delayMicroseconds(bit2400Delay);
  for (mask = 0x01; mask>0; mask <<= 1) {
    if (data & mask){ // choose bit
     digitalWrite(tx,HIGH); // send 1
    }
    else{
     digitalWrite(tx,LOW); // send 0
    }
    delayMicroseconds(bit2400Delay);
  }
  //stop bit
  digitalWrite(tx, HIGH);
  delayMicroseconds(bit2400Delay);
}

int decodeSignal()
{
  int showSignal0 = digitalRead(SHOW_SIGNAL_0);
  int showSignal1 = digitalRead(SHOW_SIGNAL_1);
  int showSignal2 = digitalRead(SHOW_SIGNAL_2);
  int showSignal3 = digitalRead(SHOW_SIGNAL_3);
  int showSignal4 = digitalRead(SHOW_SIGNAL_4);

  Serial.print("Signals: ");
  Serial.print(showSignal4);
  Serial.print(showSignal3);
  Serial.print(showSignal2);
  Serial.print(showSignal1);
  Serial.println(showSignal0);

  signalInput += showSignal4;
  signalInput += (showSignal3 << 1);
  signalInput += (showSignal2 << 2);
  signalInput += (showSignal1 << 3);
  signalInput += (showSignal0 << 4);
  
  return signalInput;
}
