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

  Serial.println("Clearing Timer");
    
  SWprint(0x11); // Initialize
  
  SWprint(0x00); // Address
  
  SWprint(0x00); // Mode Setting
  
  SWprint(0x00); // Digit 0 (Leave 0)
  SWprint(0x00); // Digit 1 (Leave 0)
  SWprint(0x00); // Digit 2
  SWprint(0x00); // Digit 3
  SWprint(0x00); // Digit 4
  SWprint(0x00); // Digit 6
  
  SWprint(0x00); // Misc Settings
  cleared = 0;
  showRunning = 0;
  
}

void loop()
{
  int curSignal = decodeSignal();

  Serial.print("Cleared: ");
  Serial.print(cleared);
  Serial.print(" ShowRuning: ");
  Serial.println(showRunning);

  if(digitalRead(SHOW_SIGNAL_0) == 0 && showRunning == 0) // Signal to start the timer
  {
    Serial.println("Setting timer");
    
    SWprint(0x11); // Initialize
    
    SWprint(0x00); // Address
    
    SWprint(0x05); // Mode Setting
    
    SWprint(0x00); // Digit 0 (Leave 0)
    SWprint(0x00); // Digit 1 (Leave 0)
    SWprint(0x00); // Digit 2
    SWprint(0x02); // Digit 3
    SWprint(0x01); // Digit 4
    SWprint(0x08); // Digit 6
    
    SWprint(0x02); // Misc Settings
    showRunning = 1;
    cleared = 0;
  }
  
  if(digitalRead(SHOW_SIGNAL_0) == 1 && cleared == 0)
  {
    Serial.println("Clearing Timer");
    
    SWprint(0x11); // Initialize
    
    SWprint(0x00); // Address
    
    SWprint(0x00); // Mode Setting
    
    SWprint(0x00); // Digit 0 (Leave 0)
    SWprint(0x00); // Digit 1 (Leave 0)
    SWprint(0x00); // Digit 2
    SWprint(0x00); // Digit 3
    SWprint(0x00); // Digit 4
    SWprint(0x00); // Digit 6
    
    SWprint(0x00); // Misc Settings
    cleared = 1;
    showRunning = 0;
  }

}

void SWprint(int data)
{
  byte mask;
  //startbit
  digitalWrite(tx,LOW);
  delayMicroseconds(bit2400Delay);
  for (mask = 0x01; mask>0; mask <<= 1) {
    if (data & mask)
    { // choose bit
     digitalWrite(tx,HIGH); // send 1
    }
    else
    {
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
  int showSignal0 = !digitalRead(SHOW_SIGNAL_0);
  int showSignal1 = !digitalRead(SHOW_SIGNAL_1);
  int showSignal2 = !digitalRead(SHOW_SIGNAL_2);
  int showSignal3 = !digitalRead(SHOW_SIGNAL_3);
  int showSignal4 = !digitalRead(SHOW_SIGNAL_4);

  signalInput = 0;
  signalInput += showSignal4;
  signalInput += (showSignal3 << 1);
  signalInput += (showSignal2 << 2);
  signalInput += (showSignal1 << 3);
  signalInput += (showSignal0 << 4);

  //Serial.println(signalInput);
  
  return signalInput;
}
