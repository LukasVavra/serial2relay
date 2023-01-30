#include <Arduino.h>

const unsigned long trigger_delay = 1000;
const uint8_t relay_count = 4;

uint8_t relays[relay_count] = {2, 3, 4, 5};
unsigned long timers[relay_count];
bool states[relay_count] = {false, false, false, false};

String incomming_message;

void trigger_pin(int index)
{
  states[index] = true;
  timers[index] = millis() + trigger_delay;
  digitalWrite(relays[index], HIGH);
}

void update_timers()
{
  unsigned long time = millis();
  for(int i = 0; i < relay_count; i++)
  {
    if(states[i] && timers[i] <= time)
    {
      states[i] = false;
      digitalWrite(relays[i], LOW);
    }
  }
}

void setup() 
{
  Serial.begin(9600);
  for(int i = 0; i < relay_count; i++)
  {
    pinMode(relays[i], OUTPUT);
    digitalWrite(relays[i], LOW);
  }
}

void loop() 
{
  /* Read trigger index from serial port */
  if(Serial.available() && Serial.read() == 't')
  {
    int index = Serial.parseInt();
    if(index >= 0 && index < relay_count)
    {
      trigger_pin((uint8_t)index);
    }
  }
  
  /* Update trigger timers */
  update_timers();
}