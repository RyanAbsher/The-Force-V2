// DmxSimple Library: http://code.google.com/p/tinkerit/
// RS-232 code adapted from https://www.arduino.cc/en/Tutorial/ArduinoSoftwareRS232

#include <ctype.h>
#include "showDef.h"
#include <ArduinoRS485.h>
#include <ArduinoDMX.h>

//List of fixture addresses and number of channels to turn off for clearAll()
int fixtureList[2][7] = {{ 2, 7, 20, 47, 51, 72, 100},
                         { 3, 4, 3,  4,  4,  4,  4  }};

#define SHOW_SIGNAL_0 6
#define SHOW_SIGNAL_1 7
#define SHOW_SIGNAL_2 8
#define SHOW_SIGNAL_3 9
#define SHOW_SIGNAL_4 10

byte tx = 3;
byte SWval;
byte running = 1;

int oldStepTime = 0;

int signalInput = 0;

int currentShowStep = 0;
unsigned long showTimer = 0;
int showStarted = 0;
int timerSet = 0;
const int universeSize = 255;
int nextStepLoaded = 0;
int nextFixture, nextValue;
unsigned long nextStepTime;


void setup()
{
  pinMode(SHOW_SIGNAL_0, INPUT);
  pinMode(SHOW_SIGNAL_1, INPUT);
  pinMode(SHOW_SIGNAL_2, INPUT);
  pinMode(SHOW_SIGNAL_3, INPUT);
  pinMode(SHOW_SIGNAL_4, INPUT);
  
  Serial.begin(115200);

  DMX.begin(universeSize);

  DMX.beginTransmission();
  DMX.write(31, 255); // Turn the sign green
  DMX.endTransmission();

  DMX.beginTransmission();
  DMX.write(90, 255); // Turn on the button and button sign
  DMX.endTransmission();

  clearAll();

  //blink(1);

  /*for(int i = 0; i < NUM_DEF; i++)
  {
    int nextFix = pgm_read_word(&fixtureNumber[i]);
    int nextVal = pgm_read_word(&sendValue[i]);
    int nextTime = pgm_read_word(&startTime[i]);

    Serial.print("Step: ");
    Serial.print(i);
    Serial.print(", Fix: ");
    Serial.print(nextFix);
    Serial.print(", Time: ");
    Serial.print(nextTime);
    Serial.print(", Value: ");
    Serial.println(nextVal);
  }*/
  
}

void loop()
{

  if(!showStarted)
  {
    if(digitalRead(SHOW_SIGNAL_0) == 0)
    {
      //blink(2);
      //Turn off the Button and button sign
      Serial.println("Show Started");
      DMX.beginTransmission();
      DMX.write(90, 0); // Turn off the button and button sign
      DMX.endTransmission();
      showStarted = 1;
      showTimer = millis();
    }
  }
  else
  {
    if(!nextStepLoaded)
    {
      oldStepTime = nextStepTime;
      nextFixture = pgm_read_word(&fixtureNumber[currentShowStep]);
      nextValue = pgm_read_word(&sendValue[currentShowStep]);
      nextStepTime = pgm_read_word(&startTime[currentShowStep]);
      nextStepTime *= 10;
      nextStepLoaded = 1;
    }
    
    
    if(millis() - showTimer >= (nextStepTime) && currentShowStep <= NUM_DEF)
    {
      /*Serial.print("Step: ");
      Serial.print(currentShowStep);
      Serial.print(", Fix: ");
      Serial.print(nextFixture);
      Serial.print(", Time: ");
      Serial.print(nextStepTime);
      Serial.print(", Value: ");
      Serial.println(nextValue);*/


      DMX.beginTransmission();
      DMX.write(nextFixture, nextValue); // Turn the sign green
      DMX.endTransmission();
      currentShowStep += 1;
      nextStepLoaded = 0;
    }
  }
    
  if(digitalRead(SHOW_SIGNAL_0) == 1)
  {
    //Stop the show
    if(showStarted)
    {
      ///blink(3);
      //Turn on the Button and button sign
      DMX.beginTransmission();
      DMX.write(90, 255); // Turn the button and button sign back on
      DMX.endTransmission();
      showStarted = 0;
      clearAll();
      timerSet = 0;
      Serial.println("Show Stopped");
      currentShowStep = 0;
    };
  }

}

int decodeSignal()
{
  // Invert signals to get the correct one
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

// Blanks out all lights except the sign.
void clearAll()
{
  for(int f = 0; f <= 6; f++)
  {
    int startAddress = fixtureList[0][f];
    int endAddress = fixtureList[0][f] + fixtureList[1][f];
    for(int n = startAddress; n < endAddress; n++)
    {
      DMX.beginTransmission();
      DMX.write(n, 0);
      DMX.endTransmission();
    }
  }
}


// JUST FOR TESTING
void blink(int num)
{
  for(int t = 0; t < num; t++)
  {
    DMX.beginTransmission();
    DMX.write(20, 255);
    DMX.endTransmission();
    delay(500);
    DMX.beginTransmission();
    DMX.write(20, 0);
    DMX.endTransmission();
    delay(500);
  }
  delay(1000);
}
